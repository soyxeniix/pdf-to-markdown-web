import os
import pymupdf4llm


def convert_pdf_to_markdown(pdf_path: str, save_path: str) -> str:
    """
    Convierte un archivo PDF a Markdown y lo guarda en la ruta especificada.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"El archivo origen no existe: {pdf_path}")

    # Conversión mediante PyMuPDF
    markdown_text = pymupdf4llm.to_markdown(pdf_path)

    # Guardar resultado
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(markdown_text)

    return save_path


def get_suggested_filename(pdf_path: str) -> str:
    """Genera un nombre sugerido agregando '_markdown.md' al nombre original."""
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    return f"{base_name}_markdown.md"