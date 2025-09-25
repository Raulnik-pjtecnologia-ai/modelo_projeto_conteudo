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

def carregar_dados_bloco1():
    """Carrega os dados do Bloco 1."""
    try:
        with open("dados_bloco1_analise_notion.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar dados do Bloco 1: {e}")
        return None

def verificar_enriquecimento_mcp(page_id, titulo, tipo):
    """Verifica se uma página tem enriquecimento MCP (Regra 1)."""
    try:
        # Buscar conteúdo da página
        blocks = notion.blocks.children.list(block_id=page_id)
        
        # Analisar enriquecimento MCP
        enriquecimento_encontrado = {
            "tem_graficos": False,
            "tem_videos_youtube": False,
            "tem_dados_atuais": False,
            "tem_fontes_confiaveis": False,
            "tem_imagens": False,
            "tem_tabelas": False,
            "tem_links_externos": False,
            "tem_estatisticas": False
        }
        
        conteudo_texto = ""
        
        # Analisar cada bloco
        for block in blocks["results"]:
            # Verificar tipos de bloco que indicam enriquecimento
            if block.get("type") == "image":
                enriquecimento_encontrado["tem_imagens"] = True
            elif block.get("type") == "video":
                enriquecimento_encontrado["tem_videos_youtube"] = True
            elif block.get("type") == "table":
                enriquecimento_encontrado["tem_tabelas"] = True
            elif block.get("type") == "bookmark":
                enriquecimento_encontrado["tem_links_externos"] = True
            elif block.get("type") == "embed":
                enriquecimento_encontrado["tem_links_externos"] = True
            
            # Analisar texto para identificar enriquecimento
            if block.get("type") == "paragraph" and block.get("paragraph", {}).get("rich_text"):
                for text in block["paragraph"]["rich_text"]:
                    conteudo_texto += text.get("text", {}).get("content", "").lower()
            elif block.get("type") == "heading_1" and block.get("heading_1", {}).get("rich_text"):
                for text in block["heading_1"]["rich_text"]:
                    conteudo_texto += text.get("text", {}).get("content", "").lower()
            elif block.get("type") == "heading_2" and block.get("heading_2", {}).get("rich_text"):
                for text in block["heading_2"]["rich_text"]:
                    conteudo_texto += text.get("text", {}).get("content", "").lower()
            elif block.get("type") == "heading_3" and block.get("heading_3", {}).get("rich_text"):
                for text in block["heading_3"]["rich_text"]:
                    conteudo_texto += text.get("text", {}).get("content", "").lower()
        
        # Verificar indicadores de enriquecimento no texto
        indicadores_enriquecimento = {
            "tem_graficos": ["gráfico", "grafico", "chart", "visualização", "visualizacao", "dados visuais"],
            "tem_videos_youtube": ["youtube", "vídeo", "video", "assistir", "tutorial", "demonstração"],
            "tem_dados_atuais": ["2024", "2023", "atual", "recente", "último", "ultimo", "dados oficiais"],
            "tem_fontes_confiaveis": ["fonte:", "referência", "referencia", "bibliografia", "link:", "http", "www"],
            "tem_estatisticas": ["%", "porcentagem", "milhões", "milhoes", "milhares", "estatística", "estatistica", "dados"]
        }
        
        for categoria, keywords in indicadores_enriquecimento.items():
            for keyword in keywords:
                if keyword in conteudo_texto:
                    enriquecimento_encontrado[categoria] = True
                    break
        
        # Calcular score de enriquecimento
        elementos_encontrados = sum(1 for v in enriquecimento_encontrado.values() if v)
        total_elementos = len(enriquecimento_encontrado)
        score_enriquecimento = (elementos_encontrados / total_elementos) * 100
        
        # Determinar nível de enriquecimento
        if score_enriquecimento >= 80:
            nivel_enriquecimento = "Alto"
        elif score_enriquecimento >= 60:
            nivel_enriquecimento = "Médio"
        elif score_enriquecimento >= 40:
            nivel_enriquecimento = "Baixo"
        else:
            nivel_enriquecimento = "Muito Baixo"
        
        # Verificar se atende critérios mínimos da Regra 1
        criterios_minimos = [
            enriquecimento_encontrado["tem_graficos"] or enriquecimento_encontrado["tem_imagens"],
            enriquecimento_encontrado["tem_videos_youtube"],
            enriquecimento_encontrado["tem_dados_atuais"] or enriquecimento_encontrado["tem_estatisticas"],
            enriquecimento_encontrado["tem_fontes_confiaveis"]
        ]
        
        criterios_atendidos = sum(criterios_minimos)
        atende_regra_mcp = criterios_atendidos >= 3  # Pelo menos 3 dos 4 critérios
        
        return {
            "enriquecimento_encontrado": enriquecimento_encontrado,
            "elementos_encontrados": elementos_encontrados,
            "total_elementos": total_elementos,
            "score_enriquecimento": score_enriquecimento,
            "nivel_enriquecimento": nivel_enriquecimento,
            "criterios_atendidos": criterios_atendidos,
            "atende_regra_mcp": atende_regra_mcp,
            "tamanho_conteudo": len(conteudo_texto)
        }
        
    except Exception as e:
        print(f"Erro ao verificar enriquecimento da página {page_id}: {e}")
        return None

def main():
    print("🔍 BLOCO 4: VERIFICAÇÃO DE ENRIQUECIMENTO MCP")
    print("======================================================================")
    print("📋 Aplicando Regra 1: Enriquecimento MCP Obrigatório")
    print("======================================================================")
    
    # Carregar dados do Bloco 1
    dados_bloco1 = carregar_dados_bloco1()
    if not dados_bloco1:
        print("❌ Erro: Não foi possível carregar dados do Bloco 1")
        return
    
    conteudos_gestao = dados_bloco1["conteudos_gestao"]
    print(f"📊 Analisando {len(conteudos_gestao)} conteúdos de gestão...\n")
    
    # Verificar enriquecimento de cada conteúdo
    verificacoes = []
    problemas_enriquecimento = []
    
    print("🔍 VERIFICANDO ENRIQUECIMENTO MCP...")
    print("======================================================================\n")
    
    for i, conteudo in enumerate(conteudos_gestao):
        print(f"{i+1}/{len(conteudos_gestao)} - {conteudo['titulo'][:60]}...")
        
        verificacao = verificar_enriquecimento_mcp(
            conteudo["id"], 
            conteudo["titulo"], 
            conteudo["tipo"]
        )
        
        if verificacao:
            verificacoes.append({
                "titulo": conteudo["titulo"],
                "tipo": conteudo["tipo"],
                "id": conteudo["id"],
                "verificacao": verificacao
            })
            
            # Identificar problemas
            problemas = []
            if not verificacao["atende_regra_mcp"]:
                problemas.append("Não atende Regra MCP")
            if verificacao["score_enriquecimento"] < 50:
                problemas.append("Baixo enriquecimento")
            if not verificacao["enriquecimento_encontrado"]["tem_graficos"] and not verificacao["enriquecimento_encontrado"]["tem_imagens"]:
                problemas.append("Sem gráficos/imagens")
            if not verificacao["enriquecimento_encontrado"]["tem_videos_youtube"]:
                problemas.append("Sem vídeos")
            if not verificacao["enriquecimento_encontrado"]["tem_dados_atuais"] and not verificacao["enriquecimento_encontrado"]["tem_estatisticas"]:
                problemas.append("Sem dados atuais")
            if not verificacao["enriquecimento_encontrado"]["tem_fontes_confiaveis"]:
                problemas.append("Sem fontes confiáveis")
            
            if problemas:
                problemas_enriquecimento.append({
                    "titulo": conteudo["titulo"],
                    "tipo": conteudo["tipo"],
                    "id": conteudo["id"],
                    "problemas": problemas,
                    "score_enriquecimento": verificacao["score_enriquecimento"],
                    "nivel_enriquecimento": verificacao["nivel_enriquecimento"],
                    "criterios_atendidos": verificacao["criterios_atendidos"]
                })
        
        if (i + 1) % 50 == 0:
            print(f"✅ Verificadas {i + 1}/{len(conteudos_gestao)} páginas...")
    
    print(f"\n📊 RESUMO DO BLOCO 4:")
    print("======================================================================")
    
    total_verificados = len(verificacoes)
    total_problemas = len(problemas_enriquecimento)
    taxa_conformidade = ((total_verificados - total_problemas) / total_verificados * 100) if total_verificados > 0 else 0
    
    print(f"📋 Total de conteúdos verificados: {total_verificados}")
    print(f"✅ Conteúdos em conformidade: {total_verificados - total_problemas}")
    print(f"❌ Conteúdos com problemas: {total_problemas}")
    print(f"📊 Taxa de conformidade: {taxa_conformidade:.1f}%")
    
    # Estatísticas dos problemas
    tipos_problemas = {}
    niveis_enriquecimento = {}
    
    for item in problemas_enriquecimento:
        for problema in item["problemas"]:
            tipos_problemas[problema] = tipos_problemas.get(problema, 0) + 1
        
        nivel = item["nivel_enriquecimento"]
        niveis_enriquecimento[nivel] = niveis_enriquecimento.get(nivel, 0) + 1
    
    print(f"\n📊 TIPOS DE PROBLEMAS ENCONTRADOS:")
    for problema, count in sorted(tipos_problemas.items()):
        print(f"   • {problema}: {count}")
    
    print(f"\n📊 DISTRIBUIÇÃO POR NÍVEL DE ENRIQUECIMENTO:")
    for nivel, count in sorted(niveis_enriquecimento.items()):
        print(f"   • {nivel}: {count}")
    
    # Calcular score médio
    scores = [item["score_enriquecimento"] for item in problemas_enriquecimento]
    score_medio = sum(scores) / len(scores) if scores else 0
    
    print(f"\n📊 SCORE MÉDIO DE ENRIQUECIMENTO: {score_medio:.1f}%")
    
    # Contar quantos atendem a Regra MCP
    atendem_regra = sum(1 for v in verificacoes if v["verificacao"]["atende_regra_mcp"])
    print(f"📊 CONTEÚDOS QUE ATENDEM REGRA MCP: {atendem_regra}/{total_verificados} ({atendem_regra/total_verificados*100:.1f}%)")
    
    # Salvar dados para próximos blocos
    dados_bloco4 = {
        "data_analise": datetime.now().isoformat(),
        "total_verificados": total_verificados,
        "total_problemas": total_problemas,
        "taxa_conformidade": taxa_conformidade,
        "score_medio": score_medio,
        "atendem_regra_mcp": atendem_regra,
        "verificacoes": verificacoes,
        "problemas_enriquecimento": problemas_enriquecimento,
        "tipos_problemas": tipos_problemas,
        "niveis_enriquecimento": niveis_enriquecimento
    }
    
    with open("dados_bloco4_analise_notion.json", "w", encoding="utf-8") as f:
        json.dump(dados_bloco4, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Dados do Bloco 4 salvos em: dados_bloco4_analise_notion.json")
    
    if total_problemas > 0:
        print(f"\n⚠️  {total_problemas} conteúdos precisam de enriquecimento MCP")
        print("   Exemplos de problemas:")
        for i, item in enumerate(problemas_enriquecimento[:5]):
            print(f"   {i+1}. {item['titulo'][:50]}... - Score: {item['score_enriquecimento']:.1f}% - {', '.join(item['problemas'][:2])}")
    else:
        print(f"\n🎉 Todos os conteúdos atendem à Regra MCP!")
    
    print("\n✅ BLOCO 4 CONCLUÍDO!")
    print("   Próximo: Bloco 5 - Gerar relatório final")

if __name__ == "__main__":
    main()
