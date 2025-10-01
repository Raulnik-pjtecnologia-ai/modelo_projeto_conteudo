#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Sincronização Direta dos Conteúdos do Editorial Aluno
Usa IDs conhecidos das páginas
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

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def print_secao(titulo):
    print("\n" + "="*60)
    print(titulo.upper())
    print("="*60)

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
    print("SINCRONIZACAO DIRETA - EDITORIAL ALUNO PRÉ-ENEM")
    print("="*60)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # IDs conhecidos das páginas
    paginas = [
        {
            "id": "27e5113a-91a3-81d3-bdff-dede52c7c12e",
            "titulo": "Simulados ENEM 2025: Como Usar de Forma Estratégica"
        },
        {
            "id": "27e5113a-91a3-81a4-b631-fb86080feb20", 
            "titulo": "Ansiedade no ENEM 2025: Guia Completo para Controlar"
        },
        {
            "id": "27f5113a-91a3-81af-9a7a-f60ed50b5c32",
            "titulo": "O Dia da Prova ENEM 2025: Checklist Completo"
        },
        {
            "id": "27f5113a-91a3-817b-b018-f997ace59629",
            "titulo": "Técnicas de Memorização ENEM 2025: Aprenda Mais Rápido"
        }
    ]
    
    print_secao("Processando Páginas")
    
    sucessos = 0
    falhas = 0
    
    for pagina in paginas:
        page_id = pagina["id"]
        titulo = pagina["titulo"]
        
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

