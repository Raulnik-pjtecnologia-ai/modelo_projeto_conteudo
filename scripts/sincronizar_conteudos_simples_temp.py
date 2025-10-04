#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script Simplificado para Sincronizar Conteúdos
Sincroniza apenas o texto, sem imagens problemáticas
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

def criar_pagina_simples(database_id, titulo, conteudo_texto):
    """Cria página simples no Notion apenas com texto"""
    print(f"📝 Criando página: {titulo}")
    
    # Converter texto em blocos simples
    linhas = conteudo_texto.split('\n')
    blocos = []
    
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
            
        if linha.startswith('# '):
            titulo_sec = linha[2:].strip()
            blocos.append({
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": titulo_sec}}]
                }
            })
        elif linha.startswith('## '):
            subtitulo = linha[3:].strip()
            blocos.append({
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": subtitulo}}]
                }
            })
        elif linha.startswith('### '):
            subsubtitulo = linha[4:].strip()
            blocos.append({
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": subsubtitulo}}]
                }
            })
        elif linha.startswith('- '):
            item = linha[2:].strip()
            blocos.append({
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": item}}]
                }
            })
        else:
            if linha and not linha.startswith('![') and not linha.startswith('*'):
                blocos.append({
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": linha}}]
                    }
                })
    
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
        "children": blocos[:50]  # Limitar a 50 blocos por vez
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    
    if response.status_code != 200:
        print(f"❌ Erro ao criar página: {response.status_code}")
        print(f"Resposta: {response.text}")
        return None
    
    data = response.json()
    page_id = data["id"]
    print(f"✅ Página criada com sucesso: {page_id}")
    
    return page_id

def processar_sincronizacao_simples(database_id):
    """Processa sincronização simplificada"""
    print_secao("SINCRONIZAÇÃO SIMPLIFICADA DE CONTEÚDOS")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Sincronizar conteúdos apenas com texto")
    
    # Conteúdos para sincronizar
    conteudos = [
        {
            "titulo": "Estratégias de Estudo ENEM 2025: Guia Completo",
            "conteudo": """# Estratégias de Estudo ENEM 2025: Guia Completo

## Introdução
O ENEM 2025 exige preparação estratégica e eficiente. Este guia apresenta as melhores estratégias de estudo comprovadas.

## Cronograma de Estudos Eficaz
- Cronograma Semanal: 6 dias de estudo + 1 dia de descanso
- Sessões de 2-3 horas: Com pausas de 15 minutos
- Revisões Regulares: 30 minutos diários de revisão
- Simulados Mensais: Avaliação completa do progresso

## Técnicas de Resolução de Questões
- Leia o Enunciado Completo: Antes de olhar as alternativas
- Identifique o Comando: O que a questão está pedindo
- Destaque Informações Importantes: Palavras-chave e dados
- Elimine Alternativas Absurdas: Reduza as opções

## Bem-Estar e Saúde Mental
- Técnicas de Relaxamento: Meditação e respiração
- Exercícios Físicos: 30 minutos, 3x por semana
- Alimentação Equilibrada: Frutas, verduras e proteínas
- Sono Adequado: 8 horas por noite

## Conclusão
Com organização, disciplina e as técnicas apresentadas, você estará preparado para conquistar uma excelente pontuação."""
        },
        {
            "titulo": "Abordagem Interdisciplinar ENEM 2025",
            "conteudo": """# Abordagem Interdisciplinar ENEM 2025

## Introdução
O ENEM valoriza a capacidade de articular diferentes áreas do conhecimento, exigindo uma abordagem interdisciplinar.

## Conexões Entre Áreas
- Ciências da Natureza + Matemática: Cálculos e fórmulas
- Ciências Humanas + Linguagens: Interpretação e contexto
- Todas as Áreas + Redação: Temas transversais

## Temas Transversais
- Sustentabilidade e Meio Ambiente
- Cidadania e Direitos Humanos
- Tecnologia e Inovação
- Globalização e Economia

## Estratégias de Integração
- Mapas Conceituais: Represente relações entre conceitos
- Estudos de Caso: Aplique conhecimentos em contextos
- Projetos Interdisciplinares: Escolha assuntos complexos

## Conclusão
A abordagem interdisciplinar é fundamental para o sucesso no ENEM 2025."""
        },
        {
            "titulo": "Sistema de Monitoramento de Progresso ENEM 2025",
            "conteudo": """# Sistema de Monitoramento de Progresso ENEM 2025

## Introdução
O monitoramento contínuo do progresso é essencial para o sucesso no ENEM 2025.

## Ferramentas de Monitoramento
- Planilha de Acompanhamento: Metas semanais e horas de estudo
- Gráficos de Evolução: Progresso ao longo dos meses
- Análise de Desempenho: Questões corretas e tempo de resolução

## Métricas Essenciais
- Métricas Quantitativas: Horas de estudo, questões resolvidas
- Métricas Qualitativas: Compreensão e aplicação
- Métricas de Desempenho: Taxa de acerto e consistência

## Sistema de Avaliação
- Avaliação Semanal: Metas alcançadas e ajustes
- Avaliação Mensal: Progresso geral e simulados
- Avaliação Trimestral: Revisão completa e mudanças

## Conclusão
O monitoramento de progresso é uma ferramenta poderosa para o sucesso no ENEM 2025."""
        },
        {
            "titulo": "Bem-Estar e Saúde Mental ENEM 2025",
            "conteudo": """# Bem-Estar e Saúde Mental ENEM 2025

## Introdução
O bem-estar e a saúde mental são fundamentais para o sucesso no ENEM 2025.

## Técnicas de Relaxamento
- Meditação e Mindfulness: 10-15 minutos diários
- Exercícios de Respiração: Técnicas de controle da ansiedade
- Técnicas de Visualização: Imagine o sucesso

## Exercícios Físicos
- Atividades Aeróbicas: Caminhada, corrida, ciclismo
- Exercícios de Força: Musculação e calistenia
- Alongamento e Flexibilidade: 15 minutos diários

## Alimentação e Hidratação
- Alimentação Equilibrada: Frutas, verduras e proteínas
- Alimentos para o Cérebro: Peixes, frutas vermelhas
- Hidratação Adequada: 2-3 litros de água por dia

## Sono e Descanso
- Higiene do Sono: Horário regular e ambiente adequado
- Qualidade do Sono: 8 horas de duração ideal
- Pausas e Descanso: 15 minutos a cada 2 horas

## Conclusão
Cuidar de si mesmo não é egoísmo, é necessidade - invista em seu bem-estar!"""
        }
    ]
    
    sucessos = 0
    erros = 0
    paginas_criadas = []
    
    for i, conteudo in enumerate(conteudos, 1):
        print(f"\n--- Conteúdo {i}/{len(conteudos)} ---")
        print(f"Título: {conteudo['titulo']}")
        
        # Criar página no Notion
        page_id = criar_pagina_simples(database_id, conteudo['titulo'], conteudo['conteudo'])
        if page_id:
            sucessos += 1
            paginas_criadas.append({"titulo": conteudo['titulo'], "id": page_id})
        else:
            erros += 1
        
        time.sleep(2)  # Pausa para não sobrecarregar a API
    
    # Relatório final
    print_secao("RELATÓRIO FINAL")
    print(f"📊 Total de conteúdos processados: {len(conteudos)}")
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Erros: {erros}")
    print(f"📈 Taxa de sucesso: {(sucessos/len(conteudos)*100):.1f}%")
    
    if paginas_criadas:
        print(f"\n📄 Páginas criadas:")
        for pagina in paginas_criadas:
            print(f"   - {pagina['titulo']} ({pagina['id']})")
    
    if sucessos == len(conteudos):
        print("🎉 SINCRONIZAÇÃO COMPLETA COM SUCESSO!")
    else:
        print("⚠️ Alguns conteúdos precisam de atenção manual")

if __name__ == "__main__":
    processar_sincronizacao_simples(DATABASE_ALUNO)
