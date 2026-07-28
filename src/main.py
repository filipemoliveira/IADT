import sys
from pathlib import Path

from analyzer import analyze_threats
from detector import detect_components
from report import generate_report


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: python src/main.py "
            "<architecture_diagram_path>"
        )
        sys.exit(1)

    image_path = Path(sys.argv[1])

    try:
        print("Detecting architecture components...")

        components = detect_components(
            image_path=str(image_path),
        )

        print(
            f"{len(components)} component type(s) detected."
        )

        print("Analyzing STRIDE threats...")

        threats = analyze_threats(components)

        print(
            f"{len(threats)} threat(s) identified."
        )

        report_path = generate_report(
            components=components,
            threats=threats,
        )

        print("Threat modeling completed successfully.")
        print(f"Report generated at: {report_path}")

    except (
        FileNotFoundError,
        ValueError,
        RuntimeError,
    ) as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()