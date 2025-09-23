#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Sincronização com Notion
Sincroniza conteúdo local com o database do Notion
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from notion_client import Client

def carregar_configuracao():
    """Carrega configuração do projeto"""
    try:
        with open('config/config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"❌ Erro ao carregar configuração: {e}")
        return None

def conectar_notion(config):
    """Conecta com a API do Notion"""
    try:
        notion = Client(auth=config['notion']['token'])
        print("✅ Conexão com Notion estabelecida!")
        return notion
    except Exception as e:
        print(f"❌ Erro ao conectar com Notion: {e}")
        return None

def obter_categorias_disponiveis(notion, config):
    """Obtém categorias disponíveis no database"""
    try:
        print("🏷️  Obtendo categorias disponíveis...")
        response = notion.databases.query(database_id=config['notion']['categorias_database_id'])
        categorias = response['results']
        
        mapeamento_categorias = {}
        for categoria in categorias:
            props = categoria.get('properties', {})
            nome = ""
            if 'Name' in props and 'title' in props['Name']:
                nome = props['Name']['title'][0]['text']['content'] if props['Name']['title'] else ""
            elif 'Título' in props and 'title' in props['Título']:
                nome = props['Título']['title'][0]['text']['content'] if props['Título']['title'] else ""
            
            if nome:
                mapeamento_categorias[nome] = categoria['id']
        
        print(f"   🏷️  {len(mapeamento_categorias)} categorias encontradas")
        return mapeamento_categorias
    except Exception as e:
        print(f"❌ Erro ao obter categorias: {e}")
        return {}

def determinar_tipo_conteudo(titulo):
    """Determina o tipo de conteúdo baseado no título"""
    titulo_lower = titulo.lower()
    
    if 'checklist' in titulo_lower:
        return 'Checklist'
    elif 'lição' in titulo_lower or 'licao' in titulo_lower:
        return 'Lição'
    elif 'artigo' in titulo_lower:
        return 'Artigo'
    elif 'vídeo' in titulo_lower or 'video' in titulo_lower:
        return 'Vídeo'
    elif 'documento' in titulo_lower:
        return 'Documento Oficial'
    elif 'apresentação' in titulo_lower or 'apresentacao' in titulo_lower:
        return 'Apresentação'
    else:
        return 'Artigo'

def determinar_funcao(categorias_relevantes, config):
    """Determina a função baseada nas categorias"""
    if not categorias_relevantes:
        return ['Gestão']
    
    funcoes_disponiveis = config.get('funcoes', ['Gestão'])
    funcoes = []
    
    for categoria, score in categorias_relevantes:
        if categoria in funcoes_disponiveis:
            funcoes.append(categoria)
    
    return funcoes[:3] if funcoes else ['Gestão']

def determinar_nivel_profundidade(titulo, categorias_relevantes):
    """Determina o nível de profundidade"""
    titulo_lower = titulo.lower()
    
    if 'básico' in titulo_lower or 'introdução' in titulo_lower:
        return ['Básico']
    elif 'avançado' in titulo_lower or 'especializado' in titulo_lower:
        return ['Avançado']
    elif 'intermediário' in titulo_lower or 'intermediario' in titulo_lower:
        return ['Intermediário']
    else:
        if categorias_relevantes and categorias_relevantes[0][1] > 20:
            return ['Avançado']
        elif categorias_relevantes and categorias_relevantes[0][1] > 10:
            return ['Intermediário']
        else:
            return ['Básico']

def sincronizar_pagina(notion, config, resultado, mapeamento_categorias):
    """Sincroniza uma página individual"""
    page_id = resultado['page_id']
    propriedades = resultado['propriedades']
    categorias_relevantes = resultado.get('categorias_relevantes', [])
    
    titulo = propriedades.get('titulo', 'Sem título')
    
    propriedades_atualizadas = {}
    
    # Atualizar Tipo
    tipo_sugerido = determinar_tipo_conteudo(titulo)
    propriedades_atualizadas['Tipo'] = {
        'select': {
            'name': tipo_sugerido
        }
    }
    
    # Atualizar Função
    funcoes = determinar_funcao(categorias_relevantes, config)
    propriedades_atualizadas['Função '] = {
        'multi_select': [{'name': funcao} for funcao in funcoes]
    }
    
    # Atualizar Nível de profundidade
    nivel = determinar_nivel_profundidade(titulo, categorias_relevantes)
    propriedades_atualizadas['Nível de profundidade'] = {
        'multi_select': [{'name': n} for n in nivel]
    }
    
    # Atualizar Tags
    tags = [categoria for categoria, _ in categorias_relevantes[:3]]
    if tags:
        propriedades_atualizadas['Tags'] = {
            'multi_select': [{'name': tag} for tag in tags]
        }
    
    # Atualizar Status editorial
    propriedades_atualizadas['Status editorial'] = {
        'status': {
            'name': 'Publicado'
        }
    }
    
    # Criar relações com categorias
    if categorias_relevantes and mapeamento_categorias:
        categorias_ids = []
        
        for categoria_auto, score in categorias_relevantes[:3]:
            if categoria_auto in mapeamento_categorias:
                categoria_id = mapeamento_categorias[categoria_auto]
                categorias_ids.append(categoria_id)
        
        if categorias_ids:
            propriedades_atualizadas['Categoria'] = {
                'relation': [{'id': cat_id} for cat_id in categorias_ids]
            }
    
    # Atualizar página
    try:
        notion.pages.update(
            page_id=page_id,
            properties=propriedades_atualizadas
        )
        return True
    except Exception as e:
        print(f"   ❌ Erro ao atualizar: {e}")
        return False

def processar_sincronizacao(notion, config, mapeamento_categorias):
    """Processa a sincronização de todas as páginas"""
    print("🔄 Iniciando sincronização com Notion...")
    
    # Buscar páginas no database
    try:
        response = notion.databases.query(database_id=config['notion']['database_id'])
        paginas = response['results']
        
        resultados = {
            'total_processadas': 0,
            'sucessos': 0,
            'erros': 0
        }
        
        for i, pagina in enumerate(paginas, 1):
            page_id = pagina['id']
            props = pagina.get('properties', {})
            
            # Extrair título
            titulo = ""
            if 'Name' in props and 'title' in props['Name']:
                titulo = props['Name']['title'][0]['text']['content'] if props['Name']['title'] else ""
            elif 'Título' in props and 'title' in props['Título']:
                titulo = props['Título']['title'][0]['text']['content'] if props['Título']['title'] else ""
            
            print(f"🔍 [{i}/{len(paginas)}] Sincronizando: {titulo[:50]}...")
            
            # Criar resultado para sincronização
            resultado = {
                'page_id': page_id,
                'propriedades': {'titulo': titulo},
                'categorias_relevantes': []
            }
            
            if sincronizar_pagina(notion, config, resultado, mapeamento_categorias):
                resultados['sucessos'] += 1
                print(f"   ✅ Sincronizado com sucesso")
            else:
                resultados['erros'] += 1
                print(f"   ❌ Erro na sincronização")
            
            resultados['total_processadas'] += 1
            print()
            time.sleep(0.3)
        
        return resultados
        
    except Exception as e:
        print(f"❌ Erro ao processar sincronização: {e}")
        return None

def main():
    """Função principal"""
    print("🔄 SINCRONIZAÇÃO COM NOTION")
    print("="*50)
    
    # Carregar configuração
    config = carregar_configuracao()
    if not config:
        return
    
    # Conectar com Notion
    notion = conectar_notion(config)
    if not notion:
        return
    
    # Obter categorias disponíveis
    mapeamento_categorias = obter_categorias_disponiveis(notion, config)
    
    # Processar sincronização
    resultados = processar_sincronizacao(notion, config, mapeamento_categorias)
    
    if resultados:
        # Exibir resumo final
        print("="*50)
        print("📊 RESUMO FINAL DA SINCRONIZAÇÃO")
        print("="*50)
        print(f"📄 Total de páginas processadas: {resultados['total_processadas']}")
        print(f"✅ Sucessos: {resultados['sucessos']}")
        print(f"❌ Erros: {resultados['erros']}")
        print(f"📊 Taxa de sucesso: {(resultados['sucessos']/resultados['total_processadas']*100):.1f}%")
        print("\n🎉 SINCRONIZAÇÃO CONCLUÍDA!")

if __name__ == "__main__":
    main()
