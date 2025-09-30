import os
import json
import time
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def verificar_distribuicao_conteudos():
    """Verificar se a distribuição por tipo de conteúdo está correta, analisando o interior de cada conteúdo."""
    print("VERIFICACAO DA DISTRIBUICAO POR TIPO DE CONTEUDO")
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
        # Buscar todos os databases
        databases = notion.search(filter={"property": "object", "value": "database"})
        
        print(f"VERIFICANDO DISTRIBUICAO EM {len(databases['results'])} DATABASES...")
        
        conteudos_analisados = []
        distribuicao_real = {}
        distribuicao_anterior = {}
        
        for i, db in enumerate(databases["results"]):
            database_id = db["id"]
            database_nome = ""
            
            if "title" in db and len(db["title"]) > 0:
                database_nome = db["title"][0]["text"]["content"]
            else:
                database_nome = f"Database {i+1} (sem nome)"
            
            print(f"\n   {i+1}. {database_nome}")
            
            try:
                # Buscar todas as paginas do database
                pages = notion.databases.query(database_id=database_id)
                
                print(f"      Analisando {len(pages['results'])} conteudos...")
                
                for j, page in enumerate(pages["results"]):
                    page_id = page["id"]
                    
                    # Extrair título da página
                    titulo = ""
                    if "properties" in page and "Name" in page["properties"]:
                        if page["properties"]["Name"]["title"]:
                            titulo = page["properties"]["Name"]["title"][0]["text"]["content"]
                    elif "properties" in page and "title" in page["properties"]:
                        if page["properties"]["title"]["title"]:
                            titulo = page["properties"]["title"]["title"][0]["text"]["content"]
                    
                    print(f"         {j+1}/{len(pages['results'])}: {titulo[:40]}...")
                    
                    try:
                        # Buscar conteúdo da página
                        page_blocks = notion.blocks.children.list(block_id=page_id)
                        
                        # Analisar conteúdo interno
                        texto_completo = ""
                        palavras_chave = []
                        
                        for block in page_blocks["results"]:
                            if block["type"] == "paragraph" and "rich_text" in block["paragraph"]:
                                for rt in block["paragraph"]["rich_text"]:
                                    texto_completo += rt["text"]["content"] + " "
                            elif block["type"] == "heading_1" and "rich_text" in block["heading_1"]:
                                for rt in block["heading_1"]["rich_text"]:
                                    texto_completo += rt["text"]["content"] + " "
                            elif block["type"] == "heading_2" and "rich_text" in block["heading_2"]:
                                for rt in block["heading_2"]["rich_text"]:
                                    texto_completo += rt["text"]["content"] + " "
                            elif block["type"] == "heading_3" and "rich_text" in block["heading_3"]:
                                for rt in block["heading_3"]["rich_text"]:
                                    texto_completo += rt["text"]["content"] + " "
                            elif block["type"] == "bulleted_list_item" and "rich_text" in block["bulleted_list_item"]:
                                for rt in block["bulleted_list_item"]["rich_text"]:
                                    texto_completo += rt["text"]["content"] + " "
                            elif block["type"] == "numbered_list_item" and "rich_text" in block["numbered_list_item"]:
                                for rt in block["numbered_list_item"]["rich_text"]:
                                    texto_completo += rt["text"]["content"] + " "
                        
                        # Converter para minúsculas para análise
                        texto_lower = texto_completo.lower()
                        
                        # Classificar por conteúdo interno (mais preciso)
                        tipo_real = "Outros"
                        confianca = 0
                        palavras_encontradas = []
                        
                        # Gestão Escolar
                        palavras_gestao = ["gestão", "gestao", "diretor", "coordenador", "supervisor", "administração escolar", "administracao escolar", "liderança escolar", "lideranca escolar", "planejamento escolar", "projeto pedagógico", "projeto pedagogico", "ppp", "conselho escolar", "grêmio estudantil", "gremio estudantil", "associação de pais", "associacao de pais", "censo escolar", "ideb", "pne", "bncc"]
                        for palavra in palavras_gestao:
                            if palavra in texto_lower:
                                confianca += 1
                                palavras_encontradas.append(palavra)
                        if confianca >= 2:
                            tipo_real = "Gestao Escolar"
                        
                        # Educação
                        palavras_educacao = ["educação", "educacao", "ensino", "aprendizagem", "pedagogia", "didática", "didatica", "metodologia", "currículo", "curriculo", "avaliação", "avaliacao", "nota", "prova", "exame", "sala de aula", "professor", "aluno", "estudante", "escola", "colégio", "colegio"]
                        if tipo_real == "Outros":
                            confianca = 0
                            palavras_encontradas = []
                            for palavra in palavras_educacao:
                                if palavra in texto_lower:
                                    confianca += 1
                                    palavras_encontradas.append(palavra)
                            if confianca >= 2:
                                tipo_real = "Educacao"
                        
                        # Tecnologia
                        palavras_tecnologia = ["tecnologia", "digital", "computador", "internet", "software", "aplicativo", "app", "plataforma", "sistema", "dados", "informação", "informacao", "ti", "informática", "informatica", "programação", "programacao", "código", "codigo"]
                        if tipo_real == "Outros":
                            confianca = 0
                            palavras_encontradas = []
                            for palavra in palavras_tecnologia:
                                if palavra in texto_lower:
                                    confianca += 1
                                    palavras_encontradas.append(palavra)
                            if confianca >= 2:
                                tipo_real = "Tecnologia"
                        
                        # Financeiro
                        palavras_financeiro = ["financeiro", "orçamento", "orcamento", "receita", "despesa", "custo", "investimento", "recursos", "dinheiro", "valor", "preço", "preco", "pagamento", "fatura", "conta", "balanço", "balanco", "contabilidade"]
                        if tipo_real == "Outros":
                            confianca = 0
                            palavras_encontradas = []
                            for palavra in palavras_financeiro:
                                if palavra in texto_lower:
                                    confianca += 1
                                    palavras_encontradas.append(palavra)
                            if confianca >= 2:
                                tipo_real = "Financeiro"
                        
                        # Legislação
                        palavras_legislacao = ["lei", "decreto", "portaria", "resolução", "resolucao", "norma", "regulamento", "legislação", "legislacao", "direito", "jurídico", "juridico", "legal", "constitucional", "estatuto", "regimento"]
                        if tipo_real == "Outros":
                            confianca = 0
                            palavras_encontradas = []
                            for palavra in palavras_legislacao:
                                if palavra in texto_lower:
                                    confianca += 1
                                    palavras_encontradas.append(palavra)
                            if confianca >= 2:
                                tipo_real = "Legislacao"
                        
                        # Formação
                        palavras_formacao = ["formação", "formacao", "capacitação", "capacitacao", "treinamento", "curso", "workshop", "seminário", "seminario", "palestra", "desenvolvimento profissional", "habilidades", "competências", "competencias", "aprendizado", "estudo"]
                        if tipo_real == "Outros":
                            confianca = 0
                            palavras_encontradas = []
                            for palavra in palavras_formacao:
                                if palavra in texto_lower:
                                    confianca += 1
                                    palavras_encontradas.append(palavra)
                            if confianca >= 2:
                                tipo_real = "Formacao"
                        
                        # Pedagógico
                        palavras_pedagogico = ["pedagógico", "pedagogico", "didática", "didatica", "metodologia", "ensino", "aprendizagem", "currículo", "curriculo", "conteúdo", "conteudo", "atividade", "exercício", "exercicio", "lição", "licao", "aula", "plano de aula"]
                        if tipo_real == "Outros":
                            confianca = 0
                            palavras_encontradas = []
                            for palavra in palavras_pedagogico:
                                if palavra in texto_lower:
                                    confianca += 1
                                    palavras_encontradas.append(palavra)
                            if confianca >= 2:
                                tipo_real = "Pedagogico"
                        
                        # Governança
                        palavras_governanca = ["governança", "governanca", "gestão pública", "gestao publica", "política pública", "politica publica", "administração pública", "administracao publica", "transparência", "transparencia", "accountability", "controle social", "participação", "participacao"]
                        if tipo_real == "Outros":
                            confianca = 0
                            palavras_encontradas = []
                            for palavra in palavras_governanca:
                                if palavra in texto_lower:
                                    confianca += 1
                                    palavras_encontradas.append(palavra)
                            if confianca >= 2:
                                tipo_real = "Governanca"
                        
                        # Classificação anterior (baseada apenas no título)
                        tipo_anterior = "Outros"
                        titulo_lower = titulo.lower()
                        if "gestão" in titulo_lower or "gestao" in titulo_lower:
                            tipo_anterior = "Gestao Escolar"
                        elif "educação" in titulo_lower or "educacao" in titulo_lower:
                            tipo_anterior = "Educacao"
                        elif "pedagógico" in titulo_lower or "pedagogico" in titulo_lower:
                            tipo_anterior = "Pedagogico"
                        elif "administrativo" in titulo_lower:
                            tipo_anterior = "Administrativo"
                        elif "financeiro" in titulo_lower:
                            tipo_anterior = "Financeiro"
                        elif "tecnologia" in titulo_lower:
                            tipo_anterior = "Tecnologia"
                        elif "legislação" in titulo_lower or "legislacao" in titulo_lower:
                            tipo_anterior = "Legislacao"
                        elif "formação" in titulo_lower or "formacao" in titulo_lower:
                            tipo_anterior = "Formacao"
                        elif "governança" in titulo_lower or "governanca" in titulo_lower:
                            tipo_anterior = "Governanca"
                        elif "biblioteca" in titulo_lower:
                            tipo_anterior = "Biblioteca"
                        elif "categoria" in titulo_lower:
                            tipo_anterior = "Categoria"
                        elif "seção" in titulo_lower or "secao" in titulo_lower:
                            tipo_anterior = "Secao"
                        elif "módulo" in titulo_lower or "modulo" in titulo_lower:
                            tipo_anterior = "Modulo"
                        elif "planner" in titulo_lower:
                            tipo_anterior = "Planner"
                        elif "autor" in titulo_lower:
                            tipo_anterior = "Autor"
                        elif "curso" in titulo_lower:
                            tipo_anterior = "Curso"
                        elif "view" in titulo_lower:
                            tipo_anterior = "View"
                        
                        # Verificar se há discrepância
                        discrepancia = tipo_anterior != tipo_real
                        
                        # Adicionar à lista de conteúdos analisados
                        conteudo_info = {
                            "page_id": page_id,
                            "titulo": titulo,
                            "database": database_nome,
                            "tipo_anterior": tipo_anterior,
                            "tipo_real": tipo_real,
                            "discrepancia": discrepancia,
                            "palavras_encontradas": palavras_encontradas,
                            "confianca": confianca,
                            "texto_amostra": texto_completo[:200] + "..." if len(texto_completo) > 200 else texto_completo
                        }
                        
                        conteudos_analisados.append(conteudo_info)
                        
                        # Atualizar distribuição real
                        distribuicao_real[tipo_real] = distribuicao_real.get(tipo_real, 0) + 1
                        distribuicao_anterior[tipo_anterior] = distribuicao_anterior.get(tipo_anterior, 0) + 1
                        
                        if discrepancia:
                            print(f"            DISCREPANCIA: {tipo_anterior} -> {tipo_real}")
                            print(f"            Palavras: {', '.join(palavras_encontradas[:5])}")
                        else:
                            print(f"            OK: {tipo_real}")
                        
                        # Pausa entre conteúdos
                        time.sleep(0.5)
                        
                    except Exception as e:
                        print(f"            ERRO: {str(e)[:30]}...")
                
                # Pausa entre databases
                time.sleep(1)
                
            except Exception as e:
                print(f"      ERRO: {str(e)[:50]}...")
        
        # Calcular estatísticas
        total_conteudos = len(conteudos_analisados)
        conteudos_com_discrepancia = len([c for c in conteudos_analisados if c["discrepancia"]])
        conteudos_sem_discrepancia = total_conteudos - conteudos_com_discrepancia
        
        print(f"\nRESULTADOS DA VERIFICACAO:")
        print(f"=" * 70)
        print(f"Total de conteudos analisados: {total_conteudos}")
        print(f"Conteudos sem discrepancia: {conteudos_sem_discrepancia}")
        print(f"Conteudos com discrepancia: {conteudos_com_discrepancia}")
        print(f"Percentual de acuracia: {(conteudos_sem_discrepancia/total_conteudos)*100:.1f}%")
        
        print(f"\nDISTRIBUICAO ANTERIOR (baseada no titulo):")
        for tipo, count in sorted(distribuicao_anterior.items(), key=lambda x: x[1], reverse=True):
            percentual = (count / total_conteudos) * 100 if total_conteudos > 0 else 0
            print(f"   {tipo}: {count} ({percentual:.1f}%)")
        
        print(f"\nDISTRIBUICAO REAL (baseada no conteudo):")
        for tipo, count in sorted(distribuicao_real.items(), key=lambda x: x[1], reverse=True):
            percentual = (count / total_conteudos) * 100 if total_conteudos > 0 else 0
            print(f"   {tipo}: {count} ({percentual:.1f}%)")
        
        # Salvar dados da verificação
        dados_verificacao = {
            "data_verificacao": datetime.now().isoformat(),
            "total_conteudos_analisados": total_conteudos,
            "conteudos_sem_discrepancia": conteudos_sem_discrepancia,
            "conteudos_com_discrepancia": conteudos_com_discrepancia,
            "percentual_acuracia": (conteudos_sem_discrepancia/total_conteudos)*100,
            "distribuicao_anterior": distribuicao_anterior,
            "distribuicao_real": distribuicao_real,
            "conteudos_analisados": conteudos_analisados
        }
        
        with open("verificacao_distribuicao_conteudos.json", "w", encoding="utf-8") as f:
            json.dump(dados_verificacao, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\nVERIFICACAO CONCLUIDA!")
        print(f"   {conteudos_sem_discrepancia}/{total_conteudos} conteudos classificados corretamente")
        print(f"   {conteudos_com_discrepancia} conteudos com classificacao incorreta")
        print(f"   Dados salvos em verificacao_distribuicao_conteudos.json")
        
        return conteudos_com_discrepancia > 0
        
    except Exception as e:
        print(f"Erro na verificacao da distribuicao: {e}")
        return False

def main():
    print("VERIFICACAO DA DISTRIBUICAO POR TIPO DE CONTEUDO")
    print("=" * 70)
    
    tem_discrepancias = verificar_distribuicao_conteudos()
    
    if tem_discrepancias:
        print(f"\nVERIFICACAO CONCLUIDA - DISCREPANCIAS ENCONTRADAS!")
        print(f"   A distribuicao anterior nao estava correta")
        print(f"   Verificar arquivo verificacao_distribuicao_conteudos.json")
    else:
        print(f"\nVERIFICACAO CONCLUIDA - DISTRIBUICAO CORRETA!")
        print(f"   A distribuicao anterior estava correta")
    
    return tem_discrepancias

if __name__ == "__main__":
    main()
