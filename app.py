from io import BytesIO

import pandas as pd
import streamlit as st
from PIL import Image

from src.detector import ArchitectureDetector
from src.report import ReportGenerator
from src.stride_engine import StrideEngine


st.set_page_config(
    page_title="Análise de Arquitetura",
    page_icon="🧩",
    layout="centered",
)


@st.cache_resource
def load_detector() -> ArchitectureDetector:
    return ArchitectureDetector(
        model_path="models/best.pt",
        confidence=0.25,
    )


@st.cache_resource
def load_stride_engine() -> StrideEngine:
    return StrideEngine(
        rules_path="data/stride_rules.json",
    )


@st.cache_resource
def load_report_generator() -> ReportGenerator:
    return ReportGenerator()


st.title("Análise de Arquitetura de Sistemas")

st.write(
    "Selecione uma imagem contendo um diagrama de arquitetura "
    "para identificar os componentes e gerar a análise STRIDE."
)

uploaded_file = st.file_uploader(
    label="Selecione uma imagem",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=False,
)

if uploaded_file is not None:
    try:
        image_bytes = uploaded_file.getvalue()
        image = Image.open(BytesIO(image_bytes)).convert("RGB")

        st.success("Imagem selecionada com sucesso!")

        st.write("### Informações do arquivo")
        st.write(f"**Nome:** {uploaded_file.name}")
        st.write(f"**Tipo:** {uploaded_file.type}")
        st.write(f"**Tamanho:** {uploaded_file.size / 1024:.2f} KB")
        st.write(
            f"**Dimensões:** "
            f"{image.width} × {image.height} pixels"
        )

        st.write("### Pré-visualização")

        st.image(
            image,
            caption=uploaded_file.name,
            use_container_width=True,
        )

        st.divider()

        if st.button(
            "Analisar arquitetura",
            type="primary",
            use_container_width=True,
        ):
            with st.spinner("Detectando componentes..."):
                detector = load_detector()

                detections, annotated_image = detector.detect(
                    image
                )

            st.success("Detecção concluída!")

            if detections:
                st.write("### Imagem analisada")

                st.image(
                    annotated_image,
                    caption="Componentes identificados",
                    use_container_width=True,
                )

                st.write("### Componentes Detectados")

                table_data = []

                for detection in detections:
                    bbox = detection["bounding_box"]

                    table_data.append(
                        {
                            "ID": detection["id"],
                            "Classe": detection["class_name"],
                            "Confiança (%)": round(
                                detection["confidence"] * 100,
                                2,
                            ),
                            "X1": bbox["x1"],
                            "Y1": bbox["y1"],
                            "X2": bbox["x2"],
                            "Y2": bbox["y2"],
                            "Largura": bbox["width"],
                            "Altura": bbox["height"],
                        }
                    )

                df = pd.DataFrame(table_data)

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                )

                st.divider()

                with st.spinner(
                    "Gerando análise de ameaças STRIDE..."
                ):
                    stride_engine = load_stride_engine()

                    threats = stride_engine.analyze(
                        detections
                    )

                    threat_summary = (
                        stride_engine.create_summary(
                            threats
                        )
                    )

                st.success(
                    "Análise STRIDE concluída!"
                )

                st.write("### Resumo da Análise STRIDE")

                summary_columns = st.columns(4)

                summary_columns[0].metric(
                    "Total",
                    threat_summary["total"],
                )

                summary_columns[1].metric(
                    "Críticas",
                    threat_summary["critical"],
                )

                summary_columns[2].metric(
                    "Altas",
                    threat_summary["high"],
                )

                summary_columns[3].metric(
                    "Médias",
                    threat_summary["medium"],
                )

                if threat_summary["low"] > 0:
                    st.metric(
                        "Ameaças baixas",
                        threat_summary["low"],
                    )

                st.write("### Ameaças Identificadas")

                threat_table_data = []

                for threat in threats:
                    threat_table_data.append(
                        {
                            "ID": threat["id"],
                            "Componente": threat["component"],
                            "Categoria": (
                                threat[
                                    "component_category"
                                ]
                            ),
                            "STRIDE": threat["stride"],
                            "Severidade": threat["severity"],
                            "Descrição": threat["description"],
                            "Recomendação": (
                                threat["recommendation"]
                            ),
                        }
                    )

                threat_df = pd.DataFrame(
                    threat_table_data
                )

                st.dataframe(
                    threat_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Descrição": (
                            st.column_config.TextColumn(
                                "Descrição",
                                width="large",
                            )
                        ),
                        "Recomendação": (
                            st.column_config.TextColumn(
                                "Recomendação",
                                width="large",
                            )
                        ),
                    },
                )

                st.divider()

                st.write("### Relatório da Análise")

                with st.spinner(
                    "Preparando relatório em PDF..."
                ):
                    report_generator = (
                        load_report_generator()
                    )

                    report_pdf = report_generator.generate(
                        original_image=image,
                        annotated_image=annotated_image,
                        detections=detections,
                        threats=threats,
                        threat_summary=threat_summary,
                        file_name=uploaded_file.name,
                        file_type=uploaded_file.type,
                        file_size=uploaded_file.size,
                    )

                report_file_name = (
                    uploaded_file.name.rsplit(
                        ".",
                        maxsplit=1,
                    )[0]
                    + "_relatorio_stride.pdf"
                )

                st.download_button(
                    label="Baixar relatório em PDF",
                    data=report_pdf,
                    file_name=report_file_name,
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True,
                )

            else:
                st.warning(
                    "Nenhum componente foi detectado."
                )

    except FileNotFoundError as error:
        st.error(str(error))

    except ValueError as error:
        st.error(
            f"Erro na configuração do STRIDE: {error}"
        )

    except Exception as error:
        st.error(
            f"Erro durante o processamento: {error}"
        )