from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image
from ultralytics import YOLO


DEFAULT_MODEL_PATH = Path("../models/best.pt")


class ArchitectureDetector:
    """
    Executa detecção de componentes em diagramas de arquitetura
    usando um modelo YOLO treinado.
    """

    def __init__(
        self,
        model_path: str | Path = DEFAULT_MODEL_PATH,
        confidence: float = 0.25,
    ) -> None:
        self.model_path = Path(model_path)
        self.confidence = confidence

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Modelo não encontrado em: {self.model_path.resolve()}"
            )

        self.model = YOLO(str(self.model_path))

    def detect(
        self,
        image: Image.Image,
    ) -> tuple[list[dict[str, Any]], Image.Image]:
        """
        Recebe uma imagem PIL e retorna:

        1. Lista de componentes detectados.
        2. Imagem anotada com bounding boxes.
        """

        if not isinstance(image, Image.Image):
            raise TypeError("A imagem deve ser uma instância de PIL.Image.")

        image_rgb = image.convert("RGB")

        results = self.model.predict(
            source=np.array(image_rgb),
            conf=self.confidence,
            verbose=False,
        )

        if not results:
            return [], image_rgb

        result = results[0]

        detections = self._parse_detections(result)

        annotated_array = result.plot()
        annotated_array = annotated_array[:, :, ::-1]

        annotated_image = Image.fromarray(annotated_array)

        return detections, annotated_image

    def _parse_detections(
        self,
        result: Any,
    ) -> list[dict[str, Any]]:
        """
        Converte o resultado do YOLO em uma lista JSON-friendly.
        """

        detections: list[dict[str, Any]] = []

        if result.boxes is None:
            return detections

        class_names = result.names

        for index, box in enumerate(result.boxes):
            class_id = int(box.cls.item())
            confidence = float(box.conf.item())

            coordinates = box.xyxy[0].tolist()

            x1, y1, x2, y2 = [
                round(float(value), 2)
                for value in coordinates
            ]

            width = round(x2 - x1, 2)
            height = round(y2 - y1, 2)

            detection = {
                "id": index + 1,
                "class_id": class_id,
                "class_name": class_names[class_id],
                "confidence": round(confidence, 4),
                "bounding_box": {
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "width": width,
                    "height": height,
                },
            }

            detections.append(detection)

        return detections