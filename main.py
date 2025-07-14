
import os
import subprocess
import shutil
from scripts_python.generador_compras import generar_csv_compras
from scripts_python.enviador import procesar_csv, resumen_final
import argparse



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


def main(query, factura, informe, enviar):
    if query:
        print("Generando archivo de compras...")
        archivo_csv = generar_csv_compras(10)
        print(f"Archivo generado: {archivo_csv}")

    if factura:
        ejecutar_script_bash("scripts_bash/generador_facturas.sh")

    if informe:
        resumen_final()

    if enviar:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        #ruta_csv = os.path.join(script_dir, "../data/pendientes_envio.csv")
        ruta_csv = os.path.join(script_dir, "data", "pendientes_envio.csv")

        if not os.path.exists(ruta_csv):
            print(f"Archivo CSV no encontrado: {ruta_csv}")
            return
        procesar_csv(ruta_csv)
        resumen_final()


if __name__ == "__main__":
    print(ascii_art)
    parse = argparse.ArgumentParser(description="Esta herramienta nos permite realizar gestión")
    parse.add_argument("-q", "--query", type=str,
                       help="Genera el cvs compras")
    parse.add_argument("-f", "--factura", type=str,
                       help="Genera facturas de compras")
    parse.add_argument("-r", "--informe", type=str,
                       help="Genera el informe de compras")
    parse.add_argument("-e", "--enviar", type=str,
                       help="Enviar Facturas a clientes")
    args=parse.parse_args()
    main(query=args.query, factura=args.factura, informe=args.informe, enviar=args.enviar)

















