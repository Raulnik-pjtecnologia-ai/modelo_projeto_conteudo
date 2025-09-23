# 📝 Instruções para Templates Atualizados

## 🎯 Visão Geral

Os templates foram atualizados para incluir seções obrigatórias de **capa**, **dados e gráficos**, **vídeos relacionados** e **fontes detalhadas**. Esta atualização garante que todo conteúdo produzido tenha elementos visuais, dados confiáveis e referências adequadas.

## 🆕 Novas Seções Obrigatórias

### 1. 🖼️ Capa
- **Obrigatória**: Sim
- **Localização**: Logo após o título
- **Conteúdo**: Imagem de capa + descrição
- **Formato**: `![Capa do Conteúdo](caminho/para/capa.jpg)`

### 2. 📊 Dados e Gráficos
- **Obrigatória**: Sim (quando aplicável)
- **Localização**: Após o contexto, antes do conteúdo principal
- **Conteúdo**: Gráficos, tabelas e dados com fontes
- **Mínimo**: 2 gráficos ou 1 tabela

### 3. 🎥 Vídeos Relacionados
- **Obrigatória**: Sim
- **Localização**: Antes das referências
- **Conteúdo**: Vídeos relevantes com thumbnails
- **Mínimo**: 2 vídeos

### 4. 📚 Recursos e Fontes
- **Obrigatória**: Sim
- **Localização**: Antes da taxonomia
- **Conteúdo**: Fontes detalhadas, legislação, referências bibliográficas
- **Mínimo**: 4 fontes diferentes

## 📋 Templates Disponíveis

### 1. Artigo Padronizado
- **Arquivo**: `template_artigo_padronizado.md`
- **Uso**: Artigos educacionais e informativos
- **Seções**: Capa, dados, vídeos, fontes completas

### 2. Checklist Padronizado
- **Arquivo**: `template_checklist_padronizado.md`
- **Uso**: Listas de verificação e processos
- **Seções**: Capa, dados, vídeos, fontes completas

### 3. Lição Padronizada
- **Arquivo**: `template_licao_padronizado.md`
- **Uso**: Lições educacionais e aulas
- **Seções**: Capa, dados, vídeos, fontes completas

### 4. Vídeo Padronizado
- **Arquivo**: `template_video_padronizado.md`
- **Uso**: Conteúdo de vídeo e mídia
- **Seções**: Capa, dados, vídeos, fontes completas

### 5. Documento Oficial Padronizado
- **Arquivo**: `template_documento_oficial_padronizado.md`
- **Uso**: Documentos oficiais e normativos
- **Seções**: Capa, dados, vídeos, fontes completas

### 6. Apresentação Padronizada
- **Arquivo**: `template_apresentacao_padronizado.md`
- **Uso**: Apresentações e slides
- **Seções**: Capa, dados, vídeos, fontes completas

## 🛠️ Como Usar os Novos Templates

### Passo 1: Seleção do Template
1. Escolha o template apropriado para seu tipo de conteúdo
2. Copie o conteúdo do template para seu arquivo de trabalho
3. Renomeie o arquivo seguindo o padrão: `[tipo]_[titulo].md`

### Passo 2: Preenchimento das Seções Obrigatórias

#### 🖼️ Capa
```markdown
## 🖼️ Capa

![Capa do Conteúdo](caminho/para/capa.jpg)
*Descrição da imagem de capa: [Breve descrição do que a imagem representa]*
```

**Dicas:**
- Use imagens de alta qualidade (mínimo 800x600px)
- Descreva claramente o que a imagem representa
- Mantenha o arquivo de imagem na pasta `assets/` do projeto

#### 📊 Dados e Gráficos
```markdown
## 📊 Dados e Gráficos

### Gráfico 1: [Título do Gráfico]
![Gráfico 1](caminho/para/grafico1.png)
*Fonte: [Fonte dos dados do gráfico]*

### Tabela de Dados: [Título da Tabela]
| Coluna 1 | Coluna 2 | Coluna 3 |
|----------|----------|----------|
| Dado 1   | Dado 2   | Dado 3   |

*Fonte: [Fonte dos dados da tabela]*
```

**Dicas:**
- Sempre inclua a fonte dos dados
- Use gráficos claros e legíveis
- Mantenha tabelas organizadas e bem formatadas

#### 🎥 Vídeos Relacionados
```markdown
## 🎥 Vídeos Relacionados

### Vídeo 1: [Título do Vídeo]
[![Vídeo 1](caminho/para/thumbnail_video1.jpg)](https://youtube.com/watch?v=VIDEO_ID)
*Descrição: [Breve descrição do conteúdo do vídeo]*
*Duração: [X minutos]*
*Canal: [Nome do canal]*
```

**Dicas:**
- Use thumbnails de alta qualidade
- Inclua duração e canal do vídeo
- Escolha vídeos relevantes e de qualidade

#### 📚 Recursos e Fontes
```markdown
## 📚 Recursos e Fontes

### **Legislação Aplicável**
- [Lei/Decreto 1]: [Descrição] - [URL ou referência completa]

### **Fontes dos Dados e Estatísticas**
- **[Fonte 1]**: [Nome da instituição] - [URL ou referência completa]

### **Referências Bibliográficas**
- [Autor 1] (Ano). [Título do trabalho]. [Editora/Publicação]. [URL se disponível]

### **Links Úteis e Recursos Online**
- [Link útil 1]: [Descrição] - [URL]
```

**Dicas:**
- Sempre inclua URLs quando disponíveis
- Use formato padrão para referências bibliográficas
- Organize as fontes por categoria

### Passo 3: Preenchimento do Conteúdo Principal
1. Substitua todos os placeholders `[texto entre colchetes]`
2. Preencha as seções específicas do seu conteúdo
3. Mantenha a estrutura e formatação do template

### Passo 4: Revisão e Validação
1. Verifique se todas as seções obrigatórias estão preenchidas
2. Confirme se as fontes estão corretas e acessíveis
3. Teste os links dos vídeos
4. Valide a qualidade das imagens

## 📁 Estrutura de Arquivos Recomendada

```
projeto/
├── assets/
│   ├── capas/
│   │   ├── capa_artigo_1.jpg
│   │   ├── capa_checklist_1.jpg
│   │   └── capa_licao_1.jpg
│   ├── graficos/
│   │   ├── grafico_1.png
│   │   ├── grafico_2.png
│   │   └── tabela_1.png
│   └── thumbnails/
│       ├── video_1.jpg
│       ├── video_2.jpg
│       └── video_3.jpg
├── conteudo/
│   ├── artigo_gestao_financeira.md
│   ├── checklist_auditoria.md
│   └── licao_planejamento.md
└── templates/
    ├── template_artigo_padronizado.md
    ├── template_checklist_padronizado.md
    └── template_licao_padronizado.md
```

## ✅ Checklist de Validação

### Antes de Publicar
- [ ] Capa incluída e descrita
- [ ] Mínimo 2 gráficos ou 1 tabela com fontes
- [ ] Mínimo 2 vídeos relacionados
- [ ] Mínimo 4 fontes diferentes
- [ ] Todas as URLs funcionando
- [ ] Imagens de alta qualidade
- [ ] Formatação consistente
- [ ] Placeholders removidos

### Qualidade do Conteúdo
- [ ] Título claro e descritivo
- [ ] Resumo executivo completo
- [ ] Contexto bem explicado
- [ ] Aplicação prática detalhada
- [ ] Exemplos relevantes
- [ ] Referências atualizadas

## 🚨 Problemas Comuns e Soluções

### Problema: Imagem não carrega
**Solução**: Verifique o caminho da imagem e se o arquivo existe

### Problema: Vídeo não abre
**Solução**: Confirme se o ID do YouTube está correto

### Problema: Fonte não encontrada
**Solução**: Verifique se a URL está funcionando e atualizada

### Problema: Gráfico ilegível
**Solução**: Use imagens de alta resolução e formatação clara

## 📞 Suporte

Para dúvidas sobre os templates atualizados:
1. Consulte este documento primeiro
2. Verifique os exemplos nos templates
3. Entre em contato com a equipe de desenvolvimento

---

**Versão**: 2.0.0  
**Última atualização**: Dezembro 2024  
**Status**: Em uso ativo
