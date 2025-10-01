#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script Robusto para Corrigir Propriedades da Biblioteca Editorial Aluno
Versão melhorada para lidar com erros e corrigir todos os problemas
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

def print_secao(titulo):
    print("\n" + "="*60)
    print(titulo)
    print("="*60)

def obter_todas_paginas():
    """Obter todas as páginas da biblioteca com paginação"""
    print("📄 Obtendo todas as páginas...")
    
    all_pages = []
    has_more = True
    start_cursor = None
    
    while has_more:
        url = f"https://api.notion.com/v1/databases/{DATABASE_ALUNO}/query"
        payload = {}
        
        if start_cursor:
            payload["start_cursor"] = start_cursor
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code != 200:
                print(f"❌ Erro ao buscar páginas: {response.status_code}")
                print(f"Resposta: {response.text}")
                return []
            
            data = response.json()
            pages = data.get("results", [])
            all_pages.extend(pages)
            
            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")
            
            print(f"   📄 Páginas obtidas: {len(pages)} (Total: {len(all_pages)})")
            
        except Exception as e:
            print(f"❌ Erro ao obter páginas: {str(e)}")
            return []
    
    print(f"✅ Total de páginas obtidas: {len(all_pages)}")
    return all_pages

def extrair_titulo_pagina(page):
    """Extrair título da página de forma segura"""
    try:
        properties = page.get("properties", {})
        titulo_prop = properties.get("Título", {})
        
        if titulo_prop.get("type") == "title":
            title_array = titulo_prop.get("title", [])
            if title_array and len(title_array) > 0:
                return title_array[0].get("text", {}).get("content", "Sem título")
        
        # Tentar outras propriedades de título
        for prop_name in ["Name", "Nome", "Titulo", "Title"]:
            if prop_name in properties:
                prop = properties[prop_name]
                if prop.get("type") == "title":
                    title_array = prop.get("title", [])
                    if title_array and len(title_array) > 0:
                        return title_array[0].get("text", {}).get("content", "Sem título")
        
        return "Sem título"
    except Exception as e:
        print(f"   ⚠️ Erro ao extrair título: {str(e)}")
        return "Sem título"

def corrigir_propriedades_pagina(page):
    """Corrigir propriedades de uma página específica"""
    page_id = page["id"]
    page_title = extrair_titulo_pagina(page)
    
    properties_to_update = {}
    properties = page.get("properties", {})
    
    # Corrigir Público Alvo
    publico_alvo = properties.get("Público Alvo", {})
    if publico_alvo.get("type") == "multi_select":
        current_values = publico_alvo.get("multi_select", [])
        if not current_values or any(not v.get("name") for v in current_values):
            properties_to_update["Público Alvo"] = {
                "multi_select": [
                    {"name": "Estudantes ENEM"},
                    {"name": "Pré-vestibulandos"}
                ]
            }
    
    # Corrigir Tags Tema
    tags_tema = properties.get("Tags Tema", {})
    if tags_tema.get("type") == "multi_select":
        current_tags = tags_tema.get("multi_select", [])
        if not current_tags or any(not t.get("name") for t in current_tags):
            # Definir tags baseadas no título
            tags_sugeridas = ["ENEM", "Estudos", "Preparação"]
            title_lower = page_title.lower()
            
            if any(word in title_lower for word in ["matemática", "matematica", "math"]):
                tags_sugeridas.append("Matemática")
            if any(word in title_lower for word in ["ansiedade", "estresse", "stress"]):
                tags_sugeridas.append("Saúde Mental")
            if any(word in title_lower for word in ["memorização", "memorizacao", "memoria"]):
                tags_sugeridas.append("Técnicas de Estudo")
            if any(word in title_lower for word in ["simulado", "simulados", "prova"]):
                tags_sugeridas.append("Simulados")
            if any(word in title_lower for word in ["checklist", "lista", "dicas"]):
                tags_sugeridas.append("Organização")
            
            properties_to_update["Tags Tema"] = {
                "multi_select": [{"name": tag} for tag in tags_sugeridas]
            }
    
    # Corrigir Função Alvo
    funcao_alvo = properties.get("Função Alvo", {})
    if funcao_alvo.get("type") == "multi_select":
        current_funcoes = funcao_alvo.get("multi_select", [])
        if not current_funcoes or any(not f.get("name") for f in current_funcoes):
            properties_to_update["Função Alvo"] = {
                "multi_select": [
                    {"name": "Pedagógica"},
                    {"name": "Estratégica"}
                ]
            }
    
    # Corrigir Status Editorial
    status_editorial = properties.get("Status Editorial", {})
    if status_editorial.get("type") == "select":
        current_status = status_editorial.get("select", {})
        if not current_status or current_status.get("name") in ["Em Curadoria", "Em Revisao", "Em Revisão"]:
            # Mapear status inválidos para válidos
            status_mapping = {
                "Em Curadoria": "Publicado",
                "Em Revisao": "Publicado",
                "Em Revisão": "Publicado"
            }
            new_status = status_mapping.get(current_status.get("name", ""), "Publicado")
            properties_to_update["Status Editorial"] = {
                "select": {"name": new_status}
            }
    
    return properties_to_update

def aplicar_correcoes_em_lote(pages):
    """Aplicar correções em todas as páginas"""
    print_secao("APLICANDO CORREÇÕES EM LOTE")
    
    correcoes_aplicadas = 0
    erros = 0
    
    for i, page in enumerate(pages, 1):
        page_id = page["id"]
        page_title = extrair_titulo_pagina(page)
        
        print(f"\n[{i}/{len(pages)}] Processando: {page_title[:50]}...")
        
        try:
            properties_to_update = corrigir_propriedades_pagina(page)
            
            if properties_to_update:
                # Aplicar correções
                update_url = f"https://api.notion.com/v1/pages/{page_id}"
                update_data = {"properties": properties_to_update}
                
                update_response = requests.patch(update_url, headers=headers, json=update_data)
                
                if update_response.status_code == 200:
                    print(f"   ✅ Propriedades corrigidas: {list(properties_to_update.keys())}")
                    correcoes_aplicadas += 1
                else:
                    print(f"   ❌ Erro ao atualizar: {update_response.status_code}")
                    print(f"   📝 Resposta: {update_response.text[:200]}...")
                    erros += 1
            else:
                print(f"   ℹ️ Nenhuma correção necessária")
        
        except Exception as e:
            print(f"   ❌ Erro ao processar página: {str(e)}")
            erros += 1
    
    print(f"\n📊 RESUMO DAS CORREÇÕES:")
    print(f"   ✅ Páginas corrigidas: {correcoes_aplicadas}")
    print(f"   ❌ Erros: {erros}")
    print(f"   📄 Total processadas: {len(pages)}")
    
    return correcoes_aplicadas, erros

def verificar_conformidade_final():
    """Verificar conformidade final após todas as correções"""
    print_secao("VERIFICAÇÃO FINAL DE CONFORMIDADE")
    
    pages = obter_todas_paginas()
    if not pages:
        print("❌ Não foi possível obter páginas para verificação")
        return False
    
    total_pages = len(pages)
    pages_conformes = 0
    problemas_detalhados = []
    
    for page in pages:
        page_title = extrair_titulo_pagina(page)
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
            problemas_detalhados.append({
                "titulo": page_title[:50],
                "problemas": problemas_pagina
            })
    
    conformidade = (pages_conformes / total_pages) * 100 if total_pages > 0 else 0
    
    print(f"📊 BIBLIOTECA EDITORIAL ALUNO - CONFORMIDADE FINAL:")
    print(f"   Total de páginas: {total_pages}")
    print(f"   Páginas conformes: {pages_conformes}")
    print(f"   Conformidade: {conformidade:.1f}%")
    
    if problemas_detalhados:
        print(f"\n⚠️ PROBLEMAS RESTANTES ({len(problemas_detalhados)} páginas):")
        for problema in problemas_detalhados[:10]:  # Mostrar apenas os primeiros 10
            print(f"   • {problema['titulo']}: {', '.join(problema['problemas'])}")
        if len(problemas_detalhados) > 10:
            print(f"   ... e mais {len(problemas_detalhados) - 10} páginas")
    
    # Salvar relatório detalhado
    relatorio = {
        "data_verificacao": datetime.now().isoformat(),
        "total_paginas": total_pages,
        "paginas_conformes": pages_conformes,
        "conformidade_percentual": conformidade,
        "problemas_detalhados": problemas_detalhados
    }
    
    with open("docs/relatorio_conformidade_final_corrigida.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 Relatório salvo em: docs/relatorio_conformidade_final_corrigida.json")
    
    return conformidade >= 80.0

def main():
    print("="*80)
    print("CORREÇÃO ROBUSTA DE PROPRIEDADES - BIBLIOTECA EDITORIAL ALUNO")
    print("="*80)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Etapa 1: Obter todas as páginas
    pages = obter_todas_paginas()
    if not pages:
        print("❌ Falha ao obter páginas. Encerrando.")
        return
    
    # Etapa 2: Aplicar correções
    correcoes, erros = aplicar_correcoes_em_lote(pages)
    
    # Etapa 3: Verificar conformidade final
    if verificar_conformidade_final():
        print("\n🎉 SUCESSO: Conformidade atingiu 80% ou mais!")
    else:
        print("\n⚠️ ATENÇÃO: Conformidade ainda abaixo de 80%")
    
    print("\n" + "="*80)
    print("CORREÇÃO CONCLUÍDA")
    print("="*80)

if __name__ == "__main__":
    main()
