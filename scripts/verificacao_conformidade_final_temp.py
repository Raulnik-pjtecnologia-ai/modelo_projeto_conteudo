#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Verificação Final de Conformidade
Verifica conformidade com as 5 regras estabelecidas
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

def obter_todas_paginas_biblioteca(database_id):
    """Obtém todas as páginas da biblioteca Editorial de Aluno"""
    print(f"🔍 Buscando todas as páginas para verificação final...")
    
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
    
    print(f"✅ Encontradas {len(all_pages)} páginas para verificação")
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
    
    data = response.json()
    return data.get("results", [])

def verificar_conformidade_5_regras(page_id, page_title, content_blocks):
    """Verifica conformidade com as 5 regras estabelecidas"""
    print(f"🔍 Verificando: {page_title}")
    
    # Critérios das 5 regras
    regras = {
        "regra_1_enriquecimento_mcp": 0,  # 20 pontos
        "regra_2_boilerplate": 0,         # 20 pontos
        "regra_3_curadoria": 0,           # 20 pontos
        "regra_4_apresentacao": 0,        # 20 pontos
        "regra_5_manutencao": 0           # 20 pontos
    }
    
    # Converter blocos para análise
    texto_completo = ""
    tem_imagens = False
    tem_videos = False
    tem_graficos = False
    tem_noticias = False
    tem_titulos = False
    tem_listas = False
    tem_exercicios = False
    
    for block in content_blocks:
        block_type = block.get("type", "")
        
        if block_type == "paragraph":
            if block.get("paragraph", {}).get("rich_text"):
                texto = "".join([text.get("text", {}).get("content", "") for text in block["paragraph"]["rich_text"]])
                texto_completo += texto + " "
        
        elif block_type in ["heading_1", "heading_2", "heading_3"]:
            tem_titulos = True
            if block.get(block_type, {}).get("rich_text"):
                texto = "".join([text.get("text", {}).get("content", "") for text in block[block_type]["rich_text"]])
                texto_completo += texto + " "
        
        elif block_type == "bulleted_list_item":
            tem_listas = True
            if block.get("bulleted_list_item", {}).get("rich_text"):
                texto = "".join([text.get("text", {}).get("content", "") for text in block["bulleted_list_item"]["rich_text"]])
                texto_completo += texto + " "
        
        elif block_type == "image":
            tem_imagens = True
        
        elif block_type in ["video", "embed"]:
            tem_videos = True
    
    # Verificar elementos específicos no texto
    if "gráfico" in texto_completo.lower() or "chart" in texto_completo.lower():
        tem_graficos = True
    if "notícia" in texto_completo.lower() or "fonte:" in texto_completo.lower():
        tem_noticias = True
    if "exercício" in texto_completo.lower() or "questão" in texto_completo.lower():
        tem_exercicios = True
    
    # REGRA 1: ENRIQUECIMENTO MCP (20 pontos)
    elementos_mcp = 0
    if tem_imagens:
        elementos_mcp += 5
    if tem_videos:
        elementos_mcp += 5
    if tem_graficos:
        elementos_mcp += 5
    if tem_noticias:
        elementos_mcp += 5
    regras["regra_1_enriquecimento_mcp"] = elementos_mcp
    
    # REGRA 2: BOILERPLATE (20 pontos)
    elementos_boilerplate = 0
    if "ENEM" in texto_completo and "2025" in texto_completo:
        elementos_boilerplate += 10
    if tem_titulos and tem_listas:
        elementos_boilerplate += 10
    regras["regra_2_boilerplate"] = elementos_boilerplate
    
    # REGRA 3: CUradoria (20 pontos)
    elementos_curadoria = 0
    if len(texto_completo) > 2000:
        elementos_curadoria += 10
    if tem_exercicios:
        elementos_curadoria += 10
    regras["regra_3_curadoria"] = elementos_curadoria
    
    # REGRA 4: APRESENTAÇÃO (20 pontos)
    elementos_apresentacao = 0
    if tem_titulos:
        elementos_apresentacao += 10
    if tem_listas:
        elementos_apresentacao += 10
    regras["regra_4_apresentacao"] = elementos_apresentacao
    
    # REGRA 5: MANUTENÇÃO (20 pontos)
    elementos_manutencao = 0
    if "estudante" in texto_completo.lower() or "aluno" in texto_completo.lower():
        elementos_manutencao += 10
    if "estratégia" in texto_completo.lower() or "técnica" in texto_completo.lower():
        elementos_manutencao += 10
    regras["regra_5_manutencao"] = elementos_manutencao
    
    # Calcular pontuação total
    pontuacao_total = sum(regras.values())
    
    print(f"   📊 Enriquecimento MCP: {regras['regra_1_enriquecimento_mcp']}/20")
    print(f"   📋 Boilerplate: {regras['regra_2_boilerplate']}/20")
    print(f"   🎯 Curadoria: {regras['regra_3_curadoria']}/20")
    print(f"   🎨 Apresentação: {regras['regra_4_apresentacao']}/20")
    print(f"   🔧 Manutenção: {regras['regra_5_manutencao']}/20")
    print(f"   🎯 TOTAL: {pontuacao_total}/100")
    
    return pontuacao_total, regras

def processar_verificacao_final(database_id):
    """Processa verificação final de conformidade"""
    print_secao("VERIFICAÇÃO FINAL DE CONFORMIDADE")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Verificar conformidade com as 5 regras estabelecidas")
    
    # Obter todas as páginas
    pages = obter_todas_paginas_biblioteca(database_id)
    
    if not pages:
        print("❌ Nenhuma página encontrada")
        return
    
    # Processar cada página
    conformes = 0
    parcialmente_conformes = 0
    nao_conformes = 0
    pontuacoes = []
    regras_totais = {
        "regra_1_enriquecimento_mcp": 0,
        "regra_2_boilerplate": 0,
        "regra_3_curadoria": 0,
        "regra_4_apresentacao": 0,
        "regra_5_manutencao": 0
    }
    
    for i, page in enumerate(pages, 1):
        page_id = page["id"]
        page_title = obter_titulo_pagina(page)
        
        print(f"\n--- Página {i}/{len(pages)} ---")
        print(f"ID: {page_id}")
        print(f"Título: {page_title}")
        
        # Obter conteúdo da página
        content_blocks = obter_conteudo_pagina(page_id)
        
        # Verificar conformidade
        pontuacao, regras = verificar_conformidade_5_regras(page_id, page_title, content_blocks)
        pontuacoes.append(pontuacao)
        
        # Acumular pontuações das regras
        for regra, valor in regras.items():
            regras_totais[regra] += valor
        
        # Classificar conformidade
        if pontuacao >= 90:
            conformes += 1
        elif pontuacao >= 70:
            parcialmente_conformes += 1
        else:
            nao_conformes += 1
        
        time.sleep(0.5)
    
    # Relatório final
    print_secao("RELATÓRIO FINAL DE CONFORMIDADE")
    print(f"📊 Total de páginas verificadas: {len(pages)}")
    print(f"✅ Conformes (≥90%): {conformes}")
    print(f"⚠️ Parcialmente Conformes (70-89%): {parcialmente_conformes}")
    print(f"❌ Não Conformes (<70%): {nao_conformes}")
    
    if pontuacoes:
        media_pontuacao = sum(pontuacoes) / len(pontuacoes)
        print(f"📈 Pontuação média: {media_pontuacao:.1f}/100")
        print(f"📊 Maior pontuação: {max(pontuacoes)}/100")
        print(f"📊 Menor pontuação: {min(pontuacoes)}/100")
    
    # Análise por regras
    print(f"\n📋 ANÁLISE POR REGRAS:")
    for regra, total in regras_totais.items():
        media_regra = total / len(pages)
        print(f"   {regra}: {media_regra:.1f}/20")
    
    # Taxa de conformidade
    taxa_conformidade = (conformes / len(pages)) * 100
    print(f"🎯 Taxa de conformidade: {taxa_conformidade:.1f}%")
    
    # Salvar relatório
    relatorio = {
        "data_verificacao": datetime.now().strftime('%d/%m/%Y %H:%M'),
        "total_paginas": len(pages),
        "conformes": conformes,
        "parcialmente_conformes": parcialmente_conformes,
        "nao_conformes": nao_conformes,
        "pontuacao_media": media_pontuacao if pontuacoes else 0,
        "taxa_conformidade": taxa_conformidade,
        "analise_regras": {regra: total/len(pages) for regra, total in regras_totais.items()},
        "pontuacoes_individual": pontuacoes
    }
    
    with open("docs/relatorio_conformidade_final_2025.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print(f"📄 Relatório salvo em: docs/relatorio_conformidade_final_2025.json")
    
    if taxa_conformidade >= 80:
        print("🎉 CONFORMIDADE FINAL EXCELENTE!")
    elif taxa_conformidade >= 60:
        print("✅ CONFORMIDADE FINAL BOA!")
    else:
        print("⚠️ CONFORMIDADE FINAL PRECISA MELHORAR!")

if __name__ == "__main__":
    processar_verificacao_final(DATABASE_ALUNO)
