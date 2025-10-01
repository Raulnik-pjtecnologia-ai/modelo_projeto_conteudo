import os
import json
import time
from pathlib import Path
from datetime import datetime, timezone
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

if not NOTION_TOKEN or not DATABASE_ID:
    print("Erro: NOTION_TOKEN ou DATABASE_ID não configurados nas variáveis de ambiente.")
    exit()

notion = Client(auth=NOTION_TOKEN)

def carregar_dados_todos_blocos():
    """Carrega os dados de todos os blocos anteriores."""
    dados = {}
    
    try:
        with open("dados_bloco1_analise_notion.json", "r", encoding="utf-8") as f:
            dados["bloco1"] = json.load(f)
    except Exception as e:
        print(f"Erro ao carregar dados do Bloco 1: {e}")
        return None
    
    try:
        with open("dados_bloco2_analise_notion.json", "r", encoding="utf-8") as f:
            dados["bloco2"] = json.load(f)
    except Exception as e:
        print(f"Erro ao carregar dados do Bloco 2: {e}")
        return None
    
    try:
        with open("dados_bloco3_analise_notion.json", "r", encoding="utf-8") as f:
            dados["bloco3"] = json.load(f)
    except Exception as e:
        print(f"Erro ao carregar dados do Bloco 3: {e}")
        return None
    
    try:
        with open("dados_bloco4_analise_notion.json", "r", encoding="utf-8") as f:
            dados["bloco4"] = json.load(f)
    except Exception as e:
        print(f"Erro ao carregar dados do Bloco 4: {e}")
        return None
    
    return dados

def gerar_relatorio_final(dados):
    """Gera o relatório final consolidado."""
    
    relatorio = {
        "data_analise": datetime.now().isoformat(),
        "resumo_executivo": {},
        "detalhamento_por_bloco": {},
        "problemas_identificados": {},
        "recomendacoes": {},
        "conclusoes": {}
    }
    
    # Resumo Executivo
    relatorio["resumo_executivo"] = {
        "total_conteudos_analisados": dados["bloco1"]["total_paginas"],
        "conteudos_gestao": len(dados["bloco1"]["conteudos_gestao"]),
        "conteudos_nao_gestao": len(dados["bloco1"]["conteudos_nao_gestao"]),
        "taxa_conformidade_categorizacao": dados["bloco2"]["taxa_conformidade"],
        "taxa_conformidade_boilerplate": dados["bloco3"]["taxa_conformidade"],
        "taxa_conformidade_mcp": dados["bloco4"]["taxa_conformidade"],
        "score_medio_boilerplate": dados["bloco3"]["score_medio"],
        "score_medio_mcp": dados["bloco4"]["score_medio"]
    }
    
    # Detalhamento por Bloco
    relatorio["detalhamento_por_bloco"] = {
        "bloco1_analise_basica": {
            "total_paginas": dados["bloco1"]["total_paginas"],
            "conteudos_gestao": len(dados["bloco1"]["conteudos_gestao"]),
            "distribuicao_por_tipo": dados["bloco1"]["tipos_gestao"],
            "distribuicao_por_status": dados["bloco1"]["status_gestao"]
        },
        "bloco2_categorizacao": {
            "total_verificados": dados["bloco2"]["total_verificados"],
            "total_problemas": dados["bloco2"]["total_problemas"],
            "taxa_conformidade": dados["bloco2"]["taxa_conformidade"],
            "tipos_problemas": dados["bloco2"]["tipos_problemas"]
        },
        "bloco3_boilerplate": {
            "total_verificados": dados["bloco3"]["total_verificados"],
            "total_problemas": dados["bloco3"]["total_problemas"],
            "taxa_conformidade": dados["bloco3"]["taxa_conformidade"],
            "score_medio": dados["bloco3"]["score_medio"],
            "tipos_problemas": dados["bloco3"]["tipos_problemas"],
            "niveis_conformidade": dados["bloco3"]["niveis_conformidade"]
        },
        "bloco4_mcp": {
            "total_verificados": dados["bloco4"]["total_verificados"],
            "total_problemas": dados["bloco4"]["total_problemas"],
            "taxa_conformidade": dados["bloco4"]["taxa_conformidade"],
            "score_medio": dados["bloco4"]["score_medio"],
            "atendem_regra_mcp": dados["bloco4"]["atendem_regra_mcp"],
            "tipos_problemas": dados["bloco4"]["tipos_problemas"],
            "niveis_enriquecimento": dados["bloco4"]["niveis_enriquecimento"]
        }
    }
    
    # Problemas Identificados
    relatorio["problemas_identificados"] = {
        "categorizacao": {
            "total_problemas": dados["bloco2"]["total_problemas"],
            "principais_problemas": dict(sorted(dados["bloco2"]["tipos_problemas"].items(), key=lambda x: x[1], reverse=True)[:5])
        },
        "boilerplate": {
            "total_problemas": dados["bloco3"]["total_problemas"],
            "principais_problemas": dict(sorted(dados["bloco3"]["tipos_problemas"].items(), key=lambda x: x[1], reverse=True)[:5])
        },
        "mcp": {
            "total_problemas": dados["bloco4"]["total_problemas"],
            "principais_problemas": dict(sorted(dados["bloco4"]["tipos_problemas"].items(), key=lambda x: x[1], reverse=True)[:5])
        }
    }
    
    # Recomendações
    relatorio["recomendacoes"] = {
        "prioridade_alta": [],
        "prioridade_media": [],
        "prioridade_baixa": []
    }
    
    # Categorização (Prioridade Alta - 0% conformidade)
    if dados["bloco2"]["taxa_conformidade"] == 0:
        relatorio["recomendacoes"]["prioridade_alta"].append({
            "area": "Categorização",
            "problema": "0% de conformidade na categorização",
            "acao": "Implementar categorização obrigatória para todos os conteúdos",
            "impacto": "Crítico - Não atende Regra 2"
        })
    
    # Boilerplate (Prioridade Média - 71.4% conformidade)
    if dados["bloco3"]["taxa_conformidade"] < 80:
        relatorio["recomendacoes"]["prioridade_media"].append({
            "area": "Boilerplate",
            "problema": f"{dados['bloco3']['taxa_conformidade']:.1f}% de conformidade com boilerplate",
            "acao": "Corrigir estrutura dos conteúdos para seguir padrão",
            "impacto": "Médio - Melhora qualidade do conteúdo"
        })
    
    # MCP (Prioridade Baixa - 80.5% conformidade)
    if dados["bloco4"]["taxa_conformidade"] < 90:
        relatorio["recomendacoes"]["prioridade_baixa"].append({
            "area": "Enriquecimento MCP",
            "problema": f"{dados['bloco4']['taxa_conformidade']:.1f}% de conformidade com MCP",
            "acao": "Adicionar gráficos, vídeos e dados atuais",
            "impacto": "Baixo - Melhora experiência do usuário"
        })
    
    # Conclusões
    relatorio["conclusoes"] = {
        "status_geral": "CRÍTICO" if dados["bloco2"]["taxa_conformidade"] == 0 else "ATENÇÃO NECESSÁRIA",
        "principais_achados": [
            f"Total de {dados['bloco1']['total_paginas']} conteúdos analisados",
            f"{len(dados['bloco1']['conteudos_gestao'])} conteúdos de gestão identificados",
            f"Categorização: {dados['bloco2']['taxa_conformidade']:.1f}% de conformidade",
            f"Boilerplate: {dados['bloco3']['taxa_conformidade']:.1f}% de conformidade",
            f"MCP: {dados['bloco4']['taxa_conformidade']:.1f}% de conformidade"
        ],
        "acoes_imediata": [
            "Implementar categorização obrigatória (CRÍTICO)",
            "Corrigir estrutura dos conteúdos (MÉDIO)",
            "Enriquecer conteúdos com MCPs (BAIXO)"
        ]
    }
    
    return relatorio

def main():
    print("🔍 BLOCO 5: GERAÇÃO DO RELATÓRIO FINAL")
    print("======================================================================")
    print("📋 Consolidando análise de todos os blocos")
    print("======================================================================")
    
    # Carregar dados de todos os blocos
    dados = carregar_dados_todos_blocos()
    if not dados:
        print("❌ Erro: Não foi possível carregar dados de todos os blocos")
        return
    
    print("✅ Dados de todos os blocos carregados com sucesso!")
    
    # Gerar relatório final
    relatorio_final = gerar_relatorio_final(dados)
    
    # Salvar relatório
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"RELATORIO_FINAL_ANALISE_NOTION_{timestamp}.json"
    
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(relatorio_final, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n📊 RELATÓRIO FINAL GERADO:")
    print("======================================================================")
    
    # Resumo Executivo
    resumo = relatorio_final["resumo_executivo"]
    print(f"📋 Total de conteúdos analisados: {resumo['total_conteudos_analisados']}")
    print(f"🎯 Conteúdos de gestão: {resumo['conteudos_gestao']}")
    print(f"📚 Conteúdos não-gestão: {resumo['conteudos_nao_gestao']}")
    print(f"🏷️ Taxa conformidade categorização: {resumo['taxa_conformidade_categorizacao']:.1f}%")
    print(f"📝 Taxa conformidade boilerplate: {resumo['taxa_conformidade_boilerplate']:.1f}%")
    print(f"🎨 Taxa conformidade MCP: {resumo['taxa_conformidade_mcp']:.1f}%")
    
    # Status Geral
    print(f"\n🚨 STATUS GERAL: {relatorio_final['conclusoes']['status_geral']}")
    
    # Principais Achados
    print(f"\n📊 PRINCIPAIS ACHADOS:")
    for achado in relatorio_final["conclusoes"]["principais_achados"]:
        print(f"   • {achado}")
    
    # Ações Imediatas
    print(f"\n⚡ AÇÕES IMEDIATAS:")
    for acao in relatorio_final["conclusoes"]["acoes_imediata"]:
        print(f"   • {acao}")
    
    # Recomendações por Prioridade
    print(f"\n🎯 RECOMENDAÇÕES POR PRIORIDADE:")
    
    if relatorio_final["recomendacoes"]["prioridade_alta"]:
        print(f"\n🔴 PRIORIDADE ALTA:")
        for rec in relatorio_final["recomendacoes"]["prioridade_alta"]:
            print(f"   • {rec['area']}: {rec['problema']}")
            print(f"     Ação: {rec['acao']}")
            print(f"     Impacto: {rec['impacto']}")
    
    if relatorio_final["recomendacoes"]["prioridade_media"]:
        print(f"\n🟡 PRIORIDADE MÉDIA:")
        for rec in relatorio_final["recomendacoes"]["prioridade_media"]:
            print(f"   • {rec['area']}: {rec['problema']}")
            print(f"     Ação: {rec['acao']}")
            print(f"     Impacto: {rec['impacto']}")
    
    if relatorio_final["recomendacoes"]["prioridade_baixa"]:
        print(f"\n🟢 PRIORIDADE BAIXA:")
        for rec in relatorio_final["recomendacoes"]["prioridade_baixa"]:
            print(f"   • {rec['area']}: {rec['problema']}")
            print(f"     Ação: {rec['acao']}")
            print(f"     Impacto: {rec['impacto']}")
    
    print(f"\n💾 Relatório final salvo em: {nome_arquivo}")
    
    print("\n✅ BLOCO 5 CONCLUÍDO!")
    print("🎉 ANÁLISE COMPLETA FINALIZADA!")
    print("======================================================================")
    print("📋 Todos os 5 blocos foram executados com sucesso:")
    print("   ✅ Bloco 1: Análise básica")
    print("   ✅ Bloco 2: Verificação de categorização")
    print("   ✅ Bloco 3: Verificação de conformidade com boilerplate")
    print("   ✅ Bloco 4: Verificação de enriquecimento MCP")
    print("   ✅ Bloco 5: Relatório final")
    print("======================================================================")

if __name__ == "__main__":
    main()
