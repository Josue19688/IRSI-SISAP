import subprocess
from scripts_python.generador_compras import generar_csv_compras

def ejecutar_script_bash(ruta_script):
    bash_path = r"C:\Program Files\Git\bin\bash.exe"  # Ajusta según tu ruta
    resultado = subprocess.run([bash_path, ruta_script], capture_output=True, text=True)
    print("Salida del script bash:\n", resultado.stdout)
    if resultado.stderr:
        print("Errores del script bash:\n", resultado.stderr)
    print("Código de salida:", resultado.returncode)


def main():
    archivo = generar_csv_compras(10)
    print(f"Archivo generado en: {archivo}")

    # Ejecutar script bash después
    ruta_script = "scripts_bash/generador_facturas.sh"  # Cambia esta ruta por la correcta
    ejecutar_script_bash(ruta_script)


if __name__ == "__main__":
    main()
