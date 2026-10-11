# PDF to Markdown Converter

PDF to Markdown Converter is a Python application built to parse PDF documents and export their layout, tables, and text content into clean Markdown (`.md`) files.

The core extraction engine is powered by PyMuPDF (`pymupdf4llm`). The application supports both a desktop interface implemented with CustomTkinter and a web deployment interface built with Streamlit.

## Features

* **Graphical User Interface:** Built with CustomTkinter featuring dark mode compatibility.
* **Batch Conversion:** Supports simultaneous processing of multiple PDF files.
* **Non-blocking Execution:** UI remains responsive during conversion tasks by running heavy operations on separate background threads.
* **Modular Architecture:** Core extraction logic (`core/`) is decoupled from presentation layers (`gui/` and Streamlit web app) to facilitate maintenance and extension.
* **Deployment Options:** Can be executed locally as a desktop app or deployed to cloud platforms such as Streamlit Cloud.
