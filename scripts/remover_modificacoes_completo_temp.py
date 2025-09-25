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

def limpar_toda_pagina(page_id):
    """Remove TODOS os blocos de uma página (conteúdo completo)."""
    try:
        # Buscar todos os blocos da página
        blocks = notion.blocks.children.list(block_id=page_id)
        
        # Lista de IDs dos blocos para deletar
        blocks_to_delete = []
        
        for block in blocks["results"]:
            # Deletar TODOS os blocos de conteúdo (não apenas os modificados)
            if block.get("type") in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item", "to_do", "toggle", "quote", "callout", "divider", "table", "code", "embed", "image", "video", "file", "pdf", "bookmark", "equation", "table_of_contents", "synced_block", "template", "link_to_page", "child_page", "child_database", "audio", "unsupported"]:
                blocks_to_delete.append(block["id"])
        
        # Deletar todos os blocos
        for block_id in blocks_to_delete:
            try:
                notion.blocks.delete(block_id=block_id)
                time.sleep(0.1)  # Evitar rate limit
            except Exception as e:
                print(f"   ❌ Erro ao deletar bloco {block_id}: {e}")
        
        return len(blocks_to_delete)
        
    except Exception as e:
        print(f"   ❌ Erro ao limpar página: {e}")
        return 0

def restaurar_propriedades_originais(page_id):
    """Restaura as propriedades da página para o estado original."""
    try:
        # Limpar todas as tags e voltar status para rascunho
        properties = {
            "Tags": {
                "multi_select": []  # Limpar todas as tags
            },
            "Status editorial": {
                "status": {
                    "name": "Rascunho"  # Voltar para rascunho
                }
            }
        }
        
        notion.pages.update(
            page_id=page_id,
            properties=properties
        )
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao restaurar propriedades: {e}")
        return False

def main():
    print("🗑️ REMOVENDO TODAS AS MODIFICAÇÕES DO NOTION")
    print("======================================================================")
    print("⚠️  ATENÇÃO: Este processo irá REMOVER TODO O CONTEÚDO das páginas!")
    print("======================================================================")
    
    notion = Client(auth=NOTION_TOKEN)
    print("✅ Conexão com Notion estabelecida!")
    
    pages = get_notion_pages(DATABASE_ID)
    print(f"📊 Total de páginas encontradas: {len(pages)}\n")

    # Confirmar ação
    print(f"⚠️  Você está prestes a LIMPAR COMPLETAMENTE {len(pages)} páginas!")
    print("Isso irá:")
    print("   - REMOVER TODO O CONTEÚDO de todas as páginas")
    print("   - Limpar todas as tags")
    print("   - Alterar status para 'Rascunho'")
    print("\nContinuar? (digite 'SIM' para confirmar)")
    
    confirmacao = input("> ")
    if confirmacao.upper() != "SIM":
        print("❌ Operação cancelada pelo usuário.")
        return
    
    # Processar páginas
    sucessos = 0
    erros = 0
    
    print(f"\n🗑️ INICIANDO LIMPEZA COMPLETA DE {len(pages)} PÁGINAS...")
    print("======================================================================")
    
    for i, page in enumerate(pages):
        title_obj = page["properties"].get("Name", {}).get("title", [])
        title = title_obj[0]["plain_text"] if title_obj else "Sem Título"
        
        print(f"\n{i+1}/{len(pages)} - {title[:60]}...")
        
        try:
            # Limpar todo o conteúdo da página
            blocos_removidos = limpar_toda_pagina(page["id"])
            print(f"   📝 Blocos removidos: {blocos_removidos}")
            
            # Restaurar propriedades
            if restaurar_propriedades_originais(page["id"]):
                sucessos += 1
                print(f"   ✅ Página limpa com sucesso!")
            else:
                erros += 1
                print(f"   ❌ Erro ao limpar página!")
            
            # Pausa entre páginas para evitar rate limit
            time.sleep(0.5)
            
        except Exception as e:
            erros += 1
            print(f"   ❌ Erro geral: {e}")
    
    print(f"\n🎉 LIMPEZA COMPLETA CONCLUÍDA!")
    print("======================================================================")
    print(f"✅ Páginas limpas com sucesso: {sucessos}")
    print(f"❌ Páginas com erro: {erros}")
    print(f"📊 Total processadas: {len(pages)}")
    
    if erros == 0:
        print("\n🎉 Todas as páginas foram limpas com sucesso!")
        print("   Os conteúdos agora estão completamente vazios, sem as modificações.")
    else:
        print(f"\n⚠️  {erros} páginas tiveram problemas durante a limpeza.")
        print("   Verifique os erros acima e execute novamente se necessário.")

if __name__ == "__main__":
    main()
