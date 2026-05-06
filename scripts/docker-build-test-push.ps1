<#
.SYNOPSIS
    Constrói a imagem Docker, corre pytest no container e faz push para um registo.

.PARAMETER Image
    Nome completo da imagem sem tag (ex.: ghcr.io/owner/cardioia ou docker.io/user/cardioia).

.PARAMETER Tag
    Tag a publicar (por defeito: latest).

.PARAMETER SkipPush
    Só build + testes, sem docker push.

.PARAMETER EnvFile
    Caminho para .env a injetar nos testes (opcional).
#>
param(
    [Parameter(Mandatory = $true)]
    [string] $Image,

    [string] $Tag = "latest",

    [switch] $SkipPush,

    [string] $EnvFile = ""
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $root

$localTag = "cardioia:local-test"
Write-Host "==> docker build -t $localTag"
docker build -t $localTag .

$envArgs = @()
if ($EnvFile -ne "" -and (Test-Path $EnvFile)) {
    $envArgs = @("--env-file", $EnvFile)
}

Write-Host "==> pytest dentro do container"
docker run --rm @envArgs $localTag python -m pytest backend/tests agents/tests -q --tb=short

if (-not $SkipPush) {
    $remote = "${Image}:${Tag}"
    Write-Host "==> docker tag + push $remote"
    docker tag $localTag $remote
    docker push $remote
    if ($Tag -ne "latest") {
        $latest = "${Image}:latest"
        docker tag $localTag $latest
        docker push $latest
    }
}

Write-Host "Concluído."
