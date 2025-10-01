import os
import json
import time
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def corrigir_imagens_sem_url():
    """Corrigir blocos de imagem sem URL no Notion."""
    print("CORRECAO DE IMAGENS SEM URL")
    print("=" * 50)
    
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
        
        print(f"CORRIGINDO IMAGENS EM {len(pages['results'])} ARTIGOS...")
        
        artigos_corrigidos = []
        total_imagens_corrigidas = 0
        
        # URLs de imagens funcionais
        imagens_funcionais = [
            "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800&h=400&fit=crop",
            "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800&h=400&fit=crop",
            "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&h=400&fit=crop",
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
                # Buscar conteudo da pagina
                page_blocks = notion.blocks.children.list(block_id=page_id)
                
                # Procurar por blocos de imagem sem URL
                blocos_imagem_sem_url = []
                for block in page_blocks["results"]:
                    if block["type"] == "image":
                        if "image" not in block or "url" not in block["image"]:
                            blocos_imagem_sem_url.append(block["id"])
                
                if not blocos_imagem_sem_url:
                    print(f"      OK - Nenhuma imagem sem URL encontrada")
                    continue
                
                # Corrigir cada bloco de imagem sem URL
                imagens_corrigidas = 0
                for j, block_id in enumerate(blocos_imagem_sem_url):
                    try:
                        # Atualizar o bloco de imagem com URL válida
                        url_imagem = imagens_funcionais[(i + j) % len(imagens_funcionais)]
                        
                        notion.blocks.update(
                            block_id=block_id,
                            type="image",
                            image={
                                "type": "external",
                                "external": {
                                    "url": url_imagem
                                }
                            }
                        )
                        
                        imagens_corrigidas += 1
                        print(f"         OK - Imagem {j+1} corrigida: {url_imagem[:50]}...")
                        
                        # Pausa entre correções
                        time.sleep(1)
                        
                    except Exception as e:
                        print(f"         ERRO - Falha ao corrigir imagem {j+1}: {str(e)[:30]}...")
                
                # Adicionar à lista de artigos corrigidos
                artigos_corrigidos.append({
                    "page_id": page_id,
                    "titulo": titulo,
                    "imagens_corrigidas": imagens_corrigidas,
                    "total_blocos_sem_url": len(blocos_imagem_sem_url)
                })
                
                total_imagens_corrigidas += imagens_corrigidas
                print(f"      OK - {imagens_corrigidas} imagens corrigidas")
                
                # Pausa entre artigos
                time.sleep(2)
                
            except Exception as e:
                print(f"      ERRO: {str(e)[:30]}...")
        
        # Salvar resultados da correção
        dados_correcao = {
            "data_correcao": datetime.now().isoformat(),
            "total_artigos_corrigidos": len(artigos_corrigidos),
            "total_imagens_corrigidas": total_imagens_corrigidas,
            "artigos_corrigidos": artigos_corrigidos
        }
        
        with open("correcao_imagens_sem_url.json", "w", encoding="utf-8") as f:
            json.dump(dados_correcao, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\nCORRECAO DE IMAGENS SEM URL CONCLUIDA!")
        print(f"   {len(artigos_corrigidos)} artigos corrigidos")
        print(f"   {total_imagens_corrigidas} imagens corrigidas")
        print(f"   Dados salvos em correcao_imagens_sem_url.json")
        
        return True
        
    except Exception as e:
        print(f"Erro na correção de imagens: {e}")
        return False

def main():
    print("CORRECAO DE IMAGENS SEM URL")
    print("=" * 50)
    
    sucesso = corrigir_imagens_sem_url()
    
    if sucesso:
        print(f"\nCORRECAO DE IMAGENS REALIZADA COM SUCESSO!")
        print(f"   Imagens sem URL foram corrigidas")
        print(f"   URLs válidas foram aplicadas")
    else:
        print(f"\nERRO NA CORRECAO DE IMAGENS")
    
    return sucesso

if __name__ == "__main__":
    main()
