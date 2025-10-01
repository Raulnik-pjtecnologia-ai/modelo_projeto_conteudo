# 📁 Estrutura do Projeto - Modelo Projeto Conteúdo

**Última atualização:** 30/09/2025  
**Status:** ✅ Organizado e Limpo

---

## 🎯 VISÃO GERAL

Projeto organizado para criação, curadoria e sincronização de conteúdos educacionais com Notion.

---

## 📂 ESTRUTURA DE DIRETÓRIOS

```
modelo_projeto_conteudo/
│
├── 📄 README.md                                    # Documentação principal
├── 📄 requirements.txt                             # Dependências Python
├── 📄 .gitignore                                  # Arquivos ignorados pelo Git
│
├── 📊 DIAGNOSTICO_MCP.md                          # Status das MCPs (Charts, Search, etc.)
├── 📊 RELATORIO_FINAL_4_CONTEUDOS_PRE_ENEM.md    # Relatório completo dos 4 conteúdos
├── 📊 RELATORIO_FINALIZACAO_PRE_ENEM.md          # Relatório de finalização
├── 📊 ESTRUTURA_PROJETO.md                        # Este arquivo
│
├── 📋 sincronizacao_pre_enem.json                 # Dados de sincronização ativa (PRÉ-ENEM)
├── 📋 analise_editorial_pre_enem.json            # Análise da biblioteca PRÉ-ENEM
│
├── 📁 2_conteudo/                                 # 🔥 CONTEÚDOS ORGANIZADOS
│   ├── 01_ideias_e_rascunhos/                   # Novos conteúdos e rascunhos
│   │   ├── artigo_simulados_enem_2025_estrategico.md ⭐
│   │   ├── artigo_ansiedade_enem_2025_gestao_emocional.md ⭐
│   │   ├── artigo_dia_prova_enem_2025_checklist.md ⭐
│   │   ├── artigo_tecnicas_memorizacao_enem_2025.md ⭐
│   │   ├── relatorio_pesquisa_pre_enem_2025.md
│   │   ├── gestao_escolar/                       # Rascunhos Gestão Escolar
│   │   └── pre_enem/                             # Rascunhos PRÉ-ENEM
│   │
│   ├── 02_em_revisao/                            # Em processo de revisão
│   ├── 03_pronto_para_publicar/                  # Aprovado, aguardando publicação
│   └── 04_publicado/                             # Conteúdos já publicados
│       ├── gestao_escolar/                       # 196 artigos publicados
│       └── pre_enem/                             # 4 artigos PRÉ-ENEM novos
│
├── 📁 scripts/                                    # 🔧 SCRIPTS ESSENCIAIS
│   ├── curadoria_automatica.py                   # Curadoria com boilerplate
│   ├── curadoria_completa.py                     # Curadoria completa + MCPs
│   ├── curadoria_e_sincronizacao_pre_enem_temp.py # ⭐ Ativo para PRÉ-ENEM
│   ├── sincronizar_notion.py                     # Sincronização com Notion
│   ├── buscar_fontes_confiaveis.py              # Busca de fontes MCP
│   ├── verificar_configuracao.py                 # Verificação de setup
│   ├── verificar_fontes_mcp.py                   # Verificação de MCPs
│   ├── setup_projeto.py                          # Setup inicial
│   └── README.md                                 # Documentação dos scripts
│
├── 📁 assets/                                     # 🎨 RECURSOS VISUAIS
│   └── images/                                   # Imagens para conteúdos
│       └── graficos/                             # Gráficos gerados
│
├── 📁 backup_imagens/                            # 💾 Backup de imagens
│
├── 📁 docs/                                       # 📚 DOCUMENTAÇÃO
│   ├── REGRA_ENRIQUECIMENTO_MCP.md              # Regra de uso de MCPs
│   ├── REGRA_BOILERPLATE_GESTAO.md              # Regra de boilerplate
│   ├── REGRA_CURADORIA_OBRIGATORIA.md           # Regra de curadoria
│   └── REGRA_APRESENTACAO_CONTEUDO.md           # Regra de apresentação
│
├── 📁 config/                                     # ⚙️ CONFIGURAÇÕES
│   └── [arquivos de configuração]
│
├── 📁 templates/                                  # 📋 TEMPLATES
│   └── [templates de conteúdo]
│
├── 📁 4_arquivos_suporte/                        # 📎 ARQUIVOS DE SUPORTE
│
└── 📁 temp_historico/                            # 🗄️ HISTÓRICO ARQUIVADO
    ├── json_historico/                           # 54 JSONs antigos
    ├── scripts_temp/                             # 67 scripts temporários
    ├── relatorios_antigos/                       # 6 relatórios com timestamp
    ├── logs/                                     # 4 arquivos de log
    └── relatorio_organizacao.json                # Relatório desta organização
```

---

## 🎯 ARQUIVOS PRINCIPAIS NA RAIZ

### Documentação e Relatórios
- `README.md` - Documentação principal do projeto
- `DIAGNOSTICO_MCP.md` - Status das ferramentas MCP
- `RELATORIO_FINAL_4_CONTEUDOS_PRE_ENEM.md` - Relatório completo (20.500+ palavras)
- `RELATORIO_FINALIZACAO_PRE_ENEM.md` - Relatório de finalização
- `ESTRUTURA_PROJETO.md` - Documentação da estrutura (este arquivo)

### Dados Ativos
- `sincronizacao_pre_enem.json` - Dados de sincronização com Notion (ativo)
- `analise_editorial_pre_enem.json` - Análise completa do Editorial PRÉ-ENEM

### Configuração
- `requirements.txt` - Dependências Python do projeto
- `.gitignore` - Arquivos ignorados pelo Git

---

## 🔥 CONTEÚDOS PRÉ-ENEM (4 NOVOS)

### Status: ✅ Sincronizados com Notion

1. **Simulados ENEM 2025: Como Usar de Forma Estratégica**
   - 📄 `artigo_simulados_enem_2025_estrategico.md`
   - 📝 4.200 palavras | 12 min leitura
   - 🔗 Notion: 27e5113a-91a3-81d3-bdff-dede52c7c12e

2. **Ansiedade no ENEM 2025: Guia Completo para Controlar o Nervosismo**
   - 📄 `artigo_ansiedade_enem_2025_gestao_emocional.md`
   - 📝 5.500 palavras | 15 min leitura
   - 🔗 Notion: 27e5113a-91a3-81a4-b631-fb86080feb20

3. **O Dia da Prova ENEM 2025: Checklist Completo**
   - 📄 `artigo_dia_prova_enem_2025_checklist.md`
   - 📝 5.000 palavras | 18 min leitura
   - 🔗 Notion: 27f5113a-91a3-81af-9a7a-f60ed50b5c32

4. **Técnicas de Memorização para o ENEM 2025**
   - 📄 `artigo_tecnicas_memorizacao_enem_2025.md`
   - 📝 5.800 palavras | 16 min leitura
   - 🔗 Notion: 27f5113a-91a3-817b-b018-f997ace59629

**Database Notion:** `2695113a-91a3-81dd-bfc4-fc8e4df72e7f`

---

## 🔧 SCRIPTS ESSENCIAIS

### Curadoria e Sincronização
- `curadoria_automatica.py` - Verificação de boilerplate (9 critérios)
- `curadoria_completa.py` - Curadoria completa com enriquecimento MCP
- `curadoria_e_sincronizacao_pre_enem_temp.py` - **Script ativo para PRÉ-ENEM**

### Sincronização Notion
- `sincronizar_notion.py` - Sincronização geral com Notion

### Verificação e Setup
- `verificar_configuracao.py` - Verifica setup do projeto
- `verificar_fontes_mcp.py` - Verifica MCPs disponíveis
- `buscar_fontes_confiaveis.py` - Busca fontes com Search MCP
- `setup_projeto.py` - Setup inicial do projeto

---

## 🗄️ HISTÓRICO ARQUIVADO

**Localização:** `/temp_historico/`

### O que foi arquivado:
- ✅ **54 arquivos JSON** históricos (análises, correções antigas)
- ✅ **67 scripts temporários** (scripts de testes e correções pontuais)
- ✅ **6 relatórios antigos** (com timestamp 20250923/20250924)
- ✅ **4 arquivos de log** (logs de curadoria e execução)

### Por que arquivado:
- Mantém raiz limpa e organizada
- Preserva histórico para consulta futura
- Facilita navegação no projeto
- Reduz poluição visual

---

## 📊 ESTATÍSTICAS DO PROJETO

### Conteúdos
- **Total PRÉ-ENEM:** 23 conteúdos (19 existentes + 4 novos)
- **Total Gestão Escolar:** 196 conteúdos publicados
- **Novos conteúdos:** 20.500+ palavras (61 min leitura)

### Organização
- **Arquivos organizados:** 131 arquivos
- **Espaço liberado na raiz:** ~60 arquivos movidos
- **Scripts ativos:** 9 essenciais
- **Scripts arquivados:** 67 temporários

### Conformidade
- **Boilerplate:** 100% (9/9 critérios em todos os 4 conteúdos)
- **Enriquecimento MCP:** Charts ✅ + Search ✅
- **Sincronização:** 4/4 conteúdos sincronizados com sucesso

---

## 🚀 COMO USAR O PROJETO

### 1. Criar Novo Conteúdo PRÉ-ENEM

```bash
# 1. Criar rascunho em 2_conteudo/01_ideias_e_rascunhos/
# 2. Executar curadoria e sincronização
cd modelo_projeto_conteudo
python scripts/curadoria_e_sincronizacao_pre_enem_temp.py
```

### 2. Verificar MCPs Disponíveis

```bash
python scripts/verificar_fontes_mcp.py
```

### 3. Buscar Fontes Confiáveis

```bash
python scripts/buscar_fontes_confiaveis.py
```

### 4. Sincronizar com Notion

```bash
python scripts/sincronizar_notion.py
```

---

## 📋 REGRAS E BOILERPLATE

### Documentação das Regras
Localização: `/docs/`

1. **REGRA_ENRIQUECIMENTO_MCP.md**
   - Uso obrigatório de MCPs (Charts, Search, YouTube)
   - 9 tipos de enriquecimento

2. **REGRA_BOILERPLATE_GESTAO.md**
   - Estrutura obrigatória para Gestão Escolar
   - Análise prévia da biblioteca

3. **REGRA_CURADORIA_OBRIGATORIA.md**
   - Pontuação mínima 80%
   - Correção automática se reprovado

4. **REGRA_APRESENTACAO_CONTEUDO.md**
   - Capa simples
   - Gráficos limpos
   - Vídeos padronizados

### Boilerplate (9 Critérios)
- ✅ Título H1
- ✅ Imagem de Capa
- ✅ Resumo Executivo
- ✅ Dados e Gráficos
- ✅ Vídeos
- ✅ Fontes Confiáveis
- ✅ Conclusão
- ✅ Tags
- ✅ Metadados Editoriais

---

## 🔍 DIAGNÓSTICO TÉCNICO

### MCPs Operacionais ✅
- **Notion MCP** - 100% funcional
- **Search MCP** - 100% funcional
- **Design MCP** - Disponível (não usado nos conteúdos atuais)

### MCPs Inoperantes ❌
- **YouTube MCP** - Não funcional
  - Workaround: Web search para vídeos
  - Impacto: Mínimo (conteúdo mantém qualidade)

---

## 📌 PRÓXIMOS PASSOS RECOMENDADOS

### Curto Prazo
1. Revisar os 4 conteúdos PRÉ-ENEM no Notion
2. Aprovar para publicação (já 100% conformes)
3. Publicar no Editorial

### Médio Prazo
4. Criar conteúdo: Análise de Desempenho
5. Criar conteúdos: Revisões Relâmpago (Ciências, Humanas, Português)
6. Reclassificar 18 conteúdos existentes (atualmente como "Gestão Escolar")

### Longo Prazo
7. Publicar os 6 rascunhos existentes
8. Criar conteúdos complementares (alimentação, sono)
9. Enriquecer conteúdos antigos com MCPs

---

## ✨ CONQUISTAS RECENTES

✅ **Estrutura 100% organizada e limpa**  
✅ **4 conteúdos PRÉ-ENEM criados** (20.500+ palavras)  
✅ **100% conformidade boilerplate** (9/9 todos)  
✅ **131 arquivos organizados** (raiz limpa)  
✅ **Histórico preservado** (temp_historico/)  
✅ **Documentação completa** (DIAGNOSTICO_MCP, Relatórios)  
✅ **Scripts otimizados** (9 essenciais mantidos)  

---

**Mantido e organizado por:** Sistema Automatizado de Conteúdo  
**Data da última organização:** 30/09/2025  
**Status:** ✅ LIMPO E ORGANIZADO

