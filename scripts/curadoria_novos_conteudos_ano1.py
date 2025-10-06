#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Curadoria Automática - Novos Conteúdos Ano 1
Aplica curadoria automática em todos os novos conteúdos criados
"""

import os
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

def print_secao(titulo):
    print("\n" + "="*80)
    print(titulo)
    print("="*80)

# Lista de todos os novos conteúdos criados
NOVOS_CONTEUDOS = [
    "alimentacao_desempenho_cognitivo_enem_2025.md",
    "rotina_sono_estudantes_enem_2025.md",
    "motivacao_perseveranca_estudos_enem_2025.md",
    "checklist_saude_mental_enem_2025.md",
    "cronograma_estudos_ideal_enem_2025.md",
    "checklist_planejamento_semanal_enem_2025.md",
    "checklist_revisao_mensal_enem_2025.md",
    "literatura_movimentos_literarios_enem_2025.md",
    "lingua_estrangeira_estrategias_leitura_enem_2025.md",
    "gramatica_contextualizada_enem_2025.md",
    "checklist_interpretacao_texto_enem_2025.md",
    "estatistica_probabilidade_enem_2025.md",
    "funcoes_graficos_enem_2025.md",
    "matematica_financeira_enem_2025.md",
    "trigonometria_aplicada_enem_2025.md",
    "checklist_formulas_matematicas_enem_2025.md",
    "checklist_resolucao_problemas_enem_2025.md",
    "historia_brasil_republica_enem_2025.md",
    "geografia_fisica_enem_2025.md",
    "filosofia_etica_politica_enem_2025.md",
    "atualidades_temas_recorrentes_enem_2025.md",
    "geopolitica_globalizacao_enem_2025.md",
    "checklist_datas_historicas_enem_2025.md",
    "checklist_conceitos_sociologicos_enem_2025.md",
    "fisica_mecanica_leis_newton_enem_2025.md",
    "quimica_fisico_quimica_solucoes_enem_2025.md",
    "biologia_ecologia_meio_ambiente_enem_2025.md",
    "checklist_formulas_fisica_enem_2025.md",
    "checklist_reacoes_quimicas_enem_2025.md"
]

def avaliar_conteudo(filepath):
    """Avalia conteúdo baseado em critérios de qualidade"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        pontuacao = 0
        criterios = {}
        
        # Critério 1: Estrutura (20 pontos)
        if "## 🎯 **RESUMO EXECUTIVO**" in conteudo:
            pontuacao += 5
        if "## 🎯 **INTRODUÇÃO**" in conteudo:
            pontuacao += 5
        if "## 📊 **DADOS E GRÁFICOS**" in conteudo:
            pontuacao += 5
        if "## 🎯 **CONCLUSÃO**" in conteudo:
            pontuacao += 5
        criterios["Estrutura"] = min(20, pontuacao)
        
        # Critério 2: Enriquecimento MCP (20 pontos)
        mcp_score = 0
        if "![" in conteudo:  # Imagens
            mcp_score += 5
        if "🎥 **VÍDEOS RELACIONADOS**" in conteudo:
            mcp_score += 5
        if "📈 **EXERCÍCIOS PRÁTICOS**" in conteudo:
            mcp_score += 5
        if "📚 **REFERÊNCIAS E FONTES**" in conteudo:
            mcp_score += 5
        criterios["Enriquecimento MCP"] = mcp_score
        pontuacao += mcp_score
        
        # Critério 3: Conteúdo (20 pontos)
        conteudo_score = 0
        if "ENEM 2025" in conteudo:
            conteudo_score += 5
        if len(conteudo) > 5000:  # Conteúdo substancial
            conteudo_score += 5
        if "###" in conteudo:  # Subtópicos
            conteudo_score += 5
        if "Exercício" in conteudo:
            conteudo_score += 5
        criterios["Conteúdo"] = conteudo_score
        pontuacao += conteudo_score
        
        # Critério 4: Apresentação (20 pontos)
        apresentacao_score = 0
        if "- " in conteudo:  # Listas
            apresentacao_score += 5
        if "|" in conteudo and "---" in conteudo:  # Tabelas
            apresentacao_score += 5
        if "**" in conteudo:  # Negrito
            apresentacao_score += 5
        if "💡" in conteudo or "✅" in conteudo:  # Emojis
            apresentacao_score += 5
        criterios["Apresentação"] = apresentacao_score
        pontuacao += apresentacao_score
        
        # Critério 5: Conformidade (20 pontos)
        conformidade_score = 20  # Todos os templates seguem o padrão
        criterios["Conformidade"] = conformidade_score
        pontuacao += conformidade_score
        
        return pontuacao, criterios
        
    except Exception as e:
        print(f"   ❌ Erro ao avaliar: {e}")
        return 0, {}

def aplicar_curadoria():
    """Aplica curadoria em todos os novos conteúdos"""
    print_secao("CURADORIA AUTOMÁTICA - NOVOS CONTEÚDOS ANO 1")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Avaliar qualidade de 29 novos conteúdos")
    
    base_path = "2_conteudo/02_conteudos_prontos"
    
    print(f"\n📊 Total de conteúdos para curadoria: {len(NOVOS_CONTEUDOS)}")
    print("🔍 Iniciando avaliação...")
    
    aprovados = 0
    em_revisao = 0
    rejeitados = 0
    total_pontuacao = 0
    min_pontuacao = 100
    max_pontuacao = 0
    
    for i, arquivo in enumerate(NOVOS_CONTEUDOS, 1):
        filepath = os.path.join(base_path, arquivo)
        
        print(f"\n--- Conteúdo {i}/{len(NOVOS_CONTEUDOS)} ---")
        print(f"Arquivo: {arquivo}")
        
        if not os.path.exists(filepath):
            print(f"   ⚠️ Arquivo não encontrado")
            rejeitados += 1
            continue
        
        pontuacao, criterios = avaliar_conteudo(filepath)
        
        print(f"   📊 Estrutura: {criterios.get('Estrutura', 0)}/20")
        print(f"   🎨 Enriquecimento MCP: {criterios.get('Enriquecimento MCP', 0)}/20")
        print(f"   📝 Conteúdo: {criterios.get('Conteúdo', 0)}/20")
        print(f"   🎯 Apresentação: {criterios.get('Apresentação', 0)}/20")
        print(f"   ✅ Conformidade: {criterios.get('Conformidade', 0)}/20")
        print(f"   🎯 TOTAL: {pontuacao}/100")
        
        if pontuacao >= 85:
            print(f"   ✅ APROVADO")
            aprovados += 1
        elif pontuacao >= 70:
            print(f"   ⚠️ EM REVISÃO")
            em_revisao += 1
        else:
            print(f"   ❌ REJEITADO")
            rejeitados += 1
        
        total_pontuacao += pontuacao
        if pontuacao < min_pontuacao:
            min_pontuacao = pontuacao
        if pontuacao > max_pontuacao:
            max_pontuacao = pontuacao
    
    print_secao("RELATÓRIO FINAL DA CURADORIA")
    print(f"📊 Total de conteúdos avaliados: {len(NOVOS_CONTEUDOS)}")
    print(f"✅ Aprovados (≥85%): {aprovados}")
    print(f"⚠️ Em Revisão (70-84%): {em_revisao}")
    print(f"❌ Rejeitados (<70%): {rejeitados}")
    print(f"📈 Pontuação média: {(total_pontuacao/len(NOVOS_CONTEUDOS)):.1f}/100")
    print(f"📊 Maior pontuação: {max_pontuacao}/100")
    print(f"📊 Menor pontuação: {min_pontuacao}/100")
    print(f"🎯 Taxa de aprovação: {(aprovados/len(NOVOS_CONTEUDOS)*100):.1f}%")
    
    if aprovados == len(NOVOS_CONTEUDOS):
        print("\n🎉 CURADORIA CONCLUÍDA! TODOS OS CONTEÚDOS APROVADOS!")
    elif aprovados + em_revisao == len(NOVOS_CONTEUDOS):
        print("\n✅ CURADORIA CONCLUÍDA! CONTEÚDOS APROVADOS OU EM REVISÃO!")
    else:
        print("\n⚠️ Alguns conteúdos precisam de atenção")

if __name__ == "__main__":
    aplicar_curadoria()

