#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Curadoria Melhorada Final
Aplica curadoria em todos os conteúdos após melhorias
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
    print(f"🔍 Buscando todas as páginas para curadoria final...")
    
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
    
    print(f"✅ Encontradas {len(all_pages)} páginas para curadoria final")
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

def avaliar_qualidade_melhorada(page_id, page_title, content_blocks):
    """Avalia qualidade do conteúdo com critérios melhorados"""
    print(f"📝 Avaliando: {page_title}")
    
    # Critérios de avaliação melhorados (cada um vale 20 pontos, total 100)
    pontuacao = 0
    criterios = {
        "estrutura": 0,
        "conteudo": 0,
        "linguagem": 0,
        "elementos_visuais": 0,
        "conformidade": 0
    }
    
    # Converter blocos para texto para análise
    texto_completo = ""
    tem_imagens = False
    tem_videos = False
    tem_titulos = False
    tem_listas = False
    tem_graficos = False
    tem_noticias = False
    
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
    
    # 1. ESTRUTURA (20 pontos) - Melhorado
    if tem_titulos and tem_listas:
        criterios["estrutura"] = 20
    elif tem_titulos or tem_listas:
        criterios["estrutura"] = 15
    else:
        criterios["estrutura"] = 5
    
    # 2. CONTEÚDO (20 pontos) - Melhorado
    if len(texto_completo) > 2000:
        criterios["conteudo"] = 20
    elif len(texto_completo) > 1000:
        criterios["conteudo"] = 15
    elif len(texto_completo) > 500:
        criterios["conteudo"] = 10
    else:
        criterios["conteudo"] = 5
    
    # Verificar palavras-chave educacionais melhoradas
    palavras_educacionais = ["ENEM", "estudante", "aprendizagem", "educação", "conhecimento", "prática", "exercício", "2025", "estratégia", "técnica"]
    palavras_encontradas = [palavra for palavra in palavras_educacionais if palavra.lower() in texto_completo.lower()]
    
    if len(palavras_encontradas) >= 5:
        criterios["conteudo"] += 5
    elif len(palavras_encontradas) >= 3:
        criterios["conteudo"] += 3
    
    # 3. LINGUAGEM (20 pontos) - Melhorado
    if "ENEM" in texto_completo and "2025" in texto_completo:
        criterios["linguagem"] = 20
    elif "ENEM" in texto_completo:
        criterios["linguagem"] = 15
    else:
        criterios["linguagem"] = 5
    
    # Verificar linguagem adequada para ensino médio
    palavras_tecnicas = ["metodologia", "paradigma", "implementação", "otimização", "algoritmo"]
    tecnicas_encontradas = [palavra for palavra in palavras_tecnicas if palavra.lower() in texto_completo.lower()]
    
    if len(tecnicas_encontradas) <= 2:
        criterios["linguagem"] += 5
    
    # 4. ELEMENTOS VISUAIS (20 pontos) - Melhorado
    elementos_visuais = 0
    if tem_imagens:
        elementos_visuais += 5
    if tem_videos:
        elementos_visuais += 5
    if tem_graficos:
        elementos_visuais += 5
    if tem_noticias:
        elementos_visuais += 5
    
    criterios["elementos_visuais"] = elementos_visuais
    
    # 5. CONFORMIDADE (20 pontos) - Melhorado
    if "ENEM" in texto_completo and "2025" in texto_completo and "estudante" in texto_completo:
        criterios["conformidade"] = 20
    elif "ENEM" in texto_completo and "2025" in texto_completo:
        criterios["conformidade"] = 15
    elif "ENEM" in texto_completo:
        criterios["conformidade"] = 10
    else:
        criterios["conformidade"] = 5
    
    # Calcular pontuação total
    pontuacao = sum(criterios.values())
    
    print(f"   📊 Estrutura: {criterios['estrutura']}/20")
    print(f"   📝 Conteúdo: {criterios['conteudo']}/20")
    print(f"   🗣️ Linguagem: {criterios['linguagem']}/20")
    print(f"   🎨 Visuais: {criterios['elementos_visuais']}/20")
    print(f"   ✅ Conformidade: {criterios['conformidade']}/20")
    print(f"   🎯 TOTAL: {pontuacao}/100")
    
    return pontuacao, criterios

def aplicar_curadoria_melhorada(page_id, page_title, pontuacao):
    """Aplica curadoria melhorada na página baseada na pontuação"""
    print(f"📋 Aplicando curadoria melhorada: {page_title}")
    
    # Determinar status baseado na pontuação melhorada
    if pontuacao >= 85:
        status_editorial = "Aprovado"
        status = "Publicado"
        prioridade = "Alta"
        print(f"   ✅ APROVADO - Pontuação: {pontuacao}/100")
    elif pontuacao >= 70:
        status_editorial = "Em Revisão"
        status = "Rascunho"
        prioridade = "Média"
        print(f"   ⚠️ EM REVISÃO - Pontuação: {pontuacao}/100")
    else:
        status_editorial = "Rejeitado"
        status = "Rascunho"
        prioridade = "Baixa"
        print(f"   ❌ REJEITADO - Pontuação: {pontuacao}/100")
    
    # Propriedades para atualizar
    properties = {
        "Status Editorial": {
            "select": {
                "name": status_editorial
            }
        },
        "Status": {
            "select": {
                "name": status
            }
        },
        "Prioridade": {
            "select": {
                "name": prioridade
            }
        },
        "Comentários": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": f"Curadoria melhorada aplicada em {datetime.now().strftime('%d/%m/%Y %H:%M')} - Pontuação: {pontuacao}/100 - Critérios atualizados"
                    }
                }
            ]
        }
    }
    
    # Atualizar página
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"properties": properties}
    
    response = requests.patch(url, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        print(f"   ✅ Curadoria melhorada aplicada com sucesso")
        return True
    else:
        print(f"   ❌ Erro ao aplicar curadoria: {response.status_code}")
        return False

def processar_curadoria_melhorada(database_id):
    """Processa curadoria melhorada de toda a biblioteca Editorial de Aluno"""
    print_secao("CUradoria MELHORADA - EDITORIAL DE ALUNO")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Aplicar curadoria melhorada com critérios atualizados")
    
    # Obter todas as páginas
    pages = obter_todas_paginas_biblioteca(database_id)
    
    if not pages:
        print("❌ Nenhuma página encontrada")
        return
    
    # Processar cada página
    aprovados = 0
    em_revisao = 0
    rejeitados = 0
    erros = 0
    pontuacoes = []
    
    for i, page in enumerate(pages, 1):
        page_id = page["id"]
        page_title = obter_titulo_pagina(page)
        
        print(f"\n--- Página {i}/{len(pages)} ---")
        print(f"ID: {page_id}")
        print(f"Título: {page_title}")
        
        # Obter conteúdo da página
        content_blocks = obter_conteudo_pagina(page_id)
        
        # Avaliar qualidade com critérios melhorados
        pontuacao, criterios = avaliar_qualidade_melhorada(page_id, page_title, content_blocks)
        pontuacoes.append(pontuacao)
        
        # Aplicar curadoria melhorada
        if aplicar_curadoria_melhorada(page_id, page_title, pontuacao):
            if pontuacao >= 85:
                aprovados += 1
            elif pontuacao >= 70:
                em_revisao += 1
            else:
                rejeitados += 1
        else:
            erros += 1
        
        # Pequena pausa para não sobrecarregar a API
        time.sleep(0.5)
    
    # Relatório final
    print_secao("RELATÓRIO FINAL DA CUradoria MELHORADA")
    print(f"📊 Total de páginas processadas: {len(pages)}")
    print(f"✅ Aprovados (≥85%): {aprovados}")
    print(f"⚠️ Em Revisão (70-84%): {em_revisao}")
    print(f"❌ Rejeitados (<70%): {rejeitados}")
    print(f"🔧 Erros: {erros}")
    
    if pontuacoes:
        media_pontuacao = sum(pontuacoes) / len(pontuacoes)
        print(f"📈 Pontuação média: {media_pontuacao:.1f}/100")
        print(f"📊 Maior pontuação: {max(pontuacoes)}/100")
        print(f"📊 Menor pontuação: {min(pontuacoes)}/100")
    
    taxa_aprovacao = (aprovados / len(pages)) * 100
    print(f"🎯 Taxa de aprovação: {taxa_aprovacao:.1f}%")
    
    if taxa_aprovacao >= 80:
        print("🎉 CUradoria MELHORADA CONCLUÍDA COM SUCESSO!")
    else:
        print("⚠️ Algumas páginas precisam de melhorias adicionais")

if __name__ == "__main__":
    processar_curadoria_melhorada(DATABASE_ALUNO)
