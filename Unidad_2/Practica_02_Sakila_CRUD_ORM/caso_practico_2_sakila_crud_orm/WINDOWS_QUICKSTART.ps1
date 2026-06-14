$ErrorActionPreference = "Stop"

$ContainerName = if ($env:CONTAINER_NAME) { $env:CONTAINER_NAME } else { "sakila-mysql" }
$MysqlImage = if ($env:MYSQL_IMAGE) { $env:MYSQL_IMAGE } else { "mysql:8.0" }
$MysqlRootPassword = if ($env:MYSQL_ROOT_PASSWORD) { $env:MYSQL_ROOT_PASSWORD } else { "sakila123" }
$MysqlDatabase = if ($env:MYSQL_DATABASE) { $env:MYSQL_DATABASE } else { "sakila" }
$MysqlPort = if ($env:MYSQL_PORT) { $env:MYSQL_PORT } else { "3307" }
$SakilaUrl = "https://downloads.mysql.com/docs/sakila-db.zip"
$SakilaZip = Join-Path $env:TEMP "sakila-db.zip"
$SakilaDir = Join-Path $env:TEMP "sakila-db"

Set-Location $PSScriptRoot

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==> $Message"
}

Write-Host "Quickstart Windows - Sakila CRUD/ORM"
Write-Host "Requisitos: Docker Desktop activo y Python 3 instalado."

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker no esta instalado o no esta en PATH."
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python no esta instalado o no esta en PATH."
}

Write-Step "Verificando Docker"
docker info | Out-Null

$ExistingContainer = docker ps -a --format "{{.Names}}" | Where-Object { $_ -eq $ContainerName }
$RunningContainer = docker ps --format "{{.Names}}" | Where-Object { $_ -eq $ContainerName }

if ($ExistingContainer) {
    if (-not $RunningContainer) {
        Write-Step "Iniciando contenedor $ContainerName"
        docker start $ContainerName | Out-Null
    } else {
        Write-Step "El contenedor $ContainerName ya esta corriendo"
    }
} else {
    Write-Step "Creando contenedor MySQL $ContainerName en puerto $MysqlPort"
    docker run --name $ContainerName `
        -e MYSQL_ROOT_PASSWORD=$MysqlRootPassword `
        -e MYSQL_DATABASE=$MysqlDatabase `
        -p "${MysqlPort}:3306" `
        -d $MysqlImage | Out-Null
}

Write-Step "Esperando a que MySQL este listo"
do {
    Start-Sleep -Seconds 2
    docker exec $ContainerName mysqladmin ping -uroot "-p$MysqlRootPassword" *> $null
    $Ready = $LASTEXITCODE -eq 0
} until ($Ready)

$TableCount = docker exec $ContainerName mysql -uroot "-p$MysqlRootPassword" -Nse "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '$MysqlDatabase';" 2>$null

if ([int]$TableCount -lt 10) {
    Write-Step "Importando base de datos Sakila"

    if ((-not (Test-Path (Join-Path $SakilaDir "sakila-schema.sql"))) -or (-not (Test-Path (Join-Path $SakilaDir "sakila-data.sql")))) {
        Write-Step "Descargando Sakila oficial"
        Invoke-WebRequest -Uri $SakilaUrl -OutFile $SakilaZip
        Expand-Archive -Path $SakilaZip -DestinationPath $env:TEMP -Force
    }

    docker cp (Join-Path $SakilaDir "sakila-schema.sql") "${ContainerName}:/tmp/sakila-schema.sql"
    docker cp (Join-Path $SakilaDir "sakila-data.sql") "${ContainerName}:/tmp/sakila-data.sql"
    docker exec $ContainerName mysql -uroot "-p$MysqlRootPassword" -e "SOURCE /tmp/sakila-schema.sql; SOURCE /tmp/sakila-data.sql;"
} else {
    Write-Step "Sakila ya parece estar importada ($TableCount tablas)"
}

$env:SAKILA_DB_HOST = "127.0.0.1"
$env:SAKILA_DB_PORT = $MysqlPort
$env:SAKILA_DB_USER = "root"
$env:SAKILA_DB_PASSWORD = $MysqlRootPassword
$env:SAKILA_DB_NAME = $MysqlDatabase

Write-Step "Probando conexion desde Python"
python -m src.check_connection

Write-Step "Abriendo menu CRUD/ORM"
python -m src.main
