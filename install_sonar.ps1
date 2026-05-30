$ErrorActionPreference = "Stop"
$Url = "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-6.2.1.4610-windows-x64.zip"
$ZipPath = "$env:TEMP\sonar-scanner.zip"
$InstallDir = "$env:USERPROFILE\sonar-scanner"

Write-Host "Descargando SonarScanner..."
Invoke-WebRequest -Uri $Url -OutFile $ZipPath

Write-Host "Extrayendo archivos..."
if (Test-Path "$env:TEMP\sonar-extract") { Remove-Item -Recurse -Force "$env:TEMP\sonar-extract" }
Expand-Archive -Path $ZipPath -DestinationPath "$env:TEMP\sonar-extract" -Force

Write-Host "Instalando en $InstallDir..."
if (Test-Path $InstallDir) { Remove-Item -Recurse -Force $InstallDir }
Move-Item -Path "$env:TEMP\sonar-extract\sonar-scanner-*" -Destination $InstallDir -Force

Write-Host "Limpiando archivos temporales..."
Remove-Item $ZipPath -Force
Remove-Item -Recurse -Force "$env:TEMP\sonar-extract"

Write-Host "Agregando al PATH de Windows..."
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
$BinPath = "$InstallDir\bin"

if ($UserPath -notlike "*$BinPath*") {
    [Environment]::SetEnvironmentVariable("Path", "$UserPath;$BinPath", "User")
    Write-Host "Se agregó correctamente al PATH."
} else {
    Write-Host "El PATH ya contenía SonarScanner."
}

Write-Host "¡Instalación completada exitosamente!"
