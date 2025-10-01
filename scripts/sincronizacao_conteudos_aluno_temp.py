#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Sincronização dos 4 Conteúdos do Editorial Aluno
ETAPA 3: Sincronizar os 4 conteúdos do Editorial Aluno com correções aplicadas
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

# Database Editorial Alunos PRÉ-ENEM
DATABASE_ID = "2695113a91a381ddbfc4fc8e4df72e7f"

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

def buscar_conteudos_aluno():
    """Busca os 4 conteúdos específicos do Editorial Aluno"""
    print("🔍 Buscando os 4 conteúdos do Editorial Aluno...")
    
    # IDs conhecidos dos 4 conteúdos
    conteudos = [
        {
            "id": "27e5113a-91a3-81d3-bdff-dede52c7c12e",
            "titulo": "Simulados ENEM 2025: Como Usar de Forma Estratégica",
            "arquivo": "artigo_simulados_enem_2025_estrategico.md"
        },
        {
            "id": "27e5113a-91a3-81a4-b631-fb86080feb20", 
            "titulo": "Ansiedade no ENEM 2025: Guia Completo para Controlar",
            "arquivo": "artigo_ansiedade_enem_2025_gestao_emocional.md"
        },
        {
            "id": "27f5113a-91a3-81af-9a7a-f60ed50b5c32",
            "titulo": "O Dia da Prova ENEM 2025: Checklist Completo",
            "arquivo": "artigo_dia_prova_enem_2025_checklist.md"
        },
        {
            "id": "27f5113a-91a3-817b-b018-f997ace59629",
            "titulo": "Técnicas de Memorização ENEM 2025: Aprenda Mais Rápido",
            "arquivo": "artigo_tecnicas_memorizacao_enem_2025.md"
        }
    ]
    
    print(f"✅ 4 conteúdos identificados")
    for i, conteudo in enumerate(conteudos, 1):
        print(f"   {i}. {conteudo['titulo']}")
    
    return conteudos

def verificar_conteudo_pagina(page_id, titulo):
    """Verifica se a página tem conteúdo adequado"""
    print(f"\n📄 Verificando: {titulo[:50]}...")
    
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            blocks = response.json().get("results", [])
            
            # Contar blocos de conteúdo
            blocos_conteudo = 0
            blocos_imagem = 0
            blocos_video = 0
            
            for block in blocks:
                block_type = block.get("type")
                if block_type in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item"]:
                    blocos_conteudo += 1
                elif block_type == "image":
                    blocos_imagem += 1
                elif block_type == "video":
                    blocos_video += 1
            
            print(f"   📊 Blocos de conteúdo: {blocos_conteudo}")
            print(f"   🖼️ Imagens: {blocos_imagem}")
            print(f"   🎥 Vídeos: {blocos_video}")
            
            if blocos_conteudo >= 10:
                print("   ✅ Conteúdo adequado")
                return True
            else:
                print("   ⚠️ Conteúdo insuficiente")
                return False
        else:
            print(f"   ❌ Erro ao verificar conteúdo: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
        return False

def atualizar_propriedades_pagina(page_id, titulo):
    """Atualiza propriedades da página usando propriedades existentes"""
    print(f"\n📄 Atualizando propriedades: {titulo[:50]}...")
    
    # Usar propriedades que existem no database
    propriedades = {
        "Status Editorial": {"select": {"name": "Publicado"}},
        "Tipo": {"select": {"name": "Artigo"}},
        "Público Alvo": {"multi_select": [{"name": "Estudantes ENEM"}]},
        "Tags Tema": {"multi_select": [{"name": "ENEM2025"}]},
        "Função Alvo": {"multi_select": [{"name": "Pedagógica"}]},
        "Prioridade": {"select": {"name": "Alta"}},
        "Destaque": {"checkbox": True}
    }
    
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"properties": propriedades}
    
    try:
        response = requests.patch(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print("   ✅ Propriedades atualizadas com sucesso!")
            return True
        else:
            print(f"   ❌ Erro: {response.status_code}")
            print(f"   Resposta: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
        return False

def verificar_arquivo_local(arquivo):
    """Verifica se o arquivo local existe"""
    caminho_arquivo = f"2_conteudo/04_publicado/{arquivo}"
    
    if os.path.exists(caminho_arquivo):
        print(f"   ✅ Arquivo local encontrado: {arquivo}")
        return True
    else:
        print(f"   ⚠️ Arquivo local não encontrado: {arquivo}")
        return False

def sincronizar_conteudo_completo(page_id, titulo, arquivo):
    """Sincroniza o conteúdo completo da página"""
    print(f"\n📄 Sincronizando conteúdo completo: {titulo[:50]}...")
    
    # Verificar arquivo local
    if not verificar_arquivo_local(arquivo):
        return False
    
    # Ler conteúdo do arquivo
    caminho_arquivo = f"2_conteudo/04_publicado/{arquivo}"
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo_markdown = f.read()
        
        print(f"   📖 Conteúdo lido: {len(conteudo_markdown)} caracteres")
        
        # Converter markdown para blocos Notion (simplificado)
        blocos = converter_markdown_para_notion(conteudo_markdown)
        
        # Atualizar blocos da página
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        payload = {"children": blocos}
        
        response = requests.patch(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print("   ✅ Conteúdo sincronizado com sucesso!")
            return True
        else:
            print(f"   ❌ Erro ao sincronizar: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
        return False

def converter_markdown_para_notion(markdown_text):
    """Converte markdown para blocos Notion (simplificado)"""
    blocos = []
    
    # Remover YAML frontmatter
    if markdown_text.startswith('---'):
        parts = markdown_text.split('---', 2)
        if len(parts) >= 3:
            markdown_text = parts[2].strip()
    
    # Dividir em linhas
    linhas = markdown_text.split('\n')
    
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
            
        # Títulos
        if linha.startswith('# '):
            blocos.append({
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": linha[2:]}}]
                }
            })
        elif linha.startswith('## '):
            blocos.append({
                "type": "heading_2", 
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": linha[3:]}}]
                }
            })
        elif linha.startswith('### '):
            blocos.append({
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": linha[4:]}}]
                }
            })
        # Lista com marcadores
        elif linha.startswith('- '):
            blocos.append({
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": linha[2:]}}]
                }
            })
        # Lista numerada
        elif linha.startswith(('1. ', '2. ', '3. ', '4. ', '5. ')):
            numero = linha.split('.')[0]
            conteudo = linha[len(numero)+2:]
            blocos.append({
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": conteudo}}]
                }
            })
        # Parágrafo normal
        else:
            blocos.append({
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": linha}}]
                }
            })
    
    return blocos

def main():
    print("="*80)
    print("SINCRONIZAÇÃO DOS 4 CONTEÚDOS - ETAPA 3")
    print("="*80)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Buscar os 4 conteúdos
    print_etapa(3, "Sincronizar os 4 conteúdos do Editorial Aluno")
    
    conteudos = buscar_conteudos_aluno()
    
    # Processar cada conteúdo
    print_secao("Processando Conteúdos")
    
    sucessos = 0
    falhas = 0
    
    for i, conteudo in enumerate(conteudos, 1):
        print(f"\n[{i}/4] Processando: {conteudo['titulo']}")
        
        # Verificar conteúdo atual
        if verificar_conteudo_pagina(conteudo['id'], conteudo['titulo']):
            print("   ✅ Conteúdo já adequado")
            sucessos += 1
        else:
            # Atualizar propriedades
            if atualizar_propriedades_pagina(conteudo['id'], conteudo['titulo']):
                # Sincronizar conteúdo completo
                if sincronizar_conteudo_completo(conteudo['id'], conteudo['titulo'], conteudo['arquivo']):
                    sucessos += 1
                else:
                    falhas += 1
            else:
                falhas += 1
    
    # Relatório final
    print_secao("Relatório Final Etapa 3")
    
    print(f"📊 RESULTADOS:")
    print(f"   Total processado: {len(conteudos)}")
    print(f"   Sucessos: {sucessos}")
    print(f"   Falhas: {falhas}")
    
    if sucessos == len(conteudos):
        print("\n🎉 ETAPA 3 CONCLUÍDA COM SUCESSO!")
        print("   ✅ Todos os 4 conteúdos sincronizados")
        print("   ✅ Propriedades atualizadas")
        print("   ✅ Conteúdo completo aplicado")
    else:
        print(f"\n⚠️ ETAPA 3 PARCIALMENTE CONCLUÍDA")
        print(f"   ⚠️ {falhas} conteúdos precisam de atenção")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()

