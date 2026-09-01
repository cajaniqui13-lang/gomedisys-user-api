import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def _base_dir() -> Path:
    """
    Devuelve la carpeta base correcta tanto si el proyecto corre
    normal (python app.py / python gui.py) como si está empaquetado
    en un .exe con PyInstaller (donde __file__ apunta a una carpeta
    temporal, no a donde está el .exe).
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


BASE_DIR = _base_dir()

# Cargar las variables del archivo .env (buscándolo junto al .exe o al script)
load_dotenv(BASE_DIR / ".env")

# ==========================
# Configuración de Gomedisys
# ==========================

BASE_URL = os.getenv("BASE_URL")

GOMEDISYS_USER = os.getenv("GOMEDISYS_USER")

GOMEDISYS_PASS = os.getenv("GOMEDISYS_PASS")

SEDE_TRABAJO = os.getenv("SEDE_TRABAJO")

WAIT_TIMEOUT = int(os.getenv("WAIT_TIMEOUT", 20))

HEADLESS = os.getenv("HEADLESS", "0") == "1"

LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

REQUIRED_VARS = ["BASE_URL", "GOMEDISYS_USER", "GOMEDISYS_PASS", "SEDE_TRABAJO"]


def validar_configuracion():
    faltantes = [v for v in REQUIRED_VARS if not globals().get(v)]
    if faltantes:
        raise ValueError(
            f"Faltan variables de entorno requeridas en .env: {', '.join(faltantes)}"
        )
