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

def get_notion_pages(database_id):
    """Busca todas as páginas de um database do Notion."""
    results = []
    has_more = True
    next_cursor = None

    while has_more:
        query = notion.databases.query(
            database_id=database_id,
            start_cursor=next_cursor
        )
        results.extend(query["results"])
        has_more = query["has_more"]
        next_cursor = query["next_cursor"]
    return results

def verificar_pagina_restaurada(page):
    """Verifica se uma página foi restaurada corretamente."""
    try:
        # Informações básicas
        title_obj = page["properties"].get("Name", {}).get("title", [])
        title = title_obj[0]["plain_text"] if title_obj else "Sem Título"
        
        tipo = page["properties"].get("Tipo", {}).get("select", {}).get("name", "")
        
        # Verificar tags
        tags_obj = page["properties"].get("Tags", {}).get("multi_select", [])
        tag_names = [tag["name"] for tag in tags_obj]
        
        # Verificar status
        status = page["properties"].get("Status editorial", {}).get("status", {}).get("name", "")
        
        # Verificar se ainda contém modificações minhas
        contem_modificacoes_minhas = False
        conteudo_texto = ""
        
        try:
            conteudo_blocos = notion.blocks.children.list(block_id=page["id"])
            for block in conteudo_blocos["results"]:
                if block.get("type") == "paragraph" and block.get("paragraph", {}).get("rich_text"):
                    for text in block["paragraph"]["rich_text"]:
                        conteudo_texto += text.get("text", {}).get("content", "")
            
            # Verificar se ainda contém dados do Censo Escolar 2024
            if any(marker in conteudo_texto for marker in [
                "Censo Escolar 2024", 
                "179.286 escolas", 
                "47,1 milhões de matrículas",
                "163.987 diretores",
                "80,6% dos diretores",
                "Dados Reais",
                "INEP/Censo Escolar",
                "📊 Dados Reais do Censo Escolar 2024"
            ]):
                contem_modificacoes_minhas = True
                
        except Exception as e:
            print(f"Erro ao verificar conteúdo da página {page['id']}: {e}")
        
        # Verificar se ainda tem tags minhas
        tem_tags_minhas = any(tag in tag_names for tag in [
            "Dados Reais", 
            "Censo Escolar 2024", 
            "Boilerplate"
        ])
        
        return {
            "titulo": title,
            "tipo": tipo,
            "id": page["id"],
            "tags": tag_names,
            "status": status,
            "contem_modificacoes_minhas": contem_modificacoes_minhas,
            "tem_tags_minhas": tem_tags_minhas,
            "tamanho_conteudo": len(conteudo_texto),
            "foi_restaurada": not contem_modificacoes_minhas and not tem_tags_minhas and status == "Rascunho"
        }
        
    except Exception as e:
        print(f"Erro ao verificar página: {e}")
        return None

def main():
    print("🔍 VERIFICANDO RESULTADO DA RESTAURAÇÃO NO NOTION")
    print("======================================================================")
    
    notion = Client(auth=NOTION_TOKEN)
    print("✅ Conexão com Notion estabelecida!")
    
    pages = get_notion_pages(DATABASE_ID)
    print(f"📊 Total de páginas encontradas: {len(pages)}\n")

    # Verificar todas as páginas
    verificacoes = []
    paginas_restauradas = []
    paginas_nao_restauradas = []
    
    print("🔍 VERIFICANDO TODAS AS PÁGINAS...")
    print("======================================================================\n")
    
    for i, page in enumerate(pages):
        verificacao = verificar_pagina_restaurada(page)
        if verificacao:
            verificacoes.append(verificacao)
            
            if verificacao["foi_restaurada"]:
                paginas_restauradas.append(verificacao)
            else:
                paginas_nao_restauradas.append(verificacao)
        
        if (i + 1) % 50 == 0:
            print(f"✅ Verificadas {i + 1}/{len(pages)} páginas...")
    
    print(f"\n📊 RESULTADO DA VERIFICAÇÃO:")
    print("======================================================================")
    
    total_paginas = len(verificacoes)
    restauradas = len(paginas_restauradas)
    nao_restauradas = len(paginas_nao_restauradas)
    
    print(f"📋 Total de páginas verificadas: {total_paginas}")
    print(f"✅ Páginas restauradas corretamente: {restauradas}")
    print(f"❌ Páginas NÃO restauradas: {nao_restauradas}")
    print(f"📊 Taxa de sucesso: {(restauradas/total_paginas)*100:.1f}%")
    
    if nao_restauradas > 0:
        print(f"\n❌ PÁGINAS QUE NÃO FORAM RESTAURADAS CORRETAMENTE:")
        print("======================================================================")
        for item in paginas_nao_restauradas:
            print(f"• {item['tipo']}: {item['titulo'][:60]}...")
            print(f"  - Status: {item['status']}")
            print(f"  - Tags: {item['tags']}")
            print(f"  - Tem modificações minhas: {'✅' if item['contem_modificacoes_minhas'] else '❌'}")
            print(f"  - Tem tags minhas: {'✅' if item['tem_tags_minhas'] else '❌'}")
            print()
    else:
        print("\n🎉 TODAS AS PÁGINAS FORAM RESTAURADAS COM SUCESSO!")
        print("   ✅ Nenhuma página contém modificações minhas")
        print("   ✅ Nenhuma página tem tags minhas")
        print("   ✅ Todas as páginas estão com status 'Rascunho'")
    
    # Salvar relatório detalhado
    relatorio = {
        "data_verificacao": datetime.now().isoformat(),
        "total_paginas": total_paginas,
        "paginas_restauradas": restauradas,
        "paginas_nao_restauradas": nao_restauradas,
        "taxa_sucesso": (restauradas/total_paginas)*100,
        "paginas_nao_restauradas_detalhes": paginas_nao_restauradas
    }
    
    with open("relatorio_verificacao_restauracao.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n💾 Relatório detalhado salvo em: relatorio_verificacao_restauracao.json")

    print("\n🎉 Verificação concluída!")

if __name__ == "__main__":
    main()
