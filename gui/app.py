import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

from core.converter import convert_pdf_to_markdown, get_suggested_filename

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class ConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Convertidor de PDF a Markdown")
        self.geometry("650x500")
        self.minsize(600, 450)

        self.pdf_files = []
        self.is_converting = False

        self._create_widgets()

    def _create_widgets(self):
        self.title_label = ctk.CTkLabel(
            self, text="PDF a Markdown", font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(20, 5))

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Selecciona tus archivos PDF y conviértelos de forma rápida.",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        self.subtitle_label.pack(pady=(0, 15))

        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.list_label = ctk.CTkLabel(
            self.list_frame, text="Archivos seleccionados:", font=ctk.CTkFont(size=14, weight="bold")
        )
        self.list_label.pack(anchor="w", padx=15, pady=(10, 5))

        self.file_textbox = ctk.CTkTextbox(
            self.list_frame, state="disabled", wrap="none", font=ctk.CTkFont(size=12)
        )
        self.file_textbox.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(fill="x", padx=20, pady=10)

        self.select_btn = ctk.CTkButton(
            self.btn_frame,
            text="Seleccionar PDF(s)",
            command=self.select_files,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38
        )
        self.select_btn.pack(side="left", padx=(0, 10), expand=True, fill="x")

        self.convert_btn = ctk.CTkButton(
            self.btn_frame,
            text="Convertir a Markdown",
            command=self.start_conversion_thread,
            fg_color="#2FA572",
            hover_color="#1E7A52",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            state="disabled"
        )
        self.convert_btn.pack(side="right", padx=(10, 0), expand=True, fill="x")

        self.status_label = ctk.CTkLabel(
            self, text="Esperando selección de archivos...", font=ctk.CTkFont(size=12), text_color="gray"
        )
        self.status_label.pack(pady=(5, 2))

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 15))
        self.progress_bar.set(0)

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Seleccionar archivos PDF", filetypes=[("Archivos PDF", "*.pdf")]
        )
        if files:
            self.pdf_files = list(files)
            self._update_file_list()
            self.convert_btn.configure(state="normal")
            self.status_label.configure(
                text=f"{len(self.pdf_files)} archivo(s) listos para convertir.", text_color="gray"
            )
            self.progress_bar.set(0)

    def _update_file_list(self):
        self.file_textbox.configure(state="normal")
        self.file_textbox.delete("1.0", "end")
        for idx, file_path in enumerate(self.pdf_files, 1):
            file_name = os.path.basename(file_path)
            self.file_textbox.insert("end", f"{idx}. {file_name}\n   └─ {file_path}\n\n")
        self.file_textbox.configure(state="disabled")

    def start_conversion_thread(self):
        if not self.pdf_files or self.is_converting:
            return

        self.is_converting = True
        self.select_btn.configure(state="disabled")
        self.convert_btn.configure(state="disabled")

        thread = threading.Thread(target=self.process_conversion, daemon=True)
        thread.start()

    def process_conversion(self):
        total_files = len(self.pdf_files)
        converted_count = 0
        skipped_count = 0

        for idx, pdf_path in enumerate(self.pdf_files, 1):
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            suggested_name = get_suggested_filename(pdf_path)

            self.status_label.configure(
                text=f"Procesando ({idx}/{total_files}): {base_name}.pdf...", text_color="#1E90FF"
            )

            save_path = filedialog.asksaveasfilename(
                title=f"Guardar Markdown para: {base_name}.pdf",
                initialfile=suggested_name,
                defaultextension=".md",
                filetypes=[("Archivos Markdown", "*.md"), ("Todos los archivos", "*.*")]
            )

            if not save_path:
                skipped_count += 1
                self.focus_force()
                messagebox.showwarning(
                    "Archivo Omitido",
                    f"Se canceló el guardado para:\n{base_name}.pdf\n\nContinuando con el siguiente..."
                )
            else:
                try:
                    convert_pdf_to_markdown(pdf_path, save_path)
                    converted_count += 1

                    self.focus_force()
                    messagebox.showinfo(
                        "Documento Guardado",
                        f"¡El archivo se convirtió y guardó con éxito!\n\nUbicación:\n{save_path}"
                    )
                except Exception as e:
                    skipped_count += 1
                    self.focus_force()
                    messagebox.showerror(
                        "Error de Conversión",
                        f"Ocurrió un error al procesar {base_name}.pdf:\n\n{str(e)}"
                    )

            self.progress_bar.set(idx / total_files)

        self.is_converting = False
        self.select_btn.configure(state="normal")
        self.convert_btn.configure(state="normal")

        self.focus_force()
        if converted_count > 0:
            messagebox.showinfo(
                "Proceso Finalizado",
                f"Conversión completada.\n\n• Guardados: {converted_count}\n• Omitidos/Fallidos: {skipped_count}"
            )
            self.status_label.configure(text="¡Proceso finalizado con éxito!", text_color="#2FA572")
        else:
            self.status_label.configure(text="No se guardó ningún archivo.", text_color="orange")