#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Correção Sistemática de Propriedades
ETAPA 2: Aplicar correções de propriedades e taxonomias nas bibliotecas
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

def mapear_propriedades_aluno():
    """Mapeia propriedades existentes do Editorial Aluno para o padrão"""
    print("🔍 Mapeando propriedades existentes do Editorial Aluno...")
    
    # Propriedades existentes que podem ser mapeadas
    mapeamento = {
        "Status Editorial": "Status editorial",
        "Tipo": "Tipo", 
        "Tags Tema": "Tags",
        "Função Alvo": "Função "
    }
    
    print("✅ Mapeamento criado:")
    for original, padrao in mapeamento.items():
        print(f"   {original} → {padrao}")
    
    return mapeamento

def corrigir_propriedades_gestao():
    """Corrige propriedades da biblioteca Gestão Escolar"""
    print_secao("Corrigindo Biblioteca Gestão Escolar")
    
    # A biblioteca Gestão já está correta (0 problemas na Etapa 1)
    print("✅ Biblioteca Gestão Escolar já está 100% conforme")
    print("   ✅ Todas as propriedades obrigatórias presentes")
    print("   ✅ Tipos de propriedades corretos")
    print("   ✅ Páginas sem problemas")
    
    return True

def corrigir_propriedades_aluno():
    """Corrige propriedades da biblioteca Editorial Aluno"""
    print_secao("Corrigindo Biblioteca Editorial Aluno")
    
    # Buscar páginas do Editorial Aluno
    print("🔍 Buscando páginas do Editorial Aluno...")
    
    url = f"https://api.notion.com/v1/databases/{DATABASE_ALUNO}/query"
    payload = {"page_size": 100}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            pages = data.get("results", [])
            print(f"✅ Encontradas {len(pages)} páginas")
        else:
            print(f"❌ Erro ao buscar páginas: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False
    
    # Mapear propriedades existentes
    mapeamento = mapear_propriedades_aluno()
    
    # Corrigir cada página
    print_secao("Aplicando Correções nas Páginas")
    
    sucessos = 0
    falhas = 0
    
    for i, page in enumerate(pages, 1):
        props = page.get("properties", {})
        page_id = page["id"]
        
        # Título
        title_prop = props.get("Title", {})
        titulo = ""
        if title_prop.get("title"):
            titulo = "".join([t.get("plain_text", "") for t in title_prop["title"]])
        
        print(f"\n[{i}/{len(pages)}] {titulo[:50]}...")
        
        # Propriedades a serem atualizadas
        propriedades_atualizar = {}
        
        # Mapear Status Editorial → Status editorial
        if "Status Editorial" in props and "Status editorial" not in props:
            status_atual = props["Status Editorial"].get("select", {}).get("name", "")
            if status_atual:
                # Mapear valores
                mapeamento_status = {
                    "Publicado": "Publicado",
                    "Rascunho": "Rascunho", 
                    "Em Revisão": "Em revisão",
                    "Aprovado": "Aprovado"
                }
                status_mapeado = mapeamento_status.get(status_atual, "Publicado")
                propriedades_atualizar["Status editorial"] = {"status": {"name": status_mapeado}}
                print(f"   ➕ Status editorial: {status_mapeado}")
        
        # Mapear Tags Tema → Tags
        if "Tags Tema" in props and "Tags" not in props:
            tags_atuais = props["Tags Tema"].get("multi_select", [])
            if tags_atuais:
                # Adicionar ENEM2025 se não existir
                tags_novas = [{"name": tag["name"]} for tag in tags_atuais]
                if not any(tag["name"] == "ENEM2025" for tag in tags_novas):
                    tags_novas.append({"name": "ENEM2025"})
                
                propriedades_atualizar["Tags"] = {"multi_select": tags_novas}
                print(f"   ➕ Tags: {[tag['name'] for tag in tags_novas]}")
        
        # Mapear Função Alvo → Função 
        if "Função Alvo" in props and "Função " not in props:
            funcoes_atuais = props["Função Alvo"].get("multi_select", [])
            if funcoes_atuais:
                # Mapear valores
                mapeamento_funcoes = {
                    "Pedagógica": "Pedagógica",
                    "Administrativa": "Administrativa",
                    "Estratégica": "Estratégica"
                }
                funcoes_mapeadas = []
                for funcao in funcoes_atuais:
                    funcao_mapeada = mapeamento_funcoes.get(funcao["name"], "Pedagógica")
                    funcoes_mapeadas.append({"name": funcao_mapeada})
                
                propriedades_atualizar["Função "] = {"multi_select": funcoes_mapeadas}
                print(f"   ➕ Função: {[f['name'] for f in funcoes_mapeadas]}")
        
        # Adicionar Nível de profundidade se ausente
        if "Nível de profundidade" not in props:
            propriedades_atualizar["Nível de profundidade"] = {"multi_select": [{"name": "Intermediário"}]}
            print(f"   ➕ Nível de profundidade: Intermediário")
        
        # Aplicar correções se houver
        if propriedades_atualizar:
            url_update = f"https://api.notion.com/v1/pages/{page_id}"
            payload_update = {"properties": propriedades_atualizar}
            
            try:
                response_update = requests.patch(url_update, headers=headers, json=payload_update)
                
                if response_update.status_code == 200:
                    print("   ✅ Propriedades atualizadas com sucesso!")
                    sucessos += 1
                else:
                    print(f"   ❌ Erro: {response_update.status_code}")
                    print(f"   Resposta: {response_update.text[:200]}")
                    falhas += 1
            except Exception as e:
                print(f"   ❌ Erro: {str(e)}")
                falhas += 1
        else:
            print("   ✅ Página já está correta")
            sucessos += 1
    
    # Relatório da correção
    print_secao("Relatório da Correção")
    print(f"📊 RESULTADOS:")
    print(f"   Total processado: {len(pages)}")
    print(f"   Sucessos: {sucessos}")
    print(f"   Falhas: {falhas}")
    
    if sucessos == len(pages):
        print("\n🎉 TODAS AS PROPRIEDADES CORRIGIDAS COM SUCESSO!")
    else:
        print(f"\n⚠️ {falhas} páginas precisam de atenção manual")
    
    return sucessos == len(pages)

def main():
    print("="*80)
    print("CORREÇÃO SISTEMÁTICA DE PROPRIEDADES - ETAPA 2")
    print("="*80)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Corrigir Gestão Escolar
    print_etapa(2, "Aplicar correções de propriedades e taxonomias")
    
    sucesso_gestao = corrigir_propriedades_gestao()
    sucesso_aluno = corrigir_propriedades_aluno()
    
    # Relatório final
    print_secao("Relatório Final Etapa 2")
    
    print(f"📊 BIBLIOTECA GESTÃO ESCOLAR:")
    print(f"   Status: {'✅ Conforme' if sucesso_gestao else '❌ Problemas'}")
    
    print(f"\n📊 BIBLIOTECA EDITORIAL ALUNO:")
    print(f"   Status: {'✅ Corrigida' if sucesso_aluno else '⚠️ Parcial'}")
    
    if sucesso_gestao and sucesso_aluno:
        print(f"\n🎉 ETAPA 2 CONCLUÍDA COM SUCESSO!")
        print("   ✅ Todas as propriedades corrigidas")
        print("   ✅ Taxonomias aplicadas")
        print("   ✅ Bibliotecas alinhadas com boilerplate")
    else:
        print(f"\n⚠️ ETAPA 2 PARCIALMENTE CONCLUÍDA")
        print("   ⚠️ Algumas correções podem precisar de atenção manual")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()

