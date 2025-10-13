# 🔑 CONFIGURAÇÃO DO TOKEN NOTION

## ⚠️ **PROBLEMA IDENTIFICADO:**
A página de Matemática ENEM 2024 tem problemas que precisam ser corrigidos via API do Notion, mas o token não está configurado.

## 🚨 **PROBLEMAS CONFIRMADOS:**
1. **Vídeos quebrados** - "Vídeo indisponível" / "Este vídeo não está disponível"
2. **Títulos sem conteúdo** - "Resumo Executivo", "Contexto", "Aplicação Prática"
3. **URLs falsas** - Links de exemplo/placeholder

## 🔧 **COMO CONFIGURAR O TOKEN:**

### **Passo 1: Obter Token do Notion**
1. Acesse: https://www.notion.so/my-integrations
2. Clique em "New integration"
3. Nome: "Editorial Corrector"
4. Workspace: Selecione seu workspace
5. Clique em "Submit"
6. Copie o "Internal Integration Token"

### **Passo 2: Configurar Token Local**
1. Abra o arquivo `.env` na pasta do projeto
2. Substitua `seu_token_aqui` pelo token real:
```
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### **Passo 3: Dar Permissões à Integração**
1. Vá para a página problemática no Notion
2. Clique em "Share" (compartilhar)
3. Clique em "Add people, emails, groups, or integrations"
4. Procure por "Editorial Corrector"
5. Adicione com permissão "Can edit"
6. Clique em "Invite"

## 🎯 **APÓS CONFIGURAR:**
Execute o comando para corrigir a página:
```bash
python scripts/corrigir_pagina_matematica_especifica.py
```

## 📋 **CORREÇÕES QUE SERÃO APLICADAS:**
- ✅ Deletar vídeos quebrados
- ✅ Adicionar vídeos reais do YouTube
- ✅ Adicionar conteúdo aos títulos vazios
- ✅ Substituir URLs falsas por reais

## ⏱️ **TEMPO ESTIMADO:**
- Configuração: 5 minutos
- Correção: 10-15 minutos
- **Total: 15-20 minutos**

---

## 🔗 **LINK DA PÁGINA PROBLEMÁTICA:**
https://www.notion.so/An-lise-ENEM-2024-Tend-ncias-em-Matem-tica-Guia-Completo-ENEM-20-26a5113a91a3810bb647e10963c83524

---

**Após configurar o token, me avise para executar a correção!** 🚀
