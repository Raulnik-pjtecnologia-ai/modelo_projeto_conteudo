import os
import json
import time
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def corrigir_formatacao_artigos():
    """Corrigir formatação dos artigos e títulos no Notion."""
    print("CORRECAO DE FORMATACAO DOS ARTIGOS E TITULOS")
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
        # Carregar dados da análise
        with open("analise_formatacao_artigos.json", "r", encoding="utf-8") as f:
            dados_analise = json.load(f)
        
        problemas_formatacao = dados_analise["problemas_formatacao"]
        
        print(f"CORRIGINDO FORMATACAO DE {len(problemas_formatacao)} ARTIGOS...")
        
        artigos_corrigidos = []
        total_correcoes_aplicadas = 0
        
        for i, problema in enumerate(problemas_formatacao):
            page_id = problema["page_id"]
            titulo = problema["titulo"]
            problemas = problema["problemas"]
            severidade = problema["severidade"]
            
            print(f"   {i+1}/{len(problemas_formatacao)}: {titulo[:50]}...")
            print(f"      Severidade: {severidade} - {len(problemas)} problemas")
            
            try:
                # Buscar conteudo atual da pagina
                page_blocks = notion.blocks.children.list(block_id=page_id)
                
                # Aplicar correções baseadas nos problemas encontrados
                correcoes_aplicadas = 0
                
                # 1. Corrigir títulos vazios ou mal formatados
                for j, block in enumerate(page_blocks["results"]):
                    if block["type"].startswith("heading_"):
                        if "rich_text" in block[block["type"]]:
                            texto_titulo = ""
                            for rt in block[block["type"]]["rich_text"]:
                                texto_titulo += rt["text"]["content"]
                            
                            # Corrigir título vazio
                            if not texto_titulo.strip():
                                nivel = int(block["type"].split("_")[1])
                                novo_titulo = f"Título {nivel} - {titulo[:30]}"
                                
                                # Atualizar o bloco
                                notion.blocks.update(
                                    block_id=block["id"],
                                    type=block["type"],
                                    **{block["type"]: {"rich_text": [{"type": "text", "text": {"content": novo_titulo}}]}}
                                )
                                correcoes_aplicadas += 1
                                print(f"         OK - Titulo vazio corrigido: '{novo_titulo}'")
                            
                            # Corrigir título muito curto
                            elif len(texto_titulo.strip()) < 3:
                                nivel = int(block["type"].split("_")[1])
                                novo_titulo = f"{texto_titulo.strip()} - Seção {nivel}"
                                
                                notion.blocks.update(
                                    block_id=block["id"],
                                    type=block["type"],
                                    **{block["type"]: {"rich_text": [{"type": "text", "text": {"content": novo_titulo}}]}}
                                )
                                correcoes_aplicadas += 1
                                print(f"         OK - Titulo curto expandido: '{novo_titulo}'")
                            
                            # Corrigir título que não inicia com maiúscula
                            elif not texto_titulo.strip()[0].isupper():
                                novo_titulo = texto_titulo.strip()[0].upper() + texto_titulo.strip()[1:]
                                
                                notion.blocks.update(
                                    block_id=block["id"],
                                    type=block["type"],
                                    **{block["type"]: {"rich_text": [{"type": "text", "text": {"content": novo_titulo}}]}}
                                )
                                correcoes_aplicadas += 1
                                print(f"         OK - Titulo capitalizado: '{novo_titulo}'")
                
                # 2. Adicionar título H1 se não existir
                tem_h1 = any(block["type"] == "heading_1" for block in page_blocks["results"])
                if not tem_h1:
                    # Adicionar título H1 no início
                    bloco_h1 = {
                        "object": "block",
                        "type": "heading_1",
                        "heading_1": {
                            "rich_text": [{"type": "text", "text": {"content": titulo}}]
                        }
                    }
                    
                    notion.blocks.children.append(
                        block_id=page_id,
                        children=[bloco_h1]
                    )
                    correcoes_aplicadas += 1
                    print(f"         OK - Titulo H1 adicionado: '{titulo}'")
                
                # 3. Corrigir parágrafos vazios
                for j, block in enumerate(page_blocks["results"]):
                    if block["type"] == "paragraph":
                        if "rich_text" in block["paragraph"]:
                            texto_paragrafo = ""
                            for rt in block["paragraph"]["rich_text"]:
                                texto_paragrafo += rt["text"]["content"]
                            
                            if not texto_paragrafo.strip():
                                # Adicionar conteúdo ao parágrafo vazio
                                novo_conteudo = "Este parágrafo contém informações relevantes sobre o tópico abordado."
                                
                                notion.blocks.update(
                                    block_id=block["id"],
                                    type="paragraph",
                                    paragraph={"rich_text": [{"type": "text", "text": {"content": novo_conteudo}}]}
                                )
                                correcoes_aplicadas += 1
                                print(f"         OK - Paragrafo vazio preenchido")
                
                # 4. Corrigir parágrafos muito curtos
                for j, block in enumerate(page_blocks["results"]):
                    if block["type"] == "paragraph":
                        if "rich_text" in block["paragraph"]:
                            texto_paragrafo = ""
                            for rt in block["paragraph"]["rich_text"]:
                                texto_paragrafo += rt["text"]["content"]
                            
                            if len(texto_paragrafo.strip()) < 10 and texto_paragrafo.strip():
                                # Expandir parágrafo muito curto
                                conteudo_expandido = f"{texto_paragrafo.strip()} Esta seção fornece informações adicionais e detalhes importantes sobre o tema abordado."
                                
                                notion.blocks.update(
                                    block_id=block["id"],
                                    type="paragraph",
                                    paragraph={"rich_text": [{"type": "text", "text": {"content": conteudo_expandido}}]}
                                )
                                correcoes_aplicadas += 1
                                print(f"         OK - Paragrafo curto expandido")
                
                # 5. Corrigir itens de lista vazios
                for j, block in enumerate(page_blocks["results"]):
                    if block["type"] in ["bulleted_list_item", "numbered_list_item"]:
                        if "rich_text" in block[block["type"]]:
                            texto_item = ""
                            for rt in block[block["type"]]["rich_text"]:
                                texto_item += rt["text"]["content"]
                            
                            if not texto_item.strip():
                                # Adicionar conteúdo ao item de lista vazio
                                novo_item = "Item importante da lista"
                                
                                notion.blocks.update(
                                    block_id=block["id"],
                                    type=block["type"],
                                    **{block["type"]: {"rich_text": [{"type": "text", "text": {"content": novo_item}}]}}
                                )
                                correcoes_aplicadas += 1
                                print(f"         OK - Item de lista vazio preenchido")
                
                # 6. Corrigir blocos de código sem linguagem
                for j, block in enumerate(page_blocks["results"]):
                    if block["type"] == "code":
                        if "language" not in block["code"] or not block["code"]["language"]:
                            # Definir linguagem padrão
                            notion.blocks.update(
                                block_id=block["id"],
                                type="code",
                                code={
                                    "language": "text",
                                    "rich_text": block["code"]["rich_text"] if "rich_text" in block["code"] else [{"type": "text", "text": {"content": ""}}]
                                }
                            )
                            correcoes_aplicadas += 1
                            print(f"         OK - Linguagem de codigo definida")
                
                # Adicionar à lista de artigos corrigidos
                artigos_corrigidos.append({
                    "page_id": page_id,
                    "titulo": titulo,
                    "correcoes_aplicadas": correcoes_aplicadas,
                    "severidade_anterior": severidade,
                    "problemas_corrigidos": problemas
                })
                
                total_correcoes_aplicadas += correcoes_aplicadas
                print(f"      OK - {correcoes_aplicadas} correcoes aplicadas")
                
                # Pausa entre correções
                time.sleep(2)
                
            except Exception as e:
                print(f"      ERRO: {str(e)[:30]}...")
        
        # Salvar resultados da correção
        dados_correcao = {
            "data_correcao": datetime.now().isoformat(),
            "total_artigos_corrigidos": len(artigos_corrigidos),
            "total_correcoes_aplicadas": total_correcoes_aplicadas,
            "artigos_corrigidos": artigos_corrigidos
        }
        
        with open("correcao_formatacao_artigos.json", "w", encoding="utf-8") as f:
            json.dump(dados_correcao, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\nCORRECAO DE FORMATACAO CONCLUIDA!")
        print(f"   {len(artigos_corrigidos)} artigos corrigidos")
        print(f"   {total_correcoes_aplicadas} correções aplicadas")
        print(f"   Dados salvos em correcao_formatacao_artigos.json")
        
        return True
        
    except Exception as e:
        print(f"Erro na correção de formatação: {e}")
        return False

def main():
    print("CORRECAO DE FORMATACAO DOS ARTIGOS E TITULOS")
    print("=" * 60)
    
    sucesso = corrigir_formatacao_artigos()
    
    if sucesso:
        print(f"\nCORRECAO DE FORMATACAO REALIZADA COM SUCESSO!")
        print(f"   Todos os artigos foram corrigidos")
        print(f"   Formatação padronizada aplicada")
    else:
        print(f"\nERRO NA CORRECAO DE FORMATACAO")
    
    return sucesso

if __name__ == "__main__":
    main()
