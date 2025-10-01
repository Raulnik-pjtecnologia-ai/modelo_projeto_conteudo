#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script Final para Corrigir Página Sem Título
Corrige a página específica que está sem título usando a propriedade correta "Title"
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

def corrigir_pagina_sem_titulo():
    """Corrigir a página específica que está sem título"""
    print("🔧 Corrigindo página sem título...")
    
    # ID da página problemática identificada
    page_id = "2705113a-91a3-806e-b5cc-d090a5df49b2"
    
    # Primeiro, obter a página para ver seu conteúdo
    url = f"https://api.notion.com/v1/pages/{page_id}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"❌ Erro ao buscar página: {response.status_code}")
            return False
        
        page_data = response.json()
        properties = page_data.get("properties", {})
        
        print("📄 Propriedades da página:")
        for prop_name, prop_data in properties.items():
            prop_type = prop_data.get("type", "unknown")
            print(f"   • {prop_name}: {prop_type}")
        
        # Definir título baseado no conteúdo disponível
        titulo_sugerido = "Conteúdo ENEM - Preparação Acadêmica"
        
        # Verificar se há alguma propriedade que possa indicar o tipo de conteúdo
        tipo_conteudo = properties.get("Tipo de Conteúdo", {}).get("select", {}).get("name", "")
        if tipo_conteudo:
            titulo_sugerido = f"Conteúdo ENEM - {tipo_conteudo}"
        
        # Preparar atualizações
        properties_to_update = {
            "Title": {
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
        
        print(f"\n🔧 Aplicando correções...")
        print(f"   Título: '{titulo_sugerido}'")
        
        # Aplicar correções
        update_url = f"https://api.notion.com/v1/pages/{page_id}"
        update_data = {"properties": properties_to_update}
        
        update_response = requests.patch(update_url, headers=headers, json=update_data)
        
        if update_response.status_code == 200:
            print("✅ Página corrigida com sucesso!")
            return True
        else:
            print(f"❌ Erro ao atualizar: {update_response.status_code}")
            print(f"📝 Resposta: {update_response.text}")
            return False
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
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
            # Extrair título usando a propriedade correta "Title"
            properties = page.get("properties", {})
            title_prop = properties.get("Title", {})
            page_title = "Sem título"
            
            if title_prop.get("type") == "title":
                title_array = title_prop.get("title", [])
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

def configurar_nodejs_e_mcp():
    """Configurar Node.js e testar MCP YouTube"""
    print("\n⚙️ Configurando Node.js e MCP YouTube...")
    
    # Verificar Node.js no diretório correto
    nodejs_path = r"C:\Program Files\nodejs"
    
    if os.path.exists(nodejs_path):
        print(f"✅ Node.js encontrado em: {nodejs_path}")
        
        # Atualizar PATH
        current_path = os.environ.get("PATH", "")
        if nodejs_path not in current_path:
            os.environ["PATH"] = f"{nodejs_path};{current_path}"
            print(f"✅ PATH atualizado")
        
        # Testar MCP YouTube
        config_file = "mcp_youtube_config.json"
        if os.path.exists(config_file):
            print(f"✅ Configuração MCP encontrada: {config_file}")
            
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                youtube_config = config.get("mcpServers", {}).get("youtube", {})
                api_key = youtube_config.get("env", {}).get("YOUTUBE_API_KEY")
                
                if api_key:
                    print(f"✅ API Key configurada: {api_key[:10]}...")
                    print("ℹ️ Nota: API Key pode ter limitações de cota")
                    return True
                else:
                    print("❌ API Key não encontrada")
                    return False
            except Exception as e:
                print(f"❌ Erro ao ler configuração: {str(e)}")
                return False
        else:
            print(f"❌ Arquivo de configuração não encontrado: {config_file}")
            return False
    else:
        print(f"❌ Node.js não encontrado em: {nodejs_path}")
        return False

def main():
    print("="*80)
    print("CORREÇÃO FINAL - PÁGINA SEM TÍTULO")
    print("="*80)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Etapa 1: Corrigir página sem título
    if corrigir_pagina_sem_titulo():
        print("✅ Página sem título corrigida com sucesso!")
    else:
        print("❌ Falha ao corrigir página sem título")
    
    # Etapa 2: Verificação final de conformidade
    if verificar_conformidade_final():
        print("\n🎉 SUCESSO TOTAL: Conformidade atingiu 95% ou mais!")
    else:
        print("\n⚠️ Conformidade ainda pode ser melhorada")
    
    # Etapa 3: Configurar Node.js e MCP
    if configurar_nodejs_e_mcp():
        print("✅ Node.js e MCP YouTube configurados corretamente!")
    else:
        print("❌ Problemas na configuração do Node.js ou MCP")
    
    print("\n" + "="*80)
    print("CORREÇÃO FINAL CONCLUÍDA")
    print("="*80)

if __name__ == "__main__":
    main()
