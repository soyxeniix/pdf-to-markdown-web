import io
import zipfile
import fitz  # PyMuPDF
import pymupdf4llm
import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="PDF to Markdown Converter",
    page_icon="⚡",
    layout="centered"
)

# Estilos CSS personalizados para mejorar el diseño
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding-bottom: 20px;
    }
    .stDownloadButton button {
        width: 100%;
        background-color: #2FA572 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    .file-card {
        background-color: #1E1E2E;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #313244;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado principal
st.markdown("<h1 class='main-header'>⚡ PDF a Markdown Converter</h1>", unsafe_allow_html=True)
st.caption("<p style='text-align: center;'>Convierte tus documentos PDF a formato Markdown limpio en segundos.</p>", unsafe_allow_html=True)
st.divider()

# Selector de archivos
uploaded_files = st.file_uploader(
    "📥 Arrastra tus archivos PDF aquí o selecciona desde tu dispositivo",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    st.write("---")
    st.subheader(f"📑 Archivos Seleccionados ({len(uploaded_files)})")
    
    processed_results = []

    for idx, pdf_file in enumerate(uploaded_files):
        base_name = pdf_file.name.rsplit(".", 1)[0]
        md_filename = f"{base_name}_markdown.md"

        with st.container():
            col_info, col_action = st.columns([2, 1])
            
            try:
                # Procesamiento
                pdf_bytes = pdf_file.read()
                doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                page_count = len(doc)
                
                markdown_text = pymupdf4llm.to_markdown(doc)
                word_count = len(markdown_text.split())
                
                processed_results.append((md_filename, markdown_text))

                with col_info:
                    st.markdown(f"📄 **{pdf_file.name}**")
                    m1, m2 = st.columns(2)
                    m1.caption(f"📖 Páginas: **{page_count}**")
                    m2.caption(f"📝 Palabras: **{word_count}**")

                with col_action:
                    st.download_button(
                        label="⬇️ Descargar .md",
                        data=markdown_text,
                        file_name=md_filename,
                        mime="text/markdown",
                        key=f"btn_{idx}_{pdf_file.name}"
                    )

                # Vista previa expandible
                with st.expander("👁️ Ver vista previa del Markdown"):
                    st.code(markdown_text[:1000] + ("..." if len(markdown_text) > 1000 else ""), language="markdown")

            except Exception as e:
                st.error(f"Error procesando {pdf_file.name}: {str(e)}")

        st.write("")

    # Opción de descargar todo en ZIP si hay más de 1 archivo
    if len(processed_results) > 1:
        st.divider()
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for fname, fcontent in processed_results:
                zip_file.writestr(fname, fcontent)

        st.download_button(
            label="📦 Descargar Todos en un Archivo (.ZIP)",
            data=zip_buffer.getvalue(),
            file_name="documentos_markdown.zip",
            mime="application/zip",
            key="download_all_zip"
        )