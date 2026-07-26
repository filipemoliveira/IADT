from models import ArchitectureComponent
from stride import get_threats



def generate_report(
    components: list[ArchitectureComponent],
    output_path: str,
) -> None:
    """Generates a Markdown report with the STRIDE analysis."""

    lines = [
        "# STRIDE Threat Analysis Report",
        "",
        "## Architecture Components",
        "",
    ]

    for component in components:
        lines.append(
            f"- {component.name} ({component.component_type})"
        )

    lines.extend([
        "",
        "## Threat Analysis",
        "",
    ])

    for component in components:
        lines.append(f"### {component.name}")
        lines.append("")

        threats = get_threats(component.component_type)

        if not threats:
            lines.append("No threats identified.")
            lines.append("")
            continue

        for threat in threats:
            lines.append(f"#### {threat.category}")
            lines.append("")
            lines.append(f"**Description:** {threat.description}")
            lines.append("")
            lines.append(f"**Mitigation:** {threat.mitigation}")
            lines.append("")

    with open(output_path, "w", encoding="utf-8") as report_file:
        report_file.write("\n".join(lines))