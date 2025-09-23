# 🔧 Sistema de Variáveis de Ambiente

## 📋 Visão Geral

Este documento descreve o sistema completo de gerenciamento de variáveis de ambiente implementado no projeto Modelo Projeto Conteúdo, garantindo a segurança das chaves sensíveis e a portabilidade do código.

## 🎯 Objetivos

- **Segurança**: Manter chaves e tokens sensíveis fora do código-fonte
- **Portabilidade**: Facilitar a configuração em diferentes ambientes
- **Reutilização**: Permitir que o boilerplate seja usado em outros projetos
- **Manutenibilidade**: Centralizar configurações em um local único

## 🏗️ Arquitetura

### Arquivos Principais

```
📂 modelo_projeto_conteudo/
├─ 📄 .env                    # Arquivo de configuração (NÃO commitado)
├─ 📄 env_template.txt        # Template para criação do .env
├─ 📄 .gitignore             # Ignora arquivo .env
├─ 📁 config/
│  └─ 📄 config.json         # Configuração com placeholders
└─ 📁 scripts/
   ├─ 📄 configurar_ambiente.py    # Script de configuração
   ├─ 📄 carregar_configuracao.py  # Carregamento de variáveis
   └─ 📄 verificar_configuracao.py # Verificação de segurança
```

### Fluxo de Configuração

1. **Template**: `env_template.txt` contém todas as variáveis necessárias
2. **Configuração**: Scripts criam e configuram o arquivo `.env`
3. **Carregamento**: Variáveis são injetadas nos arquivos de configuração
4. **Verificação**: Sistema valida se não há tokens hardcoded

## 🔑 Variáveis de Ambiente

### Configurações Essenciais

```env
# Notion API
NOTION_TOKEN=seu_token_notion_aqui
DATABASE_ID=seu_database_id_aqui
CATEGORIA_DATABASE_ID=seu_categoria_database_id_aqui

# URLs das Categorias
CATEGORIA_FINANCEIRO_URL=https://www.notion.so/Financeiro-seu_id_aqui
CATEGORIA_FORMACAO_URL=https://www.notion.so/Forma-o-seu_id_aqui
CATEGORIA_GOVERNANCA_URL=https://www.notion.so/Governan-a-seu_id_aqui
# ... outras categorias
```

### Configurações de Curadoria

```env
# Pontuação mínima para aprovação
CURADORIA_PONTUACAO_MINIMA=70

# Quantidades mínimas
CURADORIA_MIN_GRAFICOS=2
CURADORIA_MIN_VIDEOS=2
CURADORIA_MIN_FONTES=4

# Verificações habilitadas
CURADORIA_VERIFICAR_CAPAS=true
CURADORIA_VERIFICAR_DADOS=true
CURADORIA_VERIFICAR_VIDEOS=true
CURADORIA_VERIFICAR_FONTES=true
```

## 🚀 Como Usar

### 1. Configuração Inicial

```bash
# Instalar dependências
pip install python-dotenv notion-client

# Configurar ambiente
python scripts/configurar_ambiente.py

# Carregar configurações
python scripts/carregar_configuracao.py
```

### 2. Verificação de Segurança

```bash
# Verificar se não há tokens hardcoded
python scripts/verificar_configuracao.py
```

### 3. Uso nos Scripts

```python
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Usar variáveis
notion_token = os.getenv("NOTION_TOKEN")
database_id = os.getenv("DATABASE_ID")
```

## 🔒 Segurança

### Boas Práticas

1. **Nunca commite o arquivo `.env`**
2. **Use placeholders nos templates**
3. **Verifique regularmente se não há tokens hardcoded**
4. **Mantenha o `.gitignore` atualizado**

### Verificação Automática

O script `verificar_configuracao.py` verifica:
- ✅ Ausência de tokens hardcoded
- ✅ Configuração correta das variáveis
- ✅ Presença do arquivo `.env`
- ✅ Configuração do `.gitignore`

## 📝 Templates

### Template de Artigo

```markdown
# {{TITULO}}

## 📸 Capa
![Capa do artigo]({{CAPA_URL}})

## 📊 Dados e Gráficos
{{GRAFICOS}}

## 🎥 Vídeos Relacionados
{{VIDEOS}}

## 📚 Fontes
{{FONTES}}
```

### Template de Curadoria

```markdown
# Curadoria de Conteúdo

## ✅ Verificações
- [ ] Capa presente e adequada
- [ ] Dados e gráficos incluídos
- [ ] Vídeos relacionados
- [ ] Fontes confiáveis

## 📊 Pontuação
- Estrutura: {{PONTUACAO_ESTRUTURA}}/25
- Conteúdo: {{PONTUACAO_CONTEUDO}}/25
- Formatação: {{PONTUACAO_FORMATACAO}}/25
- Completude: {{PONTUACAO_COMPLETUDE}}/25
- **Total: {{PONTUACAO_TOTAL}}/100**
```

## 🔄 Integração com Scripts

### Scripts Atualizados

Todos os scripts principais foram atualizados para usar variáveis de ambiente:

- `setup_projeto.py` - Configuração inicial
- `sincronizar_notion.py` - Sincronização com Notion
- `organizar_desktop.py` - Organização automática
- `curadoria_completa.py` - Sistema de curadoria

### Exemplo de Implementação

```python
def carregar_configuracao():
    """Carrega configuração do projeto"""
    try:
        from scripts.carregar_configuracao import carregar_variaveis_ambiente, carregar_configuracao_json
        
        variaveis = carregar_variaveis_ambiente()
        config_path = Path('config/config.json')
        
        if config_path.exists():
            carregar_configuracao_json(config_path, variaveis)
        
        with open('config/config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"❌ Erro ao carregar configuração: {e}")
        return None
```

## 📊 Benefícios

### Para Desenvolvedores

- ✅ Configuração rápida e simples
- ✅ Segurança das chaves sensíveis
- ✅ Portabilidade entre ambientes
- ✅ Verificação automática de segurança

### Para o Projeto

- ✅ Código limpo e profissional
- ✅ Fácil reutilização
- ✅ Manutenção simplificada
- ✅ Documentação completa

## 🎉 Conclusão

O sistema de variáveis de ambiente implementado garante:

1. **Segurança total** das chaves sensíveis
2. **Facilidade de uso** para novos desenvolvedores
3. **Portabilidade** entre diferentes ambientes
4. **Manutenibilidade** do código
5. **Reutilização** do boilerplate

O projeto está agora pronto para ser usado em qualquer ambiente, mantendo a segurança e a facilidade de configuração.
