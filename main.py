
import os
import subprocess
import shutil
from scripts_python.generador_compras import generar_csv_compras


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


def main():
    """
                                                                                                        
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
    print("Generando archivo de compras...")
    archivo_csv = generar_csv_compras(10)
    print(f"Archivo generado: {archivo_csv}")

    ejecutar_script_bash("scripts_bash/generador_facturas.sh")


if __name__ == "__main__":
    main()
