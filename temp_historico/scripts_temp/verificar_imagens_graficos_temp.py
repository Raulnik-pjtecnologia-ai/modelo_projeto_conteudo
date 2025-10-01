import os
import json
import time
import requests
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def verificar_imagens_graficos():
    """Verificar se imagens e gráficos foram inseridos corretamente e se estão visíveis."""
    print("VERIFICACAO DE IMAGENS E GRAFICOS")
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
        database_nome = ""
        
        for db in databases["results"]:
            if "title" in db and len(db["title"]) > 0:
                nome_db = db["title"][0]["text"]["content"]
                if "biblioteca" in nome_db.lower():
                    database_id = db["id"]
                    database_nome = nome_db
                    print(f"Database selecionado: {nome_db}")
                    break
        
        if not database_id:
            print("ERRO: Database Biblioteca nao encontrado")
            return False
        
        # Buscar todas as paginas do database
        pages = notion.databases.query(database_id=database_id)
        
        print(f"VERIFICANDO IMAGENS E GRAFICOS EM {len(pages['results'])} ARTIGOS...")
        
        artigos_analisados = []
        problemas_imagens = []
        imagens_funcionais = 0
        imagens_quebradas = 0
        
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
                
                # Analisar imagens e gráficos
                imagens_encontradas = []
                problemas_encontrados = []
                
                for block in page_blocks["results"]:
                    # Verificar blocos de imagem
                    if block["type"] == "image":
                        if "image" in block and "url" in block["image"]:
                            url_imagem = block["image"]["url"]
                            imagens_encontradas.append({
                                "url": url_imagem,
                                "tipo": "imagem",
                                "bloco_id": block["id"]
                            })
                            
                            # Testar se a imagem está acessível
                            try:
                                response = requests.head(url_imagem, timeout=10)
                                if response.status_code == 200:
                                    imagens_funcionais += 1
                                    print(f"      OK - Imagem acessível: {url_imagem[:50]}...")
                                else:
                                    imagens_quebradas += 1
                                    problemas_encontrados.append(f"Imagem inacessível (HTTP {response.status_code}): {url_imagem[:50]}...")
                                    print(f"      ERRO - Imagem inacessível: {url_imagem[:50]}...")
                            except Exception as e:
                                imagens_quebradas += 1
                                problemas_encontrados.append(f"Erro ao acessar imagem: {str(e)[:50]}...")
                                print(f"      ERRO - Erro ao acessar: {url_imagem[:50]}...")
                        else:
                            problemas_encontrados.append("Bloco de imagem sem URL")
                            print(f"      ERRO - Bloco de imagem sem URL")
                    
                    # Verificar blocos de código que podem conter URLs de imagens
                    elif block["type"] == "code":
                        if "rich_text" in block["code"]:
                            texto_codigo = ""
                            for rt in block["code"]["rich_text"]:
                                texto_codigo += rt["text"]["content"]
                            
                            # Procurar por URLs de imagem no código
                            import re
                            urls_imagem = re.findall(r'https?://[^\s]+\.(?:jpg|jpeg|png|gif|webp|svg)', texto_codigo, re.IGNORECASE)
                            for url in urls_imagem:
                                imagens_encontradas.append({
                                    "url": url,
                                    "tipo": "url_no_codigo",
                                    "bloco_id": block["id"]
                                })
                                
                                # Testar se a URL está acessível
                                try:
                                    response = requests.head(url, timeout=10)
                                    if response.status_code == 200:
                                        imagens_funcionais += 1
                                        print(f"      OK - URL de imagem no código acessível: {url[:50]}...")
                                    else:
                                        imagens_quebradas += 1
                                        problemas_encontrados.append(f"URL de imagem no código inacessível (HTTP {response.status_code}): {url[:50]}...")
                                        print(f"      ERRO - URL no código inacessível: {url[:50]}...")
                                except Exception as e:
                                    imagens_quebradas += 1
                                    problemas_encontrados.append(f"Erro ao acessar URL no código: {str(e)[:50]}...")
                                    print(f"      ERRO - Erro ao acessar URL no código: {url[:50]}...")
                    
                    # Verificar parágrafos que podem conter URLs de imagens
                    elif block["type"] == "paragraph":
                        if "rich_text" in block["paragraph"]:
                            texto_paragrafo = ""
                            for rt in block["paragraph"]["rich_text"]:
                                texto_paragrafo += rt["text"]["content"]
                            
                            # Procurar por URLs de imagem no parágrafo
                            import re
                            urls_imagem = re.findall(r'https?://[^\s]+\.(?:jpg|jpeg|png|gif|webp|svg)', texto_paragrafo, re.IGNORECASE)
                            for url in urls_imagem:
                                imagens_encontradas.append({
                                    "url": url,
                                    "tipo": "url_no_paragrafo",
                                    "bloco_id": block["id"]
                                })
                                
                                # Testar se a URL está acessível
                                try:
                                    response = requests.head(url, timeout=10)
                                    if response.status_code == 200:
                                        imagens_funcionais += 1
                                        print(f"      OK - URL de imagem no parágrafo acessível: {url[:50]}...")
                                    else:
                                        imagens_quebradas += 1
                                        problemas_encontrados.append(f"URL de imagem no parágrafo inacessível (HTTP {response.status_code}): {url[:50]}...")
                                        print(f"      ERRO - URL no parágrafo inacessível: {url[:50]}...")
                                except Exception as e:
                                    imagens_quebradas += 1
                                    problemas_encontrados.append(f"Erro ao acessar URL no parágrafo: {str(e)[:50]}...")
                                    print(f"      ERRO - Erro ao acessar URL no parágrafo: {url[:50]}...")
                
                # Verificar se há referências a gráficos ou imagens no texto
                texto_completo = ""
                for block in page_blocks["results"]:
                    if block["type"] == "paragraph" and "rich_text" in block["paragraph"]:
                        for rt in block["paragraph"]["rich_text"]:
                            texto_completo += rt["text"]["content"].lower()
                
                # Procurar por referências a gráficos
                referencias_graficos = []
                if "gráfico" in texto_completo or "grafico" in texto_completo:
                    referencias_graficos.append("Referência a gráfico encontrada no texto")
                if "imagem" in texto_completo:
                    referencias_graficos.append("Referência a imagem encontrada no texto")
                if "chart" in texto_completo:
                    referencias_graficos.append("Referência a chart encontrada no texto")
                
                # Se há referências mas não há imagens, é um problema
                if referencias_graficos and not imagens_encontradas:
                    problemas_encontrados.append(f"Referências a gráficos/imagens encontradas mas nenhuma imagem inserida: {', '.join(referencias_graficos)}")
                
                # Adicionar à lista de artigos analisados
                artigos_analisados.append({
                    "page_id": page_id,
                    "titulo": titulo,
                    "imagens_encontradas": imagens_encontradas,
                    "total_imagens": len(imagens_encontradas),
                    "problemas_encontrados": problemas_encontrados,
                    "referencias_graficos": referencias_graficos
                })
                
                if problemas_encontrados:
                    problemas_imagens.append({
                        "page_id": page_id,
                        "titulo": titulo,
                        "problemas": problemas_encontrados,
                        "imagens_encontradas": imagens_encontradas
                    })
                    print(f"      PROBLEMAS: {len(problemas_encontrados)}")
                else:
                    print(f"      OK - {len(imagens_encontradas)} imagens funcionais")
                
                # Pausa entre verificações
                time.sleep(1)
                
            except Exception as e:
                print(f"      ERRO: {str(e)[:30]}...")
        
        # Calcular estatísticas
        total_artigos = len(artigos_analisados)
        artigos_com_imagens = len([a for a in artigos_analisados if a["total_imagens"] > 0])
        artigos_sem_imagens = total_artigos - artigos_com_imagens
        artigos_com_problemas = len(problemas_imagens)
        
        print(f"\nRESULTADOS DA VERIFICACAO DE IMAGENS E GRAFICOS:")
        print(f"   Database analisado: {database_nome}")
        print(f"   Total de artigos analisados: {total_artigos}")
        print(f"   Artigos com imagens: {artigos_com_imagens}")
        print(f"   Artigos sem imagens: {artigos_sem_imagens}")
        print(f"   Artigos com problemas: {artigos_com_problemas}")
        print(f"   Imagens funcionais: {imagens_funcionais}")
        print(f"   Imagens quebradas: {imagens_quebradas}")
        
        # Salvar resultados da verificação
        dados_verificacao = {
            "data_verificacao": datetime.now().isoformat(),
            "database_analisado": database_nome,
            "total_artigos_analisados": total_artigos,
            "artigos_com_imagens": artigos_com_imagens,
            "artigos_sem_imagens": artigos_sem_imagens,
            "artigos_com_problemas": artigos_com_problemas,
            "imagens_funcionais": imagens_funcionais,
            "imagens_quebradas": imagens_quebradas,
            "artigos_analisados": artigos_analisados,
            "problemas_imagens": problemas_imagens
        }
        
        with open("verificacao_imagens_graficos.json", "w", encoding="utf-8") as f:
            json.dump(dados_verificacao, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\nVERIFICACAO DE IMAGENS E GRAFICOS CONCLUIDA!")
        print(f"   {artigos_com_imagens}/{total_artigos} artigos com imagens")
        print(f"   {imagens_funcionais} imagens funcionais, {imagens_quebradas} quebradas")
        print(f"   Dados salvos em verificacao_imagens_graficos.json")
        
        return artigos_com_problemas > 0
        
    except Exception as e:
        print(f"Erro na verificação de imagens: {e}")
        return False

def main():
    print("VERIFICACAO DE IMAGENS E GRAFICOS")
    print("=" * 60)
    
    tem_problemas = verificar_imagens_graficos()
    
    if tem_problemas:
        print(f"\nVERIFICACAO CONCLUIDA - PROBLEMAS ENCONTRADOS!")
        print(f"   Necessário corrigir problemas de imagens")
        print(f"   Verificar arquivo verificacao_imagens_graficos.json")
    else:
        print(f"\nVERIFICACAO CONCLUIDA - IMAGENS OK!")
        print(f"   Todas as imagens estão funcionando corretamente")
    
    return tem_problemas

if __name__ == "__main__":
    main()
