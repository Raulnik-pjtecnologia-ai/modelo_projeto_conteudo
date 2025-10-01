import os
import json
import time
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def contar_conteudos_banco():
    """Contar quantos conteúdos existem no banco de dados."""
    print("CONTAGEM DE CONTEUDOS NO BANCO DE DADOS")
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
        # Buscar todos os databases
        databases = notion.search(filter={"property": "object", "value": "database"})
        
        print(f"BANCO DE DADOS ENCONTRADOS: {len(databases['results'])}")
        print("=" * 60)
        
        total_conteudos = 0
        databases_info = []
        
        for i, db in enumerate(databases["results"]):
            database_id = db["id"]
            database_nome = ""
            
            if "title" in db and len(db["title"]) > 0:
                database_nome = db["title"][0]["text"]["content"]
            else:
                database_nome = f"Database {i+1} (sem nome)"
            
            print(f"   {i+1}. {database_nome}")
            
            try:
                # Buscar todas as paginas do database
                pages = notion.databases.query(database_id=database_id)
                num_paginas = len(pages["results"])
                
                print(f"      📄 Páginas: {num_paginas}")
                
                # Analisar tipos de conteúdo
                tipos_conteudo = {}
                conteudos_por_tipo = {}
                
                for page in pages["results"]:
                    # Extrair título da página
                    titulo = ""
                    if "properties" in page and "Name" in page["properties"]:
                        if page["properties"]["Name"]["title"]:
                            titulo = page["properties"]["Name"]["title"][0]["text"]["content"]
                    elif "properties" in page and "title" in page["properties"]:
                        if page["properties"]["title"]["title"]:
                            titulo = page["properties"]["title"]["title"][0]["text"]["content"]
                    
                    # Classificar por tipo baseado no título
                    tipo = "Outros"
                    if "gestão" in titulo.lower() or "gestao" in titulo.lower():
                        tipo = "Gestão Escolar"
                    elif "educação" in titulo.lower() or "educacao" in titulo.lower():
                        tipo = "Educação"
                    elif "pedagógico" in titulo.lower() or "pedagogico" in titulo.lower():
                        tipo = "Pedagógico"
                    elif "administrativo" in titulo.lower():
                        tipo = "Administrativo"
                    elif "financeiro" in titulo.lower():
                        tipo = "Financeiro"
                    elif "tecnologia" in titulo.lower():
                        tipo = "Tecnologia"
                    elif "legislação" in titulo.lower() or "legislacao" in titulo.lower():
                        tipo = "Legislação"
                    elif "formação" in titulo.lower() or "formacao" in titulo.lower():
                        tipo = "Formação"
                    elif "governança" in titulo.lower() or "governanca" in titulo.lower():
                        tipo = "Governança"
                    elif "biblioteca" in titulo.lower():
                        tipo = "Biblioteca"
                    elif "categoria" in titulo.lower():
                        tipo = "Categoria"
                    elif "seção" in titulo.lower() or "secao" in titulo.lower():
                        tipo = "Seção"
                    elif "módulo" in titulo.lower() or "modulo" in titulo.lower():
                        tipo = "Módulo"
                    elif "planner" in titulo.lower():
                        tipo = "Planner"
                    elif "autor" in titulo.lower():
                        tipo = "Autor"
                    elif "curso" in titulo.lower():
                        tipo = "Curso"
                    elif "view" in titulo.lower():
                        tipo = "View"
                    
                    tipos_conteudo[tipo] = tipos_conteudo.get(tipo, 0) + 1
                    
                    if tipo not in conteudos_por_tipo:
                        conteudos_por_tipo[tipo] = []
                    conteudos_por_tipo[tipo].append({
                        "titulo": titulo,
                        "page_id": page["id"]
                    })
                
                # Mostrar tipos de conteúdo encontrados
                if tipos_conteudo:
                    print(f"      📊 Tipos de conteúdo:")
                    for tipo, count in sorted(tipos_conteudo.items(), key=lambda x: x[1], reverse=True):
                        print(f"         - {tipo}: {count}")
                
                # Adicionar à lista de databases
                databases_info.append({
                    "database_id": database_id,
                    "nome": database_nome,
                    "total_paginas": num_paginas,
                    "tipos_conteudo": tipos_conteudo,
                    "conteudos_por_tipo": conteudos_por_tipo
                })
                
                total_conteudos += num_paginas
                
                # Pausa entre databases
                time.sleep(1)
                
            except Exception as e:
                print(f"      ERRO: {str(e)[:50]}...")
        
        # Calcular estatísticas gerais
        print(f"\nRESUMO GERAL:")
        print(f"=" * 60)
        print(f"📚 Total de databases: {len(databases['results'])}")
        print(f"📄 Total de conteúdos: {total_conteudos}")
        
        # Consolidar tipos de conteúdo de todos os databases
        tipos_gerais = {}
        for db_info in databases_info:
            for tipo, count in db_info["tipos_conteudo"].items():
                tipos_gerais[tipo] = tipos_gerais.get(tipo, 0) + count
        
        if tipos_gerais:
            print(f"\n📊 DISTRIBUIÇÃO POR TIPO DE CONTEÚDO:")
            for tipo, count in sorted(tipos_gerais.items(), key=lambda x: x[1], reverse=True):
                percentual = (count / total_conteudos) * 100 if total_conteudos > 0 else 0
                print(f"   {tipo}: {count} ({percentual:.1f}%)")
        
        # Salvar dados da contagem
        dados_contagem = {
            "data_contagem": datetime.now().isoformat(),
            "total_databases": len(databases["results"]),
            "total_conteudos": total_conteudos,
            "tipos_gerais": tipos_gerais,
            "databases_info": databases_info
        }
        
        with open("contagem_conteudos_banco.json", "w", encoding="utf-8") as f:
            json.dump(dados_contagem, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\nCONTAGEM CONCLUIDA!")
        print(f"   {total_conteudos} conteudos encontrados")
        print(f"   {len(databases['results'])} databases analisados")
        print(f"   Dados salvos em contagem_conteudos_banco.json")
        
        return total_conteudos
        
    except Exception as e:
        print(f"Erro na contagem de conteúdos: {e}")
        return 0

def main():
    print("CONTAGEM DE CONTEUDOS NO BANCO DE DADOS")
    print("=" * 60)
    
    total = contar_conteudos_banco()
    
    if total > 0:
        print(f"\nRESULTADO FINAL:")
        print(f"   {total} conteudos encontrados no banco de dados")
    else:
        print(f"\nNENHUM CONTEUDO ENCONTRADO")
    
    return total

if __name__ == "__main__":
    main()
