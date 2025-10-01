#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Corrigir os 2 Problemas Restantes
Corrige as páginas que ainda têm problemas de conformidade
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

def corrigir_paginas_problematicas():
    """Corrigir as páginas que ainda têm problemas"""
    print("🔧 Corrigindo páginas problemáticas...")
    
    # Buscar páginas com problemas específicos
    url = f"https://api.notion.com/v1/databases/{DATABASE_ALUNO}/query"
    
    try:
        response = requests.post(url, headers=headers, json={})
        if response.status_code != 200:
            print(f"❌ Erro ao buscar páginas: {response.status_code}")
            return False
        
        data = response.json()
        pages = data.get("results", [])
        
        # Filtrar páginas problemáticas
        paginas_problematicas = []
        
        for page in pages:
            page_title = page.get("properties", {}).get("Título", {}).get("title", [{}])[0].get("text", {}).get("content", "Sem título")
            
            # Verificar se é uma das páginas problemáticas
            if any(keyword in page_title.lower() for keyword in ["material de geometria", "acesse planners", "módulos de estudo"]):
                paginas_problematicas.append(page)
        
        print(f"📄 Encontradas {len(paginas_problematicas)} páginas problemáticas")
        
        for i, page in enumerate(paginas_problematicas, 1):
            page_id = page["id"]
            page_title = page.get("properties", {}).get("Título", {}).get("title", [{}])[0].get("text", {}).get("content", "Sem título")
            
            print(f"\n[{i}/{len(paginas_problematicas)}] Corrigindo: {page_title[:50]}...")
            
            # Aplicar correções completas
            properties_to_update = {
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
                        {"name": "Preparação"},
                        {"name": "Matemática" if "geometria" in page_title.lower() else "Organização"}
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
                    print(f"   ✅ Todas as propriedades corrigidas")
                else:
                    print(f"   ❌ Erro ao atualizar: {update_response.status_code}")
                    print(f"   📝 Resposta: {update_response.text[:200]}...")
            except Exception as e:
                print(f"   ❌ Erro: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")
        return False

def configurar_mcp_youtube_correto():
    """Configurar MCP YouTube corretamente"""
    print("\n🎥 Configurando MCP YouTube...")
    
    # Verificar se o arquivo de configuração existe
    config_file = "mcp_youtube_config.json"
    if not os.path.exists(config_file):
        print(f"❌ Arquivo de configuração não encontrado: {config_file}")
        return False
    
    # Ler configuração atual
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"✅ Arquivo de configuração encontrado")
        
        # Verificar se a API key está configurada
        youtube_config = config.get("mcpServers", {}).get("youtube", {})
        api_key = youtube_config.get("env", {}).get("YOUTUBE_API_KEY")
        
        if api_key:
            print(f"✅ API Key encontrada: {api_key[:10]}...")
            
            # Testar API do YouTube
            test_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q=ENEM&key={api_key}&maxResults=1"
            
            try:
                response = requests.get(test_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if "items" in data and len(data["items"]) > 0:
                        print("✅ API do YouTube funcionando corretamente")
                        return True
                    else:
                        print("⚠️ API do YouTube respondeu mas sem resultados")
                        return False
                else:
                    print(f"❌ Erro na API do YouTube: {response.status_code}")
                    if response.status_code == 403:
                        print("   💡 Possível problema: API Key inválida ou cotas esgotadas")
                    return False
            except Exception as e:
                print(f"❌ Erro ao testar API: {str(e)}")
                return False
        else:
            print("❌ API Key não encontrada na configuração")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao ler configuração: {str(e)}")
        return False

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
            page_title = page.get("properties", {}).get("Título", {}).get("title", [{}])[0].get("text", {}).get("content", "Sem título")
            problemas_pagina = []
            
            properties = page.get("properties", {})
            
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
    print("CORREÇÃO DOS PROBLEMAS RESTANTES")
    print("="*80)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Etapa 1: Corrigir páginas problemáticas
    if corrigir_paginas_problematicas():
        print("✅ Páginas problemáticas corrigidas")
    else:
        print("❌ Falha ao corrigir páginas problemáticas")
    
    # Etapa 2: Configurar MCP YouTube
    if configurar_mcp_youtube_correto():
        print("✅ MCP YouTube configurado e funcionando")
    else:
        print("❌ Problemas na configuração do MCP YouTube")
    
    # Etapa 3: Verificação final
    if verificar_conformidade_final():
        print("\n🎉 SUCESSO TOTAL: Conformidade atingiu 95% ou mais!")
    else:
        print("\n⚠️ Conformidade ainda pode ser melhorada")
    
    print("\n" + "="*80)
    print("CORREÇÃO FINAL CONCLUÍDA")
    print("="*80)

if __name__ == "__main__":
    main()
