import csv
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

def registrar_envio(nombre_pdf, correo, estado):
    with open("log_envios.csv", "a", newline='', encoding='utf-8') as log:
        escritor = csv.writer(log)
        escritor.writerow([nombre_pdf, correo, estado])

def limpiar_pendientes(pendientes):
    with open("pendientes_envio.csv", "w", newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(pendientes)


def corregir_ruta_windows(ruta):
    ruta = ruta.strip()
    if ruta.startswith("\\") and len(ruta) > 2 and ruta[1].isalpha():
        letra_unidad = ruta[1].upper()
        ruta = letra_unidad + ":" + ruta[2:]  
    elif ruta.startswith("/") and len(ruta) > 2 and ruta[1].isalpha():
        letra_unidad = ruta[1].upper()
        ruta = letra_unidad + ":" + ruta[2:]
    
    return os.path.normpath(ruta)


# def enviar_factura(correo_destino, ruta_pdf):
#     if not os.path.exists(ruta_pdf):
#         print(f"Archivo no encontrado: {ruta_pdf}")
#         return

#     if not correo_valido(correo_destino):
#         print(f"Correo inválido: {correo_destino}")
#         return

#     nombre_pdf = os.path.basename(ruta_pdf)
#     mensaje = EmailMessage()
#     mensaje['From'] = EMAIL_REMITENTE
#     mensaje['To'] = correo_destino
#     mensaje['Subject'] = ASUNTO
#     mensaje.set_content(CUERPO)

#     with open(ruta_pdf, 'rb') as f:
#         mensaje.add_attachment(f.read(), maintype='application', subtype='pdf', filename=nombre_pdf)

#     try:
#         with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
#             servidor.login(EMAIL_REMITENTE, CONTRASENA)
#             servidor.send_message(mensaje)
#             registrar_envio(nombre_pdf, correo_destino, "exitoso")
#         print(f"Enviado: {nombre_pdf} a {correo_destino}")
#     except Exception as e:
#         registrar_envio(nombre_pdf, correo_destino, f"fallido: {e}")
#         print(f"Error al enviar a {correo_destino}: {e}")


def enviar_factura(correo_destino, ruta_pdf):
    if not os.path.exists(ruta_pdf):
        print(f"Archivo no encontrado: {ruta_pdf}")
        return False

    if not correo_valido(correo_destino):
        print(f"Correo inválido: {correo_destino}")
        return False

    nombre_pdf = os.path.basename(ruta_pdf)
    mensaje = EmailMessage()
    mensaje['From'] = EMAIL_REMITENTE
    mensaje['To'] = correo_destino
    mensaje['Subject'] = ASUNTO
    mensaje.set_content(CUERPO)

    try:
        with open(ruta_pdf, 'rb') as f:
            mensaje.add_attachment(f.read(), maintype='application', subtype='pdf', filename=nombre_pdf)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
            servidor.login(EMAIL_REMITENTE, CONTRASENA)
            servidor.send_message(mensaje)

        print(f"Enviado: {nombre_pdf} a {correo_destino}")
        return True

    except Exception as e:
        print(f"Error al enviar a {correo_destino}: {e}")
        return False


# def procesar_csv(ruta_csv):
#     if not os.path.exists(ruta_csv):
#         print(f"Archivo CSV no encontrado: {ruta_csv}")
#         return

#     pendientes_restantes = []

#     with open(ruta_csv, newline='', encoding='utf-8') as archivo:
#         lector = csv.reader(archivo)
#         for fila in lector:
#             if len(fila) != 2:
#                 print(f"Línea inválida: {fila}")
#                 continue

#             ruta_pdf = corregir_ruta_windows(fila[0])
#             correo = fila[1].strip()
#             nombre_pdf = os.path.basename(ruta_pdf)

#             if enviar_factura(correo, ruta_pdf):
#                 registrar_envio(nombre_pdf, correo, "exitoso")
#             else:
#                 registrar_envio(nombre_pdf, correo, "fallido")
#                 pendientes_restantes.append(fila)

#     # Guardar pendientes no enviados al final
#     limpiar_pendientes(pendientes_restantes)

def procesar_csv(ruta_csv):
    if not os.path.exists(ruta_csv):
        print(f"Archivo CSV no encontrado: {ruta_csv}")
        return

    pendientes_restantes = []

    with open(ruta_csv, newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            if len(fila) != 2:
                print(f"Línea inválida: {fila}")
                continue

            ruta_pdf = corregir_ruta_windows(fila[0])
            correo = fila[1].strip()
            nombre_pdf = os.path.basename(ruta_pdf)

            exito = enviar_factura(correo, ruta_pdf)
            estado = "exitoso" if exito else "fallido"
            registrar_envio(nombre_pdf, correo, estado)

            if not exito:
                pendientes_restantes.append(fila)

    # Sobrescribe el archivo con solo los fallidos
    with open(ruta_csv, "w", newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(pendientes_restantes)

    print(f"Archivo '{os.path.basename(ruta_csv)}' actualizado con {len(pendientes_restantes)} pendientes.")


def resumen_final():
    if not os.path.exists("log_envios.csv"):
        print("No se encontró 'log_envios.csv'. Aún no se han registrado envíos.")
        return

    total = exitosos = fallidos = 0
    with open("log_envios.csv", newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            total += 1
            if 'exitoso' in fila[2].lower():
                exitosos += 1
            else:
                fallidos += 1
    print(f"Resumen del día:\nTotal: {total}, Exitosos: {exitosos}, Fallidos: {fallidos}")


if __name__ == "__main__":
    #resumen_final()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    archivo_csv = os.path.join(script_dir, "../data/pendientes_envio.csv")
    archivo_csv = os.path.abspath(archivo_csv)  # Convierte a ruta absoluta

   
    procesar_csv(archivo_csv)

    
    resumen_final()