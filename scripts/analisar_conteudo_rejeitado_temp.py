#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Análise Detalhada do Conteúdo Rejeitado
Identifica problemas específicos e sugere melhorias
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

def obter_paginas_por_status(database_id, status_editorial):
    """Obtém páginas por status editorial"""
    print(f"🔍 Buscando páginas com status: {status_editorial}")
    
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    payload = {
        "filter": {
            "property": "Status Editorial",
            "select": {
                "equals": status_editorial
            }
        }
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    
    if response.status_code != 200:
        print(f"❌ Erro ao buscar páginas: {response.status_code}")
        return []
    
    data = response.json()
    pages = data.get("results", [])
    
    print(f"✅ Encontradas {len(pages)} páginas com status '{status_editorial}'")
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

def analisar_problemas_conteudo(page_id, page_title, content_blocks):
    """Analisa problemas específicos do conteúdo"""
    print(f"🔍 Analisando: {page_title}")
    
    problemas = {
        "estrutura": [],
        "conteudo": [],
        "linguagem": [],
        "elementos_visuais": [],
        "conformidade": []
    }
    
    # Converter blocos para análise
    texto_completo = ""
    tem_imagens = False
    tem_videos = False
    tem_titulos = False
    tem_listas = False
    tem_paragrafos = False
    
    for block in content_blocks:
        block_type = block.get("type", "")
        
        if block_type == "paragraph":
            tem_paragrafos = True
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
    
    # 1. ANÁLISE DE ESTRUTURA
    if not tem_titulos:
        problemas["estrutura"].append("❌ Falta de títulos e subtítulos")
    if not tem_listas:
        problemas["estrutura"].append("❌ Ausência de listas organizadas")
    if not tem_paragrafos:
        problemas["estrutura"].append("❌ Poucos parágrafos de conteúdo")
    
    # 2. ANÁLISE DE CONTEÚDO
    if len(texto_completo) < 200:
        problemas["conteudo"].append("❌ Conteúdo muito curto (menos de 200 caracteres)")
    elif len(texto_completo) < 500:
        problemas["conteudo"].append("⚠️ Conteúdo curto (menos de 500 caracteres)")
    
    # Verificar palavras-chave educacionais
    palavras_educacionais = ["ENEM", "estudante", "aprendizagem", "educação", "conhecimento", "prática", "exercício"]
    palavras_encontradas = [palavra for palavra in palavras_educacionais if palavra.lower() in texto_completo.lower()]
    
    if len(palavras_encontradas) < 2:
        problemas["conteudo"].append("❌ Poucas palavras-chave educacionais")
    
    # 3. ANÁLISE DE LINGUAGEM
    if "ENEM" not in texto_completo:
        problemas["linguagem"].append("❌ Não menciona ENEM especificamente")
    if "2025" not in texto_completo:
        problemas["linguagem"].append("❌ Não menciona o ano 2025")
    
    # Verificar linguagem técnica excessiva
    palavras_tecnicas = ["metodologia", "paradigma", "implementação", "otimização"]
    tecnicas_encontradas = [palavra for palavra in palavras_tecnicas if palavra.lower() in texto_completo.lower()]
    
    if len(tecnicas_encontradas) > 2:
        problemas["linguagem"].append("⚠️ Linguagem muito técnica para ensino médio")
    
    # 4. ANÁLISE DE ELEMENTOS VISUAIS
    if not tem_imagens and not tem_videos:
        problemas["elementos_visuais"].append("❌ Ausência total de elementos visuais")
    elif not tem_imagens:
        problemas["elementos_visuais"].append("⚠️ Falta de imagens/gráficos")
    elif not tem_videos:
        problemas["elementos_visuais"].append("⚠️ Falta de vídeos")
    
    # 5. ANÁLISE DE CONFORMIDADE
    if "ENEM" not in texto_completo or "2025" not in texto_completo:
        problemas["conformidade"].append("❌ Não atende padrões de conformidade ENEM 2025")
    
    return problemas

def gerar_sugestoes_melhorias(problemas):
    """Gera sugestões específicas de melhorias"""
    sugestoes = []
    
    for categoria, lista_problemas in problemas.items():
        if lista_problemas:
            sugestoes.append(f"\n📋 {categoria.upper()}:")
            for problema in lista_problemas:
                sugestoes.append(f"   {problema}")
    
    return sugestoes

def processar_analise_completa(database_id):
    """Processa análise completa de todos os conteúdos rejeitados"""
    print_secao("ANÁLISE DETALHADA DE CONTEÚDO REJEITADO")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Identificar problemas específicos e sugerir melhorias")
    
    # Obter páginas rejeitadas
    paginas_rejeitadas = obter_paginas_por_status(database_id, "Rejeitado")
    paginas_em_revisao = obter_paginas_por_status(database_id, "Em Revisão")
    
    relatorio = {
        "rejeitadas": [],
        "em_revisao": [],
        "resumo": {
            "total_rejeitadas": len(paginas_rejeitadas),
            "total_em_revisao": len(paginas_em_revisao),
            "problemas_comuns": {}
        }
    }
    
    # Analisar páginas rejeitadas
    print_secao("PÁGINAS REJEITADAS")
    for i, page in enumerate(paginas_rejeitadas, 1):
        page_id = page["id"]
        page_title = obter_titulo_pagina(page)
        
        print(f"\n--- Página {i}/{len(paginas_rejeitadas)} ---")
        print(f"Título: {page_title}")
        
        content_blocks = obter_conteudo_pagina(page_id)
        problemas = analisar_problemas_conteudo(page_id, page_title, content_blocks)
        
        sugestoes = gerar_sugestoes_melhorias(problemas)
        for sugestao in sugestoes:
            print(sugestao)
        
        relatorio["rejeitadas"].append({
            "titulo": page_title,
            "id": page_id,
            "problemas": problemas,
            "sugestoes": sugestoes
        })
        
        time.sleep(0.5)
    
    # Analisar páginas em revisão
    print_secao("PÁGINAS EM REVISÃO")
    for i, page in enumerate(paginas_em_revisao, 1):
        page_id = page["id"]
        page_title = obter_titulo_pagina(page)
        
        print(f"\n--- Página {i}/{len(paginas_em_revisao)} ---")
        print(f"Título: {page_title}")
        
        content_blocks = obter_conteudo_pagina(page_id)
        problemas = analisar_problemas_conteudo(page_id, page_title, content_blocks)
        
        sugestoes = gerar_sugestoes_melhorias(problemas)
        for sugestao in sugestoes:
            print(sugestao)
        
        relatorio["em_revisao"].append({
            "titulo": page_title,
            "id": page_id,
            "problemas": problemas,
            "sugestoes": sugestoes
        })
        
        time.sleep(0.5)
    
    # Salvar relatório
    with open("docs/relatorio_analise_conteudo_rejeitado.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print_secao("RELATÓRIO FINAL")
    print(f"📊 Páginas rejeitadas analisadas: {len(paginas_rejeitadas)}")
    print(f"📊 Páginas em revisão analisadas: {len(paginas_em_revisao)}")
    print(f"📄 Relatório salvo em: docs/relatorio_analise_conteudo_rejeitado.json")
    print("✅ Análise concluída com sucesso!")

if __name__ == "__main__":
    processar_analise_completa(DATABASE_ALUNO)
