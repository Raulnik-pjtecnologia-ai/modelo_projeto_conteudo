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

def analisar_pagina_basica(page):
    """Analisa informações básicas de uma página."""
    try:
        # Informações básicas
        title_obj = page["properties"].get("Name", {}).get("title", [])
        title = title_obj[0]["plain_text"] if title_obj else "Sem Título"
        
        tipo = page["properties"].get("Tipo", {}).get("select", {}).get("name", "")
        
        # Tags
        tags_obj = page["properties"].get("Tags", {}).get("multi_select", [])
        tag_names = [tag["name"] for tag in tags_obj]
        
        # Status
        status = page["properties"].get("Status editorial", {}).get("status", {}).get("name", "")
        
        # Categoria (relação)
        categoria_obj = page["properties"].get("Categoria", {}).get("relation", [])
        categoria_ids = [cat["id"] for cat in categoria_obj]
        
        # Datas
        created_time = page.get("created_time")
        last_edited_time = page.get("last_edited_time")
        
        created_datetime = None
        last_edited_datetime = None
        
        if created_time:
            created_datetime = datetime.fromisoformat(created_time.replace('Z', '+00:00'))
        
        if last_edited_time:
            last_edited_datetime = datetime.fromisoformat(last_edited_time.replace('Z', '+00:00'))
        
        # Verificar se é conteúdo de gestão (ignorar AULAS e MÓDULOS)
        is_gestao = True
        if any(keyword in title.upper() for keyword in ["AULA", "MÓDULO", "MODULO"]):
            is_gestao = False
        
        return {
            "titulo": title,
            "tipo": tipo,
            "id": page["id"],
            "tags": tag_names,
            "status": status,
            "categoria_ids": categoria_ids,
            "created_datetime": created_datetime,
            "last_edited_datetime": last_edited_datetime,
            "is_gestao": is_gestao
        }
        
    except Exception as e:
        print(f"Erro ao analisar página: {e}")
        return None

def main():
    print("🔍 BLOCO 1: ANÁLISE BÁSICA DE TODAS AS PÁGINAS DO NOTION")
    print("======================================================================")
    print("📋 Aplicando Regra 1: Enriquecimento MCP")
    print("📋 Aplicando Regra 2: Boilerplate Gestão")
    print("======================================================================")
    
    notion = Client(auth=NOTION_TOKEN)
    print("✅ Conexão com Notion estabelecida!")
    
    pages = get_notion_pages(DATABASE_ID)
    print(f"📊 Total de páginas encontradas: {len(pages)}\n")

    # Analisar todas as páginas
    todas_analises = []
    conteudos_gestao = []
    conteudos_nao_gestao = []
    
    print("🔍 ANALISANDO TODAS AS PÁGINAS...")
    print("======================================================================\n")
    
    for i, page in enumerate(pages):
        analise = analisar_pagina_basica(page)
        if analise:
            todas_analises.append(analise)
            
            if analise["is_gestao"]:
                conteudos_gestao.append(analise)
            else:
                conteudos_nao_gestao.append(analise)
        
        if (i + 1) % 50 == 0:
            print(f"✅ Analisadas {i + 1}/{len(pages)} páginas...")
    
    print(f"\n📊 RESUMO DO BLOCO 1:")
    print("======================================================================")
    
    total_paginas = len(todas_analises)
    total_gestao = len(conteudos_gestao)
    total_nao_gestao = len(conteudos_nao_gestao)
    
    print(f"📋 Total de páginas analisadas: {total_paginas}")
    print(f"🎯 Conteúdos de GESTÃO: {total_gestao}")
    print(f"📚 Conteúdos NÃO-GESTÃO (AULAS/MÓDULOS): {total_nao_gestao}")
    
    # Estatísticas por tipo
    tipos_gestao = {}
    for item in conteudos_gestao:
        tipo = item["tipo"]
        tipos_gestao[tipo] = tipos_gestao.get(tipo, 0) + 1
    
    print(f"\n📊 DISTRIBUIÇÃO POR TIPO (GESTÃO):")
    for tipo, count in sorted(tipos_gestao.items()):
        print(f"   • {tipo}: {count}")
    
    # Estatísticas por status
    status_gestao = {}
    for item in conteudos_gestao:
        status = item["status"]
        status_gestao[status] = status_gestao.get(status, 0) + 1
    
    print(f"\n📊 DISTRIBUIÇÃO POR STATUS (GESTÃO):")
    for status, count in sorted(status_gestao.items()):
        print(f"   • {status}: {count}")
    
    # Salvar dados para próximos blocos
    dados_bloco1 = {
        "data_analise": datetime.now().isoformat(),
        "total_paginas": total_paginas,
        "conteudos_gestao": conteudos_gestao,
        "conteudos_nao_gestao": conteudos_nao_gestao,
        "tipos_gestao": tipos_gestao,
        "status_gestao": status_gestao
    }
    
    with open("dados_bloco1_analise_notion.json", "w", encoding="utf-8") as f:
        json.dump(dados_bloco1, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Dados do Bloco 1 salvos em: dados_bloco1_analise_notion.json")
    print(f"🎯 Foco: {total_gestao} conteúdos de GESTÃO serão analisados nos próximos blocos")
    
    print("\n✅ BLOCO 1 CONCLUÍDO!")
    print("   Próximo: Bloco 2 - Verificar categorização")

if __name__ == "__main__":
    main()
