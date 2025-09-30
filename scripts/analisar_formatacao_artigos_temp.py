import os
import json
import time
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def analisar_formatacao_artigos():
    """Analisar formatação dos artigos e títulos no Notion."""
    print("ANALISE DE FORMATACAO DOS ARTIGOS E TITULOS")
    print("=" * 60)
    
    # Carregar configuracao
    load_dotenv()
    
    notion_token = os.getenv("NOTION_TOKEN")
    
    if not notion_token:
        print("ERRO: Configuracao do Notion nao encontrada")
        return False
    
    # Inicializar cliente Notion
    notion = Client(auth=notion_token)
    
    try:
        # Buscar database "Editorial Gestao Educacional"
        databases = notion.search(filter={"property": "object", "value": "database"})
        
        database_id = None
        for db in databases["results"]:
            if "title" in db and len(db["title"]) > 0:
                if "gestao" in db["title"][0]["text"]["content"].lower() or "editorial" in db["title"][0]["text"]["content"].lower():
                    database_id = db["id"]
                    print(f"Database encontrado: {db['title'][0]['text']['content']}")
                    break
        
        if not database_id:
            print("ERRO: Database 'Editorial Gestao Educacional' nao encontrado")
            return False
        
        # Buscar todas as paginas do database
        pages = notion.databases.query(database_id=database_id)
        
        print(f"ANALISANDO {len(pages['results'])} ARTIGOS...")
        
        artigos_analisados = []
        problemas_formatacao = []
        
        for i, page in enumerate(pages["results"]):
            page_id = page["id"]
            
            # Extrair titulo da pagina
            titulo = ""
            if "properties" in page and "Name" in page["properties"]:
                if page["properties"]["Name"]["title"]:
                    titulo = page["properties"]["Name"]["title"][0]["text"]["content"]
            
            print(f"   {i+1}/{len(pages['results'])}: {titulo[:50]}...")
            
            try:
                # Buscar conteudo da pagina
                page_blocks = notion.blocks.children.list(block_id=page_id)
                
                # Analisar formatação
                problemas_encontrados = []
                
                # Verificar estrutura de títulos
                niveis_titulos = []
                titulos_sem_hierarquia = []
                
                for block in page_blocks["results"]:
                    if block["type"].startswith("heading_"):
                        nivel = int(block["type"].split("_")[1])
                        niveis_titulos.append(nivel)
                        
                        # Verificar se o título tem conteúdo
                        if "rich_text" in block[block["type"]]:
                            texto_titulo = ""
                            for rt in block[block["type"]]["rich_text"]:
                                texto_titulo += rt["text"]["content"]
                            
                            if not texto_titulo.strip():
                                problemas_encontrados.append(f"Título vazio no nível {nivel}")
                            elif len(texto_titulo.strip()) < 3:
                                problemas_encontrados.append(f"Título muito curto: '{texto_titulo.strip()}'")
                            elif not texto_titulo.strip()[0].isupper():
                                problemas_encontrados.append(f"Título não inicia com maiúscula: '{texto_titulo.strip()}'")
                
                # Verificar hierarquia de títulos
                if niveis_titulos:
                    niveis_unicos = sorted(set(niveis_titulos))
                    for i, nivel in enumerate(niveis_unicos):
                        if i > 0 and nivel - niveis_unicos[i-1] > 1:
                            problemas_encontrados.append(f"Hierarquia de títulos quebrada: nível {niveis_unicos[i-1]} para {nivel}")
                
                # Verificar se há pelo menos um título H1
                if 1 not in niveis_titulos:
                    problemas_encontrados.append("Nenhum título H1 encontrado")
                
                # Verificar estrutura de parágrafos
                paragrafos_vazios = 0
                paragrafos_muito_curtos = 0
                
                for block in page_blocks["results"]:
                    if block["type"] == "paragraph":
                        if "rich_text" in block["paragraph"]:
                            texto_paragrafo = ""
                            for rt in block["paragraph"]["rich_text"]:
                                texto_paragrafo += rt["text"]["content"]
                            
                            if not texto_paragrafo.strip():
                                paragrafos_vazios += 1
                            elif len(texto_paragrafo.strip()) < 10:
                                paragrafos_muito_curtos += 1
                
                if paragrafos_vazios > 0:
                    problemas_encontrados.append(f"{paragrafos_vazios} parágrafos vazios encontrados")
                
                if paragrafos_muito_curtos > 3:
                    problemas_encontrados.append(f"{paragrafos_muito_curtos} parágrafos muito curtos encontrados")
                
                # Verificar formatação de listas
                listas_mal_formatadas = 0
                for block in page_blocks["results"]:
                    if block["type"] in ["bulleted_list_item", "numbered_list_item"]:
                        if "rich_text" in block[block["type"]]:
                            texto_item = ""
                            for rt in block[block["type"]]["rich_text"]:
                                texto_item += rt["text"]["content"]
                            
                            if not texto_item.strip():
                                listas_mal_formatadas += 1
                
                if listas_mal_formatadas > 0:
                    problemas_encontrados.append(f"{listas_mal_formatadas} itens de lista vazios encontrados")
                
                # Verificar formatação de código
                blocos_codigo_sem_sintaxe = 0
                for block in page_blocks["results"]:
                    if block["type"] == "code":
                        if "language" not in block["code"] or not block["code"]["language"]:
                            blocos_codigo_sem_sintaxe += 1
                
                if blocos_codigo_sem_sintaxe > 0:
                    problemas_encontrados.append(f"{blocos_codigo_sem_sintaxe} blocos de código sem linguagem especificada")
                
                # Classificar severidade dos problemas
                severidade = "BAIXA"
                if len(problemas_encontrados) > 5:
                    severidade = "ALTA"
                elif len(problemas_encontrados) > 2:
                    severidade = "MEDIA"
                
                # Adicionar à lista de artigos analisados
                artigos_analisados.append({
                    "page_id": page_id,
                    "titulo": titulo,
                    "problemas_encontrados": problemas_encontrados,
                    "total_problemas": len(problemas_encontrados),
                    "severidade": severidade,
                    "niveis_titulos": niveis_titulos,
                    "paragrafos_vazios": paragrafos_vazios,
                    "paragrafos_muito_curtos": paragrafos_muito_curtos,
                    "listas_mal_formatadas": listas_mal_formatadas,
                    "blocos_codigo_sem_sintaxe": blocos_codigo_sem_sintaxe
                })
                
                if problemas_encontrados:
                    problemas_formatacao.append({
                        "page_id": page_id,
                        "titulo": titulo,
                        "problemas": problemas_encontrados,
                        "severidade": severidade
                    })
                    print(f"      PROBLEMAS: {len(problemas_encontrados)} ({severidade})")
                else:
                    print(f"      OK - Formatação correta")
                
                # Pausa entre análises
                time.sleep(1)
                
            except Exception as e:
                print(f"      ERRO: {str(e)[:30]}...")
        
        # Calcular estatísticas
        total_artigos = len(artigos_analisados)
        artigos_com_problemas = len(problemas_formatacao)
        artigos_sem_problemas = total_artigos - artigos_com_problemas
        
        problemas_por_severidade = {
            "ALTA": len([p for p in problemas_formatacao if p["severidade"] == "ALTA"]),
            "MEDIA": len([p for p in problemas_formatacao if p["severidade"] == "MEDIA"]),
            "BAIXA": len([p for p in problemas_formatacao if p["severidade"] == "BAIXA"])
        }
        
        print(f"\nRESULTADOS DA ANALISE DE FORMATACAO:")
        print(f"   Total de artigos analisados: {total_artigos}")
        print(f"   Artigos sem problemas: {artigos_sem_problemas}")
        print(f"   Artigos com problemas: {artigos_com_problemas}")
        print(f"   Problemas de severidade ALTA: {problemas_por_severidade['ALTA']}")
        print(f"   Problemas de severidade MEDIA: {problemas_por_severidade['MEDIA']}")
        print(f"   Problemas de severidade BAIXA: {problemas_por_severidade['BAIXA']}")
        
        # Salvar resultados da análise
        dados_analise = {
            "data_analise": datetime.now().isoformat(),
            "total_artigos_analisados": total_artigos,
            "artigos_sem_problemas": artigos_sem_problemas,
            "artigos_com_problemas": artigos_com_problemas,
            "problemas_por_severidade": problemas_por_severidade,
            "artigos_analisados": artigos_analisados,
            "problemas_formatacao": problemas_formatacao
        }
        
        with open("analise_formatacao_artigos.json", "w", encoding="utf-8") as f:
            json.dump(dados_analise, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\nANALISE DE FORMATACAO CONCLUIDA!")
        print(f"   {artigos_sem_problemas}/{total_artigos} artigos com formatação correta")
        print(f"   {artigos_com_problemas} artigos precisam de correção")
        print(f"   Dados salvos em analise_formatacao_artigos.json")
        
        return artigos_com_problemas > 0
        
    except Exception as e:
        print(f"Erro na análise de formatação: {e}")
        return False

def main():
    print("ANALISE DE FORMATACAO DOS ARTIGOS E TITULOS")
    print("=" * 60)
    
    tem_problemas = analisar_formatacao_artigos()
    
    if tem_problemas:
        print(f"\nANALISE CONCLUIDA - PROBLEMAS ENCONTRADOS!")
        print(f"   Necessário aplicar correções de formatação")
        print(f"   Verificar arquivo analise_formatacao_artigos.json")
    else:
        print(f"\nANALISE CONCLUIDA - FORMATACAO CORRETA!")
        print(f"   Todos os artigos estão bem formatados")
    
    return tem_problemas

if __name__ == "__main__":
    main()
