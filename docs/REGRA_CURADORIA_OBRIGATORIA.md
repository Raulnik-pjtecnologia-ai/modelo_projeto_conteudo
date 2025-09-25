# 🚀 REGRA DE CUradoria OBRIGATÓRIA

## 📋 **REGRA FUNDAMENTAL**

**TODA VEZ QUE UM CONTEÚDO NÃO PASSAR NA CUradoria COM NOTA MÍNIMA DE 80%, DEVE SER AJUSTADO IMEDIATAMENTE ANTES DE PROSSEGUIR COM AS PRÓXIMAS ETAPAS DO PROJETO.**

---

## 🎯 **CRITÉRIOS DE APROVAÇÃO**

### **Pontuação Mínima Obrigatória:**
- **Pontuação Boilerplate**: ≥ 80%
- **Pontuação MCP**: ≥ 70%
- **Pontuação Geral**: ≥ 80%

### **Status de Aprovação:**
- ✅ **APROVADO**: Todas as pontuações atingem os critérios mínimos
- ❌ **REPROVADO**: Qualquer pontuação abaixo dos critérios mínimos

---

## 🔄 **PROCESSO DE CORREÇÃO OBRIGATÓRIO**

### **QUANDO CONTEÚDO É REPROVADO:**

1. **🔍 IDENTIFICAR PROBLEMAS**
   - Analisar detalhes da curadoria
   - Listar todos os itens reprovados
   - Priorizar correções por impacto

2. **🔧 CORRIGIR CONTEÚDO**
   - Ajustar elementos do boilerplate faltantes
   - Adicionar enriquecimento MCP necessário
   - Verificar formato de tags e categorias
   - Melhorar qualidade do conteúdo

3. **✅ RE-EXECUTAR CUradoria**
   - Executar curadoria novamente
   - Verificar se critérios foram atingidos
   - **NÃO PROSSEGUIR** se ainda reprovado

4. **🔄 ITERAR ATÉ APROVAÇÃO**
   - Repetir processo até aprovação
   - Máximo de 3 tentativas por conteúdo
   - Documentar todas as correções realizadas

---

## ⚠️ **REGRAS IMPORTANTES**

1. **NUNCA** pular etapas com conteúdo reprovado
2. **SEMPRE** corrigir antes de prosseguir
3. **SEMPRE** documentar correções realizadas
4. **SEMPRE** re-executar curadoria após correções
5. **NUNCA** publicar conteúdo não aprovado

---

## 📊 **EXEMPLOS DE CORREÇÕES**

### **Problema 1**: Tags no formato incorreto
```
❌ ANTES: **Tags**: #GestãoEscolar #Estratégia
✅ DEPOIS: **Tags**: GestãoEscolar, Estratégia
```

### **Problema 2**: Falta de dados estatísticos
```
❌ ANTES: Sem dados específicos
✅ DEPOIS: 47,1 milhões de alunos, 179,3 mil escolas
```

### **Problema 3**: Ausência de vídeos
```
❌ ANTES: Sem seção de vídeos
✅ DEPOIS: 5 vídeos relevantes do YouTube incluídos
```

### **Problema 4**: Fontes insuficientes
```
❌ ANTES: Apenas 1-2 fontes
✅ DEPOIS: 5+ fontes oficiais e confiáveis
```

---

## 🔧 **SCRIPT DE CORREÇÃO AUTOMÁTICA**

```python
def corrigir_conteudo_apos_curadoria(arquivo, problemas):
    """Corrige automaticamente problemas identificados na curadoria."""
    
    # Corrigir formato de tags
    if "tem_tags" in problemas and not problemas["tem_tags"]:
        corrigir_formato_tags(arquivo)
    
    # Adicionar dados estatísticos
    if "tem_dados" in problemas and not problemas["tem_dados"]:
        adicionar_dados_estatisticos(arquivo)
    
    # Incluir vídeos do YouTube
    if "tem_videos" in problemas and not problemas["tem_videos"]:
        adicionar_videos_youtube(arquivo)
    
    # Buscar fontes confiáveis
    if "tem_fontes" in problemas and not problemas["tem_fontes"]:
        buscar_fontes_confiaveis(arquivo)
```

---

## 📋 **CHECKLIST DE CORREÇÃO**

Para cada conteúdo reprovado, verificar:

- [ ] **Formato de tags** corrigido
- [ ] **Categoria** no formato correto
- [ ] **Dados estatísticos** incluídos
- [ ] **Vídeos do YouTube** adicionados
- [ ] **Notícias atuais** pesquisadas
- [ ] **Fontes oficiais** verificadas
- [ ] **Estrutura visual** melhorada
- [ ] **Qualidade do conteúdo** aprimorada

---

## 🚀 **IMPLEMENTAÇÃO**

Esta regra deve ser aplicada em:
- ✅ Artigos
- ✅ Checklists
- ✅ Lições
- ✅ Documentos oficiais
- ✅ Apresentações
- ✅ Qualquer conteúdo gerado

---

## 📝 **EXEMPLO DE APLICAÇÃO**

### **Cenário**: Conteúdo reprovado na curadoria

```
🔍 CUradoria executada:
   📊 Pontuação Boilerplate: 60%
   📊 Pontuação MCP: 70%
   📊 Pontuação Geral: 65%
   ❌ Status: REPROVADO

🔧 CORREÇÕES REALIZADAS:
   ✅ Tags: Formato corrigido
   ✅ Dados: Estatísticas adicionadas
   ✅ Vídeos: 5 vídeos incluídos
   ✅ Fontes: 8 fontes verificadas

🔍 CUradoria re-executada:
   📊 Pontuação Boilerplate: 90%
   📊 Pontuação MCP: 85%
   📊 Pontuação Geral: 87.5%
   ✅ Status: APROVADO

🚀 PRÓXIMAS ETAPAS:
   ✅ Prosseguir com pipeline editorial
   ✅ Sincronizar com Notion
   ✅ Finalizar projeto
```

---

**Data de Criação**: 25/09/2025
**Status**: ATIVA
**Aplicação**: OBRIGATÓRIA PARA TODOS OS CONTEÚDOS
**Relacionada**: REGRA_ENRIQUECIMENTO_MCP.md, REGRA_BOILERPLATE_GESTAO.md
