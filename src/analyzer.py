from models import ArchitectureComponent, Threat


THREAT_RULES: dict[str, list[dict[str, str]]] = {
    "user": [
        {
            "category": "Spoofing",
            "description": (
                "An attacker may impersonate a legitimate user "
                "to access the system."
            ),
            "mitigation": (
                "Use multi-factor authentication and strong "
                "identity validation."
            ),
        },
        {
            "category": "Repudiation",
            "description": (
                "A user may deny having performed a sensitive action."
            ),
            "mitigation": (
                "Maintain audit logs with timestamps and user identity."
            ),
        },
    ],
    "server": [
        {
            "category": "Tampering",
            "description": (
                "Server files or configurations may be modified "
                "without authorization."
            ),
            "mitigation": (
                "Apply access controls, patch management and "
                "configuration monitoring."
            ),
        },
        {
            "category": "Denial of Service",
            "description": (
                "The server may become unavailable due to excessive "
                "traffic or resource exhaustion."
            ),
            "mitigation": (
                "Use rate limiting, monitoring and scalable resources."
            ),
        },
        {
            "category": "Elevation of Privilege",
            "description": (
                "An attacker may exploit the server to obtain "
                "higher privileges."
            ),
            "mitigation": (
                "Apply least privilege, security patches and "
                "restricted administrative access."
            ),
        },
    ],
    "process": [
        {
            "category": "Tampering",
            "description": (
                "Application logic or processed data may be modified "
                "during execution."
            ),
            "mitigation": (
                "Validate inputs and protect application integrity."
            ),
        },
        {
            "category": "Information Disclosure",
            "description": (
                "Sensitive information may be exposed during processing."
            ),
            "mitigation": (
                "Avoid exposing sensitive data and encrypt confidential "
                "information."
            ),
        },
        {
            "category": "Elevation of Privilege",
            "description": (
                "A vulnerability in the process may allow unauthorized "
                "privilege escalation."
            ),
            "mitigation": (
                "Run processes with minimum privileges and validate "
                "authorization."
            ),
        },
    ],
    "database": [
        {
            "category": "Tampering",
            "description": (
                "Stored data may be changed or deleted without "
                "authorization."
            ),
            "mitigation": (
                "Use access controls, database auditing and integrity "
                "validation."
            ),
        },
        {
            "category": "Information Disclosure",
            "description": (
                "Sensitive database information may be accessed "
                "by unauthorized users."
            ),
            "mitigation": (
                "Encrypt data at rest and restrict database permissions."
            ),
        },
        {
            "category": "Denial of Service",
            "description": (
                "Excessive queries or resource exhaustion may make "
                "the database unavailable."
            ),
            "mitigation": (
                "Use query limits, monitoring, backups and redundancy."
            ),
        },
    ],
    "storage": [
        {
            "category": "Tampering",
            "description": (
                "Stored files may be modified or deleted without "
                "authorization."
            ),
            "mitigation": (
                "Use access controls, versioning and integrity checks."
            ),
        },
        {
            "category": "Information Disclosure",
            "description": (
                "Private files may become publicly accessible."
            ),
            "mitigation": (
                "Disable public access and encrypt sensitive files."
            ),
        },
    ],
    "load_balancer": [
        {
            "category": "Spoofing",
            "description": (
                "Traffic may originate from forged or untrusted sources."
            ),
            "mitigation": (
                "Validate certificates and restrict trusted traffic "
                "sources."
            ),
        },
        {
            "category": "Denial of Service",
            "description": (
                "High traffic volume may overload the load balancer."
            ),
            "mitigation": (
                "Use rate limiting, autoscaling and DDoS protection."
            ),
        },
    ],
    "firewall": [
        {
            "category": "Tampering",
            "description": (
                "Firewall rules may be changed to allow unauthorized "
                "network access."
            ),
            "mitigation": (
                "Restrict administrative access and audit rule changes."
            ),
        },
        {
            "category": "Denial of Service",
            "description": (
                "The firewall may become overloaded and block "
                "legitimate traffic."
            ),
            "mitigation": (
                "Monitor capacity and use redundant network controls."
            ),
        },
        {
            "category": "Elevation of Privilege",
            "description": (
                "Unauthorized administrative access may allow changes "
                "to security rules."
            ),
            "mitigation": (
                "Use role-based access control and multi-factor "
                "authentication."
            ),
        },
    ],
    "external_system": [
        {
            "category": "Spoofing",
            "description": (
                "An attacker may impersonate a trusted external system."
            ),
            "mitigation": (
                "Use mutual authentication, certificates or signed "
                "requests."
            ),
        },
        {
            "category": "Tampering",
            "description": (
                "Data exchanged with the external system may be modified."
            ),
            "mitigation": (
                "Use encrypted communication and message integrity "
                "validation."
            ),
        },
        {
            "category": "Information Disclosure",
            "description": (
                "Sensitive data may be exposed during communication "
                "with the external system."
            ),
            "mitigation": (
                "Use TLS and send only the minimum required data."
            ),
        },
    ],
}


def analyze_threats(
    components: list[ArchitectureComponent],
) -> list[Threat]:
    if not components:
        raise ValueError(
            "At least one architecture component is required."
        )

    threats: list[Threat] = []

    for component in components:
        component_type = component.component_type.strip().lower()

        rules = THREAT_RULES.get(component_type, [])

        for rule in rules:
            threats.append(
                Threat(
                    component_name=component.name,
                    category=rule["category"],
                    description=rule["description"],
                    mitigation=rule["mitigation"],
                )
            )

    return threats