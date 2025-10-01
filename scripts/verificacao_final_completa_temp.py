#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Verificação Final Completa das Bibliotecas
Verifica conformidade com boilerplate e gera relatório final
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
    print(titulo.upper())
    print("="*60)

def buscar_todas_paginas(database_id, nome_biblioteca):
    """Busca todas as páginas de um database"""
    print(f"\n🔍 Verificando biblioteca: {nome_biblioteca}")
    
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    all_pages = []
    has_more = True
    start_cursor = None
    
    while has_more:
        payload = {}
        if start_cursor:
            payload["start_cursor"] = start_cursor
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            all_pages.extend(data.get("results", []))
            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")
        else:
            print(f"❌ Erro: {response.status_code}")
            break
    
    print(f"✅ Total encontrado: {len(all_pages)} páginas")
    return all_pages

def verificar_conformidade_pagina(page, nome_biblioteca):
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
        "problemas": []
    }
    
    # Verificar propriedades obrigatórias
    propriedades_obrigatorias = {
        "Status editorial": ["Rascunho", "Em revisão", "Aprovado", "Publicado"],
        "Tipo": ["Artigo", "Checklist", "Lição", "Vídeo", "Documento Oficial"],
        "Nível de profundidade": ["Básico", "Intermediário", "Avançado", "Estratégico", "Tático", "Operacional"]
    }
    
    for prop_name, valores_validos in propriedades_obrigatorias.items():
        conformidade["total"] += 1
        
        if prop_name in props:
            prop_value = props[prop_name]
            if prop_value.get("select"):
                valor = prop_value["select"]["name"]
                if valor in valores_validos:
                    conformidade["pontos"] += 1
                else:
                    conformidade["problemas"].append(f"❌ {prop_name}: '{valor}' inválido")
            elif prop_value.get("status"):
                valor = prop_value["status"]["name"]
                if valor in valores_validos:
                    conformidade["pontos"] += 1
                else:
                    conformidade["problemas"].append(f"❌ {prop_name}: '{valor}' inválido")
            elif prop_value.get("multi_select"):
                valores = [item["name"] for item in prop_value["multi_select"]]
                if any(v in valores_validos for v in valores):
                    conformidade["pontos"] += 1
                else:
                    conformidade["problemas"].append(f"❌ {prop_name}: valores inválidos")
            else:
                conformidade["problemas"].append(f"⚠️ {prop_name}: formato inválido")
        else:
            conformidade["problemas"].append(f"⚠️ {prop_name}: ausente")
    
    # Verificar Tags (deve ter pelo menos uma)
    conformidade["total"] += 1
    if "Tags" in props:
        tags = props["Tags"].get("multi_select", [])
        if tags:
            conformidade["pontos"] += 1
        else:
            conformidade["problemas"].append("⚠️ Tags vazias")
    else:
        conformidade["problemas"].append("⚠️ Tags: ausente")
    
    # Verificar Função (para Gestão)
    if nome_biblioteca == "Gestão Escolar":
        conformidade["total"] += 1
        if "Função " in props:
            funcoes = props["Função "].get("multi_select", [])
            if funcoes:
                conformidade["pontos"] += 1
            else:
                conformidade["problemas"].append("⚠️ Função vazia")
        else:
            conformidade["problemas"].append("⚠️ Função: ausente")
    
    # Calcular percentual
    if conformidade["total"] > 0:
        conformidade["percentual"] = (conformidade["pontos"] / conformidade["total"]) * 100
    else:
        conformidade["percentual"] = 0
    
    return conformidade

def gerar_relatorio_final(conformidades_gestao, conformidades_aluno):
    """Gera relatório final de conformidade"""
    
    print_secao("Relatório Final de Conformidade")
    
    # Estatísticas Gestão
    total_gestao = len(conformidades_gestao)
    conformes_gestao = len([c for c in conformidades_gestao if c["percentual"] >= 80])
    media_gestao = sum(c["percentual"] for c in conformidades_gestao) / total_gestao if total_gestao > 0 else 0
    
    # Estatísticas Aluno
    total_aluno = len(conformidades_aluno)
    conformes_aluno = len([c for c in conformidades_aluno if c["percentual"] >= 80])
    media_aluno = sum(c["percentual"] for c in conformidades_aluno) / total_aluno if total_aluno > 0 else 0
    
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
        "gestao": {
            "total": total_gestao,
            "conformes": conformes_gestao,
            "media": media_gestao,
            "conformidades": conformidades_gestao
        },
        "aluno": {
            "total": total_aluno,
            "conformes": conformes_aluno,
            "media": media_aluno,
            "conformidades": conformidades_aluno
        },
        "geral": {
            "total": total_geral,
            "conformes": conformes_geral,
            "media": media_geral
        }
    }
    
    with open("docs/relatorio_conformidade_final.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Relatório salvo em: docs/relatorio_conformidade_final.json")

def main():
    print("="*60)
    print("VERIFICACAO FINAL COMPLETA - CONFORMIDADE BOILERPLATE")
    print("="*60)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Verificar biblioteca Gestão
    print_secao("Biblioteca Gestão Escolar")
    paginas_gestao = buscar_todas_paginas(DATABASE_GESTAO, "Gestão Escolar")
    
    conformidades_gestao = []
    for page in paginas_gestao:
        conformidade = verificar_conformidade_pagina(page, "Gestão Escolar")
        conformidades_gestao.append(conformidade)
        
        if conformidade["percentual"] < 80:
            print(f"\n📄 {conformidade['titulo'][:50]}... ({conformidade['percentual']:.1f}%)")
            for problema in conformidade["problemas"][:3]:  # Mostrar apenas 3 problemas
                print(f"   {problema}")
    
    # Verificar biblioteca Aluno
    print_secao("Biblioteca Editorial Aluno")
    paginas_aluno = buscar_todas_paginas(DATABASE_ALUNO, "Editorial Alunos PRÉ-ENEM")
    
    conformidades_aluno = []
    for page in paginas_aluno:
        conformidade = verificar_conformidade_pagina(page, "Editorial Alunos PRÉ-ENEM")
        conformidades_aluno.append(conformidade)
        
        if conformidade["percentual"] < 80:
            print(f"\n📄 {conformidade['titulo'][:50]}... ({conformidade['percentual']:.1f}%)")
            for problema in conformidade["problemas"][:3]:  # Mostrar apenas 3 problemas
                print(f"   {problema}")
    
    # Gerar relatório final
    gerar_relatorio_final(conformidades_gestao, conformidades_aluno)
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()

