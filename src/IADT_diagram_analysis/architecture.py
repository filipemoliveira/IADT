import json

from models import ArchitectureComponent


def load_architecture(
    input_path: str,
) -> list[ArchitectureComponent]:
    """Loads architecture components from a JSON file."""

    with open(input_path, "r", encoding="utf-8") as input_file:
        data = json.load(input_file)

    components = []

    for item in data:
        component = ArchitectureComponent(
            name=item["name"],
            component_type=item["component_type"],
        )

        components.append(component)

    return components