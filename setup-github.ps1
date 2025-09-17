# Script PowerShell para Configuração do GitHub
# Execute como: .\setup-github.ps1

Write-Host "🚀 Configurando projeto para GitHub..." -ForegroundColor Green

# Verificar se Git está instalado
Write-Host "🔍 Verificando instalação do Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✅ Git encontrado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git não encontrado!" -ForegroundColor Red
    Write-Host "📥 Instale o Git em: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "📖 Ou siga as instruções em: INSTALACAO_GIT.md" -ForegroundColor Yellow
    exit 1
}

# Verificar se estamos no diretório correto
$currentDir = Get-Location
if (-not (Test-Path "README.md")) {
    Write-Host "❌ Execute este script no diretório do projeto!" -ForegroundColor Red
    Write-Host "📁 Diretório atual: $currentDir" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Diretório correto encontrado" -ForegroundColor Green

# Configurar Git (se não configurado)
Write-Host "⚙️ Configurando Git..." -ForegroundColor Yellow
$userName = git config --global user.name
$userEmail = git config --global user.email

if (-not $userName -or -not $userEmail) {
    Write-Host "🔧 Configuração do Git necessária" -ForegroundColor Yellow
    $name = Read-Host "Digite seu nome completo"
    $email = Read-Host "Digite seu email"
    
    git config --global user.name $name
    git config --global user.email $email
    Write-Host "✅ Git configurado com sucesso" -ForegroundColor Green
} else {
    Write-Host "✅ Git já configurado: $userName <$userEmail>" -ForegroundColor Green
}

# Inicializar repositório Git
Write-Host "📁 Inicializando repositório Git..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✅ Repositório Git inicializado" -ForegroundColor Green
} else {
    Write-Host "✅ Repositório Git já existe" -ForegroundColor Green
}

# Adicionar arquivos
Write-Host "📦 Adicionando arquivos..." -ForegroundColor Yellow
git add .
Write-Host "✅ Arquivos adicionados" -ForegroundColor Green

# Fazer commit
Write-Host "💾 Fazendo commit..." -ForegroundColor Yellow
$commitMessage = "Estrutura inicial do projeto - v1.0.0"
git commit -m $commitMessage
Write-Host "✅ Commit realizado: $commitMessage" -ForegroundColor Green

# Verificar se já existe repositório remoto
$remoteUrl = git remote get-url origin 2>$null
if ($remoteUrl) {
    Write-Host "✅ Repositório remoto já configurado: $remoteUrl" -ForegroundColor Green
} else {
    Write-Host "🔗 Configurando repositório remoto..." -ForegroundColor Yellow
    Write-Host "📝 Primeiro, crie um repositório no GitHub:" -ForegroundColor Cyan
    Write-Host "   1. Acesse: https://github.com/new" -ForegroundColor White
    Write-Host "   2. Nome: modelo_projeto_conteudo" -ForegroundColor White
    Write-Host "   3. Descrição: Modelo profissional para gestão de conteúdo editorial educacional" -ForegroundColor White
    Write-Host "   4. Público ✅" -ForegroundColor White
    Write-Host "   5. NÃO marque 'Initialize with README'" -ForegroundColor White
    Write-Host "   6. Clique 'Create repository'" -ForegroundColor White
    Write-Host ""
    
    $githubUser = Read-Host "Digite seu usuário do GitHub"
    $remoteUrl = "https://github.com/$githubUser/modelo_projeto_conteudo.git"
    
    git remote add origin $remoteUrl
    Write-Host "✅ Repositório remoto configurado: $remoteUrl" -ForegroundColor Green
}

# Renomear branch para main
Write-Host "🌿 Configurando branch main..." -ForegroundColor Yellow
git branch -M main
Write-Host "✅ Branch configurada como 'main'" -ForegroundColor Green

# Fazer push
Write-Host "🚀 Enviando para GitHub..." -ForegroundColor Yellow
Write-Host "⚠️ Se solicitado, use seu Personal Access Token como senha" -ForegroundColor Yellow
Write-Host "🔑 Token: https://github.com/settings/tokens" -ForegroundColor Cyan

try {
    git push -u origin main
    Write-Host "✅ Projeto enviado para GitHub com sucesso!" -ForegroundColor Green
    Write-Host "🌐 Acesse: $remoteUrl" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Erro ao enviar para GitHub" -ForegroundColor Red
    Write-Host "💡 Verifique:" -ForegroundColor Yellow
    Write-Host "   - Se o repositório foi criado no GitHub" -ForegroundColor White
    Write-Host "   - Se você tem permissão de escrita" -ForegroundColor White
    Write-Host "   - Se está usando o token correto" -ForegroundColor White
    Write-Host "   - Se a URL do repositório está correta" -ForegroundColor White
}

Write-Host ""
Write-Host "🎉 Configuração concluída!" -ForegroundColor Green
Write-Host "📚 Próximos passos:" -ForegroundColor Cyan
Write-Host "   1. Acesse seu repositório no GitHub" -ForegroundColor White
Write-Host "   2. Configure colaboradores se necessário" -ForegroundColor White
Write-Host "   3. Crie uma release v1.0.0" -ForegroundColor White
Write-Host "   4. Compartilhe o projeto!" -ForegroundColor White
