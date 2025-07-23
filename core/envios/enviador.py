import csv
import os
from core.utils.logger import agregar_log
from .enviar_correo import enviar_correo

EMAIL_DESTINO = "advinjosuev899@gmail.com"
ASUNTO = "Factura Electrónica"
CUERPO = """Estimado cliente,

Adjunto a este correo encontrará su factura en formato PDF.

Saludos cordiales,
Tu Empresa"""

script_dir = os.path.dirname(os.path.abspath(__file__))
proyecto_dir = os.path.abspath(os.path.join(script_dir, "../../"))
log_path = os.path.join(proyecto_dir, "data", "logs", "log_envios.log")

def registrar_envio(nombre_pdf, correo, estado):
    agregar_log(log_path, [nombre_pdf, correo, estado])

def limpiar_pendientes(pendientes):
    ruta_pendientes = os.path.join(proyecto_dir, "data", "csv", "pendientes_envio.csv")
    with open(ruta_pendientes, "w", newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(pendientes)

def corregir_ruta_windows(ruta):
    ruta = ruta.strip()
    if not ruta:
        return None

    # Soporte para rutas tipo /c/Users/... => C:\Users\...
    if ruta.startswith("/"):
        partes = ruta.lstrip("/").split("/", 1)
        if len(partes) == 2 and len(partes[0]) == 1 and partes[0].isalpha():
            letra_unidad = partes[0].upper()
            resto = partes[1].replace("/", "\\")
            ruta = f"{letra_unidad}:\\" + resto
        else:
            ruta = ruta.replace("/", "\\")
    else:
        ruta = ruta.replace("/", "\\")

    # Normalizar y resolver rutas relativas (../..)
    ruta = os.path.normpath(ruta)

    if ruta in ('\\', ''):
        return None

    return ruta

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

            ruta_original = fila[0].strip()
            correo = fila[1].strip()

            ruta_pdf = corregir_ruta_windows(ruta_original)
            print(f"📂 Ruta corregida del PDF: {ruta_pdf}")

            if not ruta_pdf or not os.path.isfile(ruta_pdf):
                print(f"❌ Archivo no encontrado: {ruta_pdf}")
                pendientes_restantes.append(fila)
                continue

            print(f"📨 Enviando PDF: {ruta_pdf} a {correo}")
            # exito = enviar_correo(correo, ASUNTO, CUERPO, ruta_pdf)
            exito = enviar_correo(correo, ASUNTO, CUERPO, [ruta_pdf])
            estado = "exitoso" if exito else "fallido"
            registrar_envio(os.path.basename(ruta_pdf), correo, estado)

            if not exito:
                pendientes_restantes.append(fila)

    limpiar_pendientes(pendientes_restantes)

