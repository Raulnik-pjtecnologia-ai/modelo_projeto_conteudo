#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Sincronizar Conteúdos Finais
Sincroniza os novos conteúdos criados (Física, Química, Sociologia) com Notion
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

def processar_sincronizacao_final(database_id):
    """Processa sincronização dos conteúdos finais"""
    print_secao("SINCRONIZAÇÃO DE CONTEÚDOS FINAIS")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Sincronizar novos conteúdos específicos por matéria")
    
    # Conteúdos para sincronizar
    conteudos = [
        {
            "titulo": "Física ENEM 2025: Ondas e Energia - Guia Completo",
            "conteudo": """# Física ENEM 2025: Ondas e Energia - Guia Completo

## Introdução
Ondas e Energia são tópicos fundamentais da Física no ENEM, representando cerca de 30% das questões da área.

## Ondas - Conceitos Fundamentais
- Amplitude: Máximo deslocamento da onda
- Frequência: Número de oscilações por segundo
- Período: Tempo para uma oscilação completa
- Comprimento de Onda: Distância entre duas cristas

## Tipos de Ondas
- Mecânicas: Precisam de meio material
- Eletromagnéticas: Não precisam de meio
- Transversais: Vibração perpendicular à propagação
- Longitudinais: Vibração paralela à propagação

## Energia - Princípios Básicos
- Cinética: Energia do movimento
- Potencial: Energia armazenada
- Mecânica: Soma da cinética e potencial
- Térmica: Energia das partículas

## Estratégias de Resolução
- Identifique o Tipo de Questão
- Use Fórmulas Corretas
- Aplique Princípios Físicos

## Exercícios Práticos
### Questão 1: Ondas
Uma onda tem frequência de 50 Hz e comprimento de onda de 4 m. Qual sua velocidade?
Resolução: v = λf = 4 × 50 = 200 m/s

### Questão 2: Energia
Um objeto de 2 kg cai de 10 m de altura. Qual sua velocidade ao tocar o solo?
Resolução: Ep = mgh = 2 × 10 × 10 = 200 J
Ec = Ep (conservação)
v = √(2Ec/m) = √(2×200/2) = √200 = 14,1 m/s

## Conclusão
Ondas e Energia são tópicos fascinantes e essenciais da Física no ENEM 2025."""
        },
        {
            "titulo": "Química ENEM 2025: Orgânica Essencial - Guia Completo",
            "conteudo": """# Química ENEM 2025: Orgânica Essencial - Guia Completo

## Introdução
A Química Orgânica é uma das áreas mais importantes da Química no ENEM, representando cerca de 35% das questões da disciplina.

## Hidrocarbonetos
### Alcanos
- Fórmula Geral: CnH2n+2
- Ligações: Apenas simples (C-C)
- Exemplos: Metano (CH4), Etano (C2H6)
- Propriedades: Menos reativos, combustíveis

### Alcenos
- Fórmula Geral: CnH2n
- Ligações: Uma dupla (C=C)
- Exemplos: Eteno (C2H4), Propeno (C3H6)
- Propriedades: Mais reativos, polimerização

## Funções Orgânicas
### Álcoois
- Grupo Funcional: -OH
- Exemplos: Metanol (CH3OH), Etanol (C2H5OH)
- Propriedades: Solúveis em água, combustíveis

### Ácidos Carboxílicos
- Grupo Funcional: -COOH
- Exemplos: Ácido acético (CH3COOH)
- Propriedades: Ácidos fracos, sabor azedo

## Reações Orgânicas
### Combustão
- Tipo: Oxidação completa
- Produtos: CO2 + H2O
- Exemplo: CH4 + 2O2 → CO2 + 2H2O

### Substituição
- Tipo: Troca de átomos
- Exemplo: CH4 + Cl2 → CH3Cl + HCl

## Exercícios Práticos
### Questão 1: Nomenclatura
Qual o nome do composto CH3-CH2-CH2-OH?
Resolução: Cadeia: 3 carbonos (propano)
Função: álcool (-OH)
Nome: 1-propanol ou propan-1-ol

### Questão 2: Reação
Complete a reação: CH2=CH2 + H2O → ?
Resolução: Adição de água ao alceno
CH2=CH2 + H2O → CH3-CH2OH
Produto: etanol

## Conclusão
A Química Orgânica é fundamental para compreender a vida e a tecnologia moderna."""
        },
        {
            "titulo": "Sociologia ENEM 2025: Movimentos Sociais - Guia Completo",
            "conteudo": """# Sociologia ENEM 2025: Movimentos Sociais - Guia Completo

## Introdução
Os Movimentos Sociais são tópicos fundamentais da Sociologia no ENEM, representando cerca de 25% das questões da área de Ciências Humanas.

## Conceitos Fundamentais
### Definição de Movimentos Sociais
- Conceito: Ações coletivas organizadas
- Objetivo: Transformação social
- Características: Mobilização, organização, reivindicação
- Contexto: Conflitos e desigualdades sociais

### Tipos de Movimentos Sociais
- Movimentos de Classe: Luta por direitos trabalhistas
- Movimentos Identitários: Questões de gênero, raça, etnia
- Movimentos Ambientais: Proteção do meio ambiente
- Movimentos Urbanos: Direito à cidade e moradia

## Movimentos Sociais no Brasil
### Movimentos Trabalhistas
- História: Desde o século XIX
- Principais Lutas: Direitos trabalhistas, salários
- Conquistas: CLT, previdência social
- Atualidade: Reformas trabalhistas

### Movimentos de Moradia
- Contexto: Déficit habitacional
- Estratégias: Ocupações, manifestações
- Conquistas: Programas habitacionais
- Desafios: Especulação imobiliária

## Estratégias de Resolução
- Identifique o Contexto
- Analise as Causas
- Avalie os Impactos

## Exercícios Práticos
### Questão 1: Movimentos Trabalhistas
Qual foi a principal conquista do movimento trabalhista brasileiro na Era Vargas?
Resolução: CLT (Consolidação das Leis do Trabalho): Estabeleceu direitos trabalhistas como férias, 13º salário, jornada de trabalho e previdência social.

### Questão 2: Movimentos Ambientais
Qual estratégia os movimentos ambientais usam para pressionar governos?
Resolução: Mobilização e Pressão Política: Através de manifestações, campanhas de conscientização, lobby e pressão sobre autoridades para implementar políticas ambientais.

## Conclusão
Os Movimentos Sociais são fundamentais para a democracia e a transformação social."""
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
    processar_sincronizacao_final(DATABASE_ALUNO)
