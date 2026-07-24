import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# ==========================
# Configuración de Gomedisys
# ==========================

BASE_URL = os.getenv("BASE_URL")

GOMEDISYS_USER = os.getenv("GOMEDISYS_USER")

GOMEDISYS_PASS = os.getenv("GOMEDISYS_PASS")

SEDE_TRABAJO = os.getenv("SEDE_TRABAJO")

WAIT_TIMEOUT = int(os.getenv("WAIT_TIMEOUT", 20))

HEADLESS = os.getenv("HEADLESS", "0") == "1"

CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
