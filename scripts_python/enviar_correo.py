import re
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

EMAIL_REMITENTE = os.getenv("EMAIL_REMITENTE")
CONTRASENA = os.getenv("CONTRASENA")

ASUNTO = "Factura Electrónica"
CUERPO = """Estimado cliente,

Adjunto a este correo encontrará su factura en formato PDF.

Saludos cordiales,
Tu Empresa"""


def correo_valido(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(patron, correo) is not None


# def enviar_correo(correo_destino, asunto, cuerpo, ruta_pdf):
#     if not os.path.exists(ruta_pdf):
#         print(f"Archivo no encontrado: {ruta_pdf}")
#         return False

#     if not correo_valido(correo_destino):
#         print(f"Correo inválido: {correo_destino}")
#         return False

#     nombre_pdf = os.path.basename(ruta_pdf)
#     mensaje = EmailMessage()
#     mensaje['From'] = EMAIL_REMITENTE
#     mensaje['To'] = correo_destino
#     mensaje['Subject'] = ASUNTO
#     mensaje.set_content(CUERPO)

#     try:
#         with open(ruta_pdf, 'rb') as f:
#             mensaje.add_attachment(f.read(), maintype='application', subtype='pdf', filename=nombre_pdf)

#         with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
#             servidor.login(EMAIL_REMITENTE, CONTRASENA)
#             servidor.send_message(mensaje)

#         print(f"Enviado: {nombre_pdf} a {correo_destino}")
#         return True

#     except Exception as e:
#         print(f"Error al enviar a {correo_destino}: {e}")
#         return False




def enviar_correo(correo_destino, asunto, cuerpo, ruta_pdf=None):
    # Validar correo
    if not correo_valido(correo_destino):
        print(f"Correo inválido: {correo_destino}")
        return False

    mensaje = EmailMessage()
    mensaje['From'] = EMAIL_REMITENTE
    mensaje['To'] = correo_destino
    mensaje['Subject'] = asunto
    mensaje.set_content(cuerpo)

    # Intentar adjuntar el PDF solo si la ruta es válida y el archivo existe
    if ruta_pdf:
        if os.path.exists(ruta_pdf):
            try:
                with open(ruta_pdf, 'rb') as f:
                    mensaje.add_attachment(
                        f.read(),
                        maintype='application',
                        subtype='pdf',
                        filename=os.path.basename(ruta_pdf)
                    )
                    print(f"Adjunto agregado: {ruta_pdf}")
            except Exception as e:
                print(f"Error al adjuntar archivo: {e}")
        else:
            print(f"Advertencia: archivo no encontrado ({ruta_pdf}). Se enviará sin adjunto.")

    # Enviar correo
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
            servidor.login(EMAIL_REMITENTE, CONTRASENA)
            servidor.send_message(mensaje)

        print(f"Correo enviado a {correo_destino}")
        return True

    except Exception as e:
        print(f"Error al enviar correo a {correo_destino}: {e}")
        return False
