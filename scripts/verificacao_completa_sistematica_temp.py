#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Verificação Completa e Sistemática das Bibliotecas
Executa todas as 5 etapas do processo de forma organizada
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

# IDs das bibliotecas
DATABASE_GESTAO = "2325113a91a381c09b33f826449a218f"
DATABASE_ALUNO = "2695113a91a381ddbfc4fc8e4df72e7f"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def print_etapa(numero, titulo):
    print("\n" + "="*80)
    print(f"ETAPA {numero}: {titulo.upper()}")
    print("="*80)

def print_secao(titulo):
    print("\n" + "-"*60)
    print(titulo)
    print("-"*60)

def buscar_propriedades_database(database_id, nome_biblioteca):
    """Busca propriedades de um database"""
    print(f"\n🔍 Analisando propriedades: {nome_biblioteca}")
    
    url = f"https://api.notion.com/v1/databases/{database_id}"
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            properties = data.get("properties", {})
            
            print(f"✅ Propriedades encontradas: {len(properties)}")
            
            propriedades_info = {}
            for prop_name, prop_data in properties.items():
                prop_type = prop_data.get("type", "unknown")
                propriedades_info[prop_name] = prop_type
                print(f"   📋 {prop_name}: {prop_type}")
            
            return propriedades_info
        else:
            print(f"❌ Erro ao buscar propriedades: {response.status_code}")
            return {}
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return {}

def buscar_paginas_database(database_id, nome_biblioteca, limite=50):
    """Busca páginas de um database"""
    print(f"\n🔍 Buscando páginas: {nome_biblioteca}")
    
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    payload = {"page_size": limite}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            pages = data.get("results", [])
            
            print(f"✅ Páginas encontradas: {len(pages)}")
            return pages
        else:
            print(f"❌ Erro ao buscar páginas: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return []

def verificar_propriedades_obrigatorias(propriedades, biblioteca_tipo):
    """Verifica se as propriedades obrigatórias existem"""
    print(f"\n📋 Verificando propriedades obrigatórias para: {biblioteca_tipo}")
    
    if biblioteca_tipo == "Gestão Escolar":
        obrigatorias = {
            "Status editorial": "status",
            "Tipo": "select", 
            "Nível de profundidade": "multi_select",
            "Tags": "multi_select",
            "Função ": "multi_select"
        }
    else:  # Editorial Aluno
        obrigatorias = {
            "Status editorial": "status",
            "Tipo": "select",
            "Nível de profundidade": "multi_select", 
            "Tags": "multi_select",
            "Função ": "multi_select"
        }
    
    problemas = []
    for prop_name, prop_type_esperado in obrigatorias.items():
        if prop_name in propriedades:
            prop_type_atual = propriedades[prop_name]
            if prop_type_atual == prop_type_esperado:
                print(f"   ✅ {prop_name}: {prop_type_atual}")
            else:
                print(f"   ⚠️ {prop_name}: {prop_type_atual} (esperado: {prop_type_esperado})")
                problemas.append(f"{prop_name}: tipo incorreto")
        else:
            print(f"   ❌ {prop_name}: AUSENTE")
            problemas.append(f"{prop_name}: ausente")
    
    return problemas

def analisar_conteudo_paginas(pages, nome_biblioteca):
    """Analisa o conteúdo das páginas"""
    print(f"\n📄 Analisando conteúdo: {nome_biblioteca}")
    
    total_pages = len(pages)
    pages_com_problemas = []
    
    for i, page in enumerate(pages[:10], 1):  # Analisar apenas as primeiras 10
        props = page.get("properties", {})
        
        # Título
        title_prop = props.get("Name", {}) or props.get("Title", {})
        titulo = ""
        if title_prop.get("title"):
            titulo = "".join([t.get("plain_text", "") for t in title_prop["title"]])
        
        print(f"\n[{i}/10] {titulo[:50]}...")
        
        # Verificar propriedades críticas
        problemas_pagina = []
        
        # Status editorial
        if "Status editorial" in props:
            status = props["Status editorial"].get("status", {}).get("name", "")
            if not status:
                problemas_pagina.append("Status editorial vazio")
        else:
            problemas_pagina.append("Status editorial ausente")
        
        # Tags
        if "Tags" in props:
            tags = props["Tags"].get("multi_select", [])
            if not tags:
                problemas_pagina.append("Tags vazias")
        else:
            problemas_pagina.append("Tags ausente")
        
        if problemas_pagina:
            pages_com_problemas.append({
                "titulo": titulo,
                "problemas": problemas_pagina
            })
            print(f"   ⚠️ Problemas: {', '.join(problemas_pagina)}")
        else:
            print(f"   ✅ OK")
    
    print(f"\n📊 Resumo: {len(pages_com_problemas)}/{min(10, total_pages)} páginas com problemas")
    return pages_com_problemas

def main():
    print("="*80)
    print("VERIFICAÇÃO COMPLETA E SISTEMÁTICA DAS BIBLIOTECAS")
    print("="*80)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # ETAPA 1: Verificar bibliotecas
    print_etapa(1, "Verificar ambas as bibliotecas (Gestão e Aluno)")
    
    # Verificar Gestão Escolar
    print_secao("Biblioteca Gestão Escolar")
    props_gestao = buscar_propriedades_database(DATABASE_GESTAO, "Gestão Escolar")
    pages_gestao = buscar_paginas_database(DATABASE_GESTAO, "Gestão Escolar")
    problemas_gestao = verificar_propriedades_obrigatorias(props_gestao, "Gestão Escolar")
    analise_gestao = analisar_conteudo_paginas(pages_gestao, "Gestão Escolar")
    
    # Verificar Editorial Aluno
    print_secao("Biblioteca Editorial Aluno")
    props_aluno = buscar_propriedades_database(DATABASE_ALUNO, "Editorial Alunos PRÉ-ENEM")
    pages_aluno = buscar_paginas_database(DATABASE_ALUNO, "Editorial Alunos PRÉ-ENEM")
    problemas_aluno = verificar_propriedades_obrigatorias(props_aluno, "Editorial Alunos PRÉ-ENEM")
    analise_aluno = analisar_conteudo_paginas(pages_aluno, "Editorial Alunos PRÉ-ENEM")
    
    # Relatório da Etapa 1
    print_secao("Relatório Etapa 1")
    print(f"📊 GESTÃO ESCOLAR:")
    print(f"   Propriedades: {len(props_gestao)}")
    print(f"   Páginas: {len(pages_gestao)}")
    print(f"   Problemas de propriedades: {len(problemas_gestao)}")
    print(f"   Páginas com problemas: {len(analise_gestao)}")
    
    print(f"\n📊 EDITORIAL ALUNO:")
    print(f"   Propriedades: {len(props_aluno)}")
    print(f"   Páginas: {len(pages_aluno)}")
    print(f"   Problemas de propriedades: {len(problemas_aluno)}")
    print(f"   Páginas com problemas: {len(analise_aluno)}")
    
    # Salvar relatório
    relatorio = {
        "data": datetime.now().isoformat(),
        "etapa_1": {
            "gestao": {
                "propriedades": props_gestao,
                "total_pages": len(pages_gestao),
                "problemas_propriedades": problemas_gestao,
                "pages_com_problemas": analise_gestao
            },
            "aluno": {
                "propriedades": props_aluno,
                "total_pages": len(pages_aluno),
                "problemas_propriedades": problemas_aluno,
                "pages_com_problemas": analise_aluno
            }
        }
    }
    
    with open("docs/relatorio_etapa_1_verificacao.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Relatório salvo em: docs/relatorio_etapa_1_verificacao.json")
    
    # Próximas etapas
    print_etapa(2, "Próximas Etapas")
    print("✅ Etapa 1 concluída: Verificação das bibliotecas")
    print("⏳ Etapa 2: Aplicar correções de propriedades")
    print("⏳ Etapa 3: Sincronizar conteúdos do Editorial Aluno")
    print("⏳ Etapa 4: Verificação final de conformidade")
    print("⏳ Etapa 5: Instalar e configurar MCP do YouTube")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()

