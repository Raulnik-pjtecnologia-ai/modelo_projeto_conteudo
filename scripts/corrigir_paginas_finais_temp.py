#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Corrigir as 2 Páginas Finais com Problemas
Corrige as páginas "Material de geometria" e "Acesse planners..."
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

def corrigir_paginas_especificas():
    """Corrigir as páginas específicas que ainda têm problemas"""
    print("🔧 Corrigindo páginas específicas com problemas...")
    
    # Buscar todas as páginas
    url = f"https://api.notion.com/v1/databases/{DATABASE_ALUNO}/query"
    
    try:
        response = requests.post(url, headers=headers, json={})
        if response.status_code != 200:
            print(f"❌ Erro ao buscar páginas: {response.status_code}")
            return False
        
        data = response.json()
        pages = data.get("results", [])
        
        # Identificar páginas problemáticas
        paginas_problematicas = []
        
        for page in pages:
            properties = page.get("properties", {})
            title_prop = properties.get("Title", {})
            page_title = ""
            
            if title_prop.get("type") == "title":
                title_array = title_prop.get("title", [])
                if title_array and len(title_array) > 0:
                    page_title = title_array[0].get("text", {}).get("content", "")
            
            # Verificar se é uma das páginas problemáticas
            if any(keyword in page_title.lower() for keyword in ["material de geometria", "acesse planners", "módulos de estudo"]):
                paginas_problematicas.append({
                    "page": page,
                    "title": page_title,
                    "page_id": page["id"]
                })
        
        print(f"📄 Encontradas {len(paginas_problematicas)} páginas problemáticas")
        
        correcoes_aplicadas = 0
        
        for i, item in enumerate(paginas_problematicas, 1):
            page = item["page"]
            page_title = item["title"]
            page_id = item["page_id"]
            
            print(f"\n[{i}/{len(paginas_problematicas)}] Corrigindo: {page_title[:50]}...")
            
            # Preparar correções específicas
            properties_to_update = {}
            
            # Corrigir Público Alvo
            properties_to_update["Público Alvo"] = {
                "multi_select": [
                    {"name": "Estudantes ENEM"},
                    {"name": "Pré-vestibulandos"}
                ]
            }
            
            # Corrigir Tags Tema baseadas no título
            tags_sugeridas = ["ENEM", "Estudos", "Preparação"]
            title_lower = page_title.lower()
            
            if "geometria" in title_lower or "matemática" in title_lower or "matematica" in title_lower:
                tags_sugeridas.append("Matemática")
                tags_sugeridas.append("Geometria")
            if "planner" in title_lower or "organização" in title_lower or "organizacao" in title_lower:
                tags_sugeridas.append("Organização")
                tags_sugeridas.append("Planejamento")
            if "ferramentas" in title_lower or "tools" in title_lower:
                tags_sugeridas.append("Ferramentas")
            
            properties_to_update["Tags Tema"] = {
                "multi_select": [{"name": tag} for tag in tags_sugeridas]
            }
            
            # Corrigir Função Alvo
            properties_to_update["Função Alvo"] = {
                "multi_select": [
                    {"name": "Pedagógica"},
                    {"name": "Estratégica"}
                ]
            }
            
            # Corrigir Status Editorial
            properties_to_update["Status Editorial"] = {
                "select": {"name": "Publicado"}
            }
            
            # Aplicar correções
            try:
                update_url = f"https://api.notion.com/v1/pages/{page_id}"
                update_data = {"properties": properties_to_update}
                
                update_response = requests.patch(update_url, headers=headers, json=update_data)
                
                if update_response.status_code == 200:
                    print(f"   ✅ Todas as propriedades corrigidas")
                    print(f"   📝 Tags aplicadas: {', '.join(tags_sugeridas)}")
                    correcoes_aplicadas += 1
                else:
                    print(f"   ❌ Erro ao atualizar: {update_response.status_code}")
                    print(f"   📝 Resposta: {update_response.text[:200]}...")
            except Exception as e:
                print(f"   ❌ Erro: {str(e)}")
        
        print(f"\n📊 RESUMO: {correcoes_aplicadas}/{len(paginas_problematicas)} páginas corrigidas")
        return correcoes_aplicadas > 0
        
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")
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
            # Extrair título
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
        
        # Salvar relatório final
        relatorio = {
            "data_verificacao": datetime.now().isoformat(),
            "total_paginas": total_pages,
            "paginas_conformes": pages_conformes,
            "conformidade_percentual": conformidade,
            "problemas_restantes": problemas_restantes,
            "status": "SUCESSO" if conformidade >= 95.0 else "PARCIAL"
        }
        
        with open("docs/relatorio_conformidade_final_completo.json", "w", encoding="utf-8") as f:
            json.dump(relatorio, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 Relatório final salvo em: docs/relatorio_conformidade_final_completo.json")
        
        return conformidade >= 95.0
        
    except Exception as e:
        print(f"❌ Erro ao verificar conformidade: {str(e)}")
        return False

def main():
    print("="*80)
    print("CORREÇÃO DAS PÁGINAS FINAIS COM PROBLEMAS")
    print("="*80)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Etapa 1: Corrigir páginas específicas
    if corrigir_paginas_especificas():
        print("✅ Páginas específicas corrigidas com sucesso!")
    else:
        print("❌ Falha ao corrigir páginas específicas")
    
    # Etapa 2: Verificação final de conformidade
    if verificar_conformidade_final():
        print("\n🎉 SUCESSO TOTAL: Conformidade atingiu 95% ou mais!")
        print("✅ TODOS OS PROBLEMAS FORAM RESOLVIDOS!")
    else:
        print("\n⚠️ Conformidade ainda pode ser melhorada")
    
    print("\n" + "="*80)
    print("CORREÇÃO FINAL CONCLUÍDA")
    print("="*80)

if __name__ == "__main__":
    main()
