#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Adicionar Exercícios Práticos
Adiciona seção de exercícios práticos em todas as páginas da biblioteca
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

def obter_todas_paginas(database_id):
    """Obtém todas as páginas da biblioteca"""
    print(f"🔍 Buscando todas as páginas da biblioteca...")
    
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    all_pages = []
    start_cursor = None
    
    while True:
        payload = {
            "page_size": 100
        }
        if start_cursor:
            payload["start_cursor"] = start_cursor
            
        response = requests.post(url, headers=HEADERS, json=payload)
        
        if response.status_code != 200:
            print(f"❌ Erro ao buscar páginas: {response.status_code}")
            return []
            
        data = response.json()
        all_pages.extend(data.get("results", []))
        
        if not data.get("has_more", False):
            break
            
        start_cursor = data.get("next_cursor")
    
    print(f"✅ Encontradas {len(all_pages)} páginas")
    return all_pages

def obter_titulo_pagina(page):
    """Obtém o título da página"""
    properties = page.get("properties", {})
    title_prop = properties.get("Title") or properties.get("title")
    
    if title_prop and title_prop.get("title"):
        return title_prop["title"][0]["text"]["content"]
    return "Sem título"

def verificar_se_ja_tem_exercicios(page_id):
    """Verifica se a página já tem seção de exercícios"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        return False
    
    blocks = response.json().get("results", [])
    
    for block in blocks:
        if block.get("type") == "heading_2":
            rich_text = block.get("heading_2", {}).get("rich_text", [])
            if rich_text and "📈" in rich_text[0].get("text", {}).get("content", ""):
                return True
    
    return False

def gerar_exercicios_especificos(titulo):
    """Gera exercícios específicos baseados no título"""
    
    exercicios_por_tema = {
        "matemática": [
            {
                "titulo": "Exercício 1: Cálculo de Área",
                "enunciado": "Calcule a área de um retângulo com base 8 cm e altura 6 cm.",
                "resolucao": "Área = base × altura = 8 × 6 = 48 cm²"
            },
            {
                "titulo": "Exercício 2: Regra de Três",
                "enunciado": "Se 3 operários fazem um trabalho em 12 dias, em quantos dias 4 operários farão o mesmo trabalho?",
                "resolucao": "3 operários → 12 dias\n4 operários → x dias\n3 × 12 = 4 × x\nx = 9 dias"
            }
        ],
        "física": [
            {
                "titulo": "Exercício 1: Velocidade Média",
                "enunciado": "Um carro percorre 300 km em 4 horas. Qual sua velocidade média?",
                "resolucao": "v = Δs/Δt = 300/4 = 75 km/h"
            },
            {
                "titulo": "Exercício 2: Energia Cinética",
                "enunciado": "Calcule a energia cinética de um objeto de 2 kg a 10 m/s.",
                "resolucao": "Ec = mv²/2 = 2 × 10²/2 = 100 J"
            }
        ],
        "química": [
            {
                "titulo": "Exercício 1: Massa Molar",
                "enunciado": "Calcule a massa molar do H2SO4 (H=1, S=32, O=16).",
                "resolucao": "M = 2×1 + 1×32 + 4×16 = 2 + 32 + 64 = 98 g/mol"
            },
            {
                "titulo": "Exercício 2: Concentração",
                "enunciado": "Qual a concentração de uma solução com 20 g de soluto em 500 mL de solvente?",
                "resolucao": "C = m/V = 20/0,5 = 40 g/L"
            }
        ],
        "biologia": [
            {
                "titulo": "Exercício 1: Genética",
                "enunciado": "Um casal heterozigoto (Aa) tem filhos. Qual a probabilidade de ter um filho homozigoto recessivo (aa)?",
                "resolucao": "Aa × Aa → 1/4 AA, 1/2 Aa, 1/4 aa\nProbabilidade de aa = 1/4 = 25%"
            },
            {
                "titulo": "Exercício 2: Ecologia",
                "enunciado": "Em uma cadeia alimentar: planta → gafanhoto → pássaro → cobra. Qual o nível trófico do pássaro?",
                "resolucao": "Planta (produtor) → Gafanhoto (1º consumidor) → Pássaro (2º consumidor) → Cobra (3º consumidor)"
            }
        ],
        "história": [
            {
                "titulo": "Exercício 1: Brasil República",
                "enunciado": "Qual foi o principal objetivo da Revolução de 1930?",
                "resolucao": "A Revolução de 1930 teve como objetivo principal derrubar a República Velha e implementar reformas políticas e sociais."
            },
            {
                "titulo": "Exercício 2: Era Vargas",
                "enunciado": "Cite duas principais características do Estado Novo (1937-1945).",
                "resolucao": "1) Centralização do poder nas mãos de Vargas\n2) Censura à imprensa e repressão política"
            }
        ],
        "geografia": [
            {
                "titulo": "Exercício 1: Clima",
                "enunciado": "Qual o tipo climático predominante na região Nordeste do Brasil?",
                "resolucao": "O clima semiárido é predominante no interior do Nordeste, caracterizado por chuvas escassas e irregulares."
            },
            {
                "titulo": "Exercício 2: População",
                "enunciado": "O que é densidade demográfica?",
                "resolucao": "Densidade demográfica é a relação entre o número de habitantes e a área do território (hab/km²)."
            }
        ],
        "sociologia": [
            {
                "titulo": "Exercício 1: Movimentos Sociais",
                "enunciado": "Qual a principal característica dos movimentos sociais?",
                "resolucao": "A principal característica é a ação coletiva organizada para transformar a sociedade e reivindicar direitos."
            },
            {
                "titulo": "Exercício 2: Desigualdade",
                "enunciado": "Cite dois tipos de desigualdade social.",
                "resolucao": "1) Desigualdade econômica (renda e riqueza)\n2) Desigualdade de oportunidades (educação e saúde)"
            }
        ],
        "português": [
            {
                "titulo": "Exercício 1: Interpretação",
                "enunciado": "Leia o texto e identifique a ideia principal: 'A educação é fundamental para o desenvolvimento social.'",
                "resolucao": "A ideia principal é que a educação é essencial para o progresso da sociedade."
            },
            {
                "titulo": "Exercício 2: Gramática",
                "enunciado": "Classifique a palavra 'rapidamente' na frase: 'Ele correu rapidamente.'",
                "resolucao": "'Rapidamente' é um advérbio de modo, modificando o verbo 'correu'."
            }
        ]
    }
    
    # Buscar exercícios específicos baseados no título
    titulo_lower = titulo.lower()
    for tema, exercicios in exercicios_por_tema.items():
        if tema in titulo_lower:
            return exercicios
    
    # Exercícios genéricos se não encontrar tema específico
    return [
        {
            "titulo": "Exercício 1: Aplicação Prática",
            "enunciado": "Aplique os conceitos estudados em uma situação prática do seu cotidiano.",
            "resolucao": "Analise como os conceitos se relacionam com situações reais e pratique sua aplicação."
        },
        {
            "titulo": "Exercício 2: Síntese",
            "enunciado": "Faça um resumo dos principais pontos estudados neste conteúdo.",
            "resolucao": "Organize as informações de forma clara e objetiva, destacando os conceitos mais importantes."
        }
    ]

def adicionar_secao_exercicios(page_id, titulo, exercicios):
    """Adiciona seção de exercícios práticos à página"""
    print(f"📝 Adicionando seção de exercícios: {titulo}")
    
    blocos_exercicios = [
        {
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📈 EXERCÍCIOS PRÁTICOS"}}]
            }
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "Pratique os conceitos estudados com os exercícios abaixo:"}}]
            }
        }
    ]
    
    # Adicionar cada exercício
    for exercicio in exercicios:
        blocos_exercicios.extend([
            {
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": exercicio["titulo"]}}]
                }
            },
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": f"**Enunciado:** {exercicio['enunciado']}"}}]
                }
            },
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": f"**Resolução:** {exercicio['resolucao']}"}}]
                }
            }
        ])
    
    # Adicionar dicas sobre exercícios
    blocos_exercicios.extend([
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "💡 **Dica:** Tente resolver os exercícios antes de ver a resolução."}}]
            }
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "📚 **Complemento:** Crie seus próprios exercícios baseados nos conceitos estudados."}}]
            }
        }
    ])
    
    # Adicionar blocos à página
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    payload = {"children": blocos_exercicios}
    
    response = requests.patch(url, headers=HEADERS, json=payload)
    
    if response.status_code != 200:
        print(f"❌ Erro ao adicionar exercícios: {response.status_code}")
        return False
    
    print(f"✅ Seção de exercícios adicionada com sucesso")
    return True

def processar_adicao_exercicios(database_id):
    """Processa adição de exercícios em todas as páginas"""
    print_secao("ADIÇÃO DE EXERCÍCIOS PRÁTICOS")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Implementar seção de exercícios práticos em todas as páginas")
    
    # Obter todas as páginas
    pages = obter_todas_paginas(database_id)
    
    if not pages:
        print("❌ Nenhuma página encontrada")
        return
    
    sucessos = 0
    erros = 0
    ja_tinham_exercicios = 0
    
    for i, page in enumerate(pages, 1):
        page_id = page["id"]
        titulo = obter_titulo_pagina(page)
        
        print(f"\n--- Página {i}/{len(pages)} ---")
        print(f"Título: {titulo}")
        
        # Verificar se já tem exercícios
        if verificar_se_ja_tem_exercicios(page_id):
            print(f"⏭️ Página já possui seção de exercícios")
            ja_tinham_exercicios += 1
            continue
        
        # Gerar exercícios específicos
        exercicios = gerar_exercicios_especificos(titulo)
        
        # Adicionar seção de exercícios
        if adicionar_secao_exercicios(page_id, titulo, exercicios):
            sucessos += 1
        else:
            erros += 1
        
        time.sleep(1)  # Pausa para não sobrecarregar a API
    
    print_secao("RELATÓRIO FINAL")
    print(f"📊 Total de páginas processadas: {len(pages)}")
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Erros: {erros}")
    print(f"⏭️ Já tinham exercícios: {ja_tinham_exercicios}")
    print(f"📈 Taxa de sucesso: {(sucessos/(len(pages)-ja_tinham_exercicios)*100):.1f}%")
    
    if sucessos > 0:
        print("🎉 EXERCÍCIOS ADICIONADOS COM SUCESSO!")
    else:
        print("⚠️ Nenhum exercício foi adicionado")

if __name__ == "__main__":
    processar_adicao_exercicios(DATABASE_ALUNO)
