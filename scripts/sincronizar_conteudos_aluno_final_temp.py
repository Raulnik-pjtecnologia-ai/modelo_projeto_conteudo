#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Sincronização Final dos Conteúdos do Editorial Aluno
Aplica correções e sincroniza com Notion
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

def buscar_paginas_conteudos():
    """Busca as 4 páginas dos novos conteúdos"""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    
    # Buscar todas as páginas primeiro
    payload = {}
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        all_pages = response.json().get("results", [])
        # Filtrar apenas as 4 páginas dos novos conteúdos
        target_pages = []
        for page in all_pages:
            props = page.get("properties", {})
            title_prop = props.get("Name", {})
            titulo = ""
            if title_prop.get("title"):
                titulo = "".join([t.get("plain_text", "") for t in title_prop["title"]])
            
            if any(keyword in titulo for keyword in ["Simulados ENEM 2025", "Ansiedade no ENEM 2025", "O Dia da Prova ENEM 2025", "Técnicas de Memorização ENEM 2025"]):
                target_pages.append(page)
        
        return target_pages
    else:
        print(f"Erro ao buscar páginas: {response.status_code}")
        return []

def atualizar_propriedades_pagina(page_id, titulo):
    """Atualiza propriedades da página"""
    print(f"\n📄 Atualizando: {titulo}")
    
    # Propriedades corretas para Editorial Aluno
    propriedades = {
        "Status editorial": {"status": {"name": "Publicado"}},
        "Tipo": {"select": {"name": "Artigo"}},
        "Nível de profundidade": {"multi_select": [{"name": "Intermediário"}]},
        "Tags": {"multi_select": [{"name": "ENEM2025"}]},
        "Função ": {"multi_select": [{"name": "Pedagógica"}]}
    }
    
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"properties": propriedades}
    
    try:
        response = requests.patch(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print("   ✅ Propriedades atualizadas com sucesso!")
            return True
        else:
            print(f"   ❌ Erro: {response.status_code}")
            print(f"   Resposta: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
        return False

def verificar_conteudo_pagina(page_id, titulo):
    """Verifica se a página tem conteúdo adequado"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            blocks = response.json().get("results", [])
            
            # Contar blocos de conteúdo
            blocos_conteudo = 0
            for block in blocks:
                block_type = block.get("type")
                if block_type in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item"]:
                    blocos_conteudo += 1
            
            print(f"   📊 Blocos de conteúdo: {blocos_conteudo}")
            
            if blocos_conteudo >= 10:
                print("   ✅ Conteúdo adequado")
                return True
            else:
                print("   ⚠️ Conteúdo insuficiente")
                return False
        else:
            print(f"   ❌ Erro ao verificar conteúdo: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
        return False

def main():
    print("="*60)
    print("SINCRONIZACAO FINAL - EDITORIAL ALUNO PRÉ-ENEM")
    print("="*60)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Buscar páginas
    print_secao("Buscando Páginas dos Conteúdos")
    paginas = buscar_paginas_conteudos()
    
    if not paginas:
        print("❌ Nenhuma página encontrada!")
        return
    
    print(f"✅ Encontradas {len(paginas)} páginas")
    
    # Processar cada página
    print_secao("Processando Páginas")
    
    sucessos = 0
    falhas = 0
    
    for page in paginas:
        props = page.get("properties", {})
        
        # Título
        title_prop = props.get("Name", {})
        titulo = ""
        if title_prop.get("title"):
            titulo = "".join([t.get("plain_text", "") for t in title_prop["title"]])
        
        page_id = page["id"]
        
        # Atualizar propriedades
        if atualizar_propriedades_pagina(page_id, titulo):
            # Verificar conteúdo
            if verificar_conteudo_pagina(page_id, titulo):
                sucessos += 1
            else:
                falhas += 1
        else:
            falhas += 1
    
    # Relatório final
    print_secao("Relatório Final")
    
    print(f"\n📊 RESULTADOS:")
    print(f"   Total processado: {len(paginas)}")
    print(f"   Sucessos: {sucessos}")
    print(f"   Falhas: {falhas}")
    
    if sucessos == len(paginas):
        print("\n🎉 TODOS OS CONTEÚDOS SINCRONIZADOS COM SUCESSO!")
        print("   ✅ Propriedades atualizadas")
        print("   ✅ Conteúdo verificado")
        print("   ✅ Status: Publicado")
    else:
        print(f"\n⚠️ {falhas} conteúdos precisam de atenção")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()

