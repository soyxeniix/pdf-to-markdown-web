# 📄 PDF to Markdown Converter

**PDF to Markdown Converter** is a modern, lightweight Python desktop application designed to extract text, tables, and formatted content from PDF documents and save them as clean Markdown (`.md`) files.

Built with **CustomTkinter** for an intuitive user experience and powered by **PyMuPDF (`pymupdf4llm`)** for high-accuracy extraction, it allows for seamless batch conversion with complete control over where each output file is saved.

### ✨ Key Features

* **🎨 Modern UI:** Clean dark-themed interface built with `CustomTkinter`.
* **📚 Batch Processing:** Select and convert multiple PDF files simultaneously.
* **📂 Custom Target Paths:** Prompted save locations for each document with automatically suggested filenames (`<original_name>_markdown.md`).
* **🚀 Multi-Threaded:** Smooth UI performance with non-blocking thread execution during conversion.
* **🧱 Clean Architecture:** Fully decoupled architecture separating the backend extraction logic (`core/`) from the user interface (`gui/`).
* **🌐 Web-Ready Core:** Modular core engine easily integrable into web frameworks like Streamlit or FastAPI.
