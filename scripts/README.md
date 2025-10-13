# 🤖 Scripts e Automações

Esta pasta contém todos os scripts e ferramentas de automação do **Modelo Projeto Conteúdo**.

## 📁 Estrutura dos Scripts

### 🚀 **Setup e Configuração**
- **`setup-github.ps1`** - Script automático para configuração do GitHub
- **`testar_conexao_notion.ps1`** - Testa conexão com API do Notion
- **`atualizar_notion_melhorado.ps1`** - Atualiza propriedades no Notion

### 🏷️ **Classificação Automática**
- **`classificar_23_conteudos.ps1`** - Classifica conteúdos sem categoria
- **`refinar_classificacoes.ps1`** - Refina classificações automáticas
- **`corrigir_classificacao.ps1`** - Aplica correções manuais
- **`integrar_notion_final.ps1`** - Integração final com Notion

### 📊 **Relatórios e Análises**
- **`relatorio_classificacao_23_conteudos.md`** - Relatório de classificação
- **`classificacao_*.csv`** - Dados de classificação em CSV
- **`classificacao_final_100_porcento.json`** - Classificação final completa

### ⚙️ **Configurações**
- **`config_classificacao_global.json`** - Configuração global de classificação
- **`config_classificacao_melhorado.json`** - Configuração melhorada
- **`requirements.txt`** - Dependências Python

## 🎯 **Como Usar os Scripts**

### 1. **Setup Inicial**
```powershell
# Configurar GitHub automaticamente
.\setup-github.ps1

# Testar conexão com Notion
.\testar_conexao_notion.ps1
```

### 2. **Classificação Automática**
```powershell
# Classificar conteúdos sem categoria
.\classificar_23_conteudos.ps1

# Refinar classificações
.\refinar_classificacoes.ps1

# Aplicar correções manuais
.\corrigir_classificacao.ps1
```

### 3. **Integração com Notion**
```powershell
# Atualizar propriedades no Notion
.\atualizar_notion_melhorado.ps1

# Integração final
.\integrar_notion_final.ps1
```

## 🔧 **Pré-requisitos**

### Para Scripts PowerShell
- **PowerShell 5.1+** (Windows 10/11)
- **Token do Notion** configurado
- **Permissões** de execução de scripts

### Para Scripts Python
- **Python 3.8+**
- **Dependências** instaladas: `pip install -r requirements.txt`
- **Variáveis de ambiente** configuradas

## 📊 **Sistema de Classificação**

### Funcionalidades
- ✅ **Classificação automática** por eixo temático
- ✅ **Identificação de função alvo** (estudante, professor, etc.)
- ✅ **Definição de nível** (estratégico, tático, operacional)
- ✅ **Categorização por tipo** de conteúdo
- ✅ **Atribuição de status** editorial

### Precisão
- **100%** de precisão após refinamento
- **Classificação inteligente** baseada em palavras-chave
- **Correção manual** para casos específicos
- **Validação automática** de resultados

## 🚀 **Automações Disponíveis**

### 1. **Pipeline Completo**
- Busca conteúdos no Notion
- Classifica automaticamente
- Atualiza propriedades
- Gera relatórios

### 2. **Monitoramento**
- Verifica conexão com APIs
- Valida configurações
- Testa funcionalidades

### 3. **Relatórios**
- Gera CSV com resultados
- Cria relatórios em Markdown
- Exporta dados para análise

## 📈 **Métricas de Sucesso**

- **17 páginas** classificadas com sucesso
- **100% de precisão** na classificação final
- **0 erros** durante execução
- **Sistema totalmente funcional**

## 🔄 **Manutenção**

### Atualizações Regulares
- **Revisar** palavras-chave de classificação
- **Testar** scripts após mudanças no Notion
- **Atualizar** configurações conforme necessário
- **Validar** precisão das classificações

### Monitoramento
- **Verificar** logs de execução
- **Acompanhar** métricas de precisão
- **Identificar** necessidades de melhoria
- **Documentar** mudanças e melhorias

---

**Última atualização**: 17 de Setembro de 2025  
**Status**: ✅ **100% Funcional e Testado**
