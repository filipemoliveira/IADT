from datetime import datetime
from io import BytesIO
from typing import Any

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image as ReportLabImage,
)
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class ReportGenerator:
    """
    Gera um relatório PDF com os resultados da detecção YOLO
    e da análise de ameaças STRIDE.
    """

    def __init__(self) -> None:
        self.styles = getSampleStyleSheet()

        self.title_style = ParagraphStyle(
            name="ReportTitle",
            parent=self.styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=27,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1F2937"),
            spaceAfter=18,
        )

        self.subtitle_style = ParagraphStyle(
            name="ReportSubtitle",
            parent=self.styles["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4B5563"),
            spaceAfter=20,
        )

        self.section_style = ParagraphStyle(
            name="SectionTitle",
            parent=self.styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            textColor=colors.HexColor("#1F4E78"),
            spaceBefore=12,
            spaceAfter=10,
        )

        self.normal_style = ParagraphStyle(
            name="ReportNormal",
            parent=self.styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#1F2937"),
        )

        self.table_header_style = ParagraphStyle(
            name="TableHeader",
            parent=self.styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7,
            leading=9,
            textColor=colors.white,
            alignment=TA_CENTER,
        )

        self.table_cell_style = ParagraphStyle(
            name="TableCell",
            parent=self.styles["Normal"],
            fontName="Helvetica",
            fontSize=7,
            leading=9,
            textColor=colors.HexColor("#111827"),
        )

        self.small_style = ParagraphStyle(
            name="SmallText",
            parent=self.styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#4B5563"),
        )

    @staticmethod
    def _escape_text(value: Any) -> str:
        """
        Escapa caracteres que poderiam ser interpretados como HTML
        pelo componente Paragraph do ReportLab.
        """

        text = str(value)

        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    def _paragraph(
        self,
        value: Any,
        style: ParagraphStyle | None = None,
    ) -> Paragraph:
        return Paragraph(
            self._escape_text(value),
            style or self.table_cell_style,
        )

    @staticmethod
    def _prepare_image(
        image: Image.Image,
        max_width: float,
        max_height: float,
    ) -> ReportLabImage:
        """
        Converte uma imagem PIL para um objeto compatível
        com o ReportLab, preservando sua proporção.
        """

        image_buffer = BytesIO()

        image.convert("RGB").save(
            image_buffer,
            format="PNG",
        )

        image_buffer.seek(0)

        width, height = image.size

        scale = min(
            max_width / width,
            max_height / height,
            1,
        )

        return ReportLabImage(
            image_buffer,
            width=width * scale,
            height=height * scale,
        )

    @staticmethod
    def _add_page_number(
        canvas,
        document,
    ) -> None:
        canvas.saveState()

        canvas.setFont(
            "Helvetica",
            8,
        )

        canvas.setFillColor(
            colors.HexColor("#6B7280")
        )

        canvas.drawString(
            2 * cm,
            1.2 * cm,
            "Relatório de Análise de Arquitetura e Ameaças STRIDE",
        )

        canvas.drawRightString(
            A4[0] - 2 * cm,
            1.2 * cm,
            f"Página {document.page}",
        )

        canvas.restoreState()

    def _create_information_table(
        self,
        file_name: str,
        file_type: str,
        file_size: int,
        image: Image.Image,
        detection_count: int,
        threat_count: int,
    ) -> Table:
        analysis_date = datetime.now().strftime(
            "%d/%m/%Y às %H:%M:%S"
        )

        data = [
            [
                self._paragraph(
                    "Informação",
                    self.table_header_style,
                ),
                self._paragraph(
                    "Valor",
                    self.table_header_style,
                ),
            ],
            [
                self._paragraph("Data da análise"),
                self._paragraph(analysis_date),
            ],
            [
                self._paragraph("Arquivo analisado"),
                self._paragraph(file_name),
            ],
            [
                self._paragraph("Tipo do arquivo"),
                self._paragraph(file_type),
            ],
            [
                self._paragraph("Tamanho"),
                self._paragraph(
                    f"{file_size / 1024:.2f} KB"
                ),
            ],
            [
                self._paragraph("Dimensões"),
                self._paragraph(
                    f"{image.width} x {image.height} pixels"
                ),
            ],
            [
                self._paragraph("Componentes detectados"),
                self._paragraph(detection_count),
            ],
            [
                self._paragraph("Ameaças identificadas"),
                self._paragraph(threat_count),
            ],
        ]

        table = Table(
            data,
            colWidths=[
                5.5 * cm,
                11 * cm,
            ],
            repeatRows=1,
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#1F4E78"),
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.HexColor("#D1D5DB"),
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "BACKGROUND",
                        (0, 1),
                        (0, -1),
                        colors.HexColor("#F3F4F6"),
                    ),
                ]
            )
        )

        return table

    def _create_detection_table(
        self,
        detections: list[dict[str, Any]],
    ) -> Table:
        data = [
            [
                self._paragraph(
                    "ID",
                    self.table_header_style,
                ),
                self._paragraph(
                    "Componente",
                    self.table_header_style,
                ),
                self._paragraph(
                    "Confiança",
                    self.table_header_style,
                ),
                self._paragraph(
                    "X1",
                    self.table_header_style,
                ),
                self._paragraph(
                    "Y1",
                    self.table_header_style,
                ),
                self._paragraph(
                    "X2",
                    self.table_header_style,
                ),
                self._paragraph(
                    "Y2",
                    self.table_header_style,
                ),
                self._paragraph(
                    "Largura",
                    self.table_header_style,
                ),
                self._paragraph(
                    "Altura",
                    self.table_header_style,
                ),
            ]
        ]

        for detection in detections:
            bbox = detection["bounding_box"]

            data.append(
                [
                    self._paragraph(detection["id"]),
                    self._paragraph(
                        detection["class_name"]
                    ),
                    self._paragraph(
                        f"{detection['confidence'] * 100:.2f}%"
                    ),
                    self._paragraph(bbox["x1"]),
                    self._paragraph(bbox["y1"]),
                    self._paragraph(bbox["x2"]),
                    self._paragraph(bbox["y2"]),
                    self._paragraph(bbox["width"]),
                    self._paragraph(bbox["height"]),
                ]
            )

        table = Table(
            data,
            colWidths=[
                0.7 * cm,
                3.7 * cm,
                1.8 * cm,
                1.3 * cm,
                1.3 * cm,
                1.3 * cm,
                1.3 * cm,
                1.8 * cm,
                1.8 * cm,
            ],
            repeatRows=1,
        )

        table.setStyle(
            self._default_table_style()
        )

        return table

    def _create_summary_table(
        self,
        summary: dict[str, int],
    ) -> Table:
        data = [
            [
                self._paragraph(
                    "Total",
                    self.table_header_style,
                ),
                self._paragraph(
                    "Críticas",
                    self.table_header_style,
                ),
                self._paragraph(
                    "Altas",
                    self.table_header_style,
                ),
                self._paragraph(
                    "Médias",
                    self.table_header_style,
                ),
                self._paragraph(
                    "Baixas",
                    self.table_header_style,
                ),
            ],
            [
                self._paragraph(summary["total"]),
                self._paragraph(summary["critical"]),
                self._paragraph(summary["high"]),
                self._paragraph(summary["medium"]),
                self._paragraph(summary["low"]),
            ],
        ]

        table = Table(
            data,
            colWidths=[3.3 * cm] * 5,
        )

        table.setStyle(
            self._default_table_style()
        )

        return table

    def _create_threat_table(
        self,
        threats: list[dict[str, Any]],
    ) -> Table:
        data = [
            [
                self._paragraph(
                    "ID",
                    self.table_header_style,
                ),
                self._paragraph(
                    "Componente",
                    self.table_header_style,
                ),
                self._paragraph(
                    "STRIDE",
                    self.table_header_style,
                ),
                self._paragraph(
                    "Severidade",
                    self.table_header_style,
                ),
                self._paragraph(
                    "Descrição",
                    self.table_header_style,
                ),
                self._paragraph(
                    "Recomendação",
                    self.table_header_style,
                ),
            ]
        ]

        for threat in threats:
            data.append(
                [
                    self._paragraph(threat["id"]),
                    self._paragraph(
                        threat["component"]
                    ),
                    self._paragraph(
                        threat["stride"]
                    ),
                    self._paragraph(
                        threat["severity"]
                    ),
                    self._paragraph(
                        threat["description"]
                    ),
                    self._paragraph(
                        threat["recommendation"]
                    ),
                ]
            )

        table = Table(
            data,
            colWidths=[
                0.7 * cm,
                2.7 * cm,
                2.5 * cm,
                1.8 * cm,
                4.4 * cm,
                4.4 * cm,
            ],
            repeatRows=1,
        )

        table.setStyle(
            self._default_table_style()
        )

        for row_index, threat in enumerate(
            threats,
            start=1,
        ):
            severity = threat["severity"]

            severity_color = {
                "Critical": colors.HexColor("#FECACA"),
                "High": colors.HexColor("#FED7AA"),
                "Medium": colors.HexColor("#FEF3C7"),
                "Low": colors.HexColor("#DCFCE7"),
            }.get(
                severity,
                colors.white,
            )

            table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (3, row_index),
                            (3, row_index),
                            severity_color,
                        )
                    ]
                )
            )

        return table

    @staticmethod
    def _default_table_style() -> TableStyle:
        return TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1F4E78"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#D1D5DB"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, 0),
                    "CENTER",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F9FAFB"),
                    ],
                ),
            ]
        )

    def generate(
        self,
        original_image: Image.Image,
        annotated_image: Image.Image,
        detections: list[dict[str, Any]],
        threats: list[dict[str, Any]],
        threat_summary: dict[str, int],
        file_name: str,
        file_type: str,
        file_size: int,
    ) -> bytes:
        """
        Gera o relatório e retorna seu conteúdo em bytes.
        """

        pdf_buffer = BytesIO()

        document = SimpleDocTemplate(
            pdf_buffer,
            pagesize=A4,
            rightMargin=1.5 * cm,
            leftMargin=1.5 * cm,
            topMargin=1.5 * cm,
            bottomMargin=2 * cm,
            title="Relatório de Análise de Arquitetura e Ameaças STRIDE",
            author="Sistema de Análise de Arquitetura",
        )

        elements = []

        elements.append(
            Paragraph(
                "Relatório de Análise de Arquitetura",
                self.title_style,
            )
        )

        elements.append(
            Paragraph(
                "Detecção de componentes com YOLO e "
                "modelagem de ameaças baseada na metodologia STRIDE",
                self.subtitle_style,
            )
        )

        elements.append(
            Paragraph(
                "1. Informações gerais",
                self.section_style,
            )
        )

        elements.append(
            self._create_information_table(
                file_name=file_name,
                file_type=file_type,
                file_size=file_size,
                image=original_image,
                detection_count=len(detections),
                threat_count=len(threats),
            )
        )

        elements.append(
            Spacer(1, 0.5 * cm)
        )

        elements.append(
            Paragraph(
                "2. Diagrama original",
                self.section_style,
            )
        )

        elements.append(
            Paragraph(
                "Imagem fornecida pelo usuário para realização "
                "da análise automatizada.",
                self.normal_style,
            )
        )

        elements.append(
            Spacer(1, 0.3 * cm)
        )

        elements.append(
            self._prepare_image(
                original_image,
                max_width=16.5 * cm,
                max_height=17 * cm,
            )
        )

        elements.append(
            PageBreak()
        )

        elements.append(
            Paragraph(
                "3. Resultado da detecção",
                self.section_style,
            )
        )

        elements.append(
            Paragraph(
                "Diagrama com os componentes identificados "
                "pelo modelo de detecção de objetos.",
                self.normal_style,
            )
        )

        elements.append(
            Spacer(1, 0.3 * cm)
        )

        elements.append(
            self._prepare_image(
                annotated_image,
                max_width=16.5 * cm,
                max_height=15 * cm,
            )
        )

        elements.append(
            Spacer(1, 0.5 * cm)
        )

        elements.append(
            Paragraph(
                "4. Componentes detectados",
                self.section_style,
            )
        )

        elements.append(
            self._create_detection_table(
                detections
            )
        )

        elements.append(
            PageBreak()
        )

        elements.append(
            Paragraph(
                "5. Resumo da análise STRIDE",
                self.section_style,
            )
        )

        elements.append(
            Paragraph(
                "A tabela apresenta a distribuição das ameaças "
                "identificadas de acordo com seus níveis de severidade.",
                self.normal_style,
            )
        )

        elements.append(
            Spacer(1, 0.3 * cm)
        )

        elements.append(
            self._create_summary_table(
                threat_summary
            )
        )

        elements.append(
            Spacer(1, 0.6 * cm)
        )

        elements.append(
            Paragraph(
                "6. Ameaças identificadas",
                self.section_style,
            )
        )

        elements.append(
            Paragraph(
                "As ameaças foram associadas aos componentes "
                "identificados com base em regras predefinidas "
                "da metodologia STRIDE.",
                self.normal_style,
            )
        )

        elements.append(
            Spacer(1, 0.3 * cm)
        )

        elements.append(
            self._create_threat_table(
                threats
            )
        )

        elements.append(
            Spacer(1, 0.6 * cm)
        )

        elements.append(
            KeepTogether(
                [
                    Paragraph(
                        "7. Considerações",
                        self.section_style,
                    ),
                    Paragraph(
                        "A análise apresentada neste relatório é "
                        "baseada nos tipos de componentes identificados "
                        "no diagrama. A versão atual não interpreta "
                        "automaticamente conexões, protocolos, fluxos "
                        "de dados ou fronteiras de confiança. Os "
                        "resultados devem ser revisados por um "
                        "profissional responsável pela segurança da "
                        "arquitetura.",
                        self.normal_style,
                    ),
                ]
            )
        )

        document.build(
            elements,
            onFirstPage=self._add_page_number,
            onLaterPages=self._add_page_number,
        )

        pdf_buffer.seek(0)

        return pdf_buffer.getvalue()