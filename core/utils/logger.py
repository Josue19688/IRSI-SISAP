import os
import re
from datetime import datetime

def inicializar_logger(ruta_log):
   
    carpeta = os.path.dirname(ruta_log)
    os.makedirs(carpeta, exist_ok=True)

    if not os.path.exists(ruta_log):
        with open(ruta_log, "w", encoding="utf-8") as log:
            log.write(f"# LOG DE EVENTOS GENERADO EL {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


def agregar_log(ruta_log, datos):
   
    inicializar_logger(ruta_log)
    linea = ""
    if isinstance(datos, list):
        linea = " | ".join(str(d) for d in datos)
    else:
        linea = str(datos)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(ruta_log, "a", encoding="utf-8") as log:
        log.write(f"[{timestamp}] {linea}\n")


def leer_logs(ruta_log, filtro_regex=None):
   
    if not os.path.exists(ruta_log):
        print(f"Log no encontrado: {ruta_log}")
        return []

    with open(ruta_log, "r", encoding="utf-8") as log:
        lineas = log.readlines()

    if filtro_regex:
        patron = re.compile(filtro_regex, re.IGNORECASE)
        return [linea for linea in lineas if patron.search(linea)]
    
    return lineas
