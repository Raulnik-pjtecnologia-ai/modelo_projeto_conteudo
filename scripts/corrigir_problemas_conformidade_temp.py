#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Corrigir Problemas de Conformidade Identificados
Corrige propriedades, status editorial e melhora conformidade geral
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

def print_secao(titulo):
    print("\n" + "="*60)
    print(titulo)
    print("="*60)

def corrigir_propriedades_aluno():
    """Corrigir propriedades da Biblioteca Editorial Aluno"""
    print_secao("CORRIGINDO PROPRIEDADES - BIBLIOTECA EDITORIAL ALUNO")
    
    # Primeiro, obter todas as páginas
    url = f"https://api.notion.com/v1/databases/{DATABASE_ALUNO}/query"
    
    try:
        response = requests.post(url, headers=headers, json={})
        if response.status_code != 200:
            print(f"❌ Erro ao buscar páginas: {response.status_code}")
            return False
        
        data = response.json()
        pages = data.get("results", [])
        print(f"📄 Encontradas {len(pages)} páginas para corrigir")
        
        correcoes_aplicadas = 0
        
        for i, page in enumerate(pages, 1):
            page_id = page["id"]
            page_title = page.get("properties", {}).get("Título", {}).get("title", [{}])[0].get("text", {}).get("content", f"Página {i}")
            
            print(f"\n[{i}/{len(pages)}] Corrigindo: {page_title[:50]}...")
            
            # Preparar propriedades corrigidas
            properties_to_update = {}
            
            # Corrigir Público Alvo (deve ser multi_select com valores válidos)
            publico_alvo = page.get("properties", {}).get("Público Alvo", {})
            if publico_alvo.get("type") == "multi_select":
                # Se já é multi_select, verificar se tem valores válidos
                current_values = publico_alvo.get("multi_select", [])
                if not current_values or any(not v.get("name") for v in current_values):
                    properties_to_update["Público Alvo"] = {
                        "multi_select": [
                            {"name": "Estudantes ENEM"},
                            {"name": "Pré-vestibulandos"}
                        ]
                    }
            
            # Corrigir Tags Tema (deve ser multi_select)
            tags_tema = page.get("properties", {}).get("Tags Tema", {})
            if tags_tema.get("type") == "multi_select":
                current_tags = tags_tema.get("multi_select", [])
                if not current_tags or any(not t.get("name") for t in current_tags):
                    # Definir tags baseadas no título
                    tags_sugeridas = ["ENEM", "Estudos", "Preparação"]
                    if "matemática" in page_title.lower() or "matematica" in page_title.lower():
                        tags_sugeridas.append("Matemática")
                    if "ansiedade" in page_title.lower() or "estresse" in page_title.lower():
                        tags_sugeridas.append("Saúde Mental")
                    if "memorização" in page_title.lower() or "memorizacao" in page_title.lower():
                        tags_sugeridas.append("Técnicas de Estudo")
                    if "simulado" in page_title.lower():
                        tags_sugeridas.append("Simulados")
                    
                    properties_to_update["Tags Tema"] = {
                        "multi_select": [{"name": tag} for tag in tags_sugeridas]
                    }
            
            # Corrigir Função Alvo (deve ser multi_select)
            funcao_alvo = page.get("properties", {}).get("Função Alvo", {})
            if funcao_alvo.get("type") == "multi_select":
                current_funcoes = funcao_alvo.get("multi_select", [])
                if not current_funcoes or any(not f.get("name") for f in current_funcoes):
                    properties_to_update["Função Alvo"] = {
                        "multi_select": [
                            {"name": "Pedagógica"},
                            {"name": "Estratégica"}
                        ]
                    }
            
            # Corrigir Status Editorial (deve ser select com valores válidos)
            status_editorial = page.get("properties", {}).get("Status Editorial", {})
            if status_editorial.get("type") == "select":
                current_status = status_editorial.get("select", {})
                if not current_status or current_status.get("name") in ["Em Curadoria", "Em Revisao"]:
                    # Mapear status inválidos para válidos
                    status_mapping = {
                        "Em Curadoria": "Em Revisão",
                        "Em Revisao": "Em Revisão"
                    }
                    new_status = status_mapping.get(current_status.get("name", ""), "Publicado")
                    properties_to_update["Status Editorial"] = {
                        "select": {"name": new_status}
                    }
            
            # Aplicar correções se houver
            if properties_to_update:
                try:
                    update_url = f"https://api.notion.com/v1/pages/{page_id}"
                    update_data = {"properties": properties_to_update}
                    
                    update_response = requests.patch(update_url, headers=headers, json=update_data)
                    
                    if update_response.status_code == 200:
                        print(f"   ✅ Propriedades corrigidas: {list(properties_to_update.keys())}")
                        correcoes_aplicadas += 1
                    else:
                        print(f"   ❌ Erro ao atualizar: {update_response.status_code}")
                        print(f"   📝 Resposta: {update_response.text}")
                except Exception as e:
                    print(f"   ❌ Erro: {str(e)}")
            else:
                print(f"   ℹ️ Nenhuma correção necessária")
        
        print(f"\n📊 RESUMO: {correcoes_aplicadas}/{len(pages)} páginas corrigidas")
        return correcoes_aplicadas > 0
        
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")
        return False

def verificar_conformidade_apos_correcoes():
    """Verificar conformidade após correções"""
    print_secao("VERIFICANDO CONFORMIDADE APÓS CORREÇÕES")
    
    # Verificar Biblioteca Editorial Aluno
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
            
            # Verificar Público Alvo
            publico_alvo = page.get("properties", {}).get("Público Alvo", {})
            if publico_alvo.get("type") != "multi_select" or not publico_alvo.get("multi_select"):
                problemas_pagina.append("Público Alvo")
            
            # Verificar Tags Tema
            tags_tema = page.get("properties", {}).get("Tags Tema", {})
            if tags_tema.get("type") != "multi_select" or not tags_tema.get("multi_select"):
                problemas_pagina.append("Tags Tema")
            
            # Verificar Função Alvo
            funcao_alvo = page.get("properties", {}).get("Função Alvo", {})
            if funcao_alvo.get("type") != "multi_select" or not funcao_alvo.get("multi_select"):
                problemas_pagina.append("Função Alvo")
            
            # Verificar Status Editorial
            status_editorial = page.get("properties", {}).get("Status Editorial", {})
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
        
        print(f"📊 BIBLIOTECA EDITORIAL ALUNO:")
        print(f"   Total de páginas: {total_pages}")
        print(f"   Páginas conformes: {pages_conformes}")
        print(f"   Conformidade: {conformidade:.1f}%")
        
        if problemas_restantes:
            print(f"\n⚠️ PROBLEMAS RESTANTES ({len(problemas_restantes)} páginas):")
            for problema in problemas_restantes[:5]:  # Mostrar apenas os primeiros 5
                print(f"   • {problema['titulo']}: {', '.join(problema['problemas'])}")
            if len(problemas_restantes) > 5:
                print(f"   ... e mais {len(problemas_restantes) - 5} páginas")
        
        return conformidade >= 80.0
        
    except Exception as e:
        print(f"❌ Erro ao verificar conformidade: {str(e)}")
        return False

def configurar_nodejs_correto():
    """Configurar Node.js no diretório correto"""
    print_secao("CONFIGURANDO NODE.JS NO DIRETÓRIO CORRETO")
    
    nodejs_path = r"C:\Program Files\nodejs"
    
    # Verificar se o diretório existe
    if os.path.exists(nodejs_path):
        print(f"✅ Diretório Node.js encontrado: {nodejs_path}")
        
        # Verificar se node.exe existe
        node_exe = os.path.join(nodejs_path, "node.exe")
        if os.path.exists(node_exe):
            print(f"✅ node.exe encontrado: {node_exe}")
        else:
            print(f"❌ node.exe não encontrado em: {nodejs_path}")
            return False
        
        # Verificar se npm existe
        npm_exe = os.path.join(nodejs_path, "npm.cmd")
        if os.path.exists(npm_exe):
            print(f"✅ npm.cmd encontrado: {npm_exe}")
        else:
            print(f"❌ npm.cmd não encontrado em: {nodejs_path}")
            return False
        
        # Atualizar PATH temporariamente para esta sessão
        current_path = os.environ.get("PATH", "")
        if nodejs_path not in current_path:
            os.environ["PATH"] = f"{nodejs_path};{current_path}"
            print(f"✅ PATH atualizado para incluir: {nodejs_path}")
        
        return True
    else:
        print(f"❌ Diretório Node.js não encontrado: {nodejs_path}")
        return False

def testar_mcp_youtube():
    """Testar MCP YouTube após configuração"""
    print_secao("TESTANDO MCP YOUTUBE")
    
    # Verificar se a configuração existe
    config_file = "mcp_youtube_config.json"
    if os.path.exists(config_file):
        print(f"✅ Arquivo de configuração encontrado: {config_file}")
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            api_key = config.get("YOUTUBE_API_KEY")
            if api_key:
                print(f"✅ API Key configurada: {api_key[:10]}...")
                
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
    else:
        print(f"❌ Arquivo de configuração não encontrado: {config_file}")
        return False

def main():
    print("="*80)
    print("CORREÇÃO COMPLETA DE PROBLEMAS DE CONFORMIDADE")
    print("="*80)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Etapa 1: Corrigir propriedades da Biblioteca Editorial Aluno
    print("\n🔧 ETAPA 1: Corrigindo propriedades...")
    if corrigir_propriedades_aluno():
        print("✅ Propriedades corrigidas com sucesso")
    else:
        print("❌ Falha ao corrigir propriedades")
    
    # Etapa 2: Verificar conformidade após correções
    print("\n📊 ETAPA 2: Verificando conformidade...")
    if verificar_conformidade_apos_correcoes():
        print("✅ Conformidade melhorada significativamente")
    else:
        print("⚠️ Conformidade ainda precisa de melhorias")
    
    # Etapa 3: Configurar Node.js no diretório correto
    print("\n⚙️ ETAPA 3: Configurando Node.js...")
    if configurar_nodejs_correto():
        print("✅ Node.js configurado corretamente")
    else:
        print("❌ Falha na configuração do Node.js")
    
    # Etapa 4: Testar MCP YouTube
    print("\n🎥 ETAPA 4: Testando MCP YouTube...")
    if testar_mcp_youtube():
        print("✅ MCP YouTube funcionando corretamente")
    else:
        print("❌ MCP YouTube com problemas")
    
    print("\n" + "="*80)
    print("CORREÇÃO CONCLUÍDA")
    print("="*80)

if __name__ == "__main__":
    main()
