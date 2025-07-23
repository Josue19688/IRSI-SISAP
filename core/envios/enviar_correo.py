import re
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
import mimetypes

# Cargar variables desde .env
load_dotenv()

EMAIL_REMITENTE = os.getenv("EMAIL_REMITENTE")
CONTRASENA = os.getenv("CONTRASENA")



def correo_valido(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(patron, correo) is not None

def enviar_correo(destinatario, asunto, cuerpo, archivos_adjuntos=None):
    if not correo_valido(destinatario):
        print(f"Correo inválido: {destinatario}")
        return False

    if archivos_adjuntos and isinstance(archivos_adjuntos, str):
        archivos_adjuntos = [archivos_adjuntos]


    mensaje = EmailMessage()
    mensaje['From'] = EMAIL_REMITENTE
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto
    mensaje.set_content(cuerpo)

    if archivos_adjuntos:
        for ruta in archivos_adjuntos:
            if not ruta or ruta.strip() in ('', '\\'):
                print(f"❌ Ruta inválida (vacía o malformada): '{ruta}'")
                continue

            if not os.path.exists(ruta):
                print(f"❌ Archivo no encontrado: {ruta}")
                continue

            ctype, encoding = mimetypes.guess_type(ruta)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)

            try:
                with open(ruta, 'rb') as f:
                    data = f.read()

                mensaje.add_attachment(data, maintype=maintype, subtype=subtype, filename=os.path.basename(ruta))
            except Exception as e:
                continue


    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
            servidor.login(EMAIL_REMITENTE, CONTRASENA)
            servidor.send_message(mensaje)

        print(f"Correo enviado a {destinatario}")
        return True

    except Exception as e:
        print(f"Error al enviar correo a {destinatario}: {e}")
        return False

