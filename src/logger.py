from datetime import datetime

from config import LOGS_DIR


LOG_FILE = LOGS_DIR / "api.log"


def escribir_log(documento, mensaje):
    """
    Escribe una ejecución en el archivo de logs.
    """

    LOG_FILE.parent.mkdir(exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as archivo:

        archivo.write("=" * 60 + "\n")
        archivo.write(f"Fecha: {datetime.now()}\n")
        archivo.write(f"Documento: {documento}\n")
        archivo.write(f"Resultado: {mensaje}\n")
        archivo.write("=" * 60 + "\n\n")
