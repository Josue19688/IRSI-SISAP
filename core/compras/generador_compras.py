import os
import csv
from faker import Faker
from random import randint, choice
from datetime import datetime
from core.utils.logger import agregar_log


script_dir = os.path.dirname(os.path.abspath(__file__))
proyecto_dir = os.path.abspath(os.path.join(script_dir, "../../"))
log_path_csv = os.path.join(proyecto_dir, "data", "logs", "generacion_compras_csv.log")

def latex_escape(text):
    if not isinstance(text, str):
        text = str(text)
    replacements = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        'á': r"\'{a}",
        'é': r"\'{e}",
        'í': r"\'{i}",
        'ó': r"\'{o}",
        'ú': r"\'{u}",
        'Á': r"\'{A}",
        'É': r"\'{E}",
        'Í': r"\'{I}",
        'Ó': r"\'{O}",
        'Ú': r"\'{U}",
        'ñ': r'\~{n}',
        'Ñ': r'\~{N}',
    }
    for key, val in replacements.items():
        text = text.replace(key, val)
    return text

def crear_directorio_salida():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(BASE_DIR, "../../data", "csv")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def generar_registro(fake, idx):
    pagos = ["completo", "fraccionado"]
    estados = ["exitoso", "fallido"]

   
    nombre = latex_escape(fake.name())
    correo = latex_escape(fake.email())
    telefono = latex_escape(fake.phone_number())
    direccion = latex_escape(fake.street_address().replace(',', ''))
    ciudad = latex_escape(fake.city())
    cantidad = randint(1, 10)
    monto = round(cantidad * randint(50, 500), 2)
    pago = choice(pagos)
    estado_pago = choice(estados)
    ip = fake.ipv4()
    fecha_emision = fake.date()
    timestamp = datetime.now().isoformat()
    observaciones = latex_escape(choice(["Cliente frecuente", "Promoción aplicada", ""]))

    return [
        str(idx),
        fecha_emision,
        nombre,
        correo,
        telefono,
        direccion,
        ciudad,
        str(cantidad),
        str(monto),
        pago,
        estado_pago,
        ip,
        timestamp,
        observaciones
    ]

def generar_registros(num=10):
    fake = Faker('es-ES')
    registros = []
    for i in range(1, num+1):
        registros.append(generar_registro(fake, i))
    return registros

def guardar_csv(registros, output_dir):
    headers = [
        "id_transaccion", "fecha_emision", "nombre", "correo", "telefono",
        "direccion", "ciudad", "cantidad", "monto", "pago",
        "estado_pago", "ip", "timestamp", "observaciones"
    ]
    filename = f"compras_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(registros)
    
    agregar_log(log_path_csv, [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "CSV generado", filename, f"Registros: {len(registros)}"])
    
    return filepath

def generar_csv_compras(num_registros=10):
    output_dir = crear_directorio_salida()
    registros = generar_registros(num_registros)
    filepath = guardar_csv(registros, output_dir)
    print(f"Archivo generado: {filepath}")
    return filepath