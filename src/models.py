from dataclasses import dataclass


@dataclass
class ArchitectureComponent:
    name: str
    component_type: str


@dataclass
class Threat:
    component_name: str
    category: str
    description: str
    mitigation: str