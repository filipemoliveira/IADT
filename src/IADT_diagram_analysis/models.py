from dataclasses import dataclass


@dataclass
class ArchitectureComponent:
    """Represents a component identified in a software architecture diagram."""

    name: str
    component_type: str


@dataclass
class Threat:
    """Represents a STRIDE threat."""

    category: str
    description: str
    mitigation: str