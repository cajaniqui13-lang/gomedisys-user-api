import os
from datetime import datetime
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from src.api import registrar_rutas
from src.mailer import enviar_correo_solicitud

app = Flask(__name__)

registrar_rutas(app)

scheduler = BackgroundScheduler()
scheduler.add_job(enviar_correo_solicitud, 'date', run_date=datetime.now())
#scheduler.add_job(
#    enviar_correo_solicitud,
#    trigger='cron',
#    day=1,
#    hour=8,
#    minute=0
#)
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
    