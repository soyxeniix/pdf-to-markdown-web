import streamlit as st
import pymupdf4llm

st.set_page_config(page_title="Convertidor PDF a Markdown", page_icon="📄", layout="centered")

st.title("📄 Convertidor de PDF a Markdown")
st.write("Sube uno o varios archivos PDF para convertirlos de forma rápida.")

# Subida múltiple de archivos
uploaded_files = st.file_uploader(
    "Selecciona tus archivos PDF", 
    type=["pdf"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.divider()
    st.subheader("Archivos listos para procesar:")
    
    for pdf_file in uploaded_files:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"📌 **{pdf_file.name}**")
            
        with col2:
            try:
                # Pasar 'pdf_file' directamente en lugar de 'pdf_bytes'
                markdown_text = pymupdf4llm.to_markdown(pdf_file)
                
                base_name = pdf_file.name.rsplit(".", 1)[0]
                md_filename = f"{base_name}_markdown.md"
                
                st.download_button(
                    label="⬇️ Descargar .md",
                    data=markdown_text,
                    file_name=md_filename,
                    mime="text/markdown",
                    key=pdf_file.name
                )
            except Exception as e:
                st.error(f"Error: {str(e)}")