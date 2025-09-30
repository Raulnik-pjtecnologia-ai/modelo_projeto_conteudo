import os
from notion_client import Client
from dotenv import load_dotenv

def verificar_propriedades_database():
    """Verificar propriedades disponíveis no database Editorial Gestão de Alunos."""
    print("VERIFICACAO DE PROPRIEDADES - DATABASE EDITORIAL GESTAO DE ALUNOS")
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
        # Database do Editorial Gestão de Alunos
        database_id = "2695113a-91a3-81dd-bfc4-fc8e4df72e7f"
        
        print(f"Database: Editorial Gestao de Alunos")
        print(f"ID: {database_id}")
        
        # Buscar informações do database
        database_info = notion.databases.retrieve(database_id=database_id)
        
        print(f"\nPROPRIEDADES DISPONIVEIS:")
        print(f"=" * 50)
        
        propriedades = database_info["properties"]
        
        for nome_propriedade, dados_propriedade in propriedades.items():
            tipo_propriedade = dados_propriedade["type"]
            print(f"• {nome_propriedade}: {tipo_propriedade}")
            
            # Se for select, mostrar opções
            if tipo_propriedade == "select" and "select" in dados_propriedade:
                opcoes = dados_propriedade["select"]["options"]
                if opcoes:
                    print(f"  Opcoes disponiveis:")
                    for opcao in opcoes:
                        print(f"    - {opcao['name']}")
                else:
                    print(f"  Nenhuma opcao configurada")
            
            # Se for multi_select, mostrar opções
            elif tipo_propriedade == "multi_select" and "multi_select" in dados_propriedade:
                opcoes = dados_propriedade["multi_select"]["options"]
                if opcoes:
                    print(f"  Opcoes disponiveis:")
                    for opcao in opcoes:
                        print(f"    - {opcao['name']}")
                else:
                    print(f"  Nenhuma opcao configurada")
        
        print(f"\nTOTAL DE PROPRIEDADES: {len(propriedades)}")
        
        return propriedades
        
    except Exception as e:
        print(f"ERRO na verificacao: {e}")
        return False

def main():
    print("VERIFICACAO DE PROPRIEDADES - DATABASE EDITORIAL GESTAO DE ALUNOS")
    print("=" * 70)
    
    propriedades = verificar_propriedades_database()
    
    if propriedades:
        print(f"\nVERIFICACAO CONCLUIDA!")
        print(f"   {len(propriedades)} propriedades encontradas")
        print(f"   Pronto para sincronizacao corrigida")
    else:
        print(f"\nERRO NA VERIFICACAO")
        print(f"   Verificar configuracoes")
    
    return propriedades

if __name__ == "__main__":
    main()
