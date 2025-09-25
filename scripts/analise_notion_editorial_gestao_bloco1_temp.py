import os
import json
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def analisar_editorial_gestao_bloco1():
    """BLOCO 1: Buscar todas as páginas do editorial de gestão educacional."""
    print("🔍 BLOCO 1: BUSCANDO PÁGINAS DO EDITORIAL DE GESTÃO")
    print("=" * 60)
    
    # Carregar configuração
    load_dotenv()
    
    notion_token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("DATABASE_ID")
    
    if not notion_token or not database_id:
        print("❌ Configuração do Notion não encontrada")
        return False
    
    # Inicializar cliente Notion
    notion = Client(auth=notion_token)
    
    try:
        # Buscar todas as páginas do editorial de gestão
        print("📊 Buscando páginas do editorial de gestão educacional...")
        
        # Filtrar por editorial de gestão
        filter_params = {
            "filter": {
                "property": "Categoria",
                "select": {
                    "equals": "Administração Escolar"
                }
            }
        }
        
        response = notion.databases.query(
            database_id=database_id,
            **filter_params
        )
        
        pages = response.get("results", [])
        
        print(f"📄 {len(pages)} páginas encontradas no editorial de gestão")
        
        # Processar informações básicas das páginas
        paginas_info = []
        paginas_parceiro_escola = []
        
        for page in pages:
            page_id = page["id"]
            properties = page.get("properties", {})
            
            # Extrair informações básicas
            titulo = ""
            if "Título" in properties:
                titulo_prop = properties["Título"]
                if titulo_prop.get("title"):
                    titulo = titulo_prop["title"][0]["text"]["content"]
            
            tipo = ""
            if "Tipo" in properties:
                tipo_prop = properties["Tipo"]
                if tipo_prop.get("select"):
                    tipo = tipo_prop["select"]["name"]
            
            status = ""
            if "Status editorial" in properties:
                status_prop = properties["Status editorial"]
                if status_prop.get("status"):
                    status = status_prop["status"]["name"]
            
            data_criacao = ""
            if "Criado em" in properties:
                data_prop = properties["Criado em"]
                if data_prop.get("created_time"):
                    data_criacao = data_prop["created_time"]
            
            # Verificar se contém "Parceiro da Escola"
            contem_parceiro = "parceiro da escola" in titulo.lower() if titulo else False
            
            pagina_info = {
                "page_id": page_id,
                "titulo": titulo,
                "tipo": tipo,
                "status": status,
                "data_criacao": data_criacao,
                "contem_parceiro_escola": contem_parceiro
            }
            
            paginas_info.append(pagina_info)
            
            if contem_parceiro:
                paginas_parceiro_escola.append(pagina_info)
                print(f"   🎯 ENCONTRADO: {titulo}")
        
        # Salvar dados do bloco 1
        dados_bloco1 = {
            "data_analise": datetime.now().isoformat(),
            "bloco": 1,
            "total_paginas": len(pages),
            "paginas_parceiro_escola": len(paginas_parceiro_escola),
            "paginas_info": paginas_info,
            "paginas_parceiro_escola_detalhadas": paginas_parceiro_escola
        }
        
        with open("dados_analise_bloco1_editorial_gestao.json", "w", encoding="utf-8") as f:
            json.dump(dados_bloco1, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n📊 RESUMO BLOCO 1:")
        print(f"   📄 Total de páginas: {len(pages)}")
        print(f"   🎯 Páginas 'Parceiro da Escola': {len(paginas_parceiro_escola)}")
        print(f"   💾 Dados salvos: dados_analise_bloco1_editorial_gestao.json")
        
        if paginas_parceiro_escola:
            print(f"\n🎯 PÁGINAS COM 'PARCEIRO DA ESCOLA':")
            for i, pagina in enumerate(paginas_parceiro_escola, 1):
                print(f"   {i}. {pagina['titulo']} ({pagina['page_id']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no Bloco 1: {e}")
        return False

def main():
    print("🔍 ANÁLISE EDITORIAL DE GESTÃO - BLOCO 1")
    print("======================================================================")
    print("📋 Buscando páginas do editorial de gestão educacional")
    print("======================================================================")
    
    sucesso = analisar_editorial_gestao_bloco1()
    
    if sucesso:
        print(f"\n✅ BLOCO 1 CONCLUÍDO COM SUCESSO!")
        print(f"   📊 Páginas identificadas")
        print(f"   🎯 Páginas 'Parceiro da Escola' encontradas")
        print(f"   💾 Dados salvos para próximos blocos")
    else:
        print(f"\n❌ ERRO NO BLOCO 1")
        print(f"   🔧 Verificar configuração")
        print(f"   📋 Revisar processo")
    
    return sucesso

if __name__ == "__main__":
    main()

