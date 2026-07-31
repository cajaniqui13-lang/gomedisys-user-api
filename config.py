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

SMTP_SERVER = os.getenv("SMTP_SERVER", "mail.gesencro.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 995))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

recipients_raw = os.getenv("MAIL_RECIPIENTS", "")
MAIL_RECIPIENTS = [email.strip() for email in recipients_raw.split(",") if email.strip()]