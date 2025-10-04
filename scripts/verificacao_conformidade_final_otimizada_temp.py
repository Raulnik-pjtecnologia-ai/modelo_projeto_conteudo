#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Verificação de Conformidade Final Otimizada
Verifica conformidade de todas as páginas após as otimizações implementadas
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

def obter_conteudo_pagina(page_id):
    """Obtém o conteúdo da página"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        return []
    
    return response.json().get("results", [])

def avaliar_conformidade_otimizada(titulo, conteudo_blocks):
    """Avalia conformidade com critérios otimizados"""
    scores = {
        "regra_1_enriquecimento_mcp": 0,
        "regra_2_boilerplate": 0,
        "regra_3_curadoria": 0,
        "regra_4_apresentacao": 0,
        "regra_5_manutencao": 0,
    }
    
    # Regra 1: Enriquecimento MCP (Gráficos, Notícias, Vídeos)
    has_chart = any("mdn.alipayobjects.com" in str(block) for block in conteudo_blocks)
    has_news = any("📰" in str(block) for block in conteudo_blocks)
    has_video_section = any("🎥" in str(block) for block in conteudo_blocks)
    has_exercises = any("📈" in str(block) for block in conteudo_blocks)
    
    if has_chart:
        scores["regra_1_enriquecimento_mcp"] += 5
    if has_news:
        scores["regra_1_enriquecimento_mcp"] += 5
    if has_video_section:
        scores["regra_1_enriquecimento_mcp"] += 5
    if has_exercises:
        scores["regra_1_enriquecimento_mcp"] += 5
    
    # Regra 2: Boilerplate (Estrutura de Títulos, Seções Padrão)
    has_intro = any("introdução" in str(block).lower() for block in conteudo_blocks)
    has_conclusion = any("conclusão" in str(block).lower() for block in conteudo_blocks)
    has_structure = any(block.get("type", "").startswith("heading") for block in conteudo_blocks)
    
    if has_intro:
        scores["regra_2_boilerplate"] += 7
    if has_conclusion:
        scores["regra_2_boilerplate"] += 7
    if has_structure:
        scores["regra_2_boilerplate"] += 6
    
    # Regra 3: Curadoria (Qualidade do Conteúdo, Relevância, Profundidade)
    content_length = len(str(conteudo_blocks))
    has_enem_2025 = "2025" in titulo or "2025" in str(conteudo_blocks)
    has_educational_keywords = any(keyword in str(conteudo_blocks).lower() for keyword in ["estudo", "aprendizado", "conceito", "exercício"])
    
    if content_length > 5000:
        scores["regra_3_curadoria"] += 7
    if has_enem_2025:
        scores["regra_3_curadoria"] += 7
    if has_educational_keywords:
        scores["regra_3_curadoria"] += 6
    
    # Regra 4: Apresentação (Formatação, Escaneabilidade, Elementos Visuais)
    has_lists = any(block.get("type", "") in ["bulleted_list_item", "numbered_list_item"] for block in conteudo_blocks)
    has_headings = any(block.get("type", "").startswith("heading") for block in conteudo_blocks)
    has_paragraphs = any(block.get("type", "") == "paragraph" for block in conteudo_blocks)
    
    if has_lists:
        scores["regra_4_apresentacao"] += 7
    if has_headings:
        scores["regra_4_apresentacao"] += 7
    if has_paragraphs:
        scores["regra_4_apresentacao"] += 6
    
    # Regra 5: Manutenção (Atualização, Linguagem Acessível, Correção)
    has_2025 = "2025" in titulo
    has_clear_language = len(titulo.split()) > 3  # Títulos mais descritivos
    has_student_focus = any(keyword in titulo.lower() for keyword in ["aluno", "estudante", "enem", "pré-vestibular"])
    
    if has_2025:
        scores["regra_5_manutencao"] += 7
    if has_clear_language:
        scores["regra_5_manutencao"] += 7
    if has_student_focus:
        scores["regra_5_manutencao"] += 6
    
    return scores

def processar_verificacao_conformidade(database_id):
    """Processa verificação de conformidade de todas as páginas"""
    print_secao("VERIFICAÇÃO DE CONFORMIDADE FINAL OTIMIZADA")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Verificar conformidade após otimizações implementadas")
    
    # Obter todas as páginas
    pages = obter_todas_paginas(database_id)
    
    if not pages:
        print("❌ Nenhuma página encontrada")
        return
    
    resultados = []
    total_score = 0
    min_score = 101
    max_score = -1
    
    for i, page in enumerate(pages, 1):
        page_id = page["id"]
        titulo = obter_titulo_pagina(page)
        
        print(f"\n--- Página {i}/{len(pages)} ---")
        print(f"Título: {titulo}")
        
        # Obter conteúdo da página
        conteudo_blocks = obter_conteudo_pagina(page_id)
        
        # Avaliar conformidade
        scores = avaliar_conformidade_otimizada(titulo, conteudo_blocks)
        score_total = sum(scores.values())
        
        print(f"📊 Enriquecimento MCP: {scores['regra_1_enriquecimento_mcp']}/20")
        print(f"📋 Boilerplate: {scores['regra_2_boilerplate']}/20")
        print(f"📝 Curadoria: {scores['regra_3_curadoria']}/20")
        print(f"🎨 Apresentação: {scores['regra_4_apresentacao']}/20")
        print(f"🔧 Manutenção: {scores['regra_5_manutencao']}/20")
        print(f"🎯 TOTAL: {score_total}/100")
        
        resultados.append({
            "titulo": titulo,
            "id": page_id,
            "scores": scores,
            "total": score_total
        })
        
        total_score += score_total
        if score_total < min_score:
            min_score = score_total
        if score_total > max_score:
            max_score = score_total
        
        time.sleep(0.5)  # Pausa para não sobrecarregar a API
    
    # Análise dos resultados
    print_secao("ANÁLISE DOS RESULTADOS")
    
    # Contar páginas por faixa de pontuação
    excelentes = len([r for r in resultados if r["total"] >= 90])
    boas = len([r for r in resultados if 80 <= r["total"] < 90])
    regulares = len([r for r in resultados if 70 <= r["total"] < 80])
    ruins = len([r for r in resultados if r["total"] < 70])
    
    print(f"📊 Total de páginas analisadas: {len(pages)}")
    print(f"🏆 Excelentes (≥90%): {excelentes} ({excelentes/len(pages)*100:.1f}%)")
    print(f"✅ Boas (80-89%): {boas} ({boas/len(pages)*100:.1f}%)")
    print(f"⚠️ Regulares (70-79%): {regulares} ({regulares/len(pages)*100:.1f}%)")
    print(f"❌ Ruins (<70%): {ruins} ({ruins/len(pages)*100:.1f}%)")
    print(f"📈 Pontuação média: {total_score/len(pages):.1f}/100")
    print(f"📊 Maior pontuação: {max_score}/100")
    print(f"📊 Menor pontuação: {min_score}/100")
    
    # Análise por regras
    print_secao("ANÁLISE POR REGRAS")
    
    for regra in ["regra_1_enriquecimento_mcp", "regra_2_boilerplate", "regra_3_curadoria", "regra_4_apresentacao", "regra_5_manutencao"]:
        regra_nome = regra.replace("regra_", "").replace("_", " ").title()
        media_regra = sum(r["scores"][regra] for r in resultados) / len(resultados)
        print(f"📋 {regra_nome}: {media_regra:.1f}/20")
    
    # Salvar relatório
    relatorio = {
        "data_verificacao": datetime.now().strftime('%d/%m/%Y %H:%M'),
        "total_paginas": len(pages),
        "resultados": resultados,
        "estatisticas": {
            "pontuacao_media": total_score/len(pages),
            "maior_pontuacao": max_score,
            "menor_pontuacao": min_score,
            "excelentes": excelentes,
            "boas": boas,
            "regulares": regulares,
            "ruins": ruins
        }
    }
    
    with open("docs/relatorio_conformidade_final_otimizada.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=4)
    
    print_secao("RELATÓRIO FINAL")
    print(f"📄 Relatório salvo em: docs/relatorio_conformidade_final_otimizada.json")
    
    if excelentes + boas >= len(pages) * 0.8:
        print("🎉 CONFORMIDADE EXCELENTE ALCANÇADA!")
    elif excelentes + boas >= len(pages) * 0.6:
        print("✅ CONFORMIDADE BOA ALCANÇADA!")
    else:
        print("⚠️ CONFORMIDADE AINDA PRECISA MELHORAR!")

if __name__ == "__main__":
    processar_verificacao_conformidade(DATABASE_ALUNO)
