from pathlib import Path

from models import ArchitectureComponent, Threat


def generate_report(
    components: list[ArchitectureComponent],
    threats: list[Threat],
    output_path: str,
) -> None:
    """Generates a Markdown STRIDE report."""

    lines = [
        "# STRIDE Threat Modeling Report",
        "",
        "## Architecture Components",
        "",
    ]

    for component in components:
        lines.append(
            f"- {component.name} ({component.component_type})"
        )

    lines.extend(
        [
            "",
            f"Total components: {len(components)}",
            "",
            "## STRIDE Threat Analysis",
            "",
        ]
    )

    for component in components:
        lines.append(f"### {component.name}")
        lines.append("")

        component_threats = [
            threat
            for threat in threats
            if threat.component_name == component.name
        ]

        if not component_threats:
            lines.append("No threats identified.")
            lines.append("")
            continue

        for threat in component_threats:
            lines.append(f"#### {threat.category}")
            lines.append("")
            lines.append(
                f"**Description:** {threat.description}"
            )
            lines.append("")
            lines.append(
                f"**Mitigation:** {threat.mitigation}"
            )
            lines.append("")

    path = Path(output_path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )