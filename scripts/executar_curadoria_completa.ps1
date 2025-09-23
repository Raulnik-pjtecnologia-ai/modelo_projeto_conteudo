# Script PowerShell para Executar Curadoria Completa
# Integra verificação de capas, dados, vídeos, fontes e busca de fontes confiáveis

param(
    [string]$Diretorio = "",
    [int]$MinPontuacao = 70,
    [switch]$Ajuda
)

if ($Ajuda) {
    Write-Host "=== CUARDORIA COMPLETA DE CONTEÚDO ===" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Uso: .\executar_curadoria_completa.ps1 [opções]"
    Write-Host ""
    Write-Host "Opções:"
    Write-Host "  -Diretorio <caminho>    Diretório específico para analisar"
    Write-Host "  -MinPontuacao <numero>  Pontuação mínima para aprovação (padrão: 70)"
    Write-Host "  -Ajuda                  Mostra esta ajuda"
    Write-Host ""
    Write-Host "Funcionalidades:"
    Write-Host "  ✅ Verificação de capas (.jpg, .png, etc.)"
    Write-Host "  📊 Análise de dados e gráficos"
    Write-Host "  🎥 Verificação de vídeos relacionados"
    Write-Host "  📚 Análise de fontes e referências"
    Write-Host "  🔍 Busca de fontes confiáveis usando MCPs"
    Write-Host "  📈 Relatório consolidado com recomendações"
    Write-Host ""
    Write-Host "Exemplos:"
    Write-Host "  .\executar_curadoria_completa.ps1"
    Write-Host "  .\executar_curadoria_completa.ps1 -Diretorio '2_conteudo\04_publicado'"
    Write-Host "  .\executar_curadoria_completa.ps1 -MinPontuacao 80"
    Write-Host ""
    exit 0
}

# Configurações
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjetoRoot = Split-Path -Parent $ScriptDir
$PythonScript = Join-Path $ScriptDir "curadoria_completa.py"

Write-Host "🔍 CUARDORIA COMPLETA DE CONTEÚDO" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
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
    Write-Host "❌ Script de curadoria completa não encontrado: $PythonScript" -ForegroundColor Red
    exit 1
}

# Verificar dependências
Write-Host "🔍 Verificando dependências..." -ForegroundColor Yellow

$dependencias = @(
    "curadoria_automatica.py",
    "verificar_fontes_mcp.py", 
    "buscar_fontes_confiaveis.py"
)

foreach ($dep in $dependencias) {
    $caminho_dep = Join-Path $ScriptDir $dep
    if (Test-Path $caminho_dep) {
        Write-Host "  ✅ $dep" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $dep não encontrado" -ForegroundColor Red
        Write-Host "  Certifique-se de que todos os scripts estão no diretório scripts/" -ForegroundColor Yellow
        exit 1
    }
}

# Construir comando
$comando = "python `"$PythonScript`""

if ($Diretorio) {
    $comando += " --diretorio `"$Diretorio`""
}

$comando += " --projeto `"$ProjetoRoot`""
$comando += " --min-pontuacao $MinPontuacao"

Write-Host ""
Write-Host "📁 Diretório do projeto: $ProjetoRoot" -ForegroundColor Yellow
if ($Diretorio) {
    Write-Host "📂 Diretório para analisar: $Diretorio" -ForegroundColor Yellow
} else {
    Write-Host "📂 Analisando diretório padrão: 2_conteudo" -ForegroundColor Yellow
}
Write-Host "🎯 Pontuação mínima para aprovação: $MinPontuacao%" -ForegroundColor Yellow
Write-Host ""

# Executar curadoria completa
Write-Host "🚀 Iniciando curadoria completa..." -ForegroundColor Green
Write-Host ""

try {
    Write-Host "📋 Executando verificações..." -ForegroundColor Cyan
    Invoke-Expression $comando
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Curadoria completa concluída com sucesso!" -ForegroundColor Green
        Write-Host "📊 Relatórios salvos em: docs\relatorios\" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "📈 Resumo da análise:" -ForegroundColor Yellow
        Write-Host "  • Verificação de capas (.jpg, .png, etc.)" -ForegroundColor White
        Write-Host "  • Análise de dados e gráficos" -ForegroundColor White
        Write-Host "  • Verificação de vídeos relacionados" -ForegroundColor White
        Write-Host "  • Análise de fontes e referências" -ForegroundColor White
        Write-Host "  • Busca de fontes confiáveis" -ForegroundColor White
        Write-Host "  • Relatório consolidado gerado" -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "❌ Erro durante a execução da curadoria completa." -ForegroundColor Red
        Write-Host "Verifique os logs para mais detalhes." -ForegroundColor Yellow
    }
} catch {
    Write-Host ""
    Write-Host "❌ Erro ao executar curadoria completa: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Pressione qualquer tecla para continuar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
