import os
import json
import time
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def analisar_biblioteca_gestao_alunos():
    """Analisar biblioteca para identificar necessidade de conteúdo sobre gestão de alunos."""
    print("ANALISE DA BIBLIOTECA - EDITORIAL GESTAO DE ALUNOS")
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
        # Buscar database do Editorial Gestão de Alunos
        database_id = "2695113a-91a3-81dd-bfc4-fc8e4df72e7f"
        
        print(f"Analisando database: Editorial Gestao de Alunos")
        print(f"ID: {database_id}")
        
        # Buscar todas as paginas do database
        pages = notion.databases.query(database_id=database_id)
        
        print(f"Total de conteudos encontrados: {len(pages['results'])}")
        print("=" * 70)
        
        conteudos_analisados = []
        categorias_existentes = {}
        niveis_existentes = {}
        funcoes_existentes = {}
        
        for i, page in enumerate(pages["results"]):
            page_id = page["id"]
            
            # Extrair propriedades da página
            titulo = ""
            if "properties" in page and "Name" in page["properties"]:
                if page["properties"]["Name"]["title"]:
                    titulo = page["properties"]["Name"]["title"][0]["text"]["content"]
            elif "properties" in page and "title" in page["properties"]:
                if page["properties"]["title"]["title"]:
                    titulo = page["properties"]["title"]["title"][0]["text"]["content"]
            
            # Extrair outras propriedades
            categoria = ""
            nivel = ""
            funcao = ""
            status = ""
            
            if "Categoria" in page["properties"]:
                if page["properties"]["Categoria"]["select"]:
                    categoria = page["properties"]["Categoria"]["select"]["name"]
            
            if "Nivel" in page["properties"]:
                if page["properties"]["Nivel"]["select"]:
                    nivel = page["properties"]["Nivel"]["select"]["name"]
            
            if "Funcao" in page["properties"]:
                if page["properties"]["Funcao"]["select"]:
                    funcao = page["properties"]["Funcao"]["select"]["name"]
            
            if "Status" in page["properties"]:
                if page["properties"]["Status"]["select"]:
                    status = page["properties"]["Status"]["select"]["name"]
            
            print(f"{i+1}. {titulo[:50]}...")
            print(f"   Categoria: {categoria}")
            print(f"   Nivel: {nivel}")
            print(f"   Funcao: {funcao}")
            print(f"   Status: {status}")
            
            # Contar categorias
            if categoria:
                categorias_existentes[categoria] = categorias_existentes.get(categoria, 0) + 1
            
            # Contar niveis
            if nivel:
                niveis_existentes[nivel] = niveis_existentes.get(nivel, 0) + 1
            
            # Contar funcoes
            if funcao:
                funcoes_existentes[funcao] = funcoes_existentes.get(funcao, 0) + 1
            
            # Adicionar à lista de conteúdos analisados
            conteudos_analisados.append({
                "page_id": page_id,
                "titulo": titulo,
                "categoria": categoria,
                "nivel": nivel,
                "funcao": funcao,
                "status": status
            })
        
        # Analisar equilíbrio da biblioteca
        print(f"\nANALISE DO EQUILIBRIO DA BIBLIOTECA:")
        print(f"=" * 70)
        
        print(f"Categorias existentes:")
        for categoria, count in sorted(categorias_existentes.items(), key=lambda x: x[1], reverse=True):
            percentual = (count / len(pages["results"])) * 100 if len(pages["results"]) > 0 else 0
            print(f"   {categoria}: {count} ({percentual:.1f}%)")
        
        print(f"\nNiveis existentes:")
        for nivel, count in sorted(niveis_existentes.items(), key=lambda x: x[1], reverse=True):
            percentual = (count / len(pages["results"])) * 100 if len(pages["results"]) > 0 else 0
            print(f"   {nivel}: {count} ({percentual:.1f}%)")
        
        print(f"\nFuncoes existentes:")
        for funcao, count in sorted(funcoes_existentes.items(), key=lambda x: x[1], reverse=True):
            percentual = (count / len(pages["results"])) * 100 if len(pages["results"]) > 0 else 0
            print(f"   {funcao}: {count} ({percentual:.1f}%)")
        
        # Identificar necessidades baseadas na pesquisa anterior
        print(f"\nIDENTIFICACAO DE NECESSIDADES:")
        print(f"=" * 70)
        
        # Carregar dados da pesquisa anterior
        try:
            with open("pesquisa_editorial_gestao_alunos.json", "r", encoding="utf-8") as f:
                dados_pesquisa = json.load(f)
            
            oportunidades_prioridade_alta = dados_pesquisa["recomendacoes_conteudo"]["prioridade_alta"]
            
            print(f"Oportunidades identificadas na pesquisa:")
            for i, oportunidade in enumerate(oportunidades_prioridade_alta, 1):
                print(f"   {i}. {oportunidade}")
            
            # Verificar se já existem conteúdos sobre essas oportunidades
            conteudos_existentes_sobre_oportunidades = []
            for conteudo in conteudos_analisados:
                titulo_lower = conteudo["titulo"].lower()
                for oportunidade in oportunidades_prioridade_alta:
                    oportunidade_lower = oportunidade.lower()
                    if any(palavra in titulo_lower for palavra in oportunidade_lower.split()):
                        conteudos_existentes_sobre_oportunidades.append({
                            "titulo": conteudo["titulo"],
                            "oportunidade": oportunidade
                        })
            
            print(f"\nConteudos existentes sobre as oportunidades:")
            if conteudos_existentes_sobre_oportunidades:
                for conteudo in conteudos_existentes_sobre_oportunidades:
                    print(f"   • {conteudo['titulo']} (relacionado a: {conteudo['oportunidade']})")
            else:
                print(f"   Nenhum conteudo existente sobre as oportunidades identificadas")
            
            # Identificar lacunas
            lacunas_identificadas = []
            for oportunidade in oportunidades_prioridade_alta:
                tem_conteudo = any(
                    any(palavra in conteudo["titulo"].lower() for palavra in oportunidade.lower().split())
                    for conteudo in conteudos_analisados
                )
                if not tem_conteudo:
                    lacunas_identificadas.append(oportunidade)
            
            print(f"\nLacunas identificadas (oportunidades sem conteudo):")
            for i, lacuna in enumerate(lacunas_identificadas, 1):
                print(f"   {i}. {lacuna}")
            
        except FileNotFoundError:
            print(f"AVISO: Arquivo de pesquisa anterior nao encontrado")
            lacunas_identificadas = ["Sistemas de Gestao Escolar Modernos", "Estrategias de Combate a Evasao Escolar", "Gestao Escolar Inclusiva"]
        
        # Salvar dados da análise
        dados_analise = {
            "data_analise": datetime.now().isoformat(),
            "database_id": database_id,
            "total_conteudos": len(pages["results"]),
            "categorias_existentes": categorias_existentes,
            "niveis_existentes": niveis_existentes,
            "funcoes_existentes": funcoes_existentes,
            "conteudos_analisados": conteudos_analisados,
            "lacunas_identificadas": lacunas_identificadas,
            "necessidade_geracao": len(lacunas_identificadas) > 0
        }
        
        with open("analise_biblioteca_gestao_alunos.json", "w", encoding="utf-8") as f:
            json.dump(dados_analise, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\nANALISE CONCLUIDA!")
        print(f"   Total de conteudos: {len(pages['results'])}")
        print(f"   Lacunas identificadas: {len(lacunas_identificadas)}")
        print(f"   Necessidade de geracao: {'SIM' if len(lacunas_identificadas) > 0 else 'NAO'}")
        print(f"   Dados salvos em analise_biblioteca_gestao_alunos.json")
        
        return len(lacunas_identificadas) > 0, lacunas_identificadas
        
    except Exception as e:
        print(f"Erro na analise da biblioteca: {e}")
        return False, []

def main():
    print("ANALISE DA BIBLIOTECA - EDITORIAL GESTAO DE ALUNOS")
    print("=" * 70)
    
    necessidade, lacunas = analisar_biblioteca_gestao_alunos()
    
    if necessidade:
        print(f"\nNECESSIDADE DE GERACAO IDENTIFICADA!")
        print(f"   {len(lacunas)} lacunas encontradas")
        print(f"   Pronto para geracao de conteudo")
    else:
        print(f"\nBIBLIOTECA EQUILIBRADA!")
        print(f"   Nenhuma lacuna identificada")
    
    return necessidade, lacunas

if __name__ == "__main__":
    main()
