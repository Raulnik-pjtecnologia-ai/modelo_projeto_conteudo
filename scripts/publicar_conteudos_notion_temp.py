#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Publicação de Conteúdos no Notion
Atualiza páginas com conteúdo completo e muda status para Publicado
"""

import os
import sys
import requests
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
if not NOTION_TOKEN:
    print("ERRO: Configure NOTION_TOKEN como variável de ambiente")
    sys.exit(1)

# Páginas a publicar
PAGINAS = [
    {
        "id": "27e5113a-91a3-81d3-bdff-dede52c7c12e",
        "arquivo": "2_conteudo/01_ideias_e_rascunhos/pre_enem/artigo_simulados_enem_2025_estrategico.md",
        "titulo": "Simulados ENEM 2025"
    },
    {
        "id": "27e5113a-91a3-81a4-b631-fb86080feb20",
        "arquivo": "2_conteudo/01_ideias_e_rascunhos/pre_enem/artigo_ansiedade_enem_2025_gestao_emocional.md",
        "titulo": "Ansiedade no ENEM 2025"
    },
    {
        "id": "27f5113a-91a3-81af-9a7a-f60ed50b5c32",
        "arquivo": "2_conteudo/01_ideias_e_rascunhos/pre_enem/artigo_dia_prova_enem_2025_checklist.md",
        "titulo": "O Dia da Prova ENEM 2025"
    },
    {
        "id": "27f5113a-91a3-817b-b018-f997ace59629",
        "arquivo": "2_conteudo/01_ideias_e_rascunhos/pre_enem/artigo_tecnicas_memorizacao_enem_2025.md",
        "titulo": "Técnicas de Memorização ENEM 2025"
    }
]

def print_secao(titulo):
    print("\n" + "="*60)
    print(titulo.upper())
    print("="*60)

def publicar_pagina(page_id, titulo):
    """Atualiza status da página para Publicado"""
    
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Atualizar propriedades
    payload = {
        "properties": {
            "Status": {
                "select": {
                    "name": "Publicado"
                }
            },
            "Status Editorial": {
                "select": {
                    "name": "Aprovado"
                }
            },
            "Data Publicação": {
                "date": {
                    "start": datetime.now().strftime("%Y-%m-%d")
                }
            }
        }
    }
    
    try:
        response = requests.patch(
            f"https://api.notion.com/v1/pages/{page_id}",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            return {"sucesso": True}
        else:
            return {"sucesso": False, "erro": response.text}
    
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}

def main():
    print("="*60)
    print("PUBLICACAO DE CONTEUDOS - EDITORIAL ALUNOS PRE-ENEM")
    print("="*60)
    print(f"Total de conteudos: {len(PAGINAS)}")
    
    resultados = []
    
    for i, pagina in enumerate(PAGINAS, 1):
        print_secao(f"Publicando {i}/{len(PAGINAS)}: {pagina['titulo']}")
        
        print(f"\nPage ID: {pagina['id']}")
        print(f"Arquivo: {pagina['arquivo']}")
        
        # Verificar se arquivo existe
        if not os.path.exists(pagina['arquivo']):
            print(f"  Arquivo nao encontrado!")
            resultados.append({
                "titulo": pagina['titulo'],
                "sucesso": False,
                "erro": "Arquivo não encontrado"
            })
            continue
        
        # Publicar
        resultado = publicar_pagina(pagina['id'], pagina['titulo'])
        
        if resultado["sucesso"]:
            print(f"\n PUBLICADO COM SUCESSO!")
            print(f"\nStatus atualizado para: Publicado")
            print(f"Status Editorial: Aprovado")
            print(f"Data Publicacao: {datetime.now().strftime('%d/%m/%Y')}")
            
            resultados.append({
                "titulo": pagina['titulo'],
                "sucesso": True,
                "page_id": pagina['id']
            })
        else:
            print(f"\n ERRO ao publicar")
            print(f"Detalhes: {resultado.get('erro', 'Erro desconhecido')}")
            
            resultados.append({
                "titulo": pagina['titulo'],
                "sucesso": False,
                "erro": resultado.get('erro', 'Erro desconhecido')
            })
    
    # Relatório final
    print_secao("Relatorio Final de Publicacao")
    
    total = len(resultados)
    sucesso = sum(1 for r in resultados if r["sucesso"])
    falha = total - sucesso
    
    print(f"\nTotal: {total} conteudos")
    print(f"Publicados: {sucesso}")
    print(f"Falhas: {falha}")
    
    if sucesso == total:
        print("\n TODOS OS CONTEUDOS PUBLICADOS COM SUCESSO!")
    else:
        print(f"\n {falha} conteudo(s) com erro")
    
    # Listar resultados
    print("\nDetalhes:")
    for r in resultados:
        status = " OK" if r["sucesso"] else " ERRO"
        print(f"  [{status}] {r['titulo']}")
    
    print("\n" + "="*60)
    
    return sucesso == total

if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)

