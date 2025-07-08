import csv
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


def corregir_ruta_windows(ruta):
    ruta = ruta.strip()
    if ruta.startswith("\\") and len(ruta) > 2 and ruta[1].isalpha():
        letra_unidad = ruta[1].upper()
        ruta = letra_unidad + ":" + ruta[2:]  #
    elif ruta.startswith("/") and len(ruta) > 2 and ruta[1].isalpha():
        letra_unidad = ruta[1].upper()
        ruta = letra_unidad + ":" + ruta[2:]
    
    return os.path.normpath(ruta)


def enviar_factura(correo_destino, ruta_pdf):
    if not os.path.exists(ruta_pdf):
        print(f"Archivo no encontrado: {ruta_pdf}")
        return

    nombre_pdf = os.path.basename(ruta_pdf)
    mensaje = EmailMessage()
    mensaje['From'] = EMAIL_REMITENTE
    mensaje['To'] = correo_destino
    mensaje['Subject'] = ASUNTO
    mensaje.set_content(CUERPO)

    with open(ruta_pdf, 'rb') as f:
        mensaje.add_attachment(f.read(), maintype='application', subtype='pdf', filename=nombre_pdf)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
            servidor.login(EMAIL_REMITENTE, CONTRASENA)
            servidor.send_message(mensaje)
        print(f"Enviado: {nombre_pdf} a {correo_destino}")
    except Exception as e:
        print(f"Error al enviar a {correo_destino}: {e}")

def procesar_csv(ruta_csv):
    if not os.path.exists(ruta_csv):
        print(f"Archivo CSV no encontrado: {ruta_csv}")
        return

    with open(ruta_csv, newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            if len(fila) != 2:
                print(f"Línea inválida: {fila}")
                continue

           
            ruta_pdf = corregir_ruta_windows(fila[0])
            correo = fila[1].strip()
            print(correo)
            print(ruta_pdf)
            enviar_factura(correo, ruta_pdf)

if __name__ == "__main__":
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    archivo_csv = os.path.join(script_dir, "../data/pendientes_envio.csv")
    archivo_csv = os.path.abspath(archivo_csv)  # Convierte a ruta absoluta

   
    procesar_csv(archivo_csv)
