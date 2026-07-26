"""Basic STRIDE threat mapping."""

from models import Threat


STRIDE_THREATS = {
    "user": [
        Threat(
            category="Spoofing",
            description="An attacker may impersonate a legitimate user.",
            mitigation="Use Multi-Factor Authentication (MFA).",
        ),
        Threat(
            category="Repudiation",
            description="A user may deny performing an action.",
            mitigation="Enable audit logs and activity tracking.",
        ),
    ],

    "client": [
        Threat(
            category="Spoofing",
            description="A malicious client may impersonate a trusted client.",
            mitigation="Use strong authentication and validate client identity.",
        ),
        Threat(
            category="Tampering",
            description="Client requests or local data may be modified.",
            mitigation="Validate all data received from the client.",
        ),
        Threat(
            category="Information Disclosure",
            description="Sensitive information may be exposed on the client.",
            mitigation="Avoid storing sensitive data locally.",
        ),
    ],

    "web": [
        Threat(
            category="Spoofing",
            description="Attackers may impersonate legitimate users or services.",
            mitigation="Use secure authentication and session management.",
        ),
        Threat(
            category="Tampering",
            description="Web requests may be modified.",
            mitigation="Use HTTPS and validate all inputs.",
        ),
        Threat(
            category="Information Disclosure",
            description="Sensitive information may be exposed through the web layer.",
            mitigation="Use HTTPS and avoid exposing sensitive error details.",
        ),
        Threat(
            category="Denial of Service",
            description="The web component may be overwhelmed by excessive requests.",
            mitigation="Use rate limiting and traffic protection.",
        ),
    ],

    "api": [
        Threat(
            category="Spoofing",
            description="Requests may be sent using a false identity.",
            mitigation="Validate authentication tokens.",
        ),
        Threat(
            category="Tampering",
            description="API requests or responses may be modified.",
            mitigation="Use HTTPS and validate input.",
        ),
        Threat(
            category="Information Disclosure",
            description="The API may expose sensitive information.",
            mitigation="Apply authorization and limit response data.",
        ),
        Threat(
            category="Denial of Service",
            description="The API may receive excessive or malicious requests.",
            mitigation="Use rate limiting and request throttling.",
        ),
    ],

    "service": [
        Threat(
            category="Spoofing",
            description="Another system may impersonate a trusted service.",
            mitigation="Use service authentication and managed identities.",
        ),
        Threat(
            category="Tampering",
            description="Service messages or processing may be modified.",
            mitigation="Validate inputs and protect communication channels.",
        ),
        Threat(
            category="Denial of Service",
            description="The service may become unavailable due to excessive load.",
            mitigation="Use autoscaling, monitoring and rate limiting.",
        ),
        Threat(
            category="Elevation of Privilege",
            description="A compromised service may gain excessive permissions.",
            mitigation="Apply the principle of least privilege.",
        ),
    ],

    "database": [
        Threat(
            category="Tampering",
            description="Stored data may be modified without authorization.",
            mitigation="Restrict write permissions and audit changes.",
        ),
        Threat(
            category="Information Disclosure",
            description="Sensitive information may be exposed.",
            mitigation="Encrypt data at rest and restrict access.",
        ),
        Threat(
            category="Denial of Service",
            description="The database may become unavailable.",
            mitigation="Use backups, replication and monitoring.",
        ),
        Threat(
            category="Elevation of Privilege",
            description="A user may obtain excessive database permissions.",
            mitigation="Apply role-based access control.",
        ),
    ],

    "storage": [
        Threat(
            category="Tampering",
            description="Stored files may be modified or deleted.",
            mitigation="Use access controls, versioning and backups.",
        ),
        Threat(
            category="Information Disclosure",
            description="Stored files may be accessed by unauthorized users.",
            mitigation="Encrypt data and restrict storage permissions.",
        ),
        Threat(
            category="Denial of Service",
            description="Storage may become unavailable or reach capacity.",
            mitigation="Monitor capacity and configure redundancy.",
        ),
    ],

    "queue": [
        Threat(
            category="Spoofing",
            description="Unauthorized producers may send messages.",
            mitigation="Authenticate message producers and consumers.",
        ),
        Threat(
            category="Tampering",
            description="Messages may be modified.",
            mitigation="Use encrypted connections and message validation.",
        ),
        Threat(
            category="Denial of Service",
            description="The queue may be flooded with messages.",
            mitigation="Use quotas, monitoring and dead-letter queues.",
        ),
    ],

    "identity": [
        Threat(
            category="Spoofing",
            description="An attacker may impersonate a legitimate identity.",
            mitigation="Use MFA and strong credential policies.",
        ),
        Threat(
            category="Information Disclosure",
            description="Credentials or encryption keys may be exposed.",
            mitigation="Protect secrets and rotate keys regularly.",
        ),
        Threat(
            category="Elevation of Privilege",
            description="An identity may obtain excessive privileges.",
            mitigation="Apply least privilege and review permissions.",
        ),
    ],

    "external_system": [
        Threat(
            category="Spoofing",
            description="An external system may be impersonated.",
            mitigation="Authenticate external integrations.",
        ),
        Threat(
            category="Tampering",
            description="Data exchanged with the external system may be modified.",
            mitigation="Use HTTPS and validate received data.",
        ),
        Threat(
            category="Information Disclosure",
            description="Sensitive information may be exposed to external systems.",
            mitigation="Share only necessary data and use encryption.",
        ),
    ],

    "network": [
        Threat(
            category="Spoofing",
            description="An attacker may impersonate a trusted network resource.",
            mitigation="Use network authentication and trusted certificates.",
        ),
        Threat(
            category="Tampering",
            description="Network traffic may be intercepted and modified.",
            mitigation="Encrypt network communication using TLS.",
        ),
        Threat(
            category="Information Disclosure",
            description="Network traffic may expose sensitive information.",
            mitigation="Use encryption and network segmentation.",
        ),
        Threat(
            category="Denial of Service",
            description="Network resources may be overwhelmed or made unavailable.",
            mitigation="Use firewalls, DDoS protection and traffic monitoring.",
        ),
    ],

    "other": [
        Threat(
            category="Tampering",
            description="The component may be modified without authorization.",
            mitigation="Apply access control and integrity validation.",
        ),
        Threat(
            category="Information Disclosure",
            description="The component may expose sensitive information.",
            mitigation="Restrict access and encrypt sensitive data.",
        ),
    ],
}


def get_threats(component_type: str) -> list[Threat]:
    """Returns the threats associated with a component type."""

    return STRIDE_THREATS.get(component_type, [])