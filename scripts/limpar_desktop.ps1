# Script PowerShell para Limpeza Automática da Área de Trabalho
# NUNCA deixa arquivos poluindo o desktop

Write-Host "🧹 LIMPEZA AUTOMÁTICA DA ÁREA DE TRABALHO" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green

# Definir caminhos
$desktopPath = [Environment]::GetFolderPath("Desktop")
$projetoPath = Join-Path $desktopPath "modelo_projeto_conteudo"

# Criar pastas de organização se não existirem
$pastas = @("scripts", "docs", "binarios", "arquivos", "documentos", "imagens", "videos", "audio", "atalhos", "outros")

foreach ($pasta in $pastas) {
    $pastaPath = Join-Path $projetoPath $pasta
    if (-not (Test-Path $pastaPath)) {
        New-Item -ItemType Directory -Path $pastaPath -Force | Out-Null
        Write-Host "✅ Pasta criada: $pasta" -ForegroundColor Yellow
    }
}

# Função para determinar pasta de destino
function Get-DestinationFolder {
    param($file)
    
    $extension = [System.IO.Path]::GetExtension($file.Name).ToLower()
    
    # Ignorar arquivos do projeto e sistema
    if ($file.Name -like "*modelo_projeto_conteudo*" -or 
        $file.Name -eq "desktop.ini" -or 
        $file.Name -eq "thumbs.db") {
        return $null
    }
    
    # Mapear extensões para pastas
    $extensionMap = @{
        '.py' = 'scripts'
        '.json' = 'docs'
        '.md' = 'docs'
        '.html' = 'docs'
        '.csv' = 'docs'
        '.txt' = 'docs'
        '.log' = 'docs'
        '.ps1' = 'scripts'
        '.bat' = 'scripts'
        '.cmd' = 'scripts'
        '.exe' = 'binarios'
        '.msi' = 'binarios'
        '.zip' = 'arquivos'
        '.rar' = 'arquivos'
        '.7z' = 'arquivos'
        '.pdf' = 'documentos'
        '.doc' = 'documentos'
        '.docx' = 'documentos'
        '.xls' = 'documentos'
        '.xlsx' = 'documentos'
        '.ppt' = 'documentos'
        '.pptx' = 'documentos'
        '.png' = 'imagens'
        '.jpg' = 'imagens'
        '.jpeg' = 'imagens'
        '.gif' = 'imagens'
        '.bmp' = 'imagens'
        '.svg' = 'imagens'
        '.ico' = 'imagens'
        '.mp4' = 'videos'
        '.avi' = 'videos'
        '.mov' = 'videos'
        '.wmv' = 'videos'
        '.mp3' = 'audio'
        '.wav' = 'audio'
        '.flac' = 'audio'
        '.lnk' = 'atalhos'
    }
    
    $pasta = $extensionMap[$extension]
    if ($pasta) {
        return Join-Path $projetoPath $pasta
    } else {
        return Join-Path $projetoPath "outros"
    }
}

# Obter arquivos da área de trabalho
$arquivos = Get-ChildItem -Path $desktopPath -File

if ($arquivos.Count -eq 0) {
    Write-Host "✅ Área de trabalho já está limpa!" -ForegroundColor Green
    exit
}

Write-Host "📁 Encontrados $($arquivos.Count) arquivos na área de trabalho" -ForegroundColor Cyan
Write-Host ""

$arquivosMovidos = 0
$arquivosIgnorados = 0

foreach ($arquivo in $arquivos) {
    Write-Host "📄 Processando: $($arquivo.Name)" -ForegroundColor White
    
    $pastaDestino = Get-DestinationFolder -file $arquivo
    
    if ($pastaDestino -eq $null) {
        Write-Host "   ⏭️  Ignorado (arquivo de sistema ou projeto)" -ForegroundColor Yellow
        $arquivosIgnorados++
        continue
    }
    
    # Criar pasta se não existir
    if (-not (Test-Path $pastaDestino)) {
        New-Item -ItemType Directory -Path $pastaDestino -Force | Out-Null
    }
    
    # Verificar se arquivo já existe no destino
    $arquivoDestino = Join-Path $pastaDestino $arquivo.Name
    if (Test-Path $arquivoDestino) {
        # Adicionar timestamp para evitar conflito
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $nomeBase = [System.IO.Path]::GetFileNameWithoutExtension($arquivo.Name)
        $extensao = [System.IO.Path]::GetExtension($arquivo.Name)
        $novoNome = "${nomeBase}_${timestamp}${extensao}"
        $arquivoDestino = Join-Path $pastaDestino $novoNome
    }
    
    try {
        # Mover arquivo
        Move-Item -Path $arquivo.FullName -Destination $arquivoDestino -Force
        $pastaNome = Split-Path $pastaDestino -Leaf
        Write-Host "   ✅ Movido para: $pastaNome/" -ForegroundColor Green
        $arquivosMovidos++
    }
    catch {
        Write-Host "   ❌ Erro ao mover: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Exibir resumo final
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "📊 RESUMO DA ORGANIZAÇÃO" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "📁 Total de arquivos encontrados: $($arquivos.Count)" -ForegroundColor Cyan
Write-Host "✅ Arquivos organizados: $arquivosMovidos" -ForegroundColor Green
Write-Host "⏭️  Arquivos ignorados: $arquivosIgnorados" -ForegroundColor Yellow
Write-Host ""
Write-Host "🎉 ÁREA DE TRABALHO ORGANIZADA COM SUCESSO!" -ForegroundColor Green
