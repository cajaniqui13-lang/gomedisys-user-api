import smtplib
from email.message import EmailMessage
import config

def enviar_correo_solicitud():
    if not config.MAIL_RECIPIENTS or not config.SMTP_USER:
        print("[Mailer] Error: No se han configurado los destinatarios o el usuario.")
        return

    msg = EmailMessage()
    msg['Subject'] = 'Solicitud Mensual de Información (prueba)'
    msg['From'] = config.SMTP_USER
    msg['To'] = ", ".join(config.MAIL_RECIPIENTS)

    # Cuerpo del mensaje
    msg.set_content("""Hola,

Este es un mensaje automático del RPA. 

Se solicita la información correspondiente a este mes para proceder con los procesos habituales.

Quedamos atentos a su respuesta.

Saludos cordiales,
Sistema Automatizado RPA
""")
# Envío mediante SMTP_SSL
    try:
        with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.login(config.SMTP_USER, config.SMTP_PASS)
            server.send_message(msg)
        print(f"[Mailer] Correo enviado exitosamente a: {', '.join(config.MAIL_RECIPIENTS)}")
    except Exception as e:
        print(f"[Mailer] Error al enviar el correo: {e}")