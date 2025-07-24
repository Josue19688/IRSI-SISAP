param (
    [string]$CsvPath = ".\empleados.csv"
)

$rootPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootPath = Split-Path -Parent $rootPath
$rootPath = Split-Path -Parent $rootPath  # Tres niveles arriba para llegar a raíz

$logDir = Join-Path $rootPath "data\logs"


# Crear carpeta de logs si no existe
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

# Función para generar contraseña segura
function Generar-Contrasenia {
    Add-Type -AssemblyName System.Web
    return [System.Web.Security.Membership]::GeneratePassword(12, 3)
}

# Procesar CSV
Import-Csv -Path $CsvPath | ForEach-Object {
    $nombre = $_.Nombre
    $apellido = $_.Apellido
    $correo = $_.Correo

    # Crear nombre de usuario (ej. jlopez)
    $usuario = ("{0}{1}" -f $nombre.Substring(0,1), $apellido).ToLower()

    # Generar contraseña
    $contrasenia = Generar-Contrasenia
    $securePassword = ConvertTo-SecureString $contrasenia -AsPlainText -Force

    # Verificar existencia
    if (Get-LocalUser -Name $usuario -ErrorAction SilentlyContinue) {
        Write-Output "⚠️ Usuario $usuario ya existe. Saltando..."
        return
    }

    try {
        # Crear usuario local
        New-LocalUser -Name $usuario `
                      -FullName "$nombre $apellido" `
                      -Password $securePassword `
                      -PasswordNeverExpires:$false `
                      -UserMayNotChangePassword:$false `
                      -Description "Usuario temporal creado automáticamente"

        # Agregar al grupo de administradores
        Add-LocalGroupMember -Group "Administradores" -Member $usuario

        # Guardar log individual
        $logFile = Join-Path $logDir "$usuario.log"
        $contenidoLog = @"
Usuario: $usuario
Nombre completo: $nombre $apellido
Correo: $correo
Contraseña: $contrasenia
Fecha de creación: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@
        $contenidoLog | Out-File -FilePath $logFile -Encoding utf8

        Write-Output "✅ Usuario $usuario creado correctamente."

    } catch {
        Write-Output ("❌ Error al crear {0}: {1}" -f $usuario, $_)

    }
}
