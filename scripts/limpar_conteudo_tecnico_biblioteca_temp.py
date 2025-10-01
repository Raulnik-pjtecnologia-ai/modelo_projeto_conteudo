#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Limpar Informações Técnicas das Páginas
Remove informações não relevantes para o leitor final
"""

import os
import sys
import requests
import re

sys.stdout.reconfigure(encoding='utf-8')

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
if not NOTION_TOKEN:
    print("ERRO: Configure NOTION_TOKEN")
    sys.exit(1)

# Database de Gestão Escolar
DATABASE_ID = "2325113a91a381c09b33f826449a218f"

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
            print(f"Erro: {response.status_code}")
            break
    
    return all_pages

def obter_blocos_pagina(page_id):
    """Obtém blocos de uma página"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("results", [])
        return []
    except:
        return []

def identificar_blocos_tecnicos(blocks):
    """Identifica blocos com informações técnicas desnecessárias"""
    blocos_para_remover = []
    
    padroes_tecnicos = [
        r'Conteudo sincronizado automaticamente',
        r'Arquivo:.*\.md',
        r'caminho/para/',
        r'!\[Capa do Artigo\]',
        r'!\[.*\]\(caminho/',
        r'\*Descrição da imagem de capa:',
        r'Page ID:',
        r'Database ID:',
        r'collection://',
        r'Categoria:.*Preparação ENEM',  # Info técnica de meta
        r'Nivel:.*',  # Info técnica de meta
        r'Funcao:.*',  # Info técnica de meta
        r'Tags:.*ENEM2025',  # Info técnica de meta (quando em formato lista)
    ]
    
    for block in blocks:
        block_type = block.get("type")
        block_id = block["id"]
        
        # Verificar parágrafos
        if block_type == "paragraph":
            texto = ""
            rich_texts = block.get("paragraph", {}).get("rich_text", [])
            for rt in rich_texts:
                texto += rt.get("plain_text", "")
            
            # Verificar se contém padrões técnicos
            for padrao in padroes_tecnicos:
                if re.search(padrao, texto, re.IGNORECASE):
                    blocos_para_remover.append({
                        "id": block_id,
                        "tipo": "paragraph",
                        "texto_preview": texto[:100]
                    })
                    break
        
        # Verificar callouts com info técnica
        elif block_type == "callout":
            texto = ""
            rich_texts = block.get("callout", {}).get("rich_text", [])
            for rt in rich_texts:
                texto += rt.get("plain_text", "")
            
            # Se callout menciona arquivo ou sincronização
            if any(p in texto.lower() for p in ['sincronizado', 'arquivo:', 'caminho', 'page id']):
                blocos_para_remover.append({
                    "id": block_id,
                    "tipo": "callout",
                    "texto_preview": texto[:100]
                })
        
        # Verificar heading_2 com meta-informações
        elif block_type == "heading_2":
            texto = ""
            rich_texts = block.get("heading_2", {}).get("rich_text", [])
            for rt in rich_texts:
                texto += rt.get("plain_text", "")
            
            # Remover "Informações do Conteúdo" (técnico)
            if "Informacoes do Conteudo" in texto or "Informações do Conteúdo" in texto:
                blocos_para_remover.append({
                    "id": block_id,
                    "tipo": "heading_2",
                    "texto_preview": texto
                })
        
        # Verificar listas com info técnica
        elif block_type == "bulleted_list_item":
            texto = ""
            rich_texts = block.get("bulleted_list_item", {}).get("rich_text", [])
            for rt in rich_texts:
                texto += rt.get("plain_text", "")
            
            # Remover itens de lista técnicos
            if any(p in texto for p in ['Categoria:', 'Nivel:', 'Funcao:', 'Tags:', 'Arquivo:']):
                blocos_para_remover.append({
                    "id": block_id,
                    "tipo": "bulleted_list_item",
                    "texto_preview": texto[:80]
                })
    
    return blocos_para_remover

def limpar_blocos_tecnicos(page_id, blocos_para_remover):
    """Remove blocos técnicos da página"""
    
    removidos = 0
    for bloco in blocos_para_remover:
        try:
            response = requests.delete(
                f"https://api.notion.com/v1/blocks/{bloco['id']}",
                headers=headers
            )
            
            if response.status_code == 200:
                removidos += 1
            
        except Exception as e:
            print(f"Erro ao remover bloco: {e}")
    
    return removidos

def main():
    print("="*60)
    print("LIMPEZA DE INFORMACOES TECNICAS - BIBLIOTECA GESTAO")
    print("="*60)
    print(f"Database: {DATABASE_ID}")
    
    # Buscar páginas
    print_secao("Buscando Paginas")
    paginas = buscar_todas_paginas()
    print(f"Total encontrado: {len(paginas)}")
    
    # Processar cada página
    print_secao("Analisando e Limpando Paginas")
    
    total_blocos_removidos = 0
    paginas_processadas = 0
    
    for page in paginas:
        props = page.get("properties", {})
        
        # Título
        title_prop = props.get("Nome", {}) or props.get("Title", {})
        titulo = ""
        if title_prop.get("title"):
            titulo = "".join([t.get("plain_text", "") for t in title_prop["title"]])
        
        page_id = page["id"]
        
        # Obter blocos
        blocos = obter_blocos_pagina(page_id)
        
        if not blocos:
            continue
        
        # Identificar blocos técnicos
        blocos_tecnicos = identificar_blocos_tecnicos(blocos)
        
        if blocos_tecnicos:
            print(f"\n Processando: {titulo}")
            print(f"   Blocos tecnicos encontrados: {len(blocos_tecnicos)}")
            
            # Remover
            removidos = limpar_blocos_tecnicos(page_id, blocos_tecnicos)
            print(f"   Blocos removidos: {removidos}")
            
            total_blocos_removidos += removidos
            paginas_processadas += 1
    
    # Relatório
    print_secao("Relatorio Final")
    print(f"\nPaginas verificadas: {len(paginas)}")
    print(f"Paginas limpas: {paginas_processadas}")
    print(f"Blocos tecnicos removidos: {total_blocos_removidos}")
    
    if total_blocos_removidos > 0:
        print(f"\n {total_blocos_removidos} blocos tecnicos removidos com sucesso!")
        print("\nConteudo agora esta limpo e focado no leitor final.")
    else:
        print("\n Nenhum bloco tecnico encontrado. Conteudo ja estava limpo!")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()

