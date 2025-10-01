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

def remover_apenas_modificacoes_minhas(page_id):
    """Remove apenas os blocos que contêm modificações minhas, preservando o conteúdo original."""
    try:
        # Buscar todos os blocos da página
        blocks = notion.blocks.children.list(block_id=page_id)
        
        # Lista de IDs dos blocos para deletar (apenas os modificados por mim)
        blocks_to_delete = []
        
        for block in blocks["results"]:
            # Verificar se o bloco contém modificações minhas
            if block.get("type") == "paragraph" and block.get("paragraph", {}).get("rich_text"):
                content = ""
                for text in block["paragraph"]["rich_text"]:
                    content += text.get("text", {}).get("content", "")
                
                # Se contém dados do Censo Escolar 2024 ou outras modificações minhas, marcar para deletar
                if any(marker in content for marker in [
                    "Censo Escolar 2024", 
                    "179.286 escolas", 
                    "47,1 milhões de matrículas",
                    "163.987 diretores",
                    "80,6% dos diretores",
                    "91,4% dos diretores",
                    "22,6% dos diretores",
                    "Dados Reais",
                    "INEP/Censo Escolar",
                    "📊 Dados Reais do Censo Escolar 2024",
                    "Fonte: INEP/Censo Escolar 2024",
                    "**Total de Escolas**:",
                    "**Total de Matrículas**:",
                    "**Total de Diretores**:",
                    "**Perfil dos Diretores**:",
                    "**Formação em Gestão**:",
                    "**Desafios Comuns na Gestão Escolar**",
                    "**Capacitação**:",
                    "**Recursos**:",
                    "**Qualidade**:",
                    "Gráfico 1: Distribuição de Escolas",
                    "Tabela de Dados: Indicadores de Gestão Escolar 2024",
                    "Diretores com Formação Superior",
                    "Meta Sugerida"
                ]):
                    blocks_to_delete.append(block["id"])
        
        # Deletar apenas os blocos modificados por mim
        for block_id in blocks_to_delete:
            try:
                notion.blocks.delete(block_id=block_id)
                time.sleep(0.2)  # Evitar rate limit
            except Exception as e:
                print(f"   ❌ Erro ao deletar bloco {block_id}: {e}")
        
        return len(blocks_to_delete)
        
    except Exception as e:
        print(f"   ❌ Erro ao remover modificações: {e}")
        return 0

def restaurar_propriedades_originais(page_id):
    """Restaura as propriedades da página para o estado original (remove apenas tags minhas)."""
    try:
        # Buscar tags atuais
        page = notion.pages.retrieve(page_id=page_id)
        tags_atuais = page["properties"].get("Tags", {}).get("multi_select", [])
        
        # Filtrar apenas tags que NÃO são minhas
        tags_originais = []
        for tag in tags_atuais:
            if tag["name"] not in ["Dados Reais", "Censo Escolar 2024", "Boilerplate"]:
                tags_originais.append(tag)
        
        # Atualizar propriedades
        properties = {
            "Tags": {
                "multi_select": tags_originais  # Manter apenas tags originais
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
    print("🔧 REMOVENDO APENAS AS MODIFICAÇÕES FEITAS POR MIM")
    print("======================================================================")
    print("✅ Este processo irá:")
    print("   - Remover apenas blocos com dados do Censo Escolar 2024")
    print("   - Remover apenas tags que adicionei")
    print("   - PRESERVAR o conteúdo original das páginas")
    print("   - Alterar status para 'Rascunho'")
    print("======================================================================")
    
    notion = Client(auth=NOTION_TOKEN)
    print("✅ Conexão com Notion estabelecida!")
    
    pages = get_notion_pages(DATABASE_ID)
    print(f"📊 Total de páginas encontradas: {len(pages)}\n")

    # Processar páginas
    sucessos = 0
    erros = 0
    total_blocos_removidos = 0
    
    print(f"🔧 INICIANDO REMOÇÃO DE MODIFICAÇÕES EM {len(pages)} PÁGINAS...")
    print("======================================================================")
    
    for i, page in enumerate(pages):
        title_obj = page["properties"].get("Name", {}).get("title", [])
        title = title_obj[0]["plain_text"] if title_obj else "Sem Título"
        
        print(f"\n{i+1}/{len(pages)} - {title[:60]}...")
        
        try:
            # Remover apenas modificações minhas
            blocos_removidos = remover_apenas_modificacoes_minhas(page["id"])
            total_blocos_removidos += blocos_removidos
            print(f"   📝 Blocos modificados removidos: {blocos_removidos}")
            
            # Restaurar propriedades
            if restaurar_propriedades_originais(page["id"]):
                sucessos += 1
                print(f"   ✅ Página restaurada com sucesso!")
            else:
                erros += 1
                print(f"   ❌ Erro ao restaurar página!")
            
            # Pausa entre páginas para evitar rate limit
            time.sleep(0.5)
            
        except Exception as e:
            erros += 1
            print(f"   ❌ Erro geral: {e}")
    
    print(f"\n🎉 REMOÇÃO DE MODIFICAÇÕES CONCLUÍDA!")
    print("======================================================================")
    print(f"✅ Páginas processadas com sucesso: {sucessos}")
    print(f"❌ Páginas com erro: {erros}")
    print(f"📊 Total processadas: {len(pages)}")
    print(f"🗑️ Total de blocos modificados removidos: {total_blocos_removidos}")
    
    if erros == 0:
        print("\n🎉 Todas as modificações foram removidas com sucesso!")
        print("   ✅ Conteúdo original preservado")
        print("   ✅ Apenas modificações minhas removidas")
        print("   ✅ Tags originais mantidas")
    else:
        print(f"\n⚠️  {erros} páginas tiveram problemas durante o processo.")
        print("   Verifique os erros acima e execute novamente se necessário.")

if __name__ == "__main__":
    main()
