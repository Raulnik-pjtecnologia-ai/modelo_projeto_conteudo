# 📁 Estrutura Organizada do Projeto - Editorial Conteúdo

**Última atualização:** 30/09/2025  
**Status:** ✅ Limpa e Organizada

---

## 📂 ESTRUTURA DE DIRETÓRIOS

```
modelo_projeto_conteudo/
│
├── 📝 2_conteudo/                          # Conteúdos em diferentes estágios
│   ├── 01_ideias_e_rascunhos/              # Rascunhos e ideias iniciais
│   │   ├── pre_enem/                       # ⭐ Conteúdos PRÉ-ENEM (4 artigos)
│   │   └── gestao_escolar/                 # Conteúdos Gestão Escolar
│   │
│   ├── 02_em_revisao/                      # Em revisão editorial
│   │   ├── pre_enem/                       # Revisão PRÉ-ENEM
│   │   └── gestao_escolar/                 # Revisão Gestão
│   │
│   ├── 03_aprovado_publicacao/             # Aprovados, prontos para publicar
│   │   └── pre_enem/                       # Aprovados PRÉ-ENEM
│   │
│   └── 04_publicado/                       # Já publicados (196 arquivos)
│
├── 🔧 scripts/                             # Scripts ativos
│   ├── analisar_editorial_pre_enem_temp.py # Análise PRÉ-ENEM
│   ├── curadoria_e_sincronizacao_pre_enem_temp.py # Curadoria
│   ├── reverter_publicacao_notion_temp.py  # Reversão
│   ├── curadoria_automatica.py             # Curadoria geral
│   ├── sincronizar_notion.py               # Sincronização
│   └── [outros scripts ativos]
│
├── 📚 docs/                                # Documentação
│   ├── relatorios/                         # Relatórios históricos
│   ├── regras/                             # Regras do projeto
│   ├── RELATORIO_FINAL_4_CONTEUDOS_PRE_ENEM.md # ⭐ Relatório final
│   ├── DIAGNOSTICO_MCP.md                  # ⭐ Diagnóstico técnico
│   └── [manuais e guias]
│
├── 🗂️ temp_historico/                      # Arquivos temporários/antigos
│   ├── scripts/                            # Scripts antigos
│   ├── json/                               # JSONs de análise antiga
│   └── [arquivos históricos]
│
├── ⚙️ config/                              # Configurações
│   ├── config.json                         # Config geral
│   ├── curadoria_config.json               # Config curadoria
│   └── env.example                         # Exemplo variáveis ambiente
│
├── 📋 templates/                           # Templates de conteúdo
│   └── [10 templates .md]
│
├── 🎨 assets/                              # Recursos visuais
│   └── images/
│
├── 💾 backup_imagens/                      # Backup de imagens
│
├── 📄 README.md                            # Documentação principal
├── 📄 ESTRUTURA_PROJETO.md                 # Estrutura detalhada
├── 📄 requirements.txt                     # Dependências Python
└── 📄 .gitignore                           # Arquivos ignorados pelo Git
```

---

## 📊 ESTATÍSTICAS DO PROJETO

### Arquivos por Tipo
- **Markdown (.md):** 289 arquivos
- **Python (.py):** 8 scripts ativos
- **JSON (.json):** 71 arquivos de dados

### Conteúdos por Status
- **Rascunhos:** 9 (PRÉ-ENEM: 4 | Gestão: 5)
- **Em Revisão:** ~15
- **Aprovados:** ~10
- **Publicados:** 196

---

## ⭐ CONTEÚDOS PRÉ-ENEM RECÉM-CRIADOS

### Localização
`2_conteudo/01_ideias_e_rascunhos/pre_enem/`

### Arquivos
1. ✅ `artigo_simulados_enem_2025_estrategico.md` (4.200 palavras)
2. ✅ `artigo_ansiedade_enem_2025_gestao_emocional.md` (5.500 palavras)
3. ✅ `artigo_dia_prova_enem_2025_checklist.md` (5.000 palavras)
4. ✅ `artigo_tecnicas_memorizacao_enem_2025.md` (5.800 palavras)
5. 📋 `relatorio_pesquisa_pre_enem_2025.md` (relatório de pesquisa)
6. 📋 `README.md` (documentação da pasta)

**Todos com:**
- 100% conformidade boilerplate
- Sincronizados com Notion
- Prontos para revisão editorial

---

## 🔧 SCRIPTS ATIVOS MANTIDOS

### Scripts Essenciais
```
scripts/
├── analisar_editorial_pre_enem_temp.py      # Análise de conteúdo PRÉ-ENEM
├── curadoria_e_sincronizacao_pre_enem_temp.py # Curadoria + Notion
├── reverter_publicacao_notion_temp.py       # Reversão de publicações
├── curadoria_automatica.py                  # Curadoria geral
├── curadoria_completa.py                    # Curadoria avançada
├── sincronizar_notion.py                    # Sincronização geral
├── verificar_fontes_mcp.py                  # Verificação MCPs
└── setup_projeto.py                         # Setup inicial
```

**Total:** 8 scripts ativos (limpo e organizado)

---

## 📚 DOCUMENTAÇÃO ORGANIZADA

### Em docs/
- `RELATORIO_FINAL_4_CONTEUDOS_PRE_ENEM.md` - Relatório consolidado
- `DIAGNOSTICO_MCP.md` - Análise técnica de MCPs
- `RELATORIO_FINALIZACAO_PRE_ENEM.md` - Finalização do processo

### Em docs/relatorios/
- 5 relatórios históricos movidos
- Organização cronológica mantida

---

## 🗑️ LIMPEZA REALIZADA

### Arquivos Movidos
- ✅ 5 relatórios → `docs/relatorios/`
- ✅ 3 arquivos de finalização → `docs/`
- ✅ 2 JSONs de análise → `temp_historico/`
- ✅ 1 script antigo → `temp_historico/scripts/`
- ✅ 5 artigos PRÉ-ENEM → `2_conteudo/01_ideias_e_rascunhos/pre_enem/`

### Resultado
- 🟢 **Raiz do projeto:** Limpa (apenas essenciais)
- 🟢 **Scripts:** Apenas ativos
- 🟢 **Conteúdos:** Organizados por editorial
- 🟢 **Documentação:** Centralizada em `docs/`
- 🟢 **Histórico:** Preservado em `temp_historico/`

---

## 🎯 PRINCÍPIOS DE ORGANIZAÇÃO

### 1. Separação Clara
- **Conteúdo ativo** em pastas principais
- **Histórico/temporário** em `temp_historico/`
- **Documentação** em `docs/`

### 2. Nomenclatura Consistente
- Editorialprefix: `pre_enem/` ou `gestao_escolar/`
- Scripts temporários: `*_temp.py`
- Relatórios: `relatorio_*.md`

### 3. Não Poluir Raiz
- Apenas arquivos essenciais na raiz
- README, ESTRUTURA, requirements
- Tudo mais em subpastas apropriadas

### 4. Git Limpo
- `.gitignore` configurado
- Apenas conteúdo relevante versionado
- Histórico preservado mas organizado

---

## 📝 MANUTENÇÃO CONTÍNUA

### A Fazer Periodicamente
1. Mover conteúdos finalizados para pastas apropriadas
2. Limpar scripts `*_temp.py` antigos
3. Arquivar relatórios em `docs/relatorios/`
4. Mover JSONs de análise para `temp_historico/`
5. Atualizar este README quando estrutura mudar

### Comando Rápido de Limpeza
```bash
cd modelo_projeto_conteudo
python scripts/organizar_estrutura_projeto_temp.py
```

---

## ✅ STATUS FINAL

**Estrutura:** 🟢 LIMPA E ORGANIZADA  
**Conteúdos:** 🟢 4 PRONTOS PARA REVISÃO  
**Scripts:** 🟢 APENAS ATIVOS  
**Documentação:** 🟢 CENTRALIZADA  
**Git:** 🟢 VERSIONADO  

**Projeto pronto para continuar gerando conteúdo de qualidade!** 🚀

---

**Responsável pela organização:** Sistema Automatizado  
**Data:** 30/09/2025  
**Próxima revisão:** Quando houver novos conteúdos

