import json
from collections import Counter
from pathlib import Path
from typing import Any


DEFAULT_RULES_PATH = Path("data/stride_rules.json")


class StrideEngine:
    """
    Motor de análise STRIDE baseado em regras.

    Recebe os componentes identificados pelo detector YOLO
    e associa ameaças de acordo com a categoria do componente.
    """

    CATEGORY_ALIASES = {
        "actor": {
            "actor",
            "actor_user",
            "user",
            "human",
            "client",
            "customer",
            "administrator",
            "admin",
        },
        "compute": {
            "compute",
            "compute_service",
            "service",
            "server",
            "application",
            "app",
            "api",
            "api_gateway",
            "function",
            "container",
            "virtual_machine",
            "vm",
            "process",
            "microservice",
            "worker",
            "web_server",
        },
        "data": {
            "data",
            "data_database",
            "database",
            "db",
            "storage",
            "data_store",
            "datastore",
            "blob_storage",
            "file_storage",
            "bucket",
            "cache",
            "queue",
        },
        "network": {
            "network",
            "load_balancer",
            "gateway",
            "router",
            "dns",
            "cdn",
            "proxy",
            "network_gateway",
            "message_broker",
        },
        "security": {
            "security",
            "firewall",
            "waf",
            "identity_provider",
            "authentication",
            "authorization",
            "key_vault",
            "secrets_manager",
            "security_group",
        },
        "boundary": {
            "boundary",
            "boundary_vpc_or_vnet",
            "vpc",
            "vnet",
            "trust_boundary",
            "subnet",
            "availability_zone",
            "region",
        },
        "external": {
            "external",
            "external_system",
            "third_party",
            "internet",
            "external_service",
            "external_api",
        },
    }

    SEVERITY_ORDER = {
        "Critical": 4,
        "High": 3,
        "Medium": 2,
        "Low": 1,
    }

    def __init__(
        self,
        rules_path: str | Path = DEFAULT_RULES_PATH,
    ) -> None:
        self.rules_path = Path(rules_path)

        if not self.rules_path.exists():
            raise FileNotFoundError(
                "Arquivo de regras STRIDE não encontrado em: "
                f"{self.rules_path.resolve()}"
            )

        self.rules = self._load_rules()

    def _load_rules(self) -> dict[str, list[dict[str, Any]]]:
        """
        Carrega e valida o arquivo JSON contendo as regras.
        """

        try:
            with self.rules_path.open(
                mode="r",
                encoding="utf-8",
            ) as file:
                rules = json.load(file)

        except json.JSONDecodeError as error:
            raise ValueError(
                f"O arquivo de regras STRIDE possui JSON inválido: {error}"
            ) from error

        if not isinstance(rules, dict):
            raise ValueError(
                "O arquivo de regras STRIDE deve conter um objeto JSON."
            )

        if "generic" not in rules:
            raise ValueError(
                "O arquivo de regras deve possuir a categoria 'generic'."
            )

        return rules

    @staticmethod
    def _normalize_class_name(class_name: str) -> str:
        """
        Normaliza o nome da classe para facilitar a associação
        entre as classes do YOLO e as categorias STRIDE.
        """

        normalized = class_name.strip().lower()

        normalized = normalized.replace("-", "_")
        normalized = normalized.replace(" ", "_")
        normalized = normalized.replace("/", "_")

        while "__" in normalized:
            normalized = normalized.replace("__", "_")

        return normalized

    def classify_component(self, class_name: str) -> str:
        """
        Identifica a categoria STRIDE correspondente à classe
        detectada pelo modelo.

        Caso nenhuma categoria seja encontrada, retorna 'generic'.
        """

        normalized_name = self._normalize_class_name(class_name)

        # Primeiro tenta encontrar uma correspondência exata.
        for category, aliases in self.CATEGORY_ALIASES.items():
            if normalized_name in aliases:
                return category

        # Em seguida, tenta encontrar termos presentes no nome.
        for category, aliases in self.CATEGORY_ALIASES.items():
            for alias in aliases:
                if alias in normalized_name:
                    return category

        # Os datasets utilizados no projeto possuem nomes que
        # normalmente começam com a categoria, por exemplo:
        # actor_user, compute_service e data_database.
        prefix = normalized_name.split("_")[0]

        if prefix in self.rules:
            return prefix

        return "generic"

    def analyze(
        self,
        detections: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Aplica as regras STRIDE aos componentes detectados.

        Parameters
        ----------
        detections:
            Lista de detecções produzida pelo ArchitectureDetector.

        Returns
        -------
        Lista de ameaças em formato compatível com JSON e tabelas.
        """

        threats: list[dict[str, Any]] = []
        threat_id = 1

        for detection in detections:
            component_id = detection.get("id")
            class_name = str(
                detection.get("class_name", "unknown")
            )
            confidence = float(
                detection.get("confidence", 0.0)
            )

            category = self.classify_component(class_name)

            component_rules = self.rules.get(
                category,
                self.rules["generic"],
            )

            for rule in component_rules:
                threat = {
                    "id": threat_id,
                    "component_id": component_id,
                    "component": class_name,
                    "component_category": category,
                    "detection_confidence": round(
                        confidence,
                        4,
                    ),
                    "stride": rule["stride"],
                    "description": rule["description"],
                    "severity": rule["severity"],
                    "recommendation": rule["recommendation"],
                }

                threats.append(threat)
                threat_id += 1

        return self.sort_by_severity(threats)

    def sort_by_severity(
        self,
        threats: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Ordena as ameaças da maior para a menor severidade.
        """

        return sorted(
            threats,
            key=lambda threat: self.SEVERITY_ORDER.get(
                threat.get("severity", ""),
                0,
            ),
            reverse=True,
        )

    @staticmethod
    def create_summary(
        threats: list[dict[str, Any]],
    ) -> dict[str, int]:
        """
        Cria um resumo da quantidade de ameaças por severidade.
        """

        severity_counter = Counter(
            threat.get("severity", "Unknown")
            for threat in threats
        )

        return {
            "total": len(threats),
            "critical": severity_counter.get("Critical", 0),
            "high": severity_counter.get("High", 0),
            "medium": severity_counter.get("Medium", 0),
            "low": severity_counter.get("Low", 0),
        }

    @staticmethod
    def create_stride_summary(
        threats: list[dict[str, Any]],
    ) -> dict[str, int]:
        """
        Cria um resumo da quantidade de ameaças por categoria STRIDE.
        """

        stride_counter = Counter(
            threat.get("stride", "Unknown")
            for threat in threats
        )

        return dict(stride_counter)