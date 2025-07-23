
import os
import subprocess
import shutil
from core.compras.generador_compras import generar_csv_compras
from core.envios.enviador import procesar_csv
from infrastruture.reportes.resumen_diario import resumen_logs_multiples
import argparse
import sys

# Ruta del proyecto
RAIZ_PROYECTO = os.path.dirname(os.path.abspath(__file__))

# Agrega al sys.path si vas a importar módulos que usan rutas relativas
sys.path.append(RAIZ_PROYECTO)


ascii_art=r"""                                                                                               
            :#**********************************************************************************#.       
        .******************************************************************************************     
        #********************************************************************************************=   
        ******#                                                                                 .******#  
        =*****.                                                                                    +*****  
        +*****                                                                                      *****: 
        +*****                                                                                      *****: 
        +*****        @@@@@@@@@@@@@  :@@@@   @@@@@@@@@@@@@:       @@@@:       @@@@@@@@@@@@@         *****: 
        +*****       @@@@@@@@@@@@@@  :@@@@  @@@@@@@@@@@@@@:      @@@@@@       @@@@@@@@@@@@@@*       *****: 
        +*****       @@@@.           :@@@@  @@@@                @@@@@@@@      @@@@-     +@@@@       *****: 
        +*****       @@@@@@@@@@@@@   :@@@@  @@@@@@@@@@@@@      @@@@@@@@@@     @@@@-      @@@@       *****: 
        +*****        @@@@@@@@@@@@@* :@@@@   @@@@@@@@@@@@@%   =@@@@**@@@@@    @@@@@@@@@@@@@@@       *****: 
        +*****                 :@@@@ :@@@@            .@@@@  -@@@@@@@@@@@@+   @@@@@@@@@@@@@@        *****: 
        +*****       @@@@@@@@@@@@@@@ :@@@@  @@@@@@@@@@@@@@@ .@@@@@@@@@@@@@@-  @@@@@@@@@@@#          *****: 
        +*****       @@@@@@@@@@@@@@- :@@@@  @@@@@@@@@@@@@@+ @@@@@      @@@@@. @@@@-                 *****: 
        +*****       @@@@@@@@@@@@@   :@@@@  @@@@@@@@@@@@@  @@@@@        @@@@@ @@@@-                 *****: 
        ::::::                                                                                      :::::. 
                                                                                                            
        **************************************************************************************************
        **************************************************************************************************
        **************************************************************************************************                                      
                                                                                                            
        """

def obtener_ruta_bash():
    bash_path = shutil.which("bash")
    if not bash_path:
        raise EnvironmentError(
            "No se encontró 'bash.exe'. Asegúrate de tener Git Bash instalado y agregado al PATH."
        )
    return bash_path


def ejecutar_script_bash(ruta_script_relativa):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_script = os.path.join(base_dir, ruta_script_relativa)

    if not os.path.exists(ruta_script):
        raise FileNotFoundError(f"El script no existe: {ruta_script}")

    bash_path = obtener_ruta_bash()

    print(f"Ejecutando script Bash: {ruta_script}\n")

    resultado = subprocess.run(
        [bash_path, ruta_script],
        capture_output=True,
        text=True
    )

    if resultado.stdout:
        print("Salida del script:\n", resultado.stdout)
    if resultado.stderr:
        print("Errores del script:\n", resultado.stderr)

    print("Código de salida:", resultado.returncode)
    print("-" * 60)


def main(generar, factura, informe, enviar):
    if generar:
        print("Generando archivo de compras...")
        archivo_csv = generar_csv_compras(3)
        print(f"Archivo generado: {archivo_csv}")

    if factura:
        ejecutar_script_bash("core/facturacion/generador_facturas.sh")

    if informe:
        resumen_logs_multiples()

    if enviar:
        script_dir = os.path.dirname(os.path.abspath(__file__))  # /core/envios

        ruta_csv = os.path.join(script_dir, "data", "csv", "pendientes_envio.csv")
        print(f"Procesando archivo CSV: {ruta_csv}")

        if not os.path.exists(ruta_csv):
            print(f"Archivo CSV no encontrado: {ruta_csv}")
            return
        procesar_csv(ruta_csv)
        #resumen_final()


if __name__ == "__main__":
    print(ascii_art)
    parse = argparse.ArgumentParser(description="Esta herramienta nos permite realizar gestión")
    parse.add_argument("-g", "--generar", type=str,
                       help="Genera el cvs compras")
    parse.add_argument("-f", "--factura", type=str,
                       help="Genera facturas de compras")
    parse.add_argument("-i", "--informe", type=str,
                       help="Genera el informe de compras")
    parse.add_argument("-e", "--enviar", type=str,
                       help="Enviar Facturas a clientes")
    args=parse.parse_args()
    main(generar=args.generar, factura=args.factura, informe=args.informe, enviar=args.enviar)

















