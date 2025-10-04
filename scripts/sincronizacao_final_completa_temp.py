#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Sincronização Final Completa
Sincroniza todas as melhorias finais com Notion
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
    print(f"🔍 Buscando todas as páginas para sincronização final...")
    
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

def sincronizar_propriedades_finais(page_id, titulo):
    """Sincroniza propriedades finais com Notion"""
    print(f"📝 Sincronizando propriedades finais: {titulo}")
    
    try:
        url = f"https://api.notion.com/v1/pages/{page_id}"
        payload = {
            "properties": {
                "Status Editorial": {
                    "select": {"name": "Aprovado"}
                },
                "Status": {
                    "select": {"name": "Publicado"}
                },
                "Prioridade": {
                    "select": {"name": "Alta"}
                },
                "Comentários": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": f"Sincronização final completa em {datetime.now().strftime('%d/%m/%Y %H:%M')} - Editorial de Aluno PRÉ-ENEM 2025 otimizado e aprovado"
                            }
                        }
                    ]
                }
            }
        }
        
        response = requests.patch(url, headers=HEADERS, json=payload)
        
        if response.status_code != 200:
            print(f"❌ Erro ao sincronizar: {response.status_code}")
            return False
        
        print(f"   ✅ Propriedades sincronizadas com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao sincronizar página '{titulo}' ({page_id}): {e}")
        return False

def processar_sincronizacao_final(database_id):
    """Processa sincronização final de todas as páginas"""
    print_secao("SINCRONIZAÇÃO FINAL COMPLETA")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Sincronizar todas as melhorias finais com Notion")
    
    # Obter todas as páginas
    pages = obter_todas_paginas(database_id)
    
    if not pages:
        print("❌ Nenhuma página encontrada")
        return
    
    sucessos = 0
    erros = 0
    
    for i, page in enumerate(pages, 1):
        page_id = page["id"]
        titulo = obter_titulo_pagina(page)
        
        print(f"\n--- Página {i}/{len(pages)} ---")
        print(f"Título: {titulo}")
        
        if sincronizar_propriedades_finais(page_id, titulo):
            sucessos += 1
        else:
            erros += 1
        
        time.sleep(0.5)  # Pausa para não sobrecarregar a API
    
    print_secao("RELATÓRIO FINAL DA SINCRONIZAÇÃO")
    print(f"📊 Total de páginas processadas: {len(pages)}")
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Erros: {erros}")
    print(f"📈 Taxa de sucesso: {(sucessos/len(pages)*100):.1f}%")
    
    if sucessos == len(pages):
        print("🎉 SINCRONIZAÇÃO FINAL CONCLUÍDA COM SUCESSO!")
    else:
        print("⚠️ Algumas páginas precisam de atenção manual")

if __name__ == "__main__":
    processar_sincronizacao_final(DATABASE_ALUNO)
