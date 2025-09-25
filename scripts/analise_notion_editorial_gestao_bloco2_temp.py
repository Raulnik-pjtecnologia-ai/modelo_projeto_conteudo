import os
import json
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def analisar_editorial_gestao_bloco2():
    """BLOCO 2: Buscar conteúdo das páginas e analisar títulos."""
    print("🔍 BLOCO 2: ANALISANDO CONTEÚDO DAS PÁGINAS")
    print("=" * 60)
    
    # Carregar configuração
    load_dotenv()
    
    notion_token = os.getenv("NOTION_TOKEN")
    
    if not notion_token:
        print("❌ Configuração do Notion não encontrada")
        return False
    
    # Inicializar cliente Notion
    notion = Client(auth=notion_token)
    
    try:
        # Carregar dados do bloco 1
        with open("dados_analise_bloco1_editorial_gestao.json", "r", encoding="utf-8") as f:
            dados_bloco1 = json.load(f)
        
        paginas_info = dados_bloco1["paginas_info"]
        
        print(f"📊 Analisando {len(paginas_info)} páginas...")
        
        # Analisar cada página para obter o título real
        paginas_analisadas = []
        paginas_parceiro_escola = []
        paginas_gestao = []
        
        for i, pagina_info in enumerate(paginas_info):
            page_id = pagina_info["page_id"]
            
            try:
                # Buscar a página completa
                page = notion.pages.retrieve(page_id)
                properties = page.get("properties", {})
                
                # Extrair título real
                titulo = ""
                if "Título" in properties:
                    titulo_prop = properties["Título"]
                    if titulo_prop.get("title"):
                        titulo = titulo_prop["title"][0]["text"]["content"]
                
                # Se não encontrou no Título, tentar buscar no conteúdo
                if not titulo:
                    # Buscar blocos da página para encontrar o título
                    blocks_response = notion.blocks.children.list(page_id)
                    blocks = blocks_response.get("results", [])
                    
                    for block in blocks:
                        if block.get("type") == "heading_1":
                            heading = block.get("heading_1", {})
                            rich_text = heading.get("rich_text", [])
                            if rich_text:
                                titulo = rich_text[0]["text"]["content"]
                                break
                        elif block.get("type") == "heading_2":
                            heading = block.get("heading_2", {})
                            rich_text = heading.get("rich_text", [])
                            if rich_text and not titulo:
                                titulo = rich_text[0]["text"]["content"]
                
                # Atualizar informações da página
                pagina_atualizada = {
                    "page_id": page_id,
                    "titulo": titulo,
                    "tipo": pagina_info["tipo"],
                    "status": pagina_info["status"],
                    "data_criacao": pagina_info["data_criacao"],
                    "contem_parceiro_escola": False,
                    "eh_conteudo_gestao": False
                }
                
                # Verificar se contém "Parceiro da Escola"
                if titulo and "parceiro da escola" in titulo.lower():
                    pagina_atualizada["contem_parceiro_escola"] = True
                    paginas_parceiro_escola.append(pagina_atualizada)
                    print(f"   🎯 PARCEIRO DA ESCOLA: {titulo}")
                
                # Verificar se é conteúdo de gestão
                if titulo:
                    palavras_gestao = ["gestão", "administração", "escolar", "educacional", "pedagógico", "diretor", "coordenador"]
                    if any(palavra in titulo.lower() for palavra in palavras_gestao):
                        pagina_atualizada["eh_conteudo_gestao"] = True
                        paginas_gestao.append(pagina_atualizada)
                        print(f"   📚 GESTÃO: {titulo}")
                
                paginas_analisadas.append(pagina_atualizada)
                
                # Progresso
                if (i + 1) % 10 == 0:
                    print(f"   📊 Progresso: {i + 1}/{len(paginas_info)} páginas analisadas")
                
            except Exception as e:
                print(f"   ⚠️ Erro ao analisar página {page_id}: {e}")
                # Manter informações originais em caso de erro
                paginas_analisadas.append(pagina_info)
        
        # Salvar dados do bloco 2
        dados_bloco2 = {
            "data_analise": datetime.now().isoformat(),
            "bloco": 2,
            "total_paginas": len(paginas_analisadas),
            "paginas_parceiro_escola": len(paginas_parceiro_escola),
            "paginas_gestao": len(paginas_gestao),
            "paginas_analisadas": paginas_analisadas,
            "paginas_parceiro_escola_detalhadas": paginas_parceiro_escola,
            "paginas_gestao_detalhadas": paginas_gestao
        }
        
        with open("dados_analise_bloco2_editorial_gestao.json", "w", encoding="utf-8") as f:
            json.dump(dados_bloco2, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n📊 RESUMO BLOCO 2:")
        print(f"   📄 Total de páginas analisadas: {len(paginas_analisadas)}")
        print(f"   🎯 Páginas 'Parceiro da Escola': {len(paginas_parceiro_escola)}")
        print(f"   📚 Páginas de Gestão: {len(paginas_gestao)}")
        print(f"   💾 Dados salvos: dados_analise_bloco2_editorial_gestao.json")
        
        if paginas_parceiro_escola:
            print(f"\n🎯 PÁGINAS COM 'PARCEIRO DA ESCOLA':")
            for i, pagina in enumerate(paginas_parceiro_escola, 1):
                print(f"   {i}. {pagina['titulo']} ({pagina['page_id']})")
        
        if paginas_gestao:
            print(f"\n📚 PÁGINAS DE GESTÃO:")
            for i, pagina in enumerate(paginas_gestao[:10], 1):  # Mostrar apenas as primeiras 10
                print(f"   {i}. {pagina['titulo']} ({pagina['page_id']})")
            if len(paginas_gestao) > 10:
                print(f"   ... e mais {len(paginas_gestao) - 10} páginas de gestão")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no Bloco 2: {e}")
        return False

def main():
    print("🔍 ANÁLISE EDITORIAL DE GESTÃO - BLOCO 2")
    print("======================================================================")
    print("📋 Analisando conteúdo das páginas para identificar títulos")
    print("======================================================================")
    
    sucesso = analisar_editorial_gestao_bloco2()
    
    if sucesso:
        print(f"\n✅ BLOCO 2 CONCLUÍDO COM SUCESSO!")
        print(f"   📊 Páginas analisadas")
        print(f"   🎯 Páginas 'Parceiro da Escola' identificadas")
        print(f"   📚 Páginas de Gestão identificadas")
        print(f"   💾 Dados salvos para próximos blocos")
    else:
        print(f"\n❌ ERRO NO BLOCO 2")
        print(f"   🔧 Verificar configuração")
        print(f"   📋 Revisar processo")
    
    return sucesso

if __name__ == "__main__":
    main()

