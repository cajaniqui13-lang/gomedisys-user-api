import os
from dotenv import load_dotenv

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

# ==========================
# Configuración SMTP e IMAP
# ==========================
SMTP_SERVER = os.getenv("SMTP_SERVER", "mail.gesencro.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

# Lectura de correos (IMAP)
IMAP_SERVER = os.getenv("IMAP_SERVER", "mail.gesencro.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", 993))

RUTA_EXCEL = "ACTIVOS Y RETIRADOS- TIC.xlsx"
ESTADO_FLUJO_FILE = "estado_flujo.json"

recipients_raw = os.getenv("MAIL_RECIPIENTS", "")
MAIL_RECIPIENTS = [email.strip() for email in recipients_raw.split(",") if email.strip()]