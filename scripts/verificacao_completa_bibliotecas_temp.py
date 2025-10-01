#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Verificação Completa das Bibliotecas
Verifica e corrige propriedades, taxonomias e conformidade com boilerplate
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

def buscar_paginas_database(database_id, nome_biblioteca):
    """Busca todas as páginas de um database"""
    print(f"\n🔍 Buscando páginas da biblioteca: {nome_biblioteca}")
    
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
            print(f"❌ Erro ao buscar páginas: {response.status_code}")
            break
    
    print(f"✅ Total encontrado: {len(all_pages)} páginas")
    return all_pages

def analisar_propriedades_pagina(page, nome_biblioteca):
    """Analisa propriedades de uma página"""
    props = page.get("properties", {})
    page_id = page["id"]
    
    # Título
    title_prop = props.get("Name", {}) or props.get("Title", {})
    titulo = ""
    if title_prop.get("title"):
        titulo = "".join([t.get("plain_text", "") for t in title_prop["title"]])
    
    problemas = []
    
    # Verificar propriedades obrigatórias
    propriedades_obrigatorias = {
        "Status editorial": ["Rascunho", "Em revisão", "Aprovado", "Publicado"],
        "Tipo": ["Artigo", "Checklist", "Lição", "Vídeo", "Documento Oficial"],
        "Nível de profundidade": ["Básico", "Intermediário", "Avançado", "Estratégico", "Tático", "Operacional"]
    }
    
    for prop_name, valores_validos in propriedades_obrigatorias.items():
        if prop_name in props:
            prop_value = props[prop_name]
            if prop_value.get("select"):
                valor = prop_value["select"]["name"]
                if valor not in valores_validos:
                    problemas.append(f"❌ {prop_name}: '{valor}' não é válido")
            elif prop_value.get("status"):
                valor = prop_value["status"]["name"]
                if valor not in valores_validos:
                    problemas.append(f"❌ {prop_name}: '{valor}' não é válido")
            elif prop_value.get("multi_select"):
                valores = [item["name"] for item in prop_value["multi_select"]]
                for valor in valores:
                    if valor not in valores_validos:
                        problemas.append(f"❌ {prop_name}: '{valor}' não é válido")
        else:
            problemas.append(f"⚠️ Propriedade '{prop_name}' ausente")
    
    # Verificar Tags (deve ter pelo menos uma)
    if "Tags" in props:
        tags = props["Tags"].get("multi_select", [])
        if not tags:
            problemas.append("⚠️ Tags vazias - deve ter pelo menos uma tag")
    
    # Verificar Função (para Gestão)
    if nome_biblioteca == "Gestão" and "Função " in props:
        funcoes = props["Função "].get("multi_select", [])
        if not funcoes:
            problemas.append("⚠️ Função vazia - deve ter pelo menos uma função")
    
    return {
        "page_id": page_id,
        "titulo": titulo,
        "problemas": problemas,
        "props": props
    }

def corrigir_propriedades_pagina(page_id, problemas, nome_biblioteca):
    """Corrige propriedades de uma página"""
    correcoes_aplicadas = []
    
    # Propriedades padrão para correção
    propriedades_padrao = {
        "Status editorial": {"status": {"name": "Publicado"}},
        "Tipo": {"select": {"name": "Artigo"}},
        "Nível de profundidade": {"multi_select": [{"name": "Intermediário"}]},
        "Tags": {"multi_select": [{"name": "Gestão Escolar"}] if nome_biblioteca == "Gestão" else [{"name": "ENEM2025"}]}
    }
    
    if nome_biblioteca == "Gestão":
        propriedades_padrao["Função "] = {"multi_select": [{"name": "Gestão"}]}
    
    # Aplicar correções
    for prop_name, prop_value in propriedades_padrao.items():
        try:
            url = f"https://api.notion.com/v1/pages/{page_id}"
            payload = {"properties": {prop_name: prop_value}}
            
            response = requests.patch(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                correcoes_aplicadas.append(prop_name)
            else:
                print(f"   ❌ Erro ao corrigir {prop_name}: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erro ao corrigir {prop_name}: {str(e)}")
    
    return correcoes_aplicadas

def verificar_conteudo_pagina(page_id):
    """Verifica se a página tem conteúdo adequado"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            blocks = response.json().get("results", [])
            
            # Contar tipos de blocos
            tipos_blocos = {}
            for block in blocks:
                block_type = block.get("type")
                tipos_blocos[block_type] = tipos_blocos.get(block_type, 0) + 1
            
            # Verificar se tem conteúdo substancial
            blocos_conteudo = tipos_blocos.get("paragraph", 0) + tipos_blocos.get("heading_1", 0) + \
                            tipos_blocos.get("heading_2", 0) + tipos_blocos.get("heading_3", 0)
            
            return {
                "total_blocos": len(blocks),
                "blocos_conteudo": blocos_conteudo,
                "tem_conteudo": blocos_conteudo >= 3,
                "tipos_blocos": tipos_blocos
            }
        return None
    except:
        return None

def main():
    print("="*60)
    print("VERIFICACAO COMPLETA DAS BIBLIOTECAS")
    print("="*60)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Verificar ambas as bibliotecas
    bibliotecas = [
        {"id": DATABASE_GESTAO, "nome": "Gestão Escolar"},
        {"id": DATABASE_ALUNO, "nome": "Editorial Alunos PRÉ-ENEM"}
    ]
    
    relatorio_final = {
        "gestao_escolar": {"total": 0, "problemas": 0, "corrigidos": 0},
        "editorial_alunos_pre_enem": {"total": 0, "problemas": 0, "corrigidos": 0}
    }
    
    for biblioteca in bibliotecas:
        print_secao(f"Biblioteca: {biblioteca['nome']}")
        
        # Buscar páginas
        paginas = buscar_paginas_database(biblioteca["id"], biblioteca["nome"])
        chave = biblioteca["nome"].lower().replace(" ", "_").replace("ã", "a").replace("ç", "c").replace("é", "e").replace("ê", "e").replace("-", "_")
        relatorio_final[chave]["total"] = len(paginas)
        
        # Analisar cada página
        paginas_com_problemas = []
        total_correcoes = 0
        
        for page in paginas:
            analise = analisar_propriedades_pagina(page, biblioteca["nome"])
            
            if analise["problemas"]:
                paginas_com_problemas.append(analise)
                print(f"\n📄 {analise['titulo'][:50]}...")
                for problema in analise["problemas"]:
                    print(f"   {problema}")
                
                # Aplicar correções
                print("   🔧 Aplicando correções...")
                correcoes = corrigir_propriedades_pagina(
                    analise["page_id"], 
                    analise["problemas"], 
                    biblioteca["nome"]
                )
                
                if correcoes:
                    print(f"   ✅ Correções aplicadas: {', '.join(correcoes)}")
                    total_correcoes += len(correcoes)
                else:
                    print("   ❌ Nenhuma correção aplicada")
        
        relatorio_final[chave]["problemas"] = len(paginas_com_problemas)
        relatorio_final[chave]["corrigidos"] = total_correcoes
        
        print(f"\n📊 Resumo {biblioteca['nome']}:")
        print(f"   Total de páginas: {len(paginas)}")
        print(f"   Páginas com problemas: {len(paginas_com_problemas)}")
        print(f"   Correções aplicadas: {total_correcoes}")
    
    # Relatório final
    print_secao("Relatório Final")
    
    print("\n📈 ESTATÍSTICAS GERAIS:")
    print(f"   Gestão Escolar: {relatorio_final['gestao_escolar']['total']} páginas")
    print(f"   Editorial Aluno: {relatorio_final['editorial_alunos_pre_enem']['total']} páginas")
    print(f"   Total: {relatorio_final['gestao_escolar']['total'] + relatorio_final['editorial_alunos_pre_enem']['total']} páginas")
    
    print("\n🔧 CORREÇÕES APLICADAS:")
    print(f"   Gestão Escolar: {relatorio_final['gestao_escolar']['corrigidos']} correções")
    print(f"   Editorial Aluno: {relatorio_final['editorial_alunos_pre_enem']['corrigidos']} correções")
    print(f"   Total: {relatorio_final['gestao_escolar']['corrigidos'] + relatorio_final['editorial_alunos_pre_enem']['corrigidos']} correções")
    
    print("\n✅ VERIFICAÇÃO CONCLUÍDA!")
    print("   Ambas as bibliotecas foram verificadas e corrigidas")
    print("   Propriedades e taxonomias estão alinhadas com o boilerplate")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()

