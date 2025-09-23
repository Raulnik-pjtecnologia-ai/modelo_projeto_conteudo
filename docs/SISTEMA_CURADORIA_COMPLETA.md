# 🔍 Sistema de Curadoria Completa de Conteúdo

## 🎯 Visão Geral

O Sistema de Curadoria Completa é uma solução automatizada que utiliza MCPs (Model Context Protocols) disponíveis para verificar e garantir a qualidade de todo conteúdo produzido. O sistema verifica capas, dados, vídeos, fontes e busca automaticamente fontes confiáveis.

## 🚀 Funcionalidades Principais

### ✅ Verificação de Capas
- **Presença obrigatória**: Verifica se todo conteúdo possui capa
- **Formatos aceitos**: .jpg, .jpeg, .png, .gif, .webp
- **Qualidade mínima**: 800x600 pixels
- **Descrição obrigatória**: Texto descritivo da imagem
- **Caminho válido**: Verifica se o arquivo existe

### 📊 Análise de Dados e Gráficos
- **Quantidade mínima**: 2 gráficos ou 1 tabela
- **Fontes obrigatórias**: Todas as fontes devem ser documentadas
- **Qualidade visual**: Gráficos claros e legíveis
- **Relevância**: Dados relacionados ao conteúdo

### 🎥 Verificação de Vídeos
- **Quantidade mínima**: 2 vídeos relacionados
- **Thumbnails obrigatórios**: Imagens de pré-visualização
- **Links funcionais**: URLs do YouTube funcionando
- **Descrições completas**: Informações sobre cada vídeo

### 📚 Análise de Fontes e Referências
- **Quantidade mínima**: 4 fontes diferentes
- **Credibilidade**: Fontes confiáveis e reconhecidas
- **Acessibilidade**: URLs funcionais e válidas
- **Atualidade**: Referências recentes (máximo 2 anos)
- **Diversidade**: Variedade de tipos de fontes

### 🔍 Busca de Fontes Confiáveis
- **Integração com MCPs**: Busca automática de fontes relevantes
- **Categorização automática**: Governamentais, acadêmicas, internacionais
- **Avaliação de relevância**: Pontuação baseada em critérios
- **Sugestões de conteúdo**: Gráficos, vídeos e exemplos sugeridos

## 📁 Estrutura do Sistema

```
scripts/
├── curadoria_automatica.py          # Curadoria básica
├── verificar_fontes_mcp.py          # Verificação de fontes
├── buscar_fontes_confiaveis.py      # Busca de fontes
├── curadoria_completa.py            # Sistema integrado
├── executar_curadoria.ps1           # Script PowerShell básico
└── executar_curadoria_completa.ps1  # Script PowerShell completo

templates/
└── template_curadoria_conteudo.md   # Template de curadoria

config/
└── curadoria_config.json            # Configurações do sistema

docs/
└── relatorios/                      # Relatórios gerados
```

## 🛠️ Como Usar

### 1. Execução Básica

```powershell
# Executar curadoria básica
.\scripts\executar_curadoria.ps1

# Executar curadoria completa
.\scripts\executar_curadoria_completa.ps1
```

### 2. Execução com Parâmetros

```powershell
# Analisar diretório específico
.\scripts\executar_curadoria_completa.ps1 -Diretorio "2_conteudo\04_publicado"

# Definir pontuação mínima
.\scripts\executar_curadoria_completa.ps1 -MinPontuacao 80

# Ver ajuda
.\scripts\executar_curadoria_completa.ps1 -Ajuda
```

### 3. Execução Python Direta

```bash
# Curadoria básica
python scripts/curadoria_automatica.py --diretorio "2_conteudo"

# Verificação de fontes
python scripts/verificar_fontes_mcp.py --arquivo "conteudo.md"

# Busca de fontes
python scripts/buscar_fontes_confiaveis.py --tema "gestão escolar"

# Curadoria completa
python scripts/curadoria_completa.py --diretorio "2_conteudo"
```

## ⚙️ Configuração

### Arquivo de Configuração

Edite `config/curadoria_config.json` para personalizar:

```json
{
  "curadoria": {
    "pontuacao_minima": 70,
    "min_graficos": 2,
    "min_videos": 2,
    "min_fontes": 4
  },
  "capa": {
    "formatos_aceitos": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "tamanho_minimo": 800,
    "altura_minima": 600,
    "obrigatoria": true
  }
}
```

### Fontes Confiáveis

Adicione novas fontes em `config/curadoria_config.json`:

```json
{
  "fontes_confiaveis": {
    "governamentais": [
      "gov.br",
      "mec.gov.br",
      "inep.gov.br"
    ],
    "academicas": [
      "scielo.br",
      "scholar.google.com"
    ]
  }
}
```

## 📊 Relatórios Gerados

### 1. Relatório de Curadoria Básica
- **Arquivo**: `relatorio_curadoria_YYYYMMDD_HHMMSS.json`
- **Conteúdo**: Análise individual de cada arquivo
- **Métricas**: Pontuação, status, problemas identificados

### 2. Relatório de Fontes
- **Arquivo**: `relatorio_fontes_YYYYMMDD_HHMMSS.json`
- **Conteúdo**: Análise detalhada de fontes e referências
- **Métricas**: Credibilidade, acessibilidade, atualidade

### 3. Relatório de Busca de Fontes
- **Arquivo**: `busca_fontes_tema_YYYYMMDD_HHMMSS.json`
- **Conteúdo**: Fontes encontradas e sugestões
- **Métricas**: Relevância, categorização, recomendações

### 4. Relatório Consolidado
- **Arquivo**: `curadoria_completa_YYYYMMDD_HHMMSS.json`
- **Conteúdo**: Análise completa com todas as verificações
- **Métricas**: Estatísticas gerais, recomendações consolidadas

## 🎯 Critérios de Avaliação

### Pontuação por Categoria (0-10 cada)
- **Capa e Visual**: Presença, qualidade, descrição
- **Dados e Gráficos**: Quantidade, fontes, relevância
- **Vídeos**: Quantidade, thumbnails, descrições
- **Fontes e Referências**: Quantidade, credibilidade, atualidade
- **Qualidade do Conteúdo**: Estrutura, linguagem, exemplos
- **Estrutura**: Organização, completude
- **SEO e Acessibilidade**: Otimização, navegação

### Classificação Final
- **Excelente**: 85-100%
- **Boa**: 70-84%
- **Regular**: 55-69%
- **Ruim**: 40-54%
- **Péssima**: 0-39%

## 🚨 Problemas Comuns e Soluções

### Problema: Capa não encontrada
**Solução**: 
1. Adicionar imagem de capa no conteúdo
2. Incluir descrição da imagem
3. Verificar se o arquivo existe no caminho especificado

### Problema: Fontes insuficientes
**Solução**:
1. Adicionar mais fontes confiáveis
2. Usar fontes governamentais ou acadêmicas
3. Verificar se as URLs estão funcionando

### Problema: Vídeos ausentes
**Solução**:
1. Adicionar vídeos relacionados ao tema
2. Incluir thumbnails e descrições
3. Verificar se os links do YouTube funcionam

### Problema: Dados insuficientes
**Solução**:
1. Adicionar gráficos ou tabelas relevantes
2. Incluir fontes para todos os dados
3. Usar dados atualizados e confiáveis

## 📈 Melhorias Contínuas

### 1. Integração com MCPs
- **Busca de notícias**: Integração com MCP de notícias
- **Busca do YouTube**: Integração com MCP do YouTube
- **Busca geral**: Integração com MCP de busca

### 2. Verificações Adicionais
- **Plágio**: Verificação de conteúdo duplicado
- **SEO**: Análise de otimização para busca
- **Acessibilidade**: Verificação de padrões WCAG

### 3. Automação Avançada
- **Correção automática**: Aplicar correções sugeridas
- **Geração de conteúdo**: Criar seções ausentes
- **Notificações**: Alertas para problemas críticos

## 🔧 Desenvolvimento

### Adicionar Nova Verificação

1. Criar função de verificação
2. Adicionar ao `CuradorAutomatico`
3. Incluir na pontuação
4. Atualizar relatórios

### Adicionar Nova Fonte Confiável

1. Editar `config/curadoria_config.json`
2. Adicionar domínio na categoria apropriada
3. Testar com conteúdo real

### Personalizar Critérios

1. Editar `config/curadoria_config.json`
2. Ajustar pontuações em `curadoria_automatica.py`
3. Testar com diferentes conteúdos

## 📞 Suporte

Para dúvidas sobre o sistema de curadoria:

1. Consulte este documento
2. Verifique os logs em `curadoria.log`
3. Execute com `-Ajuda` para ver opções
4. Entre em contato com a equipe de desenvolvimento

---

**Versão**: 1.0.0  
**Última atualização**: Dezembro 2024  
**Status**: Em uso ativo
