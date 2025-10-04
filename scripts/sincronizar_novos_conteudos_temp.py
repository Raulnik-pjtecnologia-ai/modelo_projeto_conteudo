#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Sincronizar Novos Conteúdos com Notion
Sincroniza os 8 novos conteúdos criados com a biblioteca Editorial de Aluno
"""

import os
import sys
import requests
import json
from datetime import datetime
import time

sys.stdout.reconfigure(encoding='utf-8')

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
if not NOTION_TOKEN:
    print("ERRO: Configure NOTION_TOKEN")
    sys.exit(1)

# ID da biblioteca Editorial de Aluno (PRÉ-ENEM)
DATABASE_ALUNO = "2695113a-91a3-81dd-bfc4-fc8e4df72e7f"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def print_secao(titulo):
    print("\n" + "="*80)
    print(titulo)
    print("="*80)

def ler_arquivo_markdown(caminho_arquivo):
    """Lê arquivo markdown e retorna conteúdo"""
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Erro ao ler arquivo {caminho_arquivo}: {e}")
        return None

def extrair_titulo_do_conteudo(conteudo):
    """Extrai título do conteúdo markdown"""
    linhas = conteudo.split('\n')
    for linha in linhas:
        if linha.startswith('# '):
            return linha[2:].strip()
    return "Título não encontrado"

def converter_markdown_para_notion_blocks(conteudo):
    """Converte markdown para blocos do Notion"""
    blocos = []
    linhas = conteudo.split('\n')
    
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
            
        if linha.startswith('# '):
            # Título principal
            titulo = linha[2:].strip()
            blocos.append({
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": titulo}}]
                }
            })
        elif linha.startswith('## '):
            # Subtítulo
            subtitulo = linha[3:].strip()
            blocos.append({
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": subtitulo}}]
                }
            })
        elif linha.startswith('### '):
            # Sub-subtítulo
            subsubtitulo = linha[4:].strip()
            blocos.append({
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": subsubtitulo}}]
                }
            })
        elif linha.startswith('- '):
            # Lista
            item = linha[2:].strip()
            blocos.append({
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": item}}]
                }
            })
        elif linha.startswith('**') and linha.endswith('**'):
            # Texto em negrito
            texto = linha[2:-2].strip()
            blocos.append({
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": texto}}]
                }
            })
        elif linha.startswith('![') and '](' in linha:
            # Imagem
            start = linha.find('](') + 2
            end = linha.find(')', start)
            if start > 1 and end > start:
                image_url = linha[start:end]
                blocos.append({
                    "type": "image",
                    "image": {
                        "type": "external",
                        "external": {
                            "url": image_url
                        }
                    }
                })
        elif linha.startswith('*') and linha.endswith('*'):
            # Texto em itálico
            texto = linha[1:-1].strip()
            blocos.append({
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": texto}}]
                }
            })
        else:
            # Parágrafo normal
            if linha:
                blocos.append({
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": linha}}]
                    }
                })
    
    return blocos

def criar_pagina_notion(database_id, titulo, conteudo):
    """Cria nova página no Notion"""
    print(f"📝 Criando página: {titulo}")
    
    # Converter markdown para blocos
    blocos = converter_markdown_para_notion_blocks(conteudo)
    
    # Criar página
    url = f"https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Title": {
                "title": [
                    {
                        "type": "text",
                        "text": {"content": titulo}
                    }
                ]
            },
            "Status Editorial": {
                "select": {"name": "Aprovado"}
            },
            "Status": {
                "select": {"name": "Publicado"}
            },
            "Prioridade": {
                "select": {"name": "Alta"}
            },
            "Tags Área": {
                "multi_select": [{"name": "Geral"}]
            },
            "Tags Tipo": {
                "multi_select": [{"name": "Guia"}]
            },
            "Tags Tema": {
                "multi_select": [
                    {"name": "ENEM"},
                    {"name": "Estudos"},
                    {"name": "Preparação"},
                    {"name": "Alunos"},
                    {"name": "Educação"},
                    {"name": "2025"}
                ]
            },
            "Função Alvo": {
                "multi_select": [
                    {"name": "Pedagógica"},
                    {"name": "Estratégica"}
                ]
            },
            "Público Alvo": {
                "multi_select": [
                    {"name": "Estudantes ENEM"},
                    {"name": "Pré-vestibulandos"}
                ]
            },
            "Comentários": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": f"Conteúdo criado e sincronizado em {datetime.now().strftime('%d/%m/%Y %H:%M')} - Aplicação das 5 regras estabelecidas"
                        }
                    }
                ]
            }
        },
        "children": blocos[:100]  # Limitar a 100 blocos por vez
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    
    if response.status_code != 200:
        print(f"❌ Erro ao criar página: {response.status_code}")
        print(f"Resposta: {response.text}")
        return None
    
    data = response.json()
    page_id = data["id"]
    print(f"✅ Página criada com sucesso: {page_id}")
    
    # Adicionar blocos restantes se houver
    if len(blocos) > 100:
        adicionar_blocos_restantes(page_id, blocos[100:])
    
    return page_id

def adicionar_blocos_restantes(page_id, blocos_restantes):
    """Adiciona blocos restantes à página"""
    if not blocos_restantes:
        return
    
    print(f"📝 Adicionando {len(blocos_restantes)} blocos restantes...")
    
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    
    # Adicionar em lotes de 100
    for i in range(0, len(blocos_restantes), 100):
        lote = blocos_restantes[i:i+100]
        payload = {"children": lote}
        
        response = requests.patch(url, headers=HEADERS, json=payload)
        
        if response.status_code != 200:
            print(f"❌ Erro ao adicionar blocos: {response.status_code}")
            return
        
        print(f"✅ Lote {i//100 + 1} adicionado com sucesso")

def processar_sincronizacao_novos_conteudos(database_id):
    """Processa sincronização de todos os novos conteúdos"""
    print_secao("SINCRONIZAÇÃO DE NOVOS CONTEÚDOS")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Sincronizar 8 novos conteúdos com Notion")
    
    # Lista de arquivos para sincronizar
    arquivos_conteudo = [
        "2_conteudo/02_conteudos_prontos/biologia_enem_2025_genetica_evolucao.md",
        "2_conteudo/02_conteudos_prontos/historia_enem_2025_brasil_republica.md",
        "2_conteudo/02_conteudos_prontos/geografia_enem_2025_geografia_fisica.md",
        "2_conteudo/02_conteudos_prontos/estrategias_estudo_enem_2025_guia_completo.md",
        "2_conteudo/02_conteudos_prontos/abordagem_interdisciplinar_enem_2025.md",
        "2_conteudo/02_conteudos_prontos/sistema_monitoramento_progresso_enem_2025.md",
        "2_conteudo/02_conteudos_prontos/bem_estar_saude_mental_enem_2025.md",
        "2_conteudo/02_conteudos_prontos/matematica_enem_formulas_essenciais.md"
    ]
    
    sucessos = 0
    erros = 0
    paginas_criadas = []
    
    for i, arquivo in enumerate(arquivos_conteudo, 1):
        print(f"\n--- Arquivo {i}/{len(arquivos_conteudo)} ---")
        print(f"Arquivo: {arquivo}")
        
        # Ler conteúdo do arquivo
        conteudo = ler_arquivo_markdown(arquivo)
        if not conteudo:
            erros += 1
            continue
        
        # Extrair título
        titulo = extrair_titulo_do_conteudo(conteudo)
        print(f"Título: {titulo}")
        
        # Criar página no Notion
        page_id = criar_pagina_notion(database_id, titulo, conteudo)
        if page_id:
            sucessos += 1
            paginas_criadas.append({"titulo": titulo, "id": page_id})
        else:
            erros += 1
        
        time.sleep(2)  # Pausa para não sobrecarregar a API
    
    # Relatório final
    print_secao("RELATÓRIO FINAL")
    print(f"📊 Total de arquivos processados: {len(arquivos_conteudo)}")
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Erros: {erros}")
    print(f"📈 Taxa de sucesso: {(sucessos/len(arquivos_conteudo)*100):.1f}%")
    
    if paginas_criadas:
        print(f"\n📄 Páginas criadas:")
        for pagina in paginas_criadas:
            print(f"   - {pagina['titulo']} ({pagina['id']})")
    
    if sucessos == len(arquivos_conteudo):
        print("🎉 SINCRONIZAÇÃO COMPLETA COM SUCESSO!")
    else:
        print("⚠️ Alguns arquivos precisam de atenção manual")

if __name__ == "__main__":
    processar_sincronizacao_novos_conteudos(DATABASE_ALUNO)
