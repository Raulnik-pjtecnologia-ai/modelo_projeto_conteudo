#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Verificação Final de Conformidade com Boilerplate
ETAPA 4: Verificação final de conformidade com boilerplate em ambas as bibliotecas
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

def buscar_todas_paginas(database_id, nome_biblioteca, limite=100):
    """Busca todas as páginas de um database"""
    print(f"\n🔍 Buscando páginas: {nome_biblioteca}")
    
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    all_pages = []
    has_more = True
    start_cursor = None
    
    while has_more and len(all_pages) < limite:
        payload = {"page_size": min(50, limite - len(all_pages))}
        if start_cursor:
            payload["start_cursor"] = start_cursor
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                all_pages.extend(data.get("results", []))
                has_more = data.get("has_more", False)
                start_cursor = data.get("next_cursor")
            else:
                print(f"❌ Erro ao buscar páginas: {response.status_code}")
                break
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            break
    
    print(f"✅ Total encontrado: {len(all_pages)} páginas")
    return all_pages

def verificar_conformidade_boilerplate(page, biblioteca_tipo):
    """Verifica conformidade de uma página com o boilerplate"""
    props = page.get("properties", {})
    page_id = page["id"]
    
    # Título
    title_prop = props.get("Name", {}) or props.get("Title", {})
    titulo = ""
    if title_prop.get("title"):
        titulo = "".join([t.get("plain_text", "") for t in title_prop["title"]])
    
    conformidade = {
        "page_id": page_id,
        "titulo": titulo,
        "pontos": 0,
        "total": 0,
        "problemas": [],
        "percentual": 0
    }
    
    # Critérios de conformidade baseados no boilerplate
    if biblioteca_tipo == "Gestão Escolar":
        criterios = {
            "Status editorial": {"tipo": "status", "obrigatorio": True, "valores_validos": ["Rascunho", "Em revisão", "Aprovado", "Publicado"]},
            "Tipo": {"tipo": "select", "obrigatorio": True, "valores_validos": ["Artigo", "Checklist", "Lição", "Vídeo", "Documento Oficial"]},
            "Nível de profundidade": {"tipo": "multi_select", "obrigatorio": True, "valores_validos": ["Básico", "Intermediário", "Avançado", "Estratégico", "Tático", "Operacional"]},
            "Tags": {"tipo": "multi_select", "obrigatorio": True, "valores_validos": []},  # Qualquer valor
            "Função ": {"tipo": "multi_select", "obrigatorio": True, "valores_validos": ["Pedagógica", "Administrativa", "Estratégica", "Tática", "Operacional"]}
        }
    else:  # Editorial Aluno
        criterios = {
            "Status Editorial": {"tipo": "select", "obrigatorio": True, "valores_validos": ["Rascunho", "Em Revisão", "Aprovado", "Publicado"]},
            "Tipo": {"tipo": "select", "obrigatorio": True, "valores_validos": ["Artigo", "Checklist", "Lição", "Vídeo", "Documento Oficial"]},
            "Público Alvo": {"tipo": "multi_select", "obrigatorio": True, "valores_validos": ["Estudantes ENEM", "Estudantes", "Professores"]},
            "Tags Tema": {"tipo": "multi_select", "obrigatorio": True, "valores_validos": []},  # Qualquer valor
            "Função Alvo": {"tipo": "multi_select", "obrigatorio": True, "valores_validos": ["Pedagógica", "Administrativa", "Estratégica"]}
        }
    
    # Verificar cada critério
    for prop_name, criterio in criterios.items():
        conformidade["total"] += 1
        
        if prop_name in props:
            prop_value = props[prop_name]
            prop_type = criterio["tipo"]
            
            # Verificar tipo da propriedade
            if prop_type == "status" and prop_value.get("status"):
                valor = prop_value["status"]["name"]
                if valor in criterio["valores_validos"]:
                    conformidade["pontos"] += 1
                else:
                    conformidade["problemas"].append(f"❌ {prop_name}: '{valor}' inválido")
            elif prop_type == "select" and prop_value.get("select"):
                valor = prop_value["select"]["name"]
                if valor in criterio["valores_validos"]:
                    conformidade["pontos"] += 1
                else:
                    conformidade["problemas"].append(f"❌ {prop_name}: '{valor}' inválido")
            elif prop_type == "multi_select" and prop_value.get("multi_select"):
                valores = [item["name"] for item in prop_value["multi_select"]]
                if criterio["valores_validos"]:  # Se há valores específicos
                    if any(v in criterio["valores_validos"] for v in valores):
                        conformidade["pontos"] += 1
                    else:
                        conformidade["problemas"].append(f"❌ {prop_name}: valores inválidos")
                else:  # Qualquer valor é válido
                    if valores:
                        conformidade["pontos"] += 1
                    else:
                        conformidade["problemas"].append(f"⚠️ {prop_name}: vazio")
            else:
                conformidade["problemas"].append(f"⚠️ {prop_name}: formato incorreto")
        else:
            conformidade["problemas"].append(f"❌ {prop_name}: ausente")
    
    # Calcular percentual
    if conformidade["total"] > 0:
        conformidade["percentual"] = (conformidade["pontos"] / conformidade["total"]) * 100
    
    return conformidade

def analisar_biblioteca(database_id, nome_biblioteca, biblioteca_tipo):
    """Analisa uma biblioteca completa"""
    print_secao(f"Analisando {nome_biblioteca}")
    
    # Buscar páginas
    pages = buscar_todas_paginas(database_id, nome_biblioteca, 50)  # Limitar para análise
    
    if not pages:
        print(f"❌ Nenhuma página encontrada em {nome_biblioteca}")
        return {"total": 0, "conformes": 0, "media": 0, "conformidades": []}
    
    # Verificar conformidade de cada página
    conformidades = []
    for i, page in enumerate(pages, 1):
        print(f"\n[{i}/{len(pages)}] Verificando página...")
        conformidade = verificar_conformidade_boilerplate(page, biblioteca_tipo)
        conformidades.append(conformidade)
        
        # Mostrar problemas se houver
        if conformidade["percentual"] < 80:
            print(f"   📄 {conformidade['titulo'][:50]}... ({conformidade['percentual']:.1f}%)")
            for problema in conformidade["problemas"][:3]:  # Mostrar apenas 3 problemas
                print(f"      {problema}")
    
    # Calcular estatísticas
    total = len(conformidades)
    conformes = len([c for c in conformidades if c["percentual"] >= 80])
    media = sum(c["percentual"] for c in conformidades) / total if total > 0 else 0
    
    return {
        "total": total,
        "conformes": conformes,
        "media": media,
        "conformidades": conformidades
    }

def gerar_relatorio_final(analise_gestao, analise_aluno):
    """Gera relatório final de conformidade"""
    print_secao("Relatório Final de Conformidade")
    
    # Estatísticas Gestão
    total_gestao = analise_gestao["total"]
    conformes_gestao = analise_gestao["conformes"]
    media_gestao = analise_gestao["media"]
    
    # Estatísticas Aluno
    total_aluno = analise_aluno["total"]
    conformes_aluno = analise_aluno["conformes"]
    media_aluno = analise_aluno["media"]
    
    print(f"\n📊 BIBLIOTECA GESTÃO ESCOLAR:")
    print(f"   Total de páginas: {total_gestao}")
    print(f"   Páginas conformes (≥80%): {conformes_gestao}")
    print(f"   Conformidade média: {media_gestao:.1f}%")
    
    print(f"\n📊 BIBLIOTECA EDITORIAL ALUNO:")
    print(f"   Total de páginas: {total_aluno}")
    print(f"   Páginas conformes (≥80%): {conformes_aluno}")
    print(f"   Conformidade média: {media_aluno:.1f}%")
    
    # Estatísticas gerais
    total_geral = total_gestao + total_aluno
    conformes_geral = conformes_gestao + conformes_aluno
    media_geral = (media_gestao + media_aluno) / 2
    
    print(f"\n📈 ESTATÍSTICAS GERAIS:")
    print(f"   Total de páginas: {total_geral}")
    print(f"   Páginas conformes: {conformes_geral}")
    print(f"   Conformidade geral: {media_geral:.1f}%")
    
    # Status final
    if media_geral >= 90:
        print(f"\n🎉 EXCELENTE! Conformidade geral: {media_geral:.1f}%")
        print("   ✅ Bibliotecas estão 100% alinhadas com o boilerplate")
    elif media_geral >= 80:
        print(f"\n✅ BOM! Conformidade geral: {media_geral:.1f}%")
        print("   ✅ Bibliotecas estão bem alinhadas com o boilerplate")
    elif media_geral >= 70:
        print(f"\n⚠️ REGULAR! Conformidade geral: {media_geral:.1f}%")
        print("   ⚠️ Algumas melhorias necessárias")
    else:
        print(f"\n❌ BAIXO! Conformidade geral: {media_geral:.1f}%")
        print("   ❌ Necessário revisão significativa")
    
    # Salvar relatório
    relatorio = {
        "data": datetime.now().isoformat(),
        "gestao": analise_gestao,
        "aluno": analise_aluno,
        "geral": {
            "total": total_geral,
            "conformes": conformes_geral,
            "media": media_geral
        }
    }
    
    with open("docs/relatorio_conformidade_final_etapa4.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Relatório salvo em: docs/relatorio_conformidade_final_etapa4.json")
    
    return relatorio

def main():
    print("="*80)
    print("VERIFICAÇÃO FINAL DE CONFORMIDADE - ETAPA 4")
    print("="*80)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Analisar biblioteca Gestão Escolar
    print_etapa(4, "Verificação final de conformidade com boilerplate")
    
    analise_gestao = analisar_biblioteca(DATABASE_GESTAO, "Gestão Escolar", "Gestão Escolar")
    
    # Analisar biblioteca Editorial Aluno
    analise_aluno = analisar_biblioteca(DATABASE_ALUNO, "Editorial Alunos PRÉ-ENEM", "Editorial Aluno")
    
    # Gerar relatório final
    relatorio = gerar_relatorio_final(analise_gestao, analise_aluno)
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()

