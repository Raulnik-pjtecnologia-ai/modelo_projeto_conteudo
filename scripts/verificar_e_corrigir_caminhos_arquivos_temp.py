#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Verificar e Corrigir Caminhos de Arquivos no Notion
Identifica referências a arquivos que foram movidos e atualiza
"""

import os
import sys
import requests
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
if not NOTION_TOKEN:
    print("ERRO: Configure NOTION_TOKEN como variável de ambiente")
    sys.exit(1)

DATABASE_ID = "2695113a-91a3-81dd-bfc4-fc8e4df72e7f"

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
    print_secao("Buscando todas as paginas")
    
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
            print(f"Erro ao buscar: {response.status_code}")
            break
    
    print(f"Total de paginas encontradas: {len(all_pages)}")
    return all_pages

def obter_conteudo_pagina(page_id):
    """Obtém o conteúdo completo de uma página"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("results", [])
        return []
    except:
        return []

def verificar_caminho_arquivo(blocks):
    """Verifica se há referências a caminhos de arquivo incorretos"""
    caminhos_incorretos = []
    
    for block in blocks:
        block_type = block.get("type")
        
        if block_type == "paragraph":
            text_content = ""
            rich_texts = block.get("paragraph", {}).get("rich_text", [])
            for text in rich_texts:
                text_content += text.get("plain_text", "")
            
            # Verificar se menciona caminho antigo
            if "01_ideias_e_rascunhos/artigo_" in text_content:
                caminhos_incorretos.append({
                    "block_id": block["id"],
                    "texto": text_content,
                    "tipo": "caminho_antigo"
                })
    
    return caminhos_incorretos

def corrigir_caminho_arquivo(page_id, titulo_pagina):
    """Atualiza o caminho do arquivo na página"""
    
    # Mapear arquivo correto baseado no título
    mapeamento = {
        "Simulados ENEM 2025": "2_conteudo/04_publicado/artigo_simulados_enem_2025_estrategico.md",
        "Ansiedade no ENEM 2025": "2_conteudo/04_publicado/artigo_ansiedade_enem_2025_gestao_emocional.md",
        "O Dia da Prova ENEM 2025": "2_conteudo/04_publicado/artigo_dia_prova_enem_2025_checklist.md",
        "Técnicas de Memorização": "2_conteudo/04_publicado/artigo_tecnicas_memorizacao_enem_2025.md"
    }
    
    novo_caminho = None
    for chave, caminho in mapeamento.items():
        if chave in titulo_pagina:
            novo_caminho = caminho
            break
    
    if not novo_caminho:
        return False
    
    # Atualizar primeira linha da página
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    
    try:
        # Primeiro, obter blocos existentes
        response_get = requests.get(url, headers=headers)
        if response_get.status_code != 200:
            return False
        
        blocks = response_get.json().get("results", [])
        
        # Encontrar e deletar blocos com caminho antigo
        for block in blocks[:3]:  # Primeiros 3 blocos (info de sincronização)
            block_id = block["id"]
            requests.delete(
                f"https://api.notion.com/v1/blocks/{block_id}",
                headers=headers
            )
        
        # Adicionar blocos atualizados
        payload = {
            "children": [
                {
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": f"📢 Conteúdo publicado em {datetime.now().strftime('%d/%m/%Y')} | Status: APROVADO"
                                }
                            }
                        ],
                        "icon": {
                            "emoji": "✅"
                        },
                        "color": "green_background"
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": f"📁 Arquivo local: {novo_caminho}"
                                },
                                "annotations": {
                                    "code": True
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        response_add = requests.patch(url, headers=headers, json=payload)
        return response_add.status_code == 200
        
    except Exception as e:
        print(f"Erro ao corrigir: {e}")
        return False

def main():
    print("="*60)
    print("VERIFICACAO E CORRECAO DE CAMINHOS DE ARQUIVO")
    print("="*60)
    print(f"Database: {DATABASE_ID}")
    
    # 1. Buscar todas as páginas
    paginas = buscar_todas_paginas()
    
    if not paginas:
        print("\nNenhuma pagina encontrada")
        return
    
    # 2. Verificar e corrigir páginas publicadas
    print_secao("Verificando e Corrigindo Paginas")
    
    paginas_corrigidas = []
    paginas_com_erro = []
    
    for page in paginas:
        props = page.get("properties", {})
        
        # Obter título
        title_prop = props.get("Title", {})
        titulo = ""
        if title_prop.get("title"):
            titulo = "".join([t.get("plain_text", "") for t in title_prop["title"]])
        
        # Verificar se é uma das 4 páginas publicadas
        page_id = page["id"]
        
        paginas_interesse = [
            "Simulados ENEM 2025",
            "Ansiedade no ENEM 2025",
            "O Dia da Prova",
            "Técnicas de Memorização"
        ]
        
        if any(interesse in titulo for interesse in paginas_interesse):
            print(f"\n Processando: {titulo}")
            print(f"   Page ID: {page_id}")
            
            # Obter conteúdo
            blocks = obter_conteudo_pagina(page_id)
            problemas = verificar_caminho_arquivo(blocks)
            
            if problemas:
                print(f"   Caminho antigo detectado")
                
                # Corrigir
                sucesso = corrigir_caminho_arquivo(page_id, titulo)
                
                if sucesso:
                    print(f"   Caminho corrigido!")
                    paginas_corrigidas.append(titulo)
                else:
                    print(f"   Erro ao corrigir")
                    paginas_com_erro.append(titulo)
            else:
                print(f"   Caminho OK")
    
    # Relatório final
    print_secao("Relatorio Final")
    
    print(f"\nPaginas verificadas: {len(paginas)}")
    print(f"Paginas corrigidas: {len(paginas_corrigidas)}")
    print(f"Paginas com erro: {len(paginas_com_erro)}")
    
    if paginas_corrigidas:
        print("\n Corrigidas:")
        for titulo in paginas_corrigidas:
            print(f"    {titulo}")
    
    if paginas_com_erro:
        print("\n Com erro:")
        for titulo in paginas_com_erro:
            print(f"    {titulo}")
    
    if not paginas_corrigidas and not paginas_com_erro:
        print("\n Todas as paginas ja estavam corretas!")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()

