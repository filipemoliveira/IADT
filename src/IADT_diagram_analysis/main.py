from architecture import load_architecture
from models import ArchitectureComponent
from report import generate_report
from stride import get_threats
from analyzer import analyze_diagram


def print_architecture(
    components: list[ArchitectureComponent],
) -> None:
    """Displays the architecture components."""

    print("\nArchitecture Components\n")

    for component in components:
        print(f"- {component.name} ({component.component_type})")


def validate_architecture(
    components: list[ArchitectureComponent],
) -> bool:
    """Validates whether the architecture contains components."""

    return len(components) > 0


def print_threats(
    components: list[ArchitectureComponent],
) -> None:
    """Displays the STRIDE threats for each component."""

    print("\nSTRIDE Threat Analysis\n")

    for component in components:
        print(f"{component.name}:")

        threats = get_threats(component.component_type)

        if not threats:
            print("  No threats found.\n")
            continue

        for threat in threats:
            print(f"  - {threat.category}")
            print(f"    Description: {threat.description}")
            print(f"    Mitigation: {threat.mitigation}")

        print()


def main() -> None:
    from analyzer import analyze_diagram

    architecture = analyze_diagram(
        "../../data/test_diagram.jpg",
    )

    if not validate_architecture(architecture):
        print("No components found.")
        return

    print_architecture(architecture)

    print(f"\nTotal components: {len(architecture)}")

    print_threats(architecture)

    generate_report(
        components=architecture,
        output_path="../../docs/stride_report.md",
    )

    print("Report generated: docs/stride_report.md")
    


if __name__ == "__main__":
    main()