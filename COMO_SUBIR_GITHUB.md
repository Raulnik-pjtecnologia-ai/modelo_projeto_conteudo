# 🚀 Como Subir para GitHub - Instruções Rápidas

## ⚡ Método 1: Script Automático (Recomendado)

### 1. Instalar Git
- Baixe em: https://git-scm.com/download/win
- Instale com configurações padrão
- Reinicie o terminal

### 2. Executar Script
```powershell
# No PowerShell, no diretório do projeto
.\setup-github.ps1
```

O script vai:
- ✅ Verificar se Git está instalado
- ⚙️ Configurar Git (nome e email)
- 📁 Inicializar repositório
- 📦 Adicionar arquivos
- 💾 Fazer commit
- 🔗 Configurar repositório remoto
- 🚀 Enviar para GitHub

## ⚡ Método 2: Manual

### 1. Instalar Git
- Baixe em: https://git-scm.com/download/win
- Instale com configurações padrão

### 2. Configurar Git
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

### 3. Inicializar Repositório
```bash
cd "C:\Users\GasTed\Desktop\modelo_projeto_conteudo"
git init
git add .
git commit -m "Estrutura inicial do projeto - v1.0.0"
```

### 4. Criar Repositório no GitHub
1. Acesse: https://github.com/new
2. Nome: `modelo_projeto_conteudo`
3. Descrição: `Modelo profissional para gestão de conteúdo editorial educacional`
4. Público ✅
5. **NÃO** marque "Initialize with README"
6. Clique "Create repository"

### 5. Conectar e Enviar
```bash
git remote add origin https://github.com/SEU_USUARIO/modelo_projeto_conteudo.git
git branch -M main
git push -u origin main
```

## 🔐 Autenticação

### Personal Access Token (Recomendado)
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Selecionar: `repo`, `workflow`
4. Copiar token
5. Usar token como senha ao fazer push

## ✅ Verificação

Após o envio, seu repositório estará em:
`https://github.com/SEU_USUARIO/modelo_projeto_conteudo`

## 🆘 Problemas?

- **Git não encontrado**: Reinicie o terminal após instalação
- **Erro de autenticação**: Use Personal Access Token
- **Erro de push**: Verifique se o repositório foi criado no GitHub

## 📚 Documentação Completa

- `INSTALACAO_GIT.md` - Instalação detalhada do Git
- `SETUP_GITHUB.md` - Configuração completa do GitHub

---

**🎯 Recomendação**: Use o **Método 1** (script automático) para maior facilidade!
