# Script PowerShell para Executar Curadoria Automática
# Utiliza MCPs disponíveis para verificar qualidade, fontes e elementos visuais

param(
    [string]$Diretorio = "",
    [int]$MinPontuacao = 70,
    [switch]$Ajuda
)

if ($Ajuda) {
    Write-Host "=== CUARDORIA AUTOMÁTICA DE CONTEÚDO ===" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Uso: .\executar_curadoria.ps1 [opções]"
    Write-Host ""
    Write-Host "Opções:"
    Write-Host "  -Diretorio <caminho>    Diretório específico para analisar"
    Write-Host "  -MinPontuacao <numero>  Pontuação mínima para aprovação (padrão: 70)"
    Write-Host "  -Ajuda                  Mostra esta ajuda"
    Write-Host ""
    Write-Host "Exemplos:"
    Write-Host "  .\executar_curadoria.ps1"
    Write-Host "  .\executar_curadoria.ps1 -Diretorio '2_conteudo\04_publicado'"
    Write-Host "  .\executar_curadoria.ps1 -MinPontuacao 80"
    Write-Host ""
    exit 0
}

# Configurações
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjetoRoot = Split-Path -Parent $ScriptDir
$PythonScript = Join-Path $ScriptDir "curadoria_automatica.py"

Write-Host "🔍 CUARDORIA AUTOMÁTICA DE CONTEÚDO" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se o Python está disponível
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python não encontrado. Instale o Python 3.7+ e tente novamente." -ForegroundColor Red
    exit 1
}

# Verificar se o script Python existe
if (-not (Test-Path $PythonScript)) {
    Write-Host "❌ Script de curadoria não encontrado: $PythonScript" -ForegroundColor Red
    exit 1
}

# Construir comando
$comando = "python `"$PythonScript`""

if ($Diretorio) {
    $comando += " --diretorio `"$Diretorio`""
}

$comando += " --projeto `"$ProjetoRoot`""
$comando += " --min-pontuacao $MinPontuacao"

Write-Host "📁 Diretório do projeto: $ProjetoRoot" -ForegroundColor Yellow
if ($Diretorio) {
    Write-Host "📂 Diretório para analisar: $Diretorio" -ForegroundColor Yellow
} else {
    Write-Host "📂 Analisando diretório padrão: 2_conteudo" -ForegroundColor Yellow
}
Write-Host "🎯 Pontuação mínima para aprovação: $MinPontuacao%" -ForegroundColor Yellow
Write-Host ""

# Executar curadoria
Write-Host "🚀 Iniciando análise..." -ForegroundColor Green
Write-Host ""

try {
    Invoke-Expression $comando
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Curadoria concluída com sucesso!" -ForegroundColor Green
        Write-Host "📊 Relatórios salvos em: docs\relatorios\" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "❌ Erro durante a execução da curadoria." -ForegroundColor Red
        Write-Host "Verifique os logs para mais detalhes." -ForegroundColor Yellow
    }
} catch {
    Write-Host ""
    Write-Host "❌ Erro ao executar curadoria: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Pressione qualquer tecla para continuar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
