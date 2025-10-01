#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Corrigir Páginas Sem Título
Identifica e corrige páginas que não têm título definido
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

DATABASE_ALUNO = "2695113a91a381ddbfc4fc8e4df72e7f"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def identificar_paginas_sem_titulo():
    """Identificar páginas que não têm título definido"""
    print("🔍 Identificando páginas sem título...")
    
    url = f"https://api.notion.com/v1/databases/{DATABASE_ALUNO}/query"
    
    try:
        response = requests.post(url, headers=headers, json={})
        if response.status_code != 200:
            print(f"❌ Erro ao buscar páginas: {response.status_code}")
            return []
        
        data = response.json()
        pages = data.get("results", [])
        
        paginas_sem_titulo = []
        
        for i, page in enumerate(pages, 1):
            # Tentar extrair título de diferentes formas
            properties = page.get("properties", {})
            
            # Verificar propriedade "Título"
            titulo_prop = properties.get("Título", {})
            titulo = ""
            
            if titulo_prop.get("type") == "title":
                title_array = titulo_prop.get("title", [])
                if title_array and len(title_array) > 0:
                    titulo = title_array[0].get("text", {}).get("content", "")
            
            # Se não encontrou título, tentar outras propriedades
            if not titulo:
                for prop_name in ["Name", "Nome", "Titulo", "Title"]:
                    if prop_name in properties:
                        prop = properties[prop_name]
                        if prop.get("type") == "title":
                            title_array = prop.get("title", [])
                            if title_array and len(title_array) > 0:
                                titulo = title_array[0].get("text", {}).get("content", "")
                                break
            
            # Se ainda não tem título, adicionar à lista
            if not titulo or titulo.strip() == "":
                paginas_sem_titulo.append({
                    "page": page,
                    "index": i,
                    "page_id": page["id"]
                })
                print(f"   📄 Página {i} sem título: {page['id']}")
        
        print(f"✅ Encontradas {len(paginas_sem_titulo)} páginas sem título")
        return paginas_sem_titulo
        
    except Exception as e:
        print(f"❌ Erro ao identificar páginas: {str(e)}")
        return []

def corrigir_paginas_sem_titulo(paginas_sem_titulo):
    """Corrigir páginas que não têm título"""
    print(f"\n🔧 Corrigindo {len(paginas_sem_titulo)} páginas sem título...")
    
    correcoes_aplicadas = 0
    
    for i, item in enumerate(paginas_sem_titulo, 1):
        page = item["page"]
        page_id = item["page_id"]
        index = item["index"]
        
        print(f"\n[{i}/{len(paginas_sem_titulo)}] Corrigindo página {index}...")
        
        # Definir título baseado no conteúdo ou propriedades disponíveis
        titulo_sugerido = f"Conteúdo ENEM {index}"
        
        # Tentar extrair informações do conteúdo para criar um título melhor
        try:
            # Verificar se há propriedades que possam indicar o tipo de conteúdo
            properties = page.get("properties", {})
            
            # Verificar se há alguma propriedade de texto que possa ser usada como título
            for prop_name, prop_data in properties.items():
                if prop_data.get("type") == "rich_text":
                    rich_text = prop_data.get("rich_text", [])
                    if rich_text and len(rich_text) > 0:
                        content = rich_text[0].get("text", {}).get("content", "")
                        if content and len(content) > 10:  # Se tem conteúdo significativo
                            # Usar as primeiras palavras como título
                            words = content.split()[:5]
                            titulo_sugerido = " ".join(words)
                            if len(titulo_sugerido) > 50:
                                titulo_sugerido = titulo_sugerido[:47] + "..."
                            break
        except Exception as e:
            print(f"   ⚠️ Erro ao analisar conteúdo: {str(e)}")
        
        # Preparar atualizações
        properties_to_update = {
            "Título": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": titulo_sugerido
                        }
                    }
                ]
            },
            "Público Alvo": {
                "multi_select": [
                    {"name": "Estudantes ENEM"},
                    {"name": "Pré-vestibulandos"}
                ]
            },
            "Tags Tema": {
                "multi_select": [
                    {"name": "ENEM"},
                    {"name": "Estudos"},
                    {"name": "Preparação"}
                ]
            },
            "Função Alvo": {
                "multi_select": [
                    {"name": "Pedagógica"},
                    {"name": "Estratégica"}
                ]
            },
            "Status Editorial": {
                "select": {"name": "Publicado"}
            }
        }
        
        try:
            update_url = f"https://api.notion.com/v1/pages/{page_id}"
            update_data = {"properties": properties_to_update}
            
            update_response = requests.patch(update_url, headers=headers, json=update_data)
            
            if update_response.status_code == 200:
                print(f"   ✅ Página corrigida com título: '{titulo_sugerido}'")
                correcoes_aplicadas += 1
            else:
                print(f"   ❌ Erro ao atualizar: {update_response.status_code}")
                print(f"   📝 Resposta: {update_response.text[:200]}...")
        except Exception as e:
            print(f"   ❌ Erro: {str(e)}")
    
    print(f"\n📊 RESUMO: {correcoes_aplicadas}/{len(paginas_sem_titulo)} páginas corrigidas")
    return correcoes_aplicadas

def verificar_conformidade_final():
    """Verificação final de conformidade"""
    print("\n📊 Verificação final de conformidade...")
    
    url = f"https://api.notion.com/v1/databases/{DATABASE_ALUNO}/query"
    
    try:
        response = requests.post(url, headers=headers, json={})
        if response.status_code != 200:
            print(f"❌ Erro ao verificar conformidade: {response.status_code}")
            return False
        
        data = response.json()
        pages = data.get("results", [])
        
        total_pages = len(pages)
        pages_conformes = 0
        problemas_restantes = []
        
        for page in pages:
            # Extrair título
            properties = page.get("properties", {})
            titulo_prop = properties.get("Título", {})
            page_title = "Sem título"
            
            if titulo_prop.get("type") == "title":
                title_array = titulo_prop.get("title", [])
                if title_array and len(title_array) > 0:
                    page_title = title_array[0].get("text", {}).get("content", "Sem título")
            
            problemas_pagina = []
            
            # Verificar Público Alvo
            publico_alvo = properties.get("Público Alvo", {})
            if publico_alvo.get("type") != "multi_select" or not publico_alvo.get("multi_select"):
                problemas_pagina.append("Público Alvo")
            
            # Verificar Tags Tema
            tags_tema = properties.get("Tags Tema", {})
            if tags_tema.get("type") != "multi_select" or not tags_tema.get("multi_select"):
                problemas_pagina.append("Tags Tema")
            
            # Verificar Função Alvo
            funcao_alvo = properties.get("Função Alvo", {})
            if funcao_alvo.get("type") != "multi_select" or not funcao_alvo.get("multi_select"):
                problemas_pagina.append("Função Alvo")
            
            # Verificar Status Editorial
            status_editorial = properties.get("Status Editorial", {})
            if status_editorial.get("type") != "select" or not status_editorial.get("select"):
                problemas_pagina.append("Status Editorial")
            
            if not problemas_pagina:
                pages_conformes += 1
            else:
                problemas_restantes.append({
                    "titulo": page_title[:50],
                    "problemas": problemas_pagina
                })
        
        conformidade = (pages_conformes / total_pages) * 100 if total_pages > 0 else 0
        
        print(f"📊 BIBLIOTECA EDITORIAL ALUNO - CONFORMIDADE FINAL:")
        print(f"   Total de páginas: {total_pages}")
        print(f"   Páginas conformes: {pages_conformes}")
        print(f"   Conformidade: {conformidade:.1f}%")
        
        if problemas_restantes:
            print(f"\n⚠️ PROBLEMAS RESTANTES ({len(problemas_restantes)} páginas):")
            for problema in problemas_restantes:
                print(f"   • {problema['titulo']}: {', '.join(problema['problemas'])}")
        else:
            print(f"\n🎉 PERFEITO! Todas as páginas estão conformes!")
        
        return conformidade >= 95.0
        
    except Exception as e:
        print(f"❌ Erro ao verificar conformidade: {str(e)}")
        return False

def main():
    print("="*80)
    print("CORREÇÃO DE PÁGINAS SEM TÍTULO")
    print("="*80)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Etapa 1: Identificar páginas sem título
    paginas_sem_titulo = identificar_paginas_sem_titulo()
    
    if not paginas_sem_titulo:
        print("✅ Nenhuma página sem título encontrada!")
    else:
        # Etapa 2: Corrigir páginas sem título
        correcoes = corrigir_paginas_sem_titulo(paginas_sem_titulo)
        
        if correcoes > 0:
            print(f"✅ {correcoes} páginas corrigidas com sucesso!")
        else:
            print("❌ Nenhuma página foi corrigida")
    
    # Etapa 3: Verificação final
    if verificar_conformidade_final():
        print("\n🎉 SUCESSO TOTAL: Conformidade atingiu 95% ou mais!")
    else:
        print("\n⚠️ Conformidade ainda pode ser melhorada")
    
    print("\n" + "="*80)
    print("CORREÇÃO CONCLUÍDA")
    print("="*80)

if __name__ == "__main__":
    main()
