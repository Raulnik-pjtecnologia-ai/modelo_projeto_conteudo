#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Análise do Editorial Alunos PRÉ-ENEM
Identifica conteúdos existentes, lacunas e oportunidades
"""

import requests
import json
import sys

# Configurar encoding
sys.stdout.reconfigure(encoding='utf-8')

# Credenciais (usar variáveis de ambiente)
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
DATABASE_ID = "2695113a-91a3-81dd-bfc4-fc8e4df72e7f"  # Editorial Alunos PRÉ-ENEM

if not NOTION_TOKEN:
    print("ERRO: Variável de ambiente NOTION_TOKEN não configurada")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def buscar_conteudos():
    """Busca todos os conteúdos do Editorial Alunos PRÉ-ENEM"""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    
    print("\nBuscando conteudos do Editorial Alunos PRE-ENEM...")
    
    all_results = []
    has_more = True
    start_cursor = None
    
    while has_more:
        payload = {}
        if start_cursor:
            payload["start_cursor"] = start_cursor
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            all_results.extend(data.get("results", []))
            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")
        else:
            print(f"Erro ao buscar dados: {response.status_code}")
            print(response.text)
            break
    
    return all_results

def analisar_conteudos(pages):
    """Analisa a distribuição dos conteúdos"""
    categorias = {}
    tipos = {}
    status_dist = {}
    titulos = []
    
    for page in pages:
        props = page.get("properties", {})
        
        # Título
        title_prop = props.get("Title", {}) or props.get("title", {}) or props.get("Nome", {})
        if title_prop.get("title"):
            titulo = "".join([t.get("plain_text", "") for t in title_prop["title"]])
            if titulo:
                titulos.append(titulo)
        
        # Categoria
        cat_prop = props.get("Categoria", {}) or props.get("categoria", {})
        if cat_prop.get("select"):
            cat = cat_prop["select"].get("name", "Sem Categoria")
            categorias[cat] = categorias.get(cat, 0) + 1
        
        # Tipo
        tipo_prop = props.get("Tipo", {}) or props.get("tipo", {})
        if tipo_prop.get("select"):
            tipo = tipo_prop["select"].get("name", "Sem Tipo")
            tipos[tipo] = tipos.get(tipo, 0) + 1
        
        # Status
        status_prop = props.get("Status", {}) or props.get("status", {})
        if status_prop.get("select"):
            st = status_prop["select"].get("name", "Sem Status")
            status_dist[st] = status_dist.get(st, 0) + 1
    
    return categorias, tipos, status_dist, titulos

def identificar_lacunas(titulos):
    """Identifica lacunas de conteúdo baseado nos títulos existentes"""
    
    # Temas essenciais para PRÉ-ENEM
    temas_essenciais = [
        "Cronograma de Estudos",
        "Organização de Tempo",
        "Técnicas de Memorização",
        "Redação Nota 1000",
        "Estratégias de Prova",
        "Revisão de Matemática",
        "Revisão de Português",
        "Revisão de Ciências",
        "Revisão de Humanas",
        "Dia da Prova",
        "Ansiedade e Estresse",
        "Alimentação para Estudos",
        "Sono e Descanso",
        "Simulados",
        "Análise de Desempenho"
    ]
    
    lacunas = []
    for tema in temas_essenciais:
        # Verifica se há algum título relacionado
        encontrado = False
        for titulo in titulos:
            if any(palavra.lower() in titulo.lower() for palavra in tema.split()):
                encontrado = True
                break
        
        if not encontrado:
            lacunas.append(tema)
    
    return lacunas

def main():
    print("="*60)
    print("ANALISE DO EDITORIAL ALUNOS PRE-ENEM")
    print("="*60)
    
    # Buscar conteúdos
    pages = buscar_conteudos()
    
    if not pages:
        print("\nNenhum conteudo encontrado no database.")
        return
    
    print(f"\nTotal de conteudos encontrados: {len(pages)}")
    
    # Analisar distribuição
    categorias, tipos, status_dist, titulos = analisar_conteudos(pages)
    
    print("\n" + "="*60)
    print("DISTRIBUICAO POR CATEGORIA")
    print("="*60)
    for cat, count in sorted(categorias.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count}")
    
    print("\n" + "="*60)
    print("DISTRIBUICAO POR TIPO")
    print("="*60)
    for tipo, count in sorted(tipos.items(), key=lambda x: x[1], reverse=True):
        print(f"  {tipo}: {count}")
    
    print("\n" + "="*60)
    print("DISTRIBUICAO POR STATUS")
    print("="*60)
    for st, count in sorted(status_dist.items(), key=lambda x: x[1], reverse=True):
        print(f"  {st}: {count}")
    
    # Identificar lacunas
    print("\n" + "="*60)
    print("LACUNAS IDENTIFICADAS")
    print("="*60)
    lacunas = identificar_lacunas(titulos)
    
    if lacunas:
        print(f"\nForam identificadas {len(lacunas)} lacunas de conteudo:")
        for i, lacuna in enumerate(lacunas, 1):
            print(f"  {i}. {lacuna}")
    else:
        print("\nNenhuma lacuna critica identificada.")
    
    # Salvar dados
    dados_analise = {
        "total": len(pages),
        "categorias": categorias,
        "tipos": tipos,
        "status": status_dist,
        "titulos": titulos,
        "lacunas": lacunas,
        "pages": pages
    }
    
    with open("analise_editorial_pre_enem.json", "w", encoding="utf-8") as f:
        json.dump(dados_analise, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*60)
    print("RECOMENDACOES")
    print("="*60)
    
    if len(lacunas) > 0:
        print(f"\nRecomenda-se criar conteudo sobre:")
        for i, lacuna in enumerate(lacunas[:5], 1):
            print(f"  {i}. {lacuna}")
    
    print("\nDados completos salvos em: analise_editorial_pre_enem.json")
    print("\n" + "="*60)

if __name__ == "__main__":
    main()

