# ⚙️ Configurações do Projeto

Esta pasta contém todos os arquivos de configuração do **Modelo Projeto Conteúdo**.

## 📁 Arquivos de Configuração

### 🔧 **Configurações Principais**
- **`config.json`** - Configuração principal do projeto
- **`env.example`** - Modelo de variáveis de ambiente

## 🎯 **Como Configurar**

### 1. **Configuração Básica**
1. Copie `env.example` para `.env`
2. Edite as variáveis conforme sua necessidade
3. Configure o token do Notion
4. Ajuste as URLs dos bancos de dados

### 2. **Personalização**
1. Edite `config.json` para suas necessidades
2. Ajuste as categorias de classificação
3. Configure as integrações desejadas
4. Personalize as tags e funções

## 📊 **Estrutura de Configuração**

### **Notion Integration**
```json
{
  "notion": {
    "token": "seu_token_aqui",
    "biblioteca_url": "https://www.notion.so/...",
    "categoria_url": "https://www.notion.so/...",
    "modulos_url": "https://www.notion.so/...",
    "cursos_url": "https://www.notion.so/...",
    "views_url": "https://www.notion.so/..."
  }
}
```

### **Classificação**
```json
{
  "classificacao": {
    "funcoes": ["Mantenedor", "Secretário", "Diretor", "Coordenador"],
    "niveis": ["Estratégico", "Tático", "Operacional"],
    "areas_problema": ["Financeiro", "Pedagógico", "Jurídico", "Operacional"],
    "tipos_conteudo": ["Artigo", "Checklist", "Lição", "Template"],
    "tags": ["Gestão", "Educação", "Conteúdo", "Automação"]
  }
}
```

### **Integrações**
```json
{
  "integracao": {
    "wordpress": {
      "url": "https://seusite.com",
      "usuario": "admin",
      "senha": "sua_senha",
      "habilitado": false
    },
    "discord": {
      "webhook": "https://discord.com/api/webhooks/...",
      "habilitado": false
    }
  }
}
```

## 🔐 **Segurança**

### **Variáveis Sensíveis**
- **NUNCA** commite arquivos `.env` com dados reais
- **Use** `env.example` como modelo
- **Mantenha** tokens e senhas seguros
- **Revise** permissões de acesso

### **Boas Práticas**
- ✅ Use variáveis de ambiente para dados sensíveis
- ✅ Mantenha configurações de exemplo
- ✅ Documente mudanças importantes
- ✅ Teste configurações antes de usar

## 🚀 **Configurações Recomendadas**

### **Para Desenvolvimento**
```json
{
  "configuracoes": {
    "backup_enabled": true,
    "notification_enabled": true,
    "auto_publish": false,
    "log_level": "DEBUG"
  }
}
```

### **Para Produção**
```json
{
  "configuracoes": {
    "backup_enabled": true,
    "notification_enabled": true,
    "auto_publish": true,
    "log_level": "INFO"
  }
}
```

## 📋 **Checklist de Configuração**

### **Configuração Inicial**
- [ ] Copiar `env.example` para `.env`
- [ ] Configurar token do Notion
- [ ] Ajustar URLs dos bancos de dados
- [ ] Personalizar categorias de classificação
- [ ] Configurar integrações desejadas

### **Validação**
- [ ] Testar conexão com Notion
- [ ] Validar configurações de classificação
- [ ] Verificar integrações
- [ ] Executar scripts de teste

### **Produção**
- [ ] Revisar configurações de segurança
- [ ] Configurar backups automáticos
- [ ] Ativar notificações
- [ ] Monitorar logs

## 🔄 **Manutenção**

### **Atualizações Regulares**
- **Revisar** configurações mensalmente
- **Atualizar** tokens quando necessário
- **Ajustar** categorias conforme evolução
- **Testar** integrações periodicamente

### **Backup**
- **Faça backup** das configurações
- **Versionize** mudanças importantes
- **Documente** alterações significativas
- **Mantenha** histórico de configurações

---

**Última atualização**: 17 de Setembro de 2025  
**Versão**: 2.0.0
