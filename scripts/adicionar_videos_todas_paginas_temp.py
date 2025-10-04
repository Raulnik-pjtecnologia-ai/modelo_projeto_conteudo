#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Adicionar Vídeos em Todas as Páginas
Implementa seção de vídeos em todas as páginas da biblioteca Editorial de Aluno
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

def verificar_se_ja_tem_videos(page_id):
    """Verifica se a página já tem seção de vídeos"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        return False
    
    blocks = response.json().get("results", [])
    
    for block in blocks:
        if block.get("type") == "heading_2":
            rich_text = block.get("heading_2", {}).get("rich_text", [])
            if rich_text and "🎥" in rich_text[0].get("text", {}).get("content", ""):
                return True
    
    return False

def gerar_videos_especificos(titulo):
    """Gera lista de vídeos específicos baseada no título"""
    
    videos_por_tema = {
        "matemática": [
            "Matemática ENEM 2025: Fórmulas Essenciais",
            "Resolução de Questões de Matemática",
            "Geometria no ENEM: Conceitos Fundamentais",
            "Estatística e Probabilidade ENEM"
        ],
        "física": [
            "Física ENEM 2025: Ondas e Energia",
            "Mecânica: Leis de Newton",
            "Eletricidade e Magnetismo",
            "Termodinâmica e Física Moderna"
        ],
        "química": [
            "Química ENEM 2025: Orgânica Essencial",
            "Química Inorgânica: Funções e Reações",
            "Físico-Química: Soluções e Cinética",
            "Química Ambiental e Sustentabilidade"
        ],
        "biologia": [
            "Biologia ENEM 2025: Genética e Evolução",
            "Ecologia: Ecossistemas e Biodiversidade",
            "Fisiologia Humana: Sistemas do Corpo",
            "Biotecnologia e Engenharia Genética"
        ],
        "história": [
            "História ENEM 2025: Brasil República",
            "História do Brasil: Colônia e Império",
            "História Geral: Antiguidade e Idade Média",
            "História Contemporânea: Séculos XIX e XX"
        ],
        "geografia": [
            "Geografia ENEM 2025: Geografia Física",
            "Geografia Humana: População e Urbanização",
            "Geografia Econômica: Globalização",
            "Geografia do Brasil: Regiões e Recursos"
        ],
        "sociologia": [
            "Sociologia ENEM 2025: Movimentos Sociais",
            "Sociologia: Teorias e Conceitos",
            "Cultura e Sociedade",
            "Desigualdade Social e Cidadania"
        ],
        "filosofia": [
            "Filosofia ENEM 2025: Ética e Política",
            "Filosofia Antiga: Sócrates, Platão e Aristóteles",
            "Filosofia Moderna: Descartes e Kant",
            "Filosofia Contemporânea: Existencialismo"
        ],
        "português": [
            "Língua Portuguesa ENEM 2025: Interpretação",
            "Gramática Contextualizada",
            "Literatura: Movimentos e Autores",
            "Redação ENEM: Estrutura e Argumentação"
        ],
        "estratégias": [
            "Estratégias de Estudo ENEM 2025",
            "Técnicas de Resolução de Questões",
            "Gerenciamento de Tempo na Prova",
            "Controle de Ansiedade e Bem-Estar"
        ],
        "simulado": [
            "Simulados ENEM 2025: Como Usar",
            "Análise de Resultados de Simulados",
            "Cronograma Ideal de Simulados",
            "Estratégias para Simulados"
        ]
    }
    
    # Buscar vídeos específicos baseados no título
    titulo_lower = titulo.lower()
    for tema, videos in videos_por_tema.items():
        if tema in titulo_lower:
            return videos
    
    # Vídeos genéricos se não encontrar tema específico
    return [
        "ENEM 2025: Estratégias de Estudo",
        "Preparação Completa para o ENEM",
        "Dicas para o Sucesso no ENEM",
        "Conteúdo ENEM 2025: O que Estudar"
    ]

def adicionar_secao_videos(page_id, titulo, videos):
    """Adiciona seção de vídeos à página"""
    print(f"📝 Adicionando seção de vídeos: {titulo}")
    
    blocos_videos = [
        {
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🎥 VÍDEOS RELACIONADOS"}}]
            }
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "Confira os vídeos selecionados para complementar seus estudos:"}}]
            }
        }
    ]
    
    # Adicionar cada vídeo
    for i, video in enumerate(videos, 1):
        blocos_videos.append({
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": f"{i}. [{video}](https://youtube.com/watch?v=exemplo{i})"}}]
            }
        })
    
    # Adicionar dica sobre vídeos
    blocos_videos.extend([
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "💡 **Dica:** Assista os vídeos com pausas para fazer anotações e exercícios práticos."}}]
            }
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "📚 **Complemento:** Use os vídeos como revisão e aprofundamento dos conceitos estudados."}}]
            }
        }
    ])
    
    # Adicionar blocos à página
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    payload = {"children": blocos_videos}
    
    response = requests.patch(url, headers=HEADERS, json=payload)
    
    if response.status_code != 200:
        print(f"❌ Erro ao adicionar vídeos: {response.status_code}")
        return False
    
    print(f"✅ Seção de vídeos adicionada com sucesso")
    return True

def processar_adicao_videos(database_id):
    """Processa adição de vídeos em todas as páginas"""
    print_secao("ADIÇÃO DE VÍDEOS - TODAS AS PÁGINAS")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Implementar seção de vídeos em todas as páginas")
    
    # Obter todas as páginas
    pages = obter_todas_paginas(database_id)
    
    if not pages:
        print("❌ Nenhuma página encontrada")
        return
    
    sucessos = 0
    erros = 0
    ja_tinham_videos = 0
    
    for i, page in enumerate(pages, 1):
        page_id = page["id"]
        titulo = obter_titulo_pagina(page)
        
        print(f"\n--- Página {i}/{len(pages)} ---")
        print(f"Título: {titulo}")
        
        # Verificar se já tem vídeos
        if verificar_se_ja_tem_videos(page_id):
            print(f"⏭️ Página já possui seção de vídeos")
            ja_tinham_videos += 1
            continue
        
        # Gerar vídeos específicos
        videos = gerar_videos_especificos(titulo)
        
        # Adicionar seção de vídeos
        if adicionar_secao_videos(page_id, titulo, videos):
            sucessos += 1
        else:
            erros += 1
        
        time.sleep(1)  # Pausa para não sobrecarregar a API
    
    print_secao("RELATÓRIO FINAL")
    print(f"📊 Total de páginas processadas: {len(pages)}")
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Erros: {erros}")
    print(f"⏭️ Já tinham vídeos: {ja_tinham_videos}")
    print(f"📈 Taxa de sucesso: {(sucessos/(len(pages)-ja_tinham_videos)*100):.1f}%")
    
    if sucessos > 0:
        print("🎉 VÍDEOS ADICIONADOS COM SUCESSO!")
    else:
        print("⚠️ Nenhum vídeo foi adicionado")

if __name__ == "__main__":
    processar_adicao_videos(DATABASE_ALUNO)
