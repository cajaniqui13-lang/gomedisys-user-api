import os
import json
from datetime import datetime
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import config
from src.api import registrar_rutas
from src.mailer import (
    enviar_correo_solicitud,
    enviar_correo_recordatorio,
    revisar_respuesta_rrhh
)

app = Flask(__name__)
registrar_rutas(app)


def cargar_estado():
    if os.path.exists(config.ESTADO_FLUJO_FILE):
        with open(config.ESTADO_FLUJO_FILE, 'r') as f:
            return json.load(f)
    return {"mes_actual": None, "pendiente_respuesta": False, "recordatorio_pendiente": False}


def guardar_estado(estado):
    with open(config.ESTADO_FLUJO_FILE, 'w') as f:
        json.dump(estado, f, indent=4)


def flujo_inicio_mes():
    """Se ejecuta el día 1 del mes a las 8:00 AM"""
    mes_actual = datetime.now().strftime("%Y-%m")
    estado = cargar_estado()

    estado["mes_actual"] = mes_actual
    estado["pendiente_respuesta"] = True
    estado["recordatorio_pendiente"] = False
    guardar_estado(estado)

    print(f"[Scheduler] Iniciando ciclo de solicitud para el mes {mes_actual}")
    enviar_correo_solicitud(config.RUTA_EXCEL)


def flujo_revision_jornada():
    """Se ejecuta todos los días a las 6:00 PM (18:00)"""
    estado = cargar_estado()

    if not estado.get("pendiente_respuesta"):
        return

    print("[Scheduler] 6:00 PM - Verificando bandeja de entrada...")
    respuesta_recibida = revisar_respuesta_rrhh()

    if respuesta_recibida:
        print("[Scheduler] RRHH ha respondido. Proceso completado para este mes.")
        estado["pendiente_respuesta"] = False
        estado["recordatorio_pendiente"] = False
    else:
        print("[Scheduler] Sin respuesta. Se programa recordatorio para mañana a primera hora.")
        estado["recordatorio_pendiente"] = True

    guardar_estado(estado)


def flujo_recordatorio_manana():
    """Se ejecuta todos los días a las 8:00 AM para enviar recordatorio si es necesario"""
    estado = cargar_estado()

    if estado.get("pendiente_respuesta") and estado.get("recordatorio_pendiente"):
        print("[Scheduler] 8:00 AM - Enviando recordatorio diario a RRHH...")
        enviar_correo_recordatorio()


scheduler = BackgroundScheduler()

# 1. Tarea del día 1 del mes a las 8:00 AM (Solicitud inicial)
scheduler.add_job(flujo_inicio_mes, trigger='cron', day=1, hour=8, minute=0)

# 2. Revisión diaria al cierre de jornada (6:00 PM / 18:00)
scheduler.add_job(flujo_revision_jornada, trigger='cron', hour=18, minute=0)

# 3. Envío diario de recordatorios a las 8:00 AM (si RRHH sigue sin responder)
scheduler.add_job(flujo_recordatorio_manana, trigger='cron', hour=8, minute=0)

scheduler.start()

if __name__ == "__main__":
    try:
        app.run(
            host="0.0.0.0",
            port=5000,
            debug=True,
            use_reloader=False
        )
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()