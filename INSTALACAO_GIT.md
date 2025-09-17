# 🔧 Instalação do Git - Passo a Passo

## ⚠️ Git Não Encontrado

O Git não está instalado no seu sistema. Siga estas instruções para instalar e configurar:

## 📥 Instalação do Git

### Windows (Recomendado)
1. **Baixe o Git** em: https://git-scm.com/download/win
2. **Execute o instalador** e siga as instruções
3. **Mantenha as configurações padrão** (recomendado)
4. **Reinicie o terminal** após a instalação

### Verificação da Instalação
Após instalar, abra um novo terminal e execute:
```bash
git --version
```
Deve retornar algo como: `git version 2.43.0.windows.1`

## ⚡ Instalação Rápida via Chocolatey (Alternativa)
Se você tem o Chocolatey instalado:
```bash
choco install git
```

## ⚡ Instalação via Winget (Windows 10/11)
```bash
winget install --id Git.Git -e --source winget
```

## 🚀 Após a Instalação

### 1. Configurar Git (primeira vez)
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

### 2. Navegar para o projeto
```bash
cd "C:\Users\GasTed\Desktop\modelo_projeto_conteudo"
```

### 3. Inicializar repositório
```bash
git init
git add .
git commit -m "Estrutura inicial do projeto - v1.0.0"
```

### 4. Criar repositório no GitHub
1. Acesse: https://github.com/new
2. Nome: `modelo_projeto_conteudo`
3. Descrição: `Modelo profissional para gestão de conteúdo editorial educacional`
4. Público ✅
5. **NÃO** marque "Initialize with README"
6. Clique "Create repository"

### 5. Conectar e enviar
```bash
git remote add origin https://github.com/SEU_USUARIO/modelo_projeto_conteudo.git
git branch -M main
git push -u origin main
```

## 🔐 Configuração de Autenticação

### Opção 1: Personal Access Token (Recomendado)
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Selecionar: `repo`, `workflow`
4. Copiar token
5. Usar token como senha ao fazer push

### Opção 2: GitHub CLI (Mais Fácil)
```bash
# Instalar GitHub CLI
winget install GitHub.cli

# Fazer login
gh auth login

# Criar repositório e fazer push automaticamente
gh repo create modelo_projeto_conteudo --public --source=. --remote=origin --push
```

## ✅ Verificação Final

Após seguir todos os passos, seu repositório deve estar disponível em:
`https://github.com/SEU_USUARIO/modelo_projeto_conteudo`

## 🆘 Problemas Comuns

### Git não reconhecido após instalação
- **Solução**: Reinicie o terminal/PowerShell
- **Alternativa**: Reinicie o computador

### Erro de autenticação
- **Solução**: Use Personal Access Token em vez de senha
- **Verificar**: Configuração de usuário e email

### Erro de push
- **Solução**: Verificar se o repositório foi criado no GitHub
- **Verificar**: URL do repositório remoto

## 📞 Suporte

Se encontrar problemas:
1. Verifique se o Git foi instalado corretamente
2. Confirme a configuração de usuário e email
3. Teste a conectividade com o GitHub
4. Consulte a documentação oficial do Git

---

**Próximo passo**: Após instalar o Git, execute os comandos acima para enviar o projeto para o GitHub! 🚀
