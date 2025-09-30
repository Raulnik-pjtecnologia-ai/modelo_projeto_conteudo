import os
import json
from notion_client import Client
from dotenv import load_dotenv

def reverter_publicacao_notion():
    """Reverter a publicação no Notion removendo a página criada."""
    print("REVERTENDO PUBLICACAO NO NOTION")
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
        # Carregar dados da sincronização
        try:
            with open("sincronizacao_gestao_alunos.json", "r", encoding="utf-8") as f:
                dados_sincronizacao = json.load(f)
            
            page_id = dados_sincronizacao["page_id"]
            titulo = dados_sincronizacao["titulo"]
            
            print(f"Pagina a ser removida:")
            print(f"   ID: {page_id}")
            print(f"   Titulo: {titulo}")
            
        except FileNotFoundError:
            print("ERRO: Arquivo de sincronizacao nao encontrado")
            return False
        
        # Arquivar (deletar) a página no Notion
        print(f"\nArquivando pagina no Notion...")
        
        notion.pages.update(
            page_id=page_id,
            archived=True
        )
        
        print(f"Pagina arquivada com sucesso!")
        print(f"   ID: {page_id}")
        print(f"   Status: Arquivada")
        
        return True
        
    except Exception as e:
        print(f"ERRO ao arquivar pagina: {e}")
        return False

def main():
    print("REVERTENDO PUBLICACAO NO NOTION")
    print("=" * 70)
    
    sucesso = reverter_publicacao_notion()
    
    if sucesso:
        print(f"\nREVERSAO CONCLUIDA COM SUCESSO!")
        print(f"   Pagina removida do Notion")
        print(f"   Pronto para nova geracao de conteudo")
    else:
        print(f"\nERRO NA REVERSAO")
        print(f"   Verificar logs")
    
    return sucesso

if __name__ == "__main__":
    main()
