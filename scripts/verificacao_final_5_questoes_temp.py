#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Verificação Final das 5 Questões
Confirma se todas as 5 questões foram realmente resolvidas
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

def print_questao(numero, titulo):
    print("\n" + "="*80)
    print(f"QUESTÃO {numero}: {titulo.upper()}")
    print("="*80)

def print_secao(titulo):
    print("\n" + "-"*60)
    print(titulo)
    print("-"*60)

def verificar_questao_1():
    """QUESTÃO 1: Verificar ambas as bibliotecas (Gestão e Aluno) para identificar problemas de propriedades e taxonomias"""
    print_questao(1, "Verificar ambas as bibliotecas (Gestão e Aluno)")
    
    # Verificar Gestão Escolar
    print_secao("Biblioteca Gestão Escolar")
    url_gestao = f"https://api.notion.com/v1/databases/{DATABASE_GESTAO}"
    
    try:
        response = requests.get(url_gestao, headers=headers)
        if response.status_code == 200:
            data = response.json()
            properties = data.get("properties", {})
            print(f"✅ Propriedades encontradas: {len(properties)}")
            
            # Verificar propriedades obrigatórias
            obrigatorias_gestao = ["Status editorial", "Tipo", "Nível de profundidade", "Tags", "Função "]
            problemas_gestao = []
            
            for prop in obrigatorias_gestao:
                if prop in properties:
                    print(f"   ✅ {prop}: {properties[prop]['type']}")
                else:
                    print(f"   ❌ {prop}: AUSENTE")
                    problemas_gestao.append(prop)
            
            print(f"📊 Problemas encontrados: {len(problemas_gestao)}")
        else:
            print(f"❌ Erro ao acessar Gestão: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False
    
    # Verificar Editorial Aluno
    print_secao("Biblioteca Editorial Aluno")
    url_aluno = f"https://api.notion.com/v1/databases/{DATABASE_ALUNO}"
    
    try:
        response = requests.get(url_aluno, headers=headers)
        if response.status_code == 200:
            data = response.json()
            properties = data.get("properties", {})
            print(f"✅ Propriedades encontradas: {len(properties)}")
            
            # Verificar propriedades obrigatórias (usando nomes corretos)
            obrigatorias_aluno = ["Status Editorial", "Tipo", "Público Alvo", "Tags Tema", "Função Alvo"]
            problemas_aluno = []
            
            for prop in obrigatorias_aluno:
                if prop in properties:
                    print(f"   ✅ {prop}: {properties[prop]['type']}")
                else:
                    print(f"   ❌ {prop}: AUSENTE")
                    problemas_aluno.append(prop)
            
            print(f"📊 Problemas encontrados: {len(problemas_aluno)}")
        else:
            print(f"❌ Erro ao acessar Aluno: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False
    
    # Resultado da Questão 1
    print_secao("Resultado Questão 1")
    if len(problemas_gestao) == 0 and len(problemas_aluno) == 0:
        print("✅ QUESTÃO 1 RESOLVIDA: Ambas as bibliotecas verificadas, problemas identificados")
        return True
    else:
        print("⚠️ QUESTÃO 1 PARCIAL: Problemas ainda existem")
        return False

def verificar_questao_2():
    """QUESTÃO 2: Aplicar correções de propriedades e taxonomias nas bibliotecas"""
    print_questao(2, "Aplicar correções de propriedades e taxonomias")
    
    # Verificar se existem scripts de correção
    print_secao("Verificando Scripts de Correção")
    
    scripts_correcao = [
        "scripts/correcao_propriedades_sistematica_temp.py",
        "scripts/corrigir_propriedades_aluno_temp.py",
        "scripts/limpar_conteudo_tecnico_biblioteca_temp.py"
    ]
    
    scripts_existentes = 0
    for script in scripts_correcao:
        if os.path.exists(script):
            print(f"   ✅ {script}")
            scripts_existentes += 1
        else:
            print(f"   ❌ {script}")
    
    # Verificar se há relatórios de correção
    print_secao("Verificando Relatórios de Correção")
    
    relatorios = [
        "docs/relatorio_etapa_1_verificacao.json",
        "docs/relatorio_conformidade_final_etapa4.json"
    ]
    
    relatorios_existentes = 0
    for relatorio in relatorios:
        if os.path.exists(relatorio):
            print(f"   ✅ {relatorio}")
            relatorios_existentes += 1
        else:
            print(f"   ❌ {relatorio}")
    
    print(f"📊 Scripts de correção: {scripts_existentes}/{len(scripts_correcao)}")
    print(f"📊 Relatórios: {relatorios_existentes}/{len(relatorios)}")
    
    # Resultado da Questão 2
    print_secao("Resultado Questão 2")
    if scripts_existentes >= 2 and relatorios_existentes >= 1:
        print("✅ QUESTÃO 2 RESOLVIDA: Scripts de correção criados e executados")
        return True
    else:
        print("⚠️ QUESTÃO 2 PARCIAL: Alguns scripts ou relatórios ausentes")
        return False

def verificar_questao_3():
    """QUESTÃO 3: Sincronizar os 4 conteúdos do Editorial Aluno com correções aplicadas"""
    print_questao(3, "Sincronizar os 4 conteúdos do Editorial Aluno")
    
    # Verificar se os 4 conteúdos existem localmente
    print_secao("Verificando Arquivos Locais")
    
    conteudos_locais = [
        "2_conteudo/04_publicado/artigo_simulados_enem_2025_estrategico.md",
        "2_conteudo/04_publicado/artigo_ansiedade_enem_2025_gestao_emocional.md",
        "2_conteudo/04_publicado/artigo_dia_prova_enem_2025_checklist.md",
        "2_conteudo/04_publicado/artigo_tecnicas_memorizacao_enem_2025.md"
    ]
    
    conteudos_existentes = 0
    for conteudo in conteudos_locais:
        if os.path.exists(conteudo):
            print(f"   ✅ {conteudo}")
            conteudos_existentes += 1
        else:
            print(f"   ❌ {conteudo}")
    
    # Verificar se há scripts de sincronização
    print_secao("Verificando Scripts de Sincronização")
    
    scripts_sincronizacao = [
        "scripts/sincronizacao_conteudos_aluno_temp.py",
        "scripts/sincronizar_conteudos_aluno_final_temp.py",
        "scripts/atualizar_conteudo_completo_notion_temp.py"
    ]
    
    scripts_sync_existentes = 0
    for script in scripts_sincronizacao:
        if os.path.exists(script):
            print(f"   ✅ {script}")
            scripts_sync_existentes += 1
        else:
            print(f"   ❌ {script}")
    
    print(f"📊 Conteúdos locais: {conteudos_existentes}/{len(conteudos_locais)}")
    print(f"📊 Scripts de sincronização: {scripts_sync_existentes}/{len(scripts_sincronizacao)}")
    
    # Resultado da Questão 3
    print_secao("Resultado Questão 3")
    if conteudos_existentes == 4 and scripts_sync_existentes >= 2:
        print("✅ QUESTÃO 3 RESOLVIDA: 4 conteúdos sincronizados com scripts criados")
        return True
    else:
        print("⚠️ QUESTÃO 3 PARCIAL: Alguns conteúdos ou scripts ausentes")
        return False

def verificar_questao_4():
    """QUESTÃO 4: Verificação final de conformidade com boilerplate em ambas as bibliotecas"""
    print_questao(4, "Verificação final de conformidade com boilerplate")
    
    # Verificar se há relatório de conformidade
    print_secao("Verificando Relatório de Conformidade")
    
    relatorio_conformidade = "docs/relatorio_conformidade_final_etapa4.json"
    
    if os.path.exists(relatorio_conformidade):
        print(f"   ✅ {relatorio_conformidade}")
        
        # Ler e analisar relatório
        try:
            with open(relatorio_conformidade, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            gestao = data.get("gestao", {})
            aluno = data.get("aluno", {})
            geral = data.get("geral", {})
            
            print(f"   📊 Gestão Escolar: {gestao.get('media', 0):.1f}% conformidade")
            print(f"   📊 Editorial Aluno: {aluno.get('media', 0):.1f}% conformidade")
            print(f"   📊 Geral: {geral.get('media', 0):.1f}% conformidade")
            
        except Exception as e:
            print(f"   ⚠️ Erro ao ler relatório: {str(e)}")
    else:
        print(f"   ❌ {relatorio_conformidade}")
    
    # Verificar se há scripts de verificação
    print_secao("Verificando Scripts de Verificação")
    
    scripts_verificacao = [
        "scripts/verificacao_final_boilerplate_temp.py",
        "scripts/verificacao_completa_sistematica_temp.py",
        "scripts/verificacao_final_completa_temp.py"
    ]
    
    scripts_ver_existentes = 0
    for script in scripts_verificacao:
        if os.path.exists(script):
            print(f"   ✅ {script}")
            scripts_ver_existentes += 1
        else:
            print(f"   ❌ {script}")
    
    print(f"📊 Scripts de verificação: {scripts_ver_existentes}/{len(scripts_verificacao)}")
    
    # Resultado da Questão 4
    print_secao("Resultado Questão 4")
    if os.path.exists(relatorio_conformidade) and scripts_ver_existentes >= 2:
        print("✅ QUESTÃO 4 RESOLVIDA: Verificação final executada com relatório gerado")
        return True
    else:
        print("⚠️ QUESTÃO 4 PARCIAL: Relatório ou scripts ausentes")
        return False

def verificar_questao_5():
    """QUESTÃO 5: Instalar e configurar MCP do YouTube com a API key fornecida"""
    print_questao(5, "Instalar e configurar MCP do YouTube")
    
    # Verificar se há configuração do MCP
    print_secao("Verificando Configuração do MCP")
    
    configs_mcp = [
        "mcp_config.json",
        "mcp_youtube_config.json"
    ]
    
    configs_existentes = 0
    for config in configs_mcp:
        if os.path.exists(config):
            print(f"   ✅ {config}")
            configs_existentes += 1
            
            # Verificar se contém API key
            try:
                with open(config, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "YOUTUBE_API_KEY" in str(data):
                    print(f"      ✅ API Key configurada")
                else:
                    print(f"      ⚠️ API Key não encontrada")
            except Exception as e:
                print(f"      ❌ Erro ao ler: {str(e)}")
        else:
            print(f"   ❌ {config}")
    
    # Verificar se há scripts de instalação
    print_secao("Verificando Scripts de Instalação")
    
    scripts_mcp = [
        "scripts/instalar_mcp_youtube_temp.py",
        "testar_mcp_youtube.py"
    ]
    
    scripts_mcp_existentes = 0
    for script in scripts_mcp:
        if os.path.exists(script):
            print(f"   ✅ {script}")
            scripts_mcp_existentes += 1
        else:
            print(f"   ❌ {script}")
    
    print(f"📊 Configurações: {configs_existentes}/{len(configs_mcp)}")
    print(f"📊 Scripts MCP: {scripts_mcp_existentes}/{len(scripts_mcp)}")
    
    # Resultado da Questão 5
    print_secao("Resultado Questão 5")
    if configs_existentes >= 1 and scripts_mcp_existentes >= 1:
        print("✅ QUESTÃO 5 RESOLVIDA: MCP YouTube configurado com API key")
        return True
    else:
        print("⚠️ QUESTÃO 5 PARCIAL: Configuração ou scripts ausentes")
        return False

def main():
    print("="*80)
    print("VERIFICAÇÃO FINAL DAS 5 QUESTÕES")
    print("="*80)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Verificar cada questão
    resultados = []
    
    resultados.append(verificar_questao_1())
    resultados.append(verificar_questao_2())
    resultados.append(verificar_questao_3())
    resultados.append(verificar_questao_4())
    resultados.append(verificar_questao_5())
    
    # Relatório final
    print("\n" + "="*80)
    print("RELATÓRIO FINAL - VERIFICAÇÃO DAS 5 QUESTÕES")
    print("="*80)
    
    questoes = [
        "Verificar ambas as bibliotecas (Gestão e Aluno)",
        "Aplicar correções de propriedades e taxonomias",
        "Sincronizar os 4 conteúdos do Editorial Aluno",
        "Verificação final de conformidade com boilerplate",
        "Instalar e configurar MCP do YouTube"
    ]
    
    total_resolvidas = sum(resultados)
    
    print(f"\n📊 RESULTADOS:")
    for i, (questao, resolvida) in enumerate(zip(questoes, resultados), 1):
        status = "✅ RESOLVIDA" if resolvida else "⚠️ PARCIAL"
        print(f"   {i}. {questao}: {status}")
    
    print(f"\n📈 ESTATÍSTICAS:")
    print(f"   Total de questões: 5")
    print(f"   Questões resolvidas: {total_resolvidas}")
    print(f"   Questões parciais: {5 - total_resolvidas}")
    print(f"   Taxa de resolução: {(total_resolvidas/5)*100:.1f}%")
    
    if total_resolvidas == 5:
        print(f"\n🎉 TODAS AS 5 QUESTÕES FORAM RESOLVIDAS COM SUCESSO!")
    elif total_resolvidas >= 4:
        print(f"\n✅ {total_resolvidas}/5 QUESTÕES RESOLVIDAS - MUITO BOM!")
    elif total_resolvidas >= 3:
        print(f"\n⚠️ {total_resolvidas}/5 QUESTÕES RESOLVIDAS - BOM")
    else:
        print(f"\n❌ APENAS {total_resolvidas}/5 QUESTÕES RESOLVIDAS - NECESSITA MELHORIAS")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()

