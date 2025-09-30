import os
import json
import time
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def analisar_conteudo_imagens():
    """Analisar conteúdo dos artigos para encontrar referências a imagens e gráficos."""
    print("ANALISE DE CONTEUDO - REFERENCIAS A IMAGENS E GRAFICOS")
    print("=" * 70)
    
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
        
        print(f"ANALISANDO CONTEUDO DE {len(pages['results'])} ARTIGOS...")
        
        artigos_analisados = []
        referencias_encontradas = []
        
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
                
                # Analisar todo o conteúdo
                texto_completo = ""
                blocos_analisados = []
                
                for block in page_blocks["results"]:
                    bloco_info = {
                        "tipo": block["type"],
                        "conteudo": "",
                        "urls": [],
                        "referencias_imagem": []
                    }
                    
                    if block["type"] == "paragraph" and "rich_text" in block["paragraph"]:
                        for rt in block["paragraph"]["rich_text"]:
                            conteudo = rt["text"]["content"]
                            texto_completo += conteudo + " "
                            bloco_info["conteudo"] += conteudo
                    
                    elif block["type"] == "heading_1" and "rich_text" in block["heading_1"]:
                        for rt in block["heading_1"]["rich_text"]:
                            conteudo = rt["text"]["content"]
                            texto_completo += conteudo + " "
                            bloco_info["conteudo"] += conteudo
                    
                    elif block["type"] == "heading_2" and "rich_text" in block["heading_2"]:
                        for rt in block["heading_2"]["rich_text"]:
                            conteudo = rt["text"]["content"]
                            texto_completo += conteudo + " "
                            bloco_info["conteudo"] += conteudo
                    
                    elif block["type"] == "heading_3" and "rich_text" in block["heading_3"]:
                        for rt in block["heading_3"]["rich_text"]:
                            conteudo = rt["text"]["content"]
                            texto_completo += conteudo + " "
                            bloco_info["conteudo"] += conteudo
                    
                    elif block["type"] == "code" and "rich_text" in block["code"]:
                        for rt in block["code"]["rich_text"]:
                            conteudo = rt["text"]["content"]
                            texto_completo += conteudo + " "
                            bloco_info["conteudo"] += conteudo
                    
                    elif block["type"] == "bulleted_list_item" and "rich_text" in block["bulleted_list_item"]:
                        for rt in block["bulleted_list_item"]["rich_text"]:
                            conteudo = rt["text"]["content"]
                            texto_completo += conteudo + " "
                            bloco_info["conteudo"] += conteudo
                    
                    elif block["type"] == "numbered_list_item" and "rich_text" in block["numbered_list_item"]:
                        for rt in block["numbered_list_item"]["rich_text"]:
                            conteudo = rt["text"]["content"]
                            texto_completo += conteudo + " "
                            bloco_info["conteudo"] += conteudo
                    
                    # Procurar por URLs de imagem no conteúdo
                    import re
                    urls_imagem = re.findall(r'https?://[^\s]+\.(?:jpg|jpeg|png|gif|webp|svg)', bloco_info["conteudo"], re.IGNORECASE)
                    bloco_info["urls"] = urls_imagem
                    
                    # Procurar por referências a imagens/gráficos
                    referencias = []
                    conteudo_lower = bloco_info["conteudo"].lower()
                    
                    if "gráfico" in conteudo_lower or "grafico" in conteudo_lower:
                        referencias.append("Referência a gráfico")
                    if "imagem" in conteudo_lower:
                        referencias.append("Referência a imagem")
                    if "chart" in conteudo_lower:
                        referencias.append("Referência a chart")
                    if "figura" in conteudo_lower:
                        referencias.append("Referência a figura")
                    if "visual" in conteudo_lower:
                        referencias.append("Referência a visual")
                    if "dados" in conteudo_lower and ("gráfico" in conteudo_lower or "chart" in conteudo_lower):
                        referencias.append("Referência a dados gráficos")
                    if "estatística" in conteudo_lower or "estatistica" in conteudo_lower:
                        referencias.append("Referência a estatística")
                    if "censo" in conteudo_lower and ("dados" in conteudo_lower or "gráfico" in conteudo_lower):
                        referencias.append("Referência a dados do Censo")
                    
                    bloco_info["referencias_imagem"] = referencias
                    blocos_analisados.append(bloco_info)
                
                # Analisar referências no texto completo
                texto_lower = texto_completo.lower()
                referencias_gerais = []
                
                if "gráfico" in texto_lower or "grafico" in texto_lower:
                    referencias_gerais.append("Gráfico")
                if "imagem" in texto_lower:
                    referencias_gerais.append("Imagem")
                if "chart" in texto_lower:
                    referencias_gerais.append("Chart")
                if "figura" in texto_lower:
                    referencias_gerais.append("Figura")
                if "visual" in texto_lower:
                    referencias_gerais.append("Visual")
                if "dados" in texto_lower and ("gráfico" in texto_lower or "chart" in texto_lower):
                    referencias_gerais.append("Dados gráficos")
                if "estatística" in texto_lower or "estatistica" in texto_lower:
                    referencias_gerais.append("Estatística")
                if "censo" in texto_lower and ("dados" in texto_lower or "gráfico" in texto_lower):
                    referencias_gerais.append("Dados do Censo")
                
                # Procurar por URLs de imagem no texto completo
                urls_imagem_gerais = re.findall(r'https?://[^\s]+\.(?:jpg|jpeg|png|gif|webp|svg)', texto_completo, re.IGNORECASE)
                
                # Adicionar à lista de artigos analisados
                artigos_analisados.append({
                    "page_id": page_id,
                    "titulo": titulo,
                    "referencias_gerais": referencias_gerais,
                    "urls_imagem": urls_imagem_gerais,
                    "total_referencias": len(referencias_gerais),
                    "total_urls": len(urls_imagem_gerais),
                    "blocos_analisados": blocos_analisados
                })
                
                if referencias_gerais or urls_imagem_gerais:
                    referencias_encontradas.append({
                        "page_id": page_id,
                        "titulo": titulo,
                        "referencias": referencias_gerais,
                        "urls": urls_imagem_gerais
                    })
                    print(f"      REFERENCIAS: {len(referencias_gerais)} tipos, {len(urls_imagem_gerais)} URLs")
                else:
                    print(f"      NENHUMA REFERENCIA ENCONTRADA")
                
                # Pausa entre análises
                time.sleep(1)
                
            except Exception as e:
                print(f"      ERRO: {str(e)[:30]}...")
        
        # Calcular estatísticas
        total_artigos = len(artigos_analisados)
        artigos_com_referencias = len(referencias_encontradas)
        artigos_sem_referencias = total_artigos - artigos_com_referencias
        
        # Contar tipos de referências
        tipos_referencias = {}
        for artigo in artigos_analisados:
            for ref in artigo["referencias_gerais"]:
                tipos_referencias[ref] = tipos_referencias.get(ref, 0) + 1
        
        print(f"\nRESULTADOS DA ANALISE DE CONTEUDO:")
        print(f"   Total de artigos analisados: {total_artigos}")
        print(f"   Artigos com referências: {artigos_com_referencias}")
        print(f"   Artigos sem referências: {artigos_sem_referencias}")
        print(f"   Tipos de referências encontradas:")
        for tipo, count in tipos_referencias.items():
            print(f"     - {tipo}: {count} artigos")
        
        # Salvar resultados da análise
        dados_analise = {
            "data_analise": datetime.now().isoformat(),
            "total_artigos_analisados": total_artigos,
            "artigos_com_referencias": artigos_com_referencias,
            "artigos_sem_referencias": artigos_sem_referencias,
            "tipos_referencias": tipos_referencias,
            "artigos_analisados": artigos_analisados,
            "referencias_encontradas": referencias_encontradas
        }
        
        with open("analise_conteudo_imagens.json", "w", encoding="utf-8") as f:
            json.dump(dados_analise, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\nANALISE DE CONTEUDO CONCLUIDA!")
        print(f"   {artigos_com_referencias}/{total_artigos} artigos com referências")
        print(f"   Dados salvos em analise_conteudo_imagens.json")
        
        return artigos_com_referencias > 0
        
    except Exception as e:
        print(f"Erro na análise de conteúdo: {e}")
        return False

def main():
    print("ANALISE DE CONTEUDO - REFERENCIAS A IMAGENS E GRAFICOS")
    print("=" * 70)
    
    tem_referencias = analisar_conteudo_imagens()
    
    if tem_referencias:
        print(f"\nANALISE CONCLUIDA - REFERENCIAS ENCONTRADAS!")
        print(f"   Artigos fazem referência a imagens/gráficos")
        print(f"   Verificar se as imagens foram inseridas corretamente")
    else:
        print(f"\nANALISE CONCLUIDA - NENHUMA REFERENCIA!")
        print(f"   Artigos não fazem referência a imagens/gráficos")
        print(f"   Considerar adicionar elementos visuais")
    
    return tem_referencias

if __name__ == "__main__":
    main()
