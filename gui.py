import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

import config
from src.login import login
from src.usuarios import desactivar_usuario
from src.logger import escribir_log
from excel_service import ExcelService


class StdoutRedirector:
    """
    Redirige cualquier print() (del propio código o de src/*.py)
    hacia el log de la interfaz, en vez de a una consola que en el
    .exe con --windowed ni siquiera existe.
    """

    def __init__(self, log_func):
        self.log_func = log_func

    def write(self, text):
        if text.strip():
            self.log_func(text.rstrip("\n"))

    def flush(self):
        pass


class DesactivarUsuariosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RPA de Gomedisys - Desactivar Usuarios")
        self.root.geometry("600x480")
        self.root.resizable(False, False)

        self.selected_file = None
        self.running = False

        # --- Selección de archivo ---
        frame_top = tk.Frame(root, pady=10)
        frame_top.pack(fill="x", padx=10)

        self.btn_select = tk.Button(
            frame_top, text="Seleccionar Excel...", command=self.select_file, width=20
        )
        self.btn_select.pack(side="left")

        self.lbl_file = tk.Label(
            frame_top, text="Ningún archivo seleccionado", fg="gray"
        )
        self.lbl_file.pack(side="left", padx=10)

        # --- Botón de ejecución ---
        self.btn_run = tk.Button(
            root,
            text="Desactivar usuarios",
            command=self.run_process,
            bg="#c62828",
            fg="white",
            height=2,
            state="disabled",
        )
        self.btn_run.pack(fill="x", padx=10, pady=(0, 10))

        # --- Log en pantalla ---
        self.log_area = scrolledtext.ScrolledText(root, height=20, state="disabled")
        self.log_area.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # ---------------------------------------------------------------
    # Todo lo que toca la interfaz debe ejecutarse en el hilo
    # principal de Tkinter. run_process corre en un hilo aparte,
    # así que estas funciones se agendan con root.after(0, ...).
    # ---------------------------------------------------------------

    def log(self, msg: str):
        self.root.after(0, self._log_safe, msg)

    def _log_safe(self, msg: str):
        self.log_area.configure(state="normal")
        self.log_area.insert("end", msg + "\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    def show_info(self, title: str, msg: str):
        self.root.after(0, lambda: messagebox.showinfo(title, msg))

    def show_error(self, title: str, msg: str):
        self.root.after(0, lambda: messagebox.showerror(title, msg))

    def set_running_state(self, running: bool):
        self.root.after(0, self._set_running_state_safe, running)

    def _set_running_state_safe(self, running: bool):
        self.running = running
        self.btn_run.config(
            state="disabled" if running else "normal",
            text="Procesando..." if running else "Desactivar usuarios",
        )
        self.btn_select.config(state="disabled" if running else "normal")

    # ---------------------------------------------------------------

    def select_file(self):
        path = filedialog.askopenfilename(
            title="Selecciona el Excel de documentos a desactivar",
            filetypes=[("Archivos Excel", "*.xlsx *.xls")],
        )
        if path:
            self.selected_file = path
            self.lbl_file.config(text=os.path.basename(path), fg="black")
            self.btn_run.config(state="normal")
            self._log_safe(f"Archivo seleccionado: {path}")

    def run_process(self):
        if self.running:
            return
        if not self.selected_file:
            messagebox.showwarning(
                "Falta archivo", "Selecciona primero un archivo Excel."
            )
            return

        confirmado = messagebox.askyesno(
            "Confirmar",
            "Esto va a DESACTIVAR en Gomedisys a todos los usuarios del Excel seleccionado.\n\n¿Continuar?",
        )
        if not confirmado:
            return

        self.set_running_state(True)

        thread = threading.Thread(target=self._run_process_thread, daemon=True)
        thread.start()

    def _run_process_thread(self):
        old_stdout = sys.stdout
        sys.stdout = StdoutRedirector(self.log)
        driver = None

        exitosos = []
        fallidos = []

        try:
            print("========================================")
            print("          RPA DE GOMEDISYS")
            print("========================================")

            config.validar_configuracion()

            print("Leyendo archivo Excel...")
            registros = ExcelService.read_documentos_file(self.selected_file)
            print(f"Se encontraron {len(registros)} documento(s) para procesar.")

            print("Iniciando RPA de Gomedisys...")
            print("Abriendo Gomedisys...")
            print("Iniciando sesión...")
            driver = login()
            print("Inicio de sesión completado.\n")

            for idx, registro in enumerate(registros, start=1):
                documento = str(registro["Documento"]).strip()

                print(f"[{idx}/{len(registros)}] Documento: {documento}")

                try:
                    resultado = desactivar_usuario(driver, documento)
                    escribir_log(documento, resultado["mensaje"])
                    print(f"  → {resultado['mensaje']}")

                    if resultado.get("ok"):
                        exitosos.append(f"{documento}: {resultado['mensaje']}")
                    else:
                        fallidos.append(f"{documento}: {resultado['mensaje']}")

                except Exception as fila_error:
                    print(f"  → [ERROR] {fila_error}")
                    escribir_log(documento, f"ERROR: {fila_error}")
                    fallidos.append(f"{documento}: ERROR - {fila_error}")
                    continue

            print("\n========================================")
            print("RESUMEN FINAL")
            print("========================================")
            print(f"Procesados sin problema: {len(exitosos)}")
            print(f"Con error o no encontrados: {len(fallidos)}")
            if fallidos:
                print("Detalle de fallidos:")
                for f in fallidos:
                    print(f"  - {f}")

            self.show_info(
                "Proceso terminado",
                f"Procesados: {len(exitosos)}\nCon error: {len(fallidos)}",
            )

        except ValueError as ve:
            print(f"\n[ERROR DE CONFIGURACIÓN] {ve}")
            self.show_error("Error de configuración", str(ve))

        except Exception as e:
            print(f"\n[ERROR] {e}")
            self.show_error("Error", f"Ocurrió un error durante el proceso:\n{e}")

        finally:
            if driver:
                print("\nCerrando navegador...")
                driver.quit()
            sys.stdout = old_stdout
            self.set_running_state(False)


if __name__ == "__main__":
    root = tk.Tk()
    app = DesactivarUsuariosApp(root)
    root.mainloop()
