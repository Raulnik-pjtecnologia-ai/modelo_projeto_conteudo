# 📚 Guia de Uso - Modelo Projeto Conteúdo

## 🎯 Visão Geral

Este guia explica como usar o Modelo Projeto Conteúdo para criar e gerenciar conteúdo editorial de forma profissional e sistemática.

## 🚀 Configuração Inicial

### 1. Configurar o Projeto

Execute o script de configuração inicial:

```bash
python scripts/setup_projeto.py
```

Este script irá:
- Criar a estrutura de pastas
- Gerar arquivo de configuração
- Criar templates personalizados
- Gerar README personalizado

### 2. Configurar Notion

1. Edite o arquivo `config/config.json`
2. Substitua os valores de exemplo pelas suas credenciais:
   - `token`: Seu token de integração do Notion
   - `database_id`: ID do seu database principal
   - `categorias_database_id`: ID do database de categorias

### 3. Personalizar Templates

Edite os arquivos em `templates/` conforme sua necessidade:
- `template_artigo_padronizado.md`
- `template_checklist_padronizado.md`
- `template_licao_padronizado.md`

## 📝 Fluxo de Trabalho

### 1. Criação de Conteúdo

1. **Ideias e Rascunhos** (`2_conteudo/01_ideias_e_rascunhos/`)
   - Comece criando rascunhos usando os templates
   - Use nomes descritivos para os arquivos
   - Inclua tags e categorias no conteúdo

2. **Revisão** (`2_conteudo/02_em_revisao/`)
   - Mova conteúdo pronto para revisão
   - Revise estrutura, conteúdo e formatação
   - Verifique se atende aos padrões estabelecidos

3. **Aprovação** (`2_conteudo/03_pronto_para_publicar/`)
   - Conteúdo aprovado e pronto para publicação
   - Verificação final de qualidade
   - Preparação para sincronização

4. **Publicação** (`2_conteudo/04_publicado/`)
   - Conteúdo final publicado
   - Arquivo de referência
   - Histórico de versões

### 2. Sincronização com Notion

Execute a sincronização:

```bash
python scripts/sincronizar_notion.py
```

Este script irá:
- Conectar com o Notion
- Sincronizar propriedades das páginas
- Atualizar categorias e tags
- Manter consistência entre local e Notion

### 3. Organização Automática

Use o script de organização:

```bash
python scripts/organizar_desktop.py
```

Este script irá:
- Mover arquivos Python para `scripts/`
- Mover relatórios JSON para `docs/`
- Mover conteúdo Markdown para `2_conteudo/01_ideias_e_rascunhos/`
- Manter o desktop limpo

## 📊 Sistema de Classificação

### Categorias por Função
- **Gestão**: Estratégica e operacional
- **Pedagógica**: Ensino e aprendizagem
- **Financeira**: Orçamento e custos
- **Jurídica**: Conformidade legal
- **Recursos Humanos**: Gestão de pessoas
- **Infraestrutura**: Instalações e tecnologia
- **Comunicação**: Relacionamento e marketing
- **Qualidade**: Padrões e processos
- **Inovação**: Novas tecnologias e métodos
- **Sustentabilidade**: Práticas sustentáveis

### Níveis de Profundidade
- **Básico**: Conceitos fundamentais
- **Intermediário**: Aplicação prática
- **Avançado**: Especialização e expertise

### Tipos de Conteúdo
- **Artigo**: Conteúdo informativo detalhado
- **Checklist**: Lista de verificação para processos
- **Lição**: Conteúdo educacional estruturado
- **Vídeo**: Conteúdo audiovisual
- **Documento Oficial**: Documentos formais
- **Apresentação**: Slides e apresentações

## 🛠️ Scripts Disponíveis

### `setup_projeto.py`
Configuração inicial do projeto para nova área de conhecimento.

### `sincronizar_notion.py`
Sincroniza conteúdo local com o database do Notion.

### `organizar_desktop.py`
Organiza automaticamente arquivos do desktop nas pastas do projeto.

### `limpar_desktop.ps1` (PowerShell)
Script PowerShell para execução rápida da organização.

## 📁 Estrutura de Pastas

```
modelo_projeto_conteudo/
├─ config/                    # Configurações
│  └─ config.json            # Configuração principal
├─ scripts/                  # Scripts e automações
│  ├─ setup_projeto.py       # Configuração inicial
│  ├─ sincronizar_notion.py  # Sincronização Notion
│  ├─ organizar_desktop.py   # Organização automática
│  └─ limpar_desktop.ps1     # Script PowerShell
├─ templates/                # Templates de conteúdo
│  ├─ template_artigo_padronizado.md
│  ├─ template_checklist_padronizado.md
│  └─ template_licao_padronizado.md
├─ 2_conteudo/               # Pipeline de conteúdo
│  ├─ 01_ideias_e_rascunhos/ # Ideias iniciais
│  ├─ 02_em_revisao/         # Conteúdo em revisão
│  ├─ 03_pronto_para_publicar/ # Conteúdo aprovado
│  └─ 04_publicado/          # Conteúdo publicado
├─ docs/                     # Documentação
│  └─ guia_uso.md           # Este guia
└─ README.md                # Documentação principal
```

## 🔧 Personalização

### Adaptar para Nova Área

1. Execute `python scripts/setup_projeto.py`
2. Digite o nome da nova área de conhecimento
3. Personalize os templates conforme necessário
4. Ajuste as categorias em `config/config.json`

### Adicionar Novos Tipos de Conteúdo

1. Crie novo template em `templates/`
2. Atualize `config/config.json` com o novo tipo
3. Modifique `scripts/sincronizar_notion.py` se necessário

### Personalizar Classificação

1. Edite as categorias em `config/config.json`
2. Ajuste as funções disponíveis
3. Modifique os níveis de profundidade

## 📈 Boas Práticas

### Nomenclatura de Arquivos
- Use nomes descritivos e claros
- Inclua data quando relevante
- Use hífens para separar palavras
- Exemplo: `artigo-gestao-financeira-2024.md`

### Estrutura de Conteúdo
- Sempre use os templates fornecidos
- Mantenha consistência na formatação
- Inclua tags e categorias adequadas
- Revise antes de mover para próxima etapa

### Organização
- Execute `organizar_desktop.py` regularmente
- Mantenha o desktop limpo
- Use as pastas corretas para cada tipo de arquivo
- Faça backup regular dos arquivos importantes

## 🆘 Solução de Problemas

### Erro de Conexão com Notion
- Verifique se o token está correto
- Confirme se os database IDs estão corretos
- Teste a conexão manualmente

### Scripts Não Executam
- Verifique se o Python está instalado
- Confirme se as dependências estão instaladas
- Execute `pip install -r requirements.txt`

### Arquivos Não Sincronizam
- Verifique se as propriedades do Notion estão corretas
- Confirme se os nomes das propriedades coincidem
- Teste com uma página individual primeiro

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte este guia primeiro
2. Verifique a documentação em `docs/`
3. Revise os logs de erro dos scripts
4. Consulte a documentação do Notion API

---

**Versão**: 1.0.0  
**Última atualização**: Dezembro 2024  
**Status**: Estável e em produção
