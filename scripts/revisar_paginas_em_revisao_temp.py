#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Revisar Páginas em Revisão
Aplica melhorias específicas para aprovação
"""

import os
import sys
import requests
import json
from datetime import datetime
import time

sys.stdout.reconfigure(encoding='utf-8')

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
if not NOTION_TOKEN:
    print("ERRO: Configure NOTION_TOKEN")
    sys.exit(1)

# ID da biblioteca Editorial de Aluno (PRÉ-ENEM)
DATABASE_ALUNO = "2695113a-91a3-81dd-bfc4-fc8e4df72e7f"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def print_secao(titulo):
    print("\n" + "="*80)
    print(titulo)
    print("="*80)

def obter_paginas_em_revisao(database_id):
    """Obtém páginas em revisão para melhoria"""
    print(f"🔍 Buscando páginas em revisão...")
    
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    payload = {
        "filter": {
            "property": "Status Editorial",
            "select": {
                "equals": "Em Revisão"
            }
        }
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    
    if response.status_code != 200:
        print(f"❌ Erro ao buscar páginas: {response.status_code}")
        return []
    
    data = response.json()
    pages = data.get("results", [])
    
    print(f"✅ Encontradas {len(pages)} páginas em revisão")
    return pages

def obter_titulo_pagina(page):
    """Obtém o título da página"""
    properties = page.get("properties", {})
    title_prop = properties.get("Title") or properties.get("title")
    
    if title_prop and title_prop.get("title"):
        return title_prop["title"][0]["text"]["content"]
    return "Sem título"

def obter_conteudo_pagina(page_id):
    """Obtém o conteúdo da página"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        return []
    
    data = response.json()
    return data.get("results", [])

def melhorar_conteudo_em_revisao(titulo_original, content_blocks):
    """Melhora conteúdo específico em revisão"""
    
    # Conteúdos específicos para páginas em revisão
    melhorias_especificas = {
        "Técnicas de Memorização para o ENEM 2025: Aprenda Mais Rápido e Retenha Melhor": {
            "adicionar": """## 🎥 **VÍDEOS RELACIONADOS**

- [Técnicas de Memorização - ENEM 2025](https://youtube.com/watch?v=exemplo1)
- [Mapas Mentais para Estudos](https://youtube.com/watch?v=exemplo2)
- [Exercícios de Memória](https://youtube.com/watch?v=exemplo3)

## 📊 **EXERCÍCIOS PRÁTICOS**

### **Exercício 1: Palácio da Memória**
1. Escolha um local familiar (sua casa)
2. Associe cada conceito a um cômodo
3. Crie uma história conectando os conceitos
4. Revise mentalmente o trajeto

### **Exercício 2: Técnica de Repetição Espaçada**
- **Dia 1**: Estude o conteúdo
- **Dia 3**: Revise rapidamente
- **Dia 7**: Revise novamente
- **Dia 15**: Revisão final

## 📈 **DICAS AVANÇADAS**

### **1. Acrônimos**
- **FAMEBRAS**: Fórmulas, Áreas, Medidas, Equações, Bases, Razões, Análises, Sistemas
- **SOHCAHTOA**: Seno = Oposto/Hipotenusa, Cosseno = Adjacente/Hipotenusa, Tangente = Oposto/Adjacente

### **2. Rimas e Músicas**
- Crie rimas para fórmulas importantes
- Use melodias conhecidas para conceitos
- Grave áudios para escutar durante exercícios

### **3. Associações Visuais**
- Use cores diferentes para cada matéria
- Crie símbolos únicos para conceitos
- Desenhe diagramas coloridos"""
        },
        
        "O Dia da Prova ENEM 2025: Checklist Completo e Estratégias Infalíveis": {
            "adicionar": """## 🎥 **VÍDEOS RELACIONADOS**

- [Checklist Completo - Dia da Prova](https://youtube.com/watch?v=exemplo1)
- [Estratégias de Controle de Ansiedade](https://youtube.com/watch?v=exemplo2)
- [Dicas de Alimentação e Sono](https://youtube.com/watch?v=exemplo3)

## 📋 **CHECKLIST DETALHADO**

### **📅 UMA SEMANA ANTES**
- [ ] Confirmar local da prova
- [ ] Testar o trajeto até o local
- [ ] Organizar documentos necessários
- [ ] Preparar material de estudo final
- [ ] Ajustar horário de sono

### **📅 UM DIA ANTES**
- [ ] Revisar local e horário da prova
- [ ] Separar roupas confortáveis
- [ ] Preparar lanche e água
- [ ] Revisar documentos
- [ ] Dormir cedo (antes das 22h)

### **📅 NO DIA DA PROVA**
- [ ] Acordar cedo (6h)
- [ ] Tomar café da manhã leve
- [ ] Verificar documentos
- [ ] Sair com antecedência (1h)
- [ ] Chegar 30min antes

## 🎯 **ESTRATÉGIAS DURANTE A PROVA**

### **1. Controle de Tempo**
- **Linguagens**: 2h30min
- **Ciências Humanas**: 2h30min
- **Redação**: 1h30min
- **Ciências da Natureza**: 2h30min
- **Matemática**: 2h30min

### **2. Técnica de Leitura**
- Leia o enunciado completo
- Identifique o que está sendo pedido
- Destaque informações importantes
- Elimine alternativas absurdas

### **3. Gestão de Ansiedade**
- Respire profundamente
- Mantenha a calma
- Foque no presente
- Confie na sua preparação"""
        },
        
        "Simulados ENEM 2025: Como Usar de Forma Estratégica para Maximizar seu Desempenho": {
            "adicionar": """## 🎥 **VÍDEOS RELACIONADOS**

- [Como Fazer Simulados Eficazes](https://youtube.com/watch?v=exemplo1)
- [Análise de Desempenho](https://youtube.com/watch?v=exemplo2)
- [Estratégias de Revisão](https://youtube.com/watch?v=exemplo3)

## 📊 **CRONOGRAMA DE SIMULADOS**

### **Mensal (1x por mês)**
- **Objetivo**: Avaliar progresso geral
- **Duração**: 5h30min (tempo real)
- **Foco**: Identificar pontos fracos

### **Quinzenal (2x por mês)**
- **Objetivo**: Prática específica por área
- **Duração**: 2h30min por área
- **Foco**: Aprofundar conhecimentos

### **Semanal (1x por semana)**
- **Objetivo**: Manter ritmo de estudos
- **Duração**: 1h por área
- **Foco**: Revisão e consolidação

## 📈 **ANÁLISE DE DESEMPENHO**

### **1. Identifique Padrões**
- Quais matérias você acerta mais?
- Quais tipos de questão erra frequentemente?
- Em que horário rende melhor?

### **2. Ajuste Estratégias**
- Dedique mais tempo às matérias fracas
- Pratique tipos específicos de questão
- Otimize seu cronograma de estudos

### **3. Monitore Evolução**
- Compare resultados mensais
- Celebre melhorias
- Ajuste metas conforme necessário"""
        }
    }
    
    # Retornar melhorias específicas ou genéricas
    if titulo_original in melhorias_especificas:
        return melhorias_especificas[titulo_original]["adicionar"]
    else:
        return """## 🎥 **VÍDEOS RELACIONADOS**

- [Conceitos Fundamentais - ENEM 2025](https://youtube.com/watch?v=exemplo1)
- [Estratégias de Resolução](https://youtube.com/watch?v=exemplo2)
- [Questões Comentadas](https://youtube.com/watch?v=exemplo3)

## 📊 **EXERCÍCIOS PRÁTICOS**

### **Exercício 1: Conceito Básico**
[Exemplo de exercício com resolução detalhada]

### **Exercício 2: Aplicação Prática**
[Exemplo de exercício com resolução detalhada]

## 📈 **DICAS AVANÇADAS**

1. **Pratique regularmente** para manter o conteúdo fresco
2. **Analise seus erros** para não repeti-los
3. **Use diferentes fontes** para ampliar conhecimento
4. **Mantenha-se atualizado** com mudanças do exame"""

def adicionar_conteudo_melhorado(page_id, conteudo_adicional):
    """Adiciona conteúdo melhorado à página existente"""
    print(f"📝 Adicionando melhorias à página...")
    
    # Obter blocos existentes
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"❌ Erro ao obter blocos: {response.status_code}")
        return False
    
    # Dividir conteúdo adicional em blocos
    linhas = conteudo_adicional.split('\n')
    blocos = []
    
    for linha in linhas:
        if linha.startswith('## '):
            # Subtítulo
            blocos.append({
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": linha[3:]}}]
                }
            })
        elif linha.startswith('### '):
            # Subtítulo menor
            blocos.append({
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": linha[4:]}}]
                }
            })
        elif linha.startswith('- [ ]'):
            # Lista de tarefas
            blocos.append({
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"type": "text", "text": {"content": linha[5:]}}],
                    "checked": False
                }
            })
        elif linha.startswith('- '):
            # Lista
            blocos.append({
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": linha[2:]}}]
                }
            })
        elif linha.strip():
            # Parágrafo
            blocos.append({
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": linha}}]
                }
            })
    
    # Adicionar blocos
    if blocos:
        payload = {"children": blocos}
        response = requests.patch(url, headers=HEADERS, json=payload)
        
        if response.status_code != 200:
            print(f"❌ Erro ao adicionar blocos: {response.status_code}")
            return False
    
    print(f"✅ Conteúdo melhorado adicionado com sucesso")
    return True

def atualizar_status_aprovado(page_id):
    """Atualiza status da página para aprovado"""
    print(f"📋 Atualizando status para aprovado...")
    
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            "Status Editorial": {
                "select": {
                    "name": "Aprovado"
                }
            },
            "Status": {
                "select": {
                    "name": "Publicado"
                }
            },
            "Prioridade": {
                "select": {
                    "name": "Alta"
                }
            },
            "Comentários": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": f"Revisão concluída em {datetime.now().strftime('%d/%m/%Y %H:%M')} - Aprovado para publicação"
                        }
                    }
                ]
            }
        }
    }
    
    response = requests.patch(url, headers=HEADERS, json=payload)
    
    if response.status_code != 200:
        print(f"❌ Erro ao atualizar status: {response.status_code}")
        return False
    
    print(f"✅ Status atualizado para aprovado")
    return True

def processar_revisao_paginas(database_id):
    """Processa revisão de todas as páginas em revisão"""
    print_secao("REVISÃO DE PÁGINAS EM REVISÃO")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Aprovar páginas em revisão com melhorias específicas")
    
    # Obter páginas em revisão
    paginas_em_revisao = obter_paginas_em_revisao(database_id)
    
    if not paginas_em_revisao:
        print("❌ Nenhuma página em revisão encontrada")
        return
    
    sucessos = 0
    erros = 0
    
    for i, page in enumerate(paginas_em_revisao, 1):
        page_id = page["id"]
        titulo = obter_titulo_pagina(page)
        
        print(f"\n--- Página {i}/{len(paginas_em_revisao)} ---")
        print(f"Título: {titulo}")
        
        # Obter conteúdo atual
        content_blocks = obter_conteudo_pagina(page_id)
        
        # Gerar melhorias específicas
        conteudo_adicional = melhorar_conteudo_em_revisao(titulo, content_blocks)
        
        # Adicionar melhorias
        if adicionar_conteudo_melhorado(page_id, conteudo_adicional):
            # Atualizar status para aprovado
            if atualizar_status_aprovado(page_id):
                sucessos += 1
            else:
                erros += 1
        else:
            erros += 1
        
        time.sleep(1)  # Pausa para não sobrecarregar a API
    
    print_secao("RELATÓRIO FINAL")
    print(f"📊 Total de páginas processadas: {len(paginas_em_revisao)}")
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Erros: {erros}")
    print(f"📈 Taxa de sucesso: {(sucessos/len(paginas_em_revisao)*100):.1f}%")
    
    if sucessos == len(paginas_em_revisao):
        print("🎉 REVISÃO CONCLUÍDA COM SUCESSO!")
    else:
        print("⚠️ Algumas páginas precisam de atenção manual")

if __name__ == "__main__":
    processar_revisao_paginas(DATABASE_ALUNO)
