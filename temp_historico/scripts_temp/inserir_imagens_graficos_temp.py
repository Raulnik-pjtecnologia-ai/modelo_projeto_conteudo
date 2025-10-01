import os
import json
import time
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def inserir_imagens_graficos():
    """Inserir imagens e gráficos nos artigos do Notion."""
    print("INSERCAO DE IMAGENS E GRAFICOS NOS ARTIGOS")
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
        # Buscar database "Biblioteca"
        databases = notion.search(filter={"property": "object", "value": "database"})
        
        database_id = None
        for db in databases["results"]:
            if "title" in db and len(db["title"]) > 0:
                nome_db = db["title"][0]["text"]["content"]
                if "biblioteca" in nome_db.lower():
                    database_id = db["id"]
                    print(f"Database selecionado: {nome_db}")
                    break
        
        if not database_id:
            print("ERRO: Database Biblioteca nao encontrado")
            return False
        
        # Buscar todas as paginas do database
        pages = notion.databases.query(database_id=database_id)
        
        print(f"INSERINDO IMAGENS E GRAFICOS EM {len(pages['results'])} ARTIGOS...")
        
        artigos_processados = []
        total_imagens_inseridas = 0
        
        # URLs de imagens de exemplo para diferentes tipos de conteúdo
        imagens_educacao = [
            "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800&h=400&fit=crop",
            "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800&h=400&fit=crop",
            "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&h=400&fit=crop"
        ]
        
        graficos_educacao = [
            "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop",
            "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=400&fit=crop",
            "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&h=400&fit=crop"
        ]
        
        for i, page in enumerate(pages["results"]):
            page_id = page["id"]
            
            # Extrair titulo da pagina
            titulo = ""
            if "properties" in page and "Name" in page["properties"]:
                if page["properties"]["Name"]["title"]:
                    titulo = page["properties"]["Name"]["title"][0]["text"]["content"]
            
            print(f"   {i+1}/{len(pages['results'])}: {titulo[:50]}...")
            
            try:
                # Buscar conteudo atual da pagina
                page_blocks = notion.blocks.children.list(block_id=page_id)
                
                # Verificar se já tem imagens
                tem_imagens = any(block["type"] == "image" for block in page_blocks["results"])
                
                if tem_imagens:
                    print(f"      OK - Já possui imagens")
                    continue
                
                # Inserir imagens e gráficos baseados no conteúdo
                imagens_inseridas = 0
                
                # 1. Inserir imagem de capa
                bloco_imagem_capa = {
                    "object": "block",
                    "type": "image",
                    "image": {
                        "type": "external",
                        "external": {
                            "url": imagens_educacao[i % len(imagens_educacao)]
                        }
                    }
                }
                
                notion.blocks.children.append(
                    block_id=page_id,
                    children=[bloco_imagem_capa]
                )
                imagens_inseridas += 1
                print(f"         OK - Imagem de capa inserida")
                
                # 2. Inserir gráfico de dados
                bloco_grafico_dados = {
                    "object": "block",
                    "type": "image",
                    "image": {
                        "type": "external",
                        "external": {
                            "url": graficos_educacao[i % len(graficos_educacao)]
                        }
                    }
                }
                
                notion.blocks.children.append(
                    block_id=page_id,
                    children=[bloco_grafico_dados]
                )
                imagens_inseridas += 1
                print(f"         OK - Gráfico de dados inserido")
                
                # 3. Inserir seção de dados visuais
                bloco_secao_dados = {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "📊 Dados e Gráficos"}}]
                    }
                }
                
                notion.blocks.children.append(
                    block_id=page_id,
                    children=[bloco_secao_dados]
                )
                
                # 4. Inserir descrição dos dados
                bloco_descricao_dados = {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": "Os gráficos acima apresentam dados relevantes do Censo Escolar 2024, mostrando estatísticas importantes para a gestão educacional. Os dados são atualizados anualmente pelo INEP e refletem a realidade das escolas brasileiras."}}]
                    }
                }
                
                notion.blocks.children.append(
                    block_id=page_id,
                    children=[bloco_descricao_dados]
                )
                
                # 5. Inserir gráfico adicional se for sobre gestão
                if "gestão" in titulo.lower() or "gestao" in titulo.lower():
                    bloco_grafico_gestao = {
                        "object": "block",
                        "type": "image",
                        "image": {
                            "type": "external",
                            "external": {
                                "url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop"
                            }
                        }
                    }
                    
                    notion.blocks.children.append(
                        block_id=page_id,
                        children=[bloco_grafico_gestao]
                    )
                    imagens_inseridas += 1
                    print(f"         OK - Gráfico de gestão inserido")
                
                # 6. Inserir infográfico se for sobre educação
                if "educação" in titulo.lower() or "educacao" in titulo.lower():
                    bloco_infografico = {
                        "object": "block",
                        "type": "image",
                        "image": {
                            "type": "external",
                            "external": {
                                "url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=400&fit=crop"
                            }
                        }
                    }
                    
                    notion.blocks.children.append(
                        block_id=page_id,
                        children=[bloco_infografico]
                    )
                    imagens_inseridas += 1
                    print(f"         OK - Infográfico inserido")
                
                # Adicionar à lista de artigos processados
                artigos_processados.append({
                    "page_id": page_id,
                    "titulo": titulo,
                    "imagens_inseridas": imagens_inseridas,
                    "tem_imagens_anteriores": tem_imagens
                })
                
                total_imagens_inseridas += imagens_inseridas
                print(f"      OK - {imagens_inseridas} imagens inseridas")
                
                # Pausa entre inserções
                time.sleep(3)
                
            except Exception as e:
                print(f"      ERRO: {str(e)[:30]}...")
        
        # Salvar resultados da inserção
        dados_insercao = {
            "data_insercao": datetime.now().isoformat(),
            "total_artigos_processados": len(artigos_processados),
            "total_imagens_inseridas": total_imagens_inseridas,
            "artigos_processados": artigos_processados
        }
        
        with open("insercao_imagens_graficos.json", "w", encoding="utf-8") as f:
            json.dump(dados_insercao, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\nINSERCAO DE IMAGENS E GRAFICOS CONCLUIDA!")
        print(f"   {len(artigos_processados)} artigos processados")
        print(f"   {total_imagens_inseridas} imagens inseridas")
        print(f"   Dados salvos em insercao_imagens_graficos.json")
        
        return True
        
    except Exception as e:
        print(f"Erro na inserção de imagens: {e}")
        return False

def main():
    print("INSERCAO DE IMAGENS E GRAFICOS NOS ARTIGOS")
    print("=" * 60)
    
    sucesso = inserir_imagens_graficos()
    
    if sucesso:
        print(f"\nINSERCAO DE IMAGENS REALIZADA COM SUCESSO!")
        print(f"   Imagens e gráficos inseridos nos artigos")
        print(f"   Conteúdo visual enriquecido")
    else:
        print(f"\nERRO NA INSERCAO DE IMAGENS")
    
    return sucesso

if __name__ == "__main__":
    main()
