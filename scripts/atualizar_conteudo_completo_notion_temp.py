#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Atualizar Conteúdo Completo no Notion
Substitui conteúdo básico pelo markdown completo dos arquivos
"""

import os
import sys
import requests
import re

sys.stdout.reconfigure(encoding='utf-8')

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
if not NOTION_TOKEN:
    print("ERRO: Configure NOTION_TOKEN")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def converter_markdown_para_notion(markdown_text):
    """Converte markdown para formato Notion (simplificado)"""
    
    # Remover YAML frontmatter se existir
    markdown_text = re.sub(r'^---\n.*?\n---\n', '', markdown_text, flags=re.DOTALL)
    
    # Remover imagens markdown (Notion não suporta diretamente)
    markdown_text = re.sub(r'!\[.*?\]\(.*?\)', '', markdown_text)
    
    # Remover blocos de chart (já estão como referência)
    markdown_text = re.sub(r'```chart\n.*?```', '[Gráfico - ver versão web]', markdown_text, flags=re.DOTALL)
    
    # Limpar múltiplas linhas vazias
    markdown_text = re.sub(r'\n{3,}', '\n\n', markdown_text)
    
    return markdown_text.strip()

def atualizar_pagina_notion(page_id, conteudo_markdown, titulo):
    """Atualiza página do Notion com conteúdo completo"""
    
    print(f"\nProcessando: {titulo}")
    print(f"Page ID: {page_id}")
    
    # Converter markdown
    conteudo_limpo = converter_markdown_para_notion(conteudo_markdown)
    
    # Dividir em seções (por ##)
    secoes = re.split(r'\n## ', conteudo_limpo)
    
    # Primeira seção (antes do primeiro ##)
    intro = secoes[0].strip()
    
    # Preparar blocos para Notion
    blocks = []
    
    # Adicionar introdução/resumo
    if intro and len(intro) > 10:
        paragrafos_intro = intro.split('\n\n')
        for para in paragrafos_intro[:3]:  # Primeiros 3 parágrafos
            if para.strip() and '**Tempo de leitura:**' not in para:
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": para.strip()[:2000]}  # Limite de 2000 chars
                        }]
                    }
                })
    
    # Adicionar seções principais (limitado a 5 para não exceder limites)
    for secao in secoes[1:6]:  # Primeiras 5 seções
        if not secao.strip():
            continue
            
        # Título da seção
        linhas = secao.split('\n', 1)
        titulo_secao = linhas[0].strip()
        
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": titulo_secao[:100]}
                }]
            }
        })
        
        # Conteúdo da seção (primeiros 2 parágrafos)
        if len(linhas) > 1:
            paragrafos = linhas[1].split('\n\n')
            for para in paragrafos[:2]:
                para_limpo = para.strip()
                if para_limpo and len(para_limpo) > 10:
                    # Verificar se é lista
                    if para_limpo.startswith('- ') or para_limpo.startswith('* '):
                        itens = [item.strip('- *').strip() for item in para_limpo.split('\n') if item.strip()]
                        for item in itens[:5]:  # Max 5 itens
                            blocks.append({
                                "object": "block",
                                "type": "bulleted_list_item",
                                "bulleted_list_item": {
                                    "rich_text": [{
                                        "type": "text",
                                        "text": {"content": item[:2000]}
                                    }]
                                }
                            })
                    else:
                        blocks.append({
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{
                                    "type": "text",
                                    "text": {"content": para_limpo[:2000]}
                                }]
                            }
                        })
    
    # Adicionar nota de rodapé
    blocks.append({
        "object": "block",
        "type": "divider",
        "divider": {}
    })
    
    blocks.append({
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": "📄 Para ver o conteúdo completo com gráficos interativos, tabelas detalhadas e formatação completa, consulte o arquivo local mencionado acima."
                }
            }],
            "icon": {"emoji": "ℹ️"},
            "color": "blue_background"
        }
    })
    
    # Limitar a 100 blocos (limite da API)
    blocks = blocks[:100]
    
    print(f"Preparados {len(blocks)} blocos de conteúdo")
    
    # Atualizar página
    try:
        # Primeiro, substituir todo o conteúdo
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        
        # Limpar conteúdo antigo (apenas os blocos básicos)
        response_get = requests.get(url, headers=headers)
        if response_get.status_code == 200:
            blocos_antigos = response_get.json().get("results", [])
            # Deletar primeiros blocos (info básica)
            for bloco in blocos_antigos[:5]:
                requests.delete(
                    f"https://api.notion.com/v1/blocks/{bloco['id']}",
                    headers=headers
                )
        
        # Adicionar novo conteúdo
        payload = {"children": blocks}
        response = requests.patch(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print(f" Conteúdo atualizado com sucesso!")
            return True
        else:
            print(f" Erro: {response.status_code}")
            print(f"Resposta: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f" Erro: {str(e)}")
        return False

def main():
    print("="*60)
    print("ATUALIZACAO DE CONTEUDO COMPLETO NO NOTION")
    print("="*60)
    
    # Conteúdos a atualizar
    conteudos = [
        {
            "page_id": "27e5113a-91a3-81d3-bdff-dede52c7c12e",
            "arquivo": "2_conteudo/04_publicado/artigo_simulados_enem_2025_estrategico.md",
            "titulo": "Simulados ENEM 2025"
        },
        {
            "page_id": "27e5113a-91a3-81a4-b631-fb86080feb20",
            "arquivo": "2_conteudo/04_publicado/artigo_ansiedade_enem_2025_gestao_emocional.md",
            "titulo": "Ansiedade no ENEM 2025"
        },
        {
            "page_id": "27f5113a-91a3-81af-9a7a-f60ed50b5c32",
            "arquivo": "2_conteudo/04_publicado/artigo_dia_prova_enem_2025_checklist.md",
            "titulo": "O Dia da Prova ENEM 2025"
        },
        {
            "page_id": "27f5113a-91a3-817b-b018-f997ace59629",
            "arquivo": "2_conteudo/04_publicado/artigo_tecnicas_memorizacao_enem_2025.md",
            "titulo": "Técnicas de Memorização ENEM 2025"
        }
    ]
    
    sucessos = 0
    falhas = 0
    
    for conteudo in conteudos:
        print(f"\n{'='*60}")
        
        # Ler arquivo
        if not os.path.exists(conteudo["arquivo"]):
            print(f"ERRO: Arquivo não encontrado: {conteudo['arquivo']}")
            falhas += 1
            continue
        
        with open(conteudo["arquivo"], 'r', encoding='utf-8') as f:
            markdown = f.read()
        
        # Atualizar
        sucesso = atualizar_pagina_notion(
            conteudo["page_id"],
            markdown,
            conteudo["titulo"]
        )
        
        if sucesso:
            sucessos += 1
        else:
            falhas += 1
    
    # Relatório final
    print(f"\n{'='*60}")
    print("RELATORIO FINAL")
    print("="*60)
    print(f"\nTotal processado: {len(conteudos)}")
    print(f" Sucessos: {sucessos}")
    print(f" Falhas: {falhas}")
    
    if sucessos == len(conteudos):
        print("\n TODOS OS CONTEUDOS ATUALIZADOS COM SUCESSO!")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()

