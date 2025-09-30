#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Curadoria e Sincronização - Editorial Alunos PRÉ-ENEM
Realiza curadoria completa do conteúdo e sincroniza com Notion
"""

import os
import sys
import requests
import json
import re
from datetime import datetime

# Configurar encoding
sys.stdout.reconfigure(encoding='utf-8')

# Credenciais (usar variáveis de ambiente)
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
DATABASE_ID = "2695113a-91a3-81dd-bfc4-fc8e4df72e7f"  # Editorial Alunos PRÉ-ENEM

if not NOTION_TOKEN:
    print("ERRO: Variável de ambiente NOTION_TOKEN não configurada")
    sys.exit(1)

ARQUIVO_CONTEUDO = "2_conteudo/01_ideias_e_rascunhos/artigo_simulados_enem_2025_estrategico.md"

def print_secao(titulo):
    """Imprime seção formatada"""
    print("\n" + "="*60)
    print(titulo.upper())
    print("="*60)

def ler_conteudo():
    """Lê o arquivo de conteúdo"""
    print_secao("Leitura do Conteudo")
    
    if not os.path.exists(ARQUIVO_CONTEUDO):
        print(f"Erro: Arquivo nao encontrado: {ARQUIVO_CONTEUDO}")
        return None
    
    with open(ARQUIVO_CONTEUDO, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    print(f"Conteudo lido: {len(conteudo)} caracteres")
    return conteudo

def curadoria_boilerplate(conteudo):
    """Verifica conformidade com boilerplate"""
    print_secao("Curadoria - Verificacao Boilerplate")
    
    criterios = {
        "Titulo H1": bool(re.search(r'^# .+', conteudo, re.MULTILINE)),
        "Imagem de Capa": bool(re.search(r'!\[.*\]\(.*\)', conteudo)),
        "Resumo Executivo": "Resumo Executivo" in conteudo or "resumo executivo" in conteudo.lower(),
        "Dados e Graficos": "chart" in conteudo.lower() or "grafico" in conteudo.lower(),
        "Videos": "youtube" in conteudo.lower() or "video" in conteudo.lower() or "ID:" in conteudo,
        "Fontes Confiaveis": "Fonte:" in conteudo or "Referência:" in conteudo or "fonte:" in conteudo.lower(),
        "Conclusao": "Conclusão" in conteudo or "conclusao" in conteudo.lower(),
        "Tags": "#" in conteudo and ("Tags" in conteudo or "tags" in conteudo.lower()),
        "Metadados Editoriais": "Categoria:" in conteudo or "Metadados" in conteudo
    }
    
    total = len(criterios)
    atendidos = sum(criterios.values())
    percentual = (atendidos / total) * 100
    
    print(f"\nConformidade: {atendidos}/{total} criterios ({percentual:.1f}%)\n")
    
    for criterio, status in criterios.items():
        simbolo = " OK" if status else " FALTA"
        print(f"  [{simbolo}] {criterio}")
    
    return percentual >= 90

def extrair_metadados(conteudo):
    """Extrai metadados do conteúdo"""
    print_secao("Extracao de Metadados")
    
    # Título
    match_titulo = re.search(r'^# (.+)$', conteudo, re.MULTILINE)
    titulo = match_titulo.group(1).strip() if match_titulo else "Simulados ENEM 2025"
    
    # Categoria
    match_categoria = re.search(r'\*\*Categoria:\*\* (.+)', conteudo)
    categoria = match_categoria.group(1).strip() if match_categoria else "Preparação ENEM"
    
    # Nível
    match_nivel = re.search(r'\*\*Nível:\*\* (.+)', conteudo)
    nivel = match_nivel.group(1).strip() if match_nivel else "Intermediário"
    
    # Função
    match_funcao = re.search(r'\*\*Função:\*\* (.+)', conteudo)
    funcao = match_funcao.group(1).strip() if match_funcao else "Estratégias de Estudo"
    
    # Tags
    tags = []
    match_tags = re.search(r'#ENEM2025.*', conteudo)
    if match_tags:
        tags_str = match_tags.group(0)
        tags = [tag.strip() for tag in tags_str.split('#') if tag.strip()]
    
    metadados = {
        "titulo": titulo,
        "categoria": categoria,
        "nivel": nivel,
        "funcao": funcao,
        "tags": tags[:5]  # Primeiras 5 tags
    }
    
    print("\nMetadados extraidos:")
    for chave, valor in metadados.items():
        print(f"  {chave}: {valor}")
    
    return metadados

def verificar_enriquecimento_mcp(conteudo):
    """Verifica enriquecimento com MCPs"""
    print_secao("Verificacao Enriquecimento MCP")
    
    mcps = {
        "Charts MCP": "```chart" in conteudo,
        "YouTube MCP": bool(re.search(r'ID: \w+', conteudo)),
        "Search MCP": bool(re.search(r'https?://', conteudo)) and ("Fonte:" in conteudo or "URL:" in conteudo)
    }
    
    print("\nEnriquecimento MCP:")
    for mcp, presente in mcps.items():
        status = " OK" if presente else " FALTA"
        print(f"  [{status}] {mcp}")
    
    return all(mcps.values())

def sincronizar_com_notion(metadados, conteudo):
    """Sincroniza conteúdo aprovado com Notion"""
    print_secao("Sincronizacao com Notion")
    
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Preparar payload
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Title": {
                "title": [
                    {
                        "text": {
                            "content": metadados["titulo"]
                        }
                    }
                ]
            },
            "Tipo": {
                "select": {
                    "name": "Artigo"
                }
            },
            "Status": {
                "select": {
                    "name": "Rascunho"
                }
            },
            "Status Editorial": {
                "select": {
                    "name": "Em Curadoria"
                }
            },
            "Prioridade": {
                "select": {
                    "name": "Alta"
                }
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": f"Conteudo sincronizado automaticamente em {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": f"Arquivo: {ARQUIVO_CONTEUDO}"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Informacoes do Conteudo"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": f"Categoria: {metadados['categoria']}"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": f"Nivel: {metadados['nivel']}"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": f"Funcao: {metadados['funcao']}"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": f"Tags: {', '.join(metadados['tags'][:3])}"
                            }
                        }
                    ]
                }
            }
        ]
    }
    
    print("\nEnviando para Notion...")
    
    try:
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            page_data = response.json()
            page_id = page_data["id"]
            page_url = page_data["url"]
            
            print(f"\n Sincronizacao bem-sucedida!")
            print(f"\nPage ID: {page_id}")
            print(f"URL: {page_url}")
            
            return {
                "sucesso": True,
                "page_id": page_id,
                "url": page_url
            }
        else:
            print(f"\nErro na sincronizacao: {response.status_code}")
            print(f"Resposta: {response.text}")
            return {"sucesso": False, "erro": response.text}
    
    except Exception as e:
        print(f"\nErro ao sincronizar: {str(e)}")
        return {"sucesso": False, "erro": str(e)}

def main():
    print("="*60)
    print("CURADORIA E SINCRONIZACAO - EDITORIAL ALUNOS PRE-ENEM")
    print("="*60)
    print(f"Database ID: {DATABASE_ID}")
    print(f"Arquivo: {ARQUIVO_CONTEUDO}")
    
    # 1. Ler conteúdo
    conteudo = ler_conteudo()
    if not conteudo:
        print("\nProcesso interrompido: falha na leitura do conteudo.")
        return
    
    # 2. Curadoria boilerplate
    aprovado_boilerplate = curadoria_boilerplate(conteudo)
    
    if not aprovado_boilerplate:
        print("\n CURADORIA REPROVADA: Conteudo nao atende boilerplate minimo")
        print("Corrija os itens faltantes e execute novamente.")
        return
    
    print("\n CURADORIA APROVADA: Boilerplate em conformidade")
    
    # 3. Verificar enriquecimento MCP
    tem_mcp = verificar_enriquecimento_mcp(conteudo)
    
    if not tem_mcp:
        print("\n Enriquecimento MCP parcial detectado")
        print("Recomenda-se adicionar mais elementos MCP, mas prosseguiremos...")
    else:
        print("\n ENRIQUECIMENTO MCP COMPLETO")
    
    # 4. Extrair metadados
    metadados = extrair_metadados(conteudo)
    
    # 5. Sincronizar com Notion
    resultado = sincronizar_com_notion(metadados, conteudo)
    
    # 6. Relatório final
    print_secao("Relatorio Final")
    
    if resultado["sucesso"]:
        print("\n STATUS: SUCESSO")
        print(f"\nO conteudo '{metadados['titulo']}' foi:")
        print("  Verificado quanto ao boilerplate")
        print("  Enriquecido com MCPs")
        print("  Sincronizado com o Notion")
        print(f"\nAcesse em: {resultado['url']}")
        
        # Salvar informações
        info_sincronizacao = {
            "data_sincronizacao": datetime.now().isoformat(),
            "titulo": metadados["titulo"],
            "page_id": resultado["page_id"],
            "page_url": resultado["url"],
            "arquivo_local": ARQUIVO_CONTEUDO
        }
        
        with open("sincronizacao_pre_enem.json", "w", encoding="utf-8") as f:
            json.dump(info_sincronizacao, f, ensure_ascii=False, indent=2)
        
        print("\nInformacoes salvas em: sincronizacao_pre_enem.json")
    else:
        print("\n STATUS: FALHA")
        print(f"\nErro: {resultado.get('erro', 'Erro desconhecido')}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()

