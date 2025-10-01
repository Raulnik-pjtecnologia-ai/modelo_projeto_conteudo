#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Verificar Propriedades da Biblioteca Editorial Aluno
Identifica os nomes corretos das propriedades
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

def verificar_propriedades_biblioteca():
    """Verificar propriedades da biblioteca"""
    print("🔍 Verificando propriedades da biblioteca...")
    
    url = f"https://api.notion.com/v1/databases/{DATABASE_ALUNO}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"❌ Erro ao buscar biblioteca: {response.status_code}")
            return None
        
        data = response.json()
        properties = data.get("properties", {})
        
        print(f"📊 Total de propriedades: {len(properties)}")
        print("\n📋 PROPRIEDADES ENCONTRADAS:")
        
        for prop_name, prop_data in properties.items():
            prop_type = prop_data.get("type", "unknown")
            print(f"   • {prop_name}: {prop_type}")
            
            # Se for título, mostrar detalhes
            if prop_type == "title":
                print(f"      ✅ Esta é a propriedade de título!")
        
        return properties
        
    except Exception as e:
        print(f"❌ Erro ao verificar propriedades: {str(e)}")
        return None

def verificar_paginas_problematicas():
    """Verificar páginas problemáticas específicas"""
    print("\n🔍 Verificando páginas problemáticas...")
    
    url = f"https://api.notion.com/v1/databases/{DATABASE_ALUNO}/query"
    
    try:
        response = requests.post(url, headers=headers, json={})
        if response.status_code != 200:
            print(f"❌ Erro ao buscar páginas: {response.status_code}")
            return
        
        data = response.json()
        pages = data.get("results", [])
        
        print(f"📄 Total de páginas: {len(pages)}")
        
        for i, page in enumerate(pages, 1):
            properties = page.get("properties", {})
            
            # Verificar todas as propriedades de título possíveis
            titulo_encontrado = False
            titulo_value = ""
            
            for prop_name, prop_data in properties.items():
                if prop_data.get("type") == "title":
                    title_array = prop_data.get("title", [])
                    if title_array and len(title_array) > 0:
                        titulo_value = title_array[0].get("text", {}).get("content", "")
                        if titulo_value and titulo_value.strip():
                            titulo_encontrado = True
                            print(f"   [{i}] ✅ {prop_name}: '{titulo_value[:50]}...'")
                            break
                    else:
                        print(f"   [{i}] ❌ {prop_name}: vazio")
                        titulo_encontrado = False
                        break
            
            if not titulo_encontrado:
                print(f"   [{i}] ⚠️ Página sem título válido")
                print(f"       ID: {page['id']}")
                
                # Mostrar todas as propriedades desta página
                print(f"       Propriedades disponíveis:")
                for prop_name, prop_data in properties.items():
                    prop_type = prop_data.get("type", "unknown")
                    print(f"         • {prop_name}: {prop_type}")
        
    except Exception as e:
        print(f"❌ Erro ao verificar páginas: {str(e)}")

def main():
    print("="*80)
    print("VERIFICAÇÃO DE PROPRIEDADES DA BIBLIOTECA")
    print("="*80)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Verificar propriedades da biblioteca
    properties = verificar_propriedades_biblioteca()
    
    if properties:
        # Verificar páginas problemáticas
        verificar_paginas_problematicas()
    
    print("\n" + "="*80)
    print("VERIFICAÇÃO CONCLUÍDA")
    print("="*80)

if __name__ == "__main__":
    main()
