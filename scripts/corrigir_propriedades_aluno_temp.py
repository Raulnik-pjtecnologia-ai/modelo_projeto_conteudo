#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Corrigir Propriedades da Biblioteca Editorial Aluno
Adiciona propriedades ausentes para conformidade com boilerplate
"""

import os
import sys
import requests
import json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
if not NOTION_TOKEN:
    print("ERRO: Configure NOTION_TOKEN")
    sys.exit(1)

# Database Editorial Alunos PRÉ-ENEM
DATABASE_ID = "2695113a91a381ddbfc4fc8e4df72e7f"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def print_secao(titulo):
    print("\n" + "="*60)
    print(titulo.upper())
    print("="*60)

def buscar_todas_paginas():
    """Busca todas as páginas do database"""
    print("🔍 Buscando todas as páginas...")
    
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    all_pages = []
    has_more = True
    start_cursor = None
    
    while has_more:
        payload = {}
        if start_cursor:
            payload["start_cursor"] = start_cursor
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            all_pages.extend(data.get("results", []))
            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")
        else:
            print(f"❌ Erro: {response.status_code}")
            break
    
    print(f"✅ Total encontrado: {len(all_pages)} páginas")
    return all_pages

def corrigir_propriedades_pagina(page):
    """Corrige propriedades de uma página"""
    props = page.get("properties", {})
    page_id = page["id"]
    
    # Título
    title_prop = props.get("Name", {})
    titulo = ""
    if title_prop.get("title"):
        titulo = "".join([t.get("plain_text", "") for t in title_prop["title"]])
    
    print(f"\n📄 Corrigindo: {titulo[:50]}...")
    
    # Propriedades a serem adicionadas/corrigidas
    propriedades = {}
    
    # Status editorial
    if "Status editorial" not in props:
        propriedades["Status editorial"] = {"status": {"name": "Publicado"}}
        print("   ➕ Adicionando: Status editorial = Publicado")
    
    # Tipo
    if "Tipo" not in props:
        propriedades["Tipo"] = {"select": {"name": "Artigo"}}
        print("   ➕ Adicionando: Tipo = Artigo")
    
    # Nível de profundidade
    if "Nível de profundidade" not in props:
        propriedades["Nível de profundidade"] = {"multi_select": [{"name": "Intermediário"}]}
        print("   ➕ Adicionando: Nível de profundidade = Intermediário")
    
    # Tags
    if "Tags" not in props:
        propriedades["Tags"] = {"multi_select": [{"name": "ENEM2025"}]}
        print("   ➕ Adicionando: Tags = ENEM2025")
    
    # Função (para Editorial Aluno)
    if "Função " not in props:
        propriedades["Função "] = {"multi_select": [{"name": "Pedagógica"}]}
        print("   ➕ Adicionando: Função = Pedagógica")
    
    # Aplicar correções se houver
    if propriedades:
        url = f"https://api.notion.com/v1/pages/{page_id}"
        payload = {"properties": propriedades}
        
        try:
            response = requests.patch(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                print("   ✅ Propriedades corrigidas com sucesso!")
                return True
            else:
                print(f"   ❌ Erro: {response.status_code}")
                print(f"   Resposta: {response.text[:200]}")
                return False
        except Exception as e:
            print(f"   ❌ Erro: {str(e)}")
            return False
    else:
        print("   ✅ Página já está correta")
        return True

def main():
    print("="*60)
    print("CORRECAO DE PROPRIEDADES - EDITORIAL ALUNO PRÉ-ENEM")
    print("="*60)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Buscar todas as páginas
    print_secao("Buscando Páginas")
    paginas = buscar_todas_paginas()
    
    if not paginas:
        print("❌ Nenhuma página encontrada!")
        return
    
    # Processar cada página
    print_secao("Corrigindo Propriedades")
    
    sucessos = 0
    falhas = 0
    
    for i, page in enumerate(paginas, 1):
        print(f"\n[{i}/{len(paginas)}] Processando página...")
        
        if corrigir_propriedades_pagina(page):
            sucessos += 1
        else:
            falhas += 1
    
    # Relatório final
    print_secao("Relatório Final")
    
    print(f"\n📊 RESULTADOS:")
    print(f"   Total processado: {len(paginas)}")
    print(f"   Sucessos: {sucessos}")
    print(f"   Falhas: {falhas}")
    
    if sucessos == len(paginas):
        print("\n🎉 TODAS AS PROPRIEDADES CORRIGIDAS COM SUCESSO!")
        print("   ✅ Status editorial: Publicado")
        print("   ✅ Tipo: Artigo")
        print("   ✅ Nível: Intermediário")
        print("   ✅ Tags: ENEM2025")
        print("   ✅ Função: Pedagógica")
    else:
        print(f"\n⚠️ {falhas} páginas precisam de atenção manual")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()


