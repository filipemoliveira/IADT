import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Processador de Arquivos",
    page_icon="📄",
    layout="centered"
)

# Título
st.title("Processador de Arquivos")

# Texto de instrução
st.write(
    "Selecione um arquivo para realizar o processamento."
)

# Upload
uploaded_file = st.file_uploader(
    label="Escolha um arquivo",
    type=None,  # Aceita qualquer tipo de arquivo
    accept_multiple_files=False
)

# Se um arquivo foi enviado
if uploaded_file is not None:

    st.success("Arquivo selecionado com sucesso!")

    st.write("### Informações do arquivo")

    st.write(f"**Nome:** {uploaded_file.name}")
    st.write(f"**Tipo:** {uploaded_file.type}")
    st.write(f"**Tamanho:** {uploaded_file.size / 1024:.2f} KB")

    st.divider()

    if st.button("Processar arquivo", use_container_width=True):
        st.info("Aqui será executado o processamento do seu projeto Python.")

        # Exemplo:
        # resultado = processar(uploaded_file)
        # st.success("Processamento concluído!")