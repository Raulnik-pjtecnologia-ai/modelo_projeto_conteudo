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

def verificar_conformidade_boilerplate(page_id, titulo, tipo):
    """Verifica se uma página está em conformidade com o boilerplate."""
    try:
        # Buscar conteúdo da página
        blocks = notion.blocks.children.list(block_id=page_id)
        
        # Analisar estrutura do conteúdo
        conteudo_texto = ""
        estrutura_encontrada = {
            "tem_capa": False,
            "tem_resumo_executivo": False,
            "tem_contexto": False,
            "tem_dados_graficos": False,
            "tem_videos": False,
            "tem_fontes": False,
            "tem_conclusao": False,
            "tem_acoes_praticas": False
        }
        
        # Palavras-chave para identificar seções do boilerplate
        keywords_boilerplate = {
            "tem_capa": ["capa", "cover", "imagem de capa", "![capa"],
            "tem_resumo_executivo": ["resumo executivo", "executive summary", "impacto", "estratégia", "eficiência"],
            "tem_contexto": ["contexto", "por que", "fundamental", "importante", "necessário"],
            "tem_dados_graficos": ["dados", "gráfico", "grafico", "tabela", "estatística", "indicador"],
            "tem_videos": ["vídeo", "video", "youtube", "assistir", "tutorial"],
            "tem_fontes": ["fonte", "referência", "referencia", "bibliografia", "link"],
            "tem_conclusao": ["conclusão", "conclusao", "considerações finais", "resumo final"],
            "tem_acoes_praticas": ["ação", "acao", "prática", "pratica", "implementar", "aplicar"]
        }
        
        # Analisar cada bloco
        for block in blocks["results"]:
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
        
        # Verificar presença de cada seção
        for secao, keywords in keywords_boilerplate.items():
            for keyword in keywords:
                if keyword in conteudo_texto:
                    estrutura_encontrada[secao] = True
                    break
        
        # Calcular score de conformidade
        secoes_encontradas = sum(1 for v in estrutura_encontrada.values() if v)
        total_secoes = len(estrutura_encontrada)
        score_conformidade = (secoes_encontradas / total_secoes) * 100
        
        # Determinar nível de conformidade
        if score_conformidade >= 80:
            nivel_conformidade = "Alto"
        elif score_conformidade >= 60:
            nivel_conformidade = "Médio"
        elif score_conformidade >= 40:
            nivel_conformidade = "Baixo"
        else:
            nivel_conformidade = "Muito Baixo"
        
        # Verificar se tem conteúdo mínimo
        tem_conteudo_minimo = len(conteudo_texto) > 500
        
        return {
            "estrutura_encontrada": estrutura_encontrada,
            "secoes_encontradas": secoes_encontradas,
            "total_secoes": total_secoes,
            "score_conformidade": score_conformidade,
            "nivel_conformidade": nivel_conformidade,
            "tem_conteudo_minimo": tem_conteudo_minimo,
            "tamanho_conteudo": len(conteudo_texto)
        }
        
    except Exception as e:
        print(f"Erro ao verificar conformidade da página {page_id}: {e}")
        return None

def main():
    print("🔍 BLOCO 3: VERIFICAÇÃO DE CONFORMIDADE COM BOILERPLATE")
    print("======================================================================")
    print("📋 Aplicando Regra 2: Conformidade com Boilerplate")
    print("======================================================================")
    
    # Carregar dados do Bloco 1
    dados_bloco1 = carregar_dados_bloco1()
    if not dados_bloco1:
        print("❌ Erro: Não foi possível carregar dados do Bloco 1")
        return
    
    conteudos_gestao = dados_bloco1["conteudos_gestao"]
    print(f"📊 Analisando {len(conteudos_gestao)} conteúdos de gestão...\n")
    
    # Verificar conformidade de cada conteúdo
    verificacoes = []
    problemas_boilerplate = []
    
    print("🔍 VERIFICANDO CONFORMIDADE COM BOILERPLATE...")
    print("======================================================================\n")
    
    for i, conteudo in enumerate(conteudos_gestao):
        print(f"{i+1}/{len(conteudos_gestao)} - {conteudo['titulo'][:60]}...")
        
        verificacao = verificar_conformidade_boilerplate(
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
            if not verificacao["tem_conteudo_minimo"]:
                problemas.append("Conteúdo insuficiente")
            if verificacao["score_conformidade"] < 60:
                problemas.append("Baixa conformidade com boilerplate")
            if not verificacao["estrutura_encontrada"]["tem_capa"]:
                problemas.append("Sem capa")
            if not verificacao["estrutura_encontrada"]["tem_resumo_executivo"]:
                problemas.append("Sem resumo executivo")
            if not verificacao["estrutura_encontrada"]["tem_contexto"]:
                problemas.append("Sem contexto")
            if not verificacao["estrutura_encontrada"]["tem_dados_graficos"]:
                problemas.append("Sem dados/gráficos")
            if not verificacao["estrutura_encontrada"]["tem_videos"]:
                problemas.append("Sem vídeos")
            if not verificacao["estrutura_encontrada"]["tem_fontes"]:
                problemas.append("Sem fontes")
            
            if problemas:
                problemas_boilerplate.append({
                    "titulo": conteudo["titulo"],
                    "tipo": conteudo["tipo"],
                    "id": conteudo["id"],
                    "problemas": problemas,
                    "score_conformidade": verificacao["score_conformidade"],
                    "nivel_conformidade": verificacao["nivel_conformidade"],
                    "tamanho_conteudo": verificacao["tamanho_conteudo"]
                })
        
        if (i + 1) % 50 == 0:
            print(f"✅ Verificadas {i + 1}/{len(conteudos_gestao)} páginas...")
    
    print(f"\n📊 RESUMO DO BLOCO 3:")
    print("======================================================================")
    
    total_verificados = len(verificacoes)
    total_problemas = len(problemas_boilerplate)
    taxa_conformidade = ((total_verificados - total_problemas) / total_verificados * 100) if total_verificados > 0 else 0
    
    print(f"📋 Total de conteúdos verificados: {total_verificados}")
    print(f"✅ Conteúdos em conformidade: {total_verificados - total_problemas}")
    print(f"❌ Conteúdos com problemas: {total_problemas}")
    print(f"📊 Taxa de conformidade: {taxa_conformidade:.1f}%")
    
    # Estatísticas dos problemas
    tipos_problemas = {}
    niveis_conformidade = {}
    
    for item in problemas_boilerplate:
        for problema in item["problemas"]:
            tipos_problemas[problema] = tipos_problemas.get(problema, 0) + 1
        
        nivel = item["nivel_conformidade"]
        niveis_conformidade[nivel] = niveis_conformidade.get(nivel, 0) + 1
    
    print(f"\n📊 TIPOS DE PROBLEMAS ENCONTRADOS:")
    for problema, count in sorted(tipos_problemas.items()):
        print(f"   • {problema}: {count}")
    
    print(f"\n📊 DISTRIBUIÇÃO POR NÍVEL DE CONFORMIDADE:")
    for nivel, count in sorted(niveis_conformidade.items()):
        print(f"   • {nivel}: {count}")
    
    # Calcular score médio
    scores = [item["score_conformidade"] for item in problemas_boilerplate]
    score_medio = sum(scores) / len(scores) if scores else 0
    
    print(f"\n📊 SCORE MÉDIO DE CONFORMIDADE: {score_medio:.1f}%")
    
    # Salvar dados para próximos blocos
    dados_bloco3 = {
        "data_analise": datetime.now().isoformat(),
        "total_verificados": total_verificados,
        "total_problemas": total_problemas,
        "taxa_conformidade": taxa_conformidade,
        "score_medio": score_medio,
        "verificacoes": verificacoes,
        "problemas_boilerplate": problemas_boilerplate,
        "tipos_problemas": tipos_problemas,
        "niveis_conformidade": niveis_conformidade
    }
    
    with open("dados_bloco3_analise_notion.json", "w", encoding="utf-8") as f:
        json.dump(dados_bloco3, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Dados do Bloco 3 salvos em: dados_bloco3_analise_notion.json")
    
    if total_problemas > 0:
        print(f"\n⚠️  {total_problemas} conteúdos precisam de correção na conformidade com boilerplate")
        print("   Exemplos de problemas:")
        for i, item in enumerate(problemas_boilerplate[:5]):
            print(f"   {i+1}. {item['titulo'][:50]}... - Score: {item['score_conformidade']:.1f}% - {', '.join(item['problemas'][:2])}")
    else:
        print(f"\n🎉 Todos os conteúdos estão em conformidade com o boilerplate!")
    
    print("\n✅ BLOCO 3 CONCLUÍDO!")
    print("   Próximo: Bloco 4 - Verificar enriquecimento MCP")

if __name__ == "__main__":
    main()
