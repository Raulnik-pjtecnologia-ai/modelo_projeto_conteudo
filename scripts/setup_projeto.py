#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Configuração Inicial do Projeto
Configura o projeto para uma nova área de conhecimento
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime

def criar_estrutura_pastas(area_conhecimento):
    """Cria a estrutura de pastas para o projeto"""
    print(f"📁 Criando estrutura de pastas para: {area_conhecimento}")
    
    # Estrutura base
    estrutura = {
        "2_conteudo": {
            "01_ideias_e_rascunhos": {
                area_conhecimento: []
            },
            "02_em_revisao": {
                area_conhecimento: []
            },
            "03_pronto_para_publicar": {
                area_conhecimento: []
            },
            "04_publicado": {
                area_conhecimento: []
            }
        },
        "docs": [],
        "scripts": [],
        "templates": [],
        "config": []
    }
    
    # Criar pastas
    for pasta_principal, subpastas in estrutura.items():
        pasta_path = Path(pasta_principal)
        pasta_path.mkdir(exist_ok=True)
        
        if isinstance(subpastas, dict):
            for subpasta, conteudo in subpastas.items():
                subpasta_path = pasta_path / subpasta
                subpasta_path.mkdir(exist_ok=True)
                
                if isinstance(conteudo, dict):
                    for subsubpasta in conteudo:
                        (subpasta_path / subsubpasta).mkdir(exist_ok=True)
    
    print("✅ Estrutura de pastas criada com sucesso!")

def criar_configuracao(area_conhecimento, config_path="config/config.json"):
    """Cria arquivo de configuração para a área de conhecimento"""
    print(f"⚙️  Criando configuração para: {area_conhecimento}")
    
    config = {
        "projeto": {
            "nome": f"Modelo Projeto Conteúdo - {area_conhecimento.title()}",
            "area_conhecimento": area_conhecimento,
            "versao": "1.0.0",
            "data_criacao": datetime.now().isoformat(),
            "descricao": f"Modelo profissional para criação e gestão de conteúdo editorial em {area_conhecimento}"
        },
        "notion": {
            "token": "SEU_TOKEN_AQUI",
            "database_id": "SEU_DATABASE_ID_AQUI",
            "categorias_database_id": "SEU_CATEGORIAS_DATABASE_ID_AQUI"
        },
        "categorias": [
            "Estratégico",
            "Tático", 
            "Operacional"
        ],
        "funcoes": [
            "Gestão",
            "Pedagógica",
            "Financeira",
            "Jurídica",
            "Recursos Humanos",
            "Infraestrutura",
            "Comunicação",
            "Qualidade",
            "Inovação",
            "Sustentabilidade"
        ],
        "tipos_conteudo": [
            "Artigo",
            "Checklist",
            "Lição",
            "Vídeo",
            "Documento Oficial",
            "Apresentação"
        ],
        "niveis": [
            "Básico",
            "Intermediário",
            "Avançado"
        ]
    }
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ Configuração criada com sucesso!")

def criar_templates_personalizados(area_conhecimento):
    """Cria templates personalizados para a área de conhecimento"""
    print(f"📝 Criando templates personalizados para: {area_conhecimento}")
    
    # Template de artigo
    template_artigo = f"""# [TÍTULO DO ARTIGO] - {area_conhecimento.title()}

## 📋 Resumo Executivo

[Resumo de 2-3 parágrafos sobre o conteúdo do artigo]

## 🎯 Objetivos

- [Objetivo 1]
- [Objetivo 2]
- [Objetivo 3]

## 📚 Conteúdo Principal

### 1. [Seção Principal 1]

[Conteúdo detalhado]

### 2. [Seção Principal 2]

[Conteúdo detalhado]

### 3. [Seção Principal 3]

[Conteúdo detalhado]

## ✅ Checklist de Aplicação

- [ ] [Item de aplicação 1]
- [ ] [Item de aplicação 2]
- [ ] [Item de aplicação 3]

## 📖 Referências

- [Referência 1]
- [Referência 2]

## 🏷️ Tags

**Categoria:** [Categoria]
**Função:** [Função]
**Nível:** [Nível]
**Área:** {area_conhecimento}

---
*Criado em: {datetime.now().strftime('%d/%m/%Y')}*
*Versão: 1.0*
"""
    
    # Template de checklist
    template_checklist = f"""# 📋 CHECKLIST: [NOME DO PROCESSO] - {area_conhecimento.title()}

## 🎯 Objetivo

[Descrição do objetivo do checklist]

## ⏱️ Tempo Estimado

[ ] 15 minutos
[ ] 30 minutos
[ ] 1 hora
[ ] 2+ horas

## 📋 Lista de Verificação

### ✅ Preparação
- [ ] [Item de preparação 1]
- [ ] [Item de preparação 2]
- [ ] [Item de preparação 3]

### ✅ Execução
- [ ] [Item de execução 1]
- [ ] [Item de execução 2]
- [ ] [Item de execução 3]

### ✅ Finalização
- [ ] [Item de finalização 1]
- [ ] [Item de finalização 2]
- [ ] [Item de finalização 3]

## ⚠️ Pontos de Atenção

- [Ponto de atenção 1]
- [Ponto de atenção 2]

## 📞 Suporte

[Informações de suporte ou contato]

---
*Criado em: {datetime.now().strftime('%d/%m/%Y')}*
*Versão: 1.0*
"""
    
    # Template de lição
    template_licao = f"""# 📚 Lição: [TÍTULO DA LIÇÃO] - {area_conhecimento.title()}

## 🎯 Objetivos de Aprendizagem

Ao final desta lição, você será capaz de:
- [Objetivo 1]
- [Objetivo 2]
- [Objetivo 3]

## 📖 Conteúdo da Lição

### Introdução

[Introdução ao tema]

### Desenvolvimento

#### 1. [Conceito Principal 1]

[Explicação detalhada]

**Exemplo Prático:**
[Exemplo aplicado]

#### 2. [Conceito Principal 2]

[Explicação detalhada]

**Exemplo Prático:**
[Exemplo aplicado]

#### 3. [Conceito Principal 3]

[Explicação detalhada]

**Exemplo Prático:**
[Exemplo aplicado]

### Conclusão

[Síntese dos pontos principais]

## 🧪 Atividades Práticas

### Atividade 1: [Nome da Atividade]
[Descrição da atividade]

### Atividade 2: [Nome da Atividade]
[Descrição da atividade]

## 📝 Avaliação

[Critérios de avaliação]

## 📚 Recursos Adicionais

- [Recurso 1]
- [Recurso 2]

---
*Criado em: {datetime.now().strftime('%d/%m/%Y')}*
*Versão: 1.0*
"""
    
    # Salvar templates
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    with open(templates_dir / "template_artigo_padronizado.md", 'w', encoding='utf-8') as f:
        f.write(template_artigo)
    
    with open(templates_dir / "template_checklist_padronizado.md", 'w', encoding='utf-8') as f:
        f.write(template_checklist)
    
    with open(templates_dir / "template_licao_padronizado.md", 'w', encoding='utf-8') as f:
        f.write(template_licao)
    
    print("✅ Templates personalizados criados com sucesso!")

def criar_readme_personalizado(area_conhecimento):
    """Cria README personalizado para a área de conhecimento"""
    print(f"📄 Criando README personalizado para: {area_conhecimento}")
    
    readme_content = f"""# 📚 Modelo Projeto Conteúdo - {area_conhecimento.title()}

## 🎯 Visão Geral

Este é um modelo profissional e reutilizável para criação e gestão de conteúdo editorial em {area_conhecimento}. O projeto foi desenvolvido para ser adaptável a qualquer área de conhecimento que necessite de produção sistemática de conteúdo educacional.

## 🏗️ Arquitetura do Projeto

```
📂 modelo_projeto_conteudo/
├─ 📄 README.md                    # Este arquivo
├─ 📄 .gitignore                   # Configuração do Git
├─ 📄 requirements.txt             # Dependências Python
├─ 📁 config/                      # ⚙️ Configurações
│  └─ 📄 config.json               # Configuração principal
├─ 📁 scripts/                     # 🤖 Scripts e automações
│  ├─ 📄 setup_projeto.py          # Configuração inicial
│  ├─ 📄 sincronizar_notion.py     # Sincronização com Notion
│  └─ 📄 organizar_desktop.py      # Organização automática
├─ 📁 templates/                   # 📝 Templates de conteúdo
│  ├─ 📄 template_artigo_padronizado.md
│  ├─ 📄 template_checklist_padronizado.md
│  └─ 📄 template_licao_padronizado.md
├─ 📁 2_conteudo/                  # 📚 Pipeline de conteúdo
│  ├─ 📁 01_ideias_e_rascunhos/    # Ideias iniciais
│  ├─ 📁 02_em_revisao/            # Conteúdo em revisão
│  ├─ 📁 03_pronto_para_publicar/  # Conteúdo aprovado
│  └─ 📁 04_publicado/             # Conteúdo publicado
└─ 📁 docs/                        # 📚 Documentação
   └─ 📄 guia_uso.md               # Guia de uso
```

## 🚀 Como Usar

### 1. Configuração Inicial
1. Execute: `python scripts/setup_projeto.py`
2. Configure as credenciais do Notion em `config/config.json`
3. Personalize os templates conforme necessário

### 2. Produção de Conteúdo
1. **Ideias**: Comece em `2_conteudo/01_ideias_e_rascunhos/`
2. **Desenvolvimento**: Use os templates em `templates/`
3. **Revisão**: Mova para `2_conteudo/02_em_revisao/`
4. **Aprovação**: Transfira para `2_conteudo/03_pronto_para_publicar/`
5. **Publicação**: Finalize em `2_conteudo/04_publicado/`

### 3. Automação
- Use `scripts/sincronizar_notion.py` para sincronizar com Notion
- Use `scripts/organizar_desktop.py` para organização automática

## 🎯 Características Principais

### ✅ Sistema de Pipeline Editorial
- **4 estágios claros**: Ideias → Revisão → Aprovação → Publicação
- **Controle de qualidade**: Checklist integrado
- **Rastreabilidade**: Histórico completo

### ✅ Templates Padronizados
- **Artigos**: Estrutura consistente
- **Checklists**: Formato padronizado
- **Lições**: Template educacional
- **Personalizáveis**: Adaptáveis à área

### ✅ Integração com Notion
- **Sincronização automática**
- **Classificação multidimensional**
- **Sistema de tags**
- **Views especializadas**

## 📊 Sistema de Classificação

### Por Função
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

### Por Nível
- **Básico**: Conceitos fundamentais
- **Intermediário**: Aplicação prática
- **Avançado**: Especialização e expertise

## 🔧 Tecnologias Utilizadas

- **Notion**: Plataforma principal
- **Markdown**: Formato padrão
- **Python**: Scripts de automação
- **Git**: Controle de versão

## 📈 Métricas de Sucesso

- **Qualidade**: Conteúdo completo e aplicável
- **Eficiência**: Redução do tempo de produção
- **Consistência**: Padrões uniformes
- **Escalabilidade**: Fácil adaptação

## 🤝 Contribuição

Este modelo está em constante evolução. Contribuições são bem-vindas!

## 📄 Licença

Este projeto está sob licença MIT.

---
**Versão**: 1.0.0  
**Última atualização**: {datetime.now().strftime('%d/%m/%Y')}  
**Status**: Estável e em produção
"""
    
    with open("README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ README personalizado criado com sucesso!")

def main():
    """Função principal"""
    print("🚀 CONFIGURAÇÃO INICIAL DO PROJETO")
    print("="*50)
    
    # Solicitar área de conhecimento
    area_conhecimento = input("📚 Digite a área de conhecimento para o projeto: ").strip()
    
    if not area_conhecimento:
        print("❌ Área de conhecimento é obrigatória!")
        return
    
    print(f"\n🎯 Configurando projeto para: {area_conhecimento}")
    print()
    
    # Executar configuração
    criar_estrutura_pastas(area_conhecimento)
    criar_configuracao(area_conhecimento)
    criar_templates_personalizados(area_conhecimento)
    criar_readme_personalizado(area_conhecimento)
    
    print("\n" + "="*50)
    print("🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*50)
    print(f"✅ Projeto configurado para: {area_conhecimento}")
    print("✅ Estrutura de pastas criada")
    print("✅ Configuração salva em config/config.json")
    print("✅ Templates personalizados criados")
    print("✅ README personalizado criado")
    print()
    print("📝 PRÓXIMOS PASSOS:")
    print("1. Configure suas credenciais do Notion em config/config.json")
    print("2. Personalize os templates conforme necessário")
    print("3. Comece a criar conteúdo em 2_conteudo/01_ideias_e_rascunhos/")
    print("4. Use scripts/sincronizar_notion.py para sincronizar com Notion")

if __name__ == "__main__":
    main()
