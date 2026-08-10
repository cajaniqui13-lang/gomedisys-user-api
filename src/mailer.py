import smtplib
import imaplib
import email
import os
import mimetypes
from email.message import EmailMessage
import config


def enviar_correo_solicitud(ruta_excel=None):
    if ruta_excel is None:
        ruta_excel = getattr(config, 'RUTA_EXCEL', None)

    if not config.MAIL_RECIPIENTS or not config.SMTP_USER:
        print("[Mailer] Error: No se han configurado los destinatarios o el usuario.")
        return

    msg = EmailMessage()
    msg['Subject'] = 'Solicitud Mensual de Información de Nómina'
    msg['From'] = config.SMTP_USER
    msg['To'] = ", ".join(config.MAIL_RECIPIENTS)

    msg.set_content("""Hola,

Este es un mensaje automático del RPA.

Se solicita comedidamente el envío de la nómina correspondiente a este mes para proceder con la actualización del sistema.

Quedamos atentos a su respuesta.

Saludos cordiales,
Sistema Automatizado RPA
""")

    if ruta_excel and os.path.exists(ruta_excel):
        nombre_archivo = os.path.basename(ruta_excel)
        ctype, encoding = mimetypes.guess_type(ruta_excel)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)

        with open(ruta_excel, 'rb') as f:
            contenido_archivo = f.read()

        msg.add_attachment(
            contenido_archivo,
            maintype=maintype,
            subtype=subtype,
            filename=nombre_archivo
        )
        print(f"[Mailer] Archivo '{nombre_archivo}' adjuntado correctamente.")

    try:
        with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.login(config.SMTP_USER, config.SMTP_PASS)
            server.send_message(msg)
        print(f"[Mailer] Solicitud enviada exitosamente a: {', '.join(config.MAIL_RECIPIENTS)}")
    except Exception as e:
        print(f"[Mailer] Error al enviar el correo: {e}")


def enviar_correo_recordatorio():
    """Envía un correo de recordatorio a Recursos Humanos."""
    if not config.MAIL_RECIPIENTS or not config.SMTP_USER:
        return

    msg = EmailMessage()
    msg['Subject'] = 'RECORDATORIO: Solicitud Mensual de Información de Nómina'
    msg['From'] = config.SMTP_USER
    msg['To'] = ", ".join(config.MAIL_RECIPIENTS)

    msg.set_content("""Hola,

Recordamos amablemente la solicitud de la nómina del presente mes enviada anteriormente.

Agradecemos su colaboración para continuar con los procesos automatizados.

Saludos cordiales,
Sistema Automatizado RPA
""")

    try:
        with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.login(config.SMTP_USER, config.SMTP_PASS)
            server.send_message(msg)
        print(f"[Mailer] Recordatorio enviado exitosamente a: {', '.join(config.MAIL_RECIPIENTS)}")
    except Exception as e:
        print(f"[Mailer] Error al enviar recordatorio: {e}")


def revisar_respuesta_rrhh():
    """
    Conecta vía IMAP y busca si existe un correo de respuesta de RRHH en la bandeja de entrada.
    Retorna True si encontró respuesta, False en caso contrario.
    """
    try:
        mail = imaplib.IMAP4_SSL(config.IMAP_SERVER, config.IMAP_PORT)
        mail.login(config.SMTP_USER, config.SMTP_PASS)
        mail.select("inbox")

        # Buscar correos no leídos o procedentes de los destinatarios de RRHH
        for remitente in config.MAIL_RECIPIENTS:
            status, response = mail.search(None, f'(FROM "{remitente}")')
            if status == 'OK':
                email_ids = response[0].split()
                if email_ids:
                    print(f"[Mailer IMAP] Respuesta encontrada de: {remitente}")
                    mail.logout()
                    return True

        mail.logout()
        print("[Mailer IMAP] No se ha encontrado respuesta de Recursos Humanos aún.")
        return False

    except Exception as e:
        print(f"[Mailer IMAP] Error al verificar la bandeja de entrada: {e}")
        return False