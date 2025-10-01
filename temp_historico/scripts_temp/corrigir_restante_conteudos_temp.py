import os
import json
import time
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def corrigir_restante_conteudos():
    """Corrigir o restante dos conteúdos que não puderam ser corrigidos anteriormente."""
    print("CORRECAO DO RESTANTE DOS CONTEUDOS")
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
        # Carregar dados da correcao anterior
        try:
            with open("correcao_distribuicao_conteudos.json", "r", encoding="utf-8") as f:
                dados_correcao = json.load(f)
            
            detalhes_correcoes = dados_correcao["detalhes_correcoes"]
            print(f"Dados da correcao anterior carregados: {len(detalhes_correcoes)} correcoes")
            
        except FileNotFoundError:
            print("ERRO: Arquivo de correcao anterior nao encontrado")
            print("Execute primeiro a correcao da distribuicao")
            return False
        
        # Filtrar apenas correcoes que falharam
        correcoes_falharam = [c for c in detalhes_correcoes if not c["sucesso"]]
        
        print(f"Correcoes que falharam encontradas: {len(correcoes_falharam)}")
        print("=" * 70)
        
        correcoes_aplicadas = 0
        erros_correcao = 0
        detalhes_correcoes_restantes = []
        
        for i, correcao in enumerate(correcoes_falharam):
            page_id = correcao["page_id"]
            titulo = correcao["titulo"]
            tipo_anterior = correcao["tipo_anterior"]
            tipo_real = correcao["tipo_real"]
            database = correcao["database"]
            
            print(f"\n{i+1}/{len(correcoes_falharam)}: {titulo[:40]}...")
            print(f"   Database: {database}")
            print(f"   Correcao: {tipo_anterior} -> {tipo_real}")
            
            try:
                # Buscar a pagina no Notion
                page = notion.pages.retrieve(page_id=page_id)
                
                # Verificar se a pagina tem propriedade de categoria/tipo
                propriedades_disponiveis = list(page["properties"].keys())
                print(f"   Propriedades disponiveis: {', '.join(propriedades_disponiveis)}")
                
                # Tentar diferentes estrategias para adicionar propriedade de categoria
                propriedade_categoria = None
                possiveis_nomes = ["Categoria", "Tipo", "Category", "Type", "Classificacao", "Classificacao", "Area", "Area", "Tag", "Tags"]
                
                for nome in possiveis_nomes:
                    if nome in propriedades_disponiveis:
                        propriedade_categoria = nome
                        break
                
                if propriedade_categoria:
                    print(f"   Propriedade encontrada: {propriedade_categoria}")
                    
                    # Verificar o tipo da propriedade
                    tipo_propriedade = page["properties"][propriedade_categoria]["type"]
                    print(f"   Tipo da propriedade: {tipo_propriedade}")
                    
                    # Atualizar a propriedade baseada no tipo
                    if tipo_propriedade == "select":
                        # Propriedade select - atualizar com o novo valor
                        notion.pages.update(
                            page_id=page_id,
                            properties={
                                propriedade_categoria: {
                                    "select": {"name": tipo_real}
                                }
                            }
                        )
                        print(f"   OK - Propriedade select atualizada para: {tipo_real}")
                        correcoes_aplicadas += 1
                        
                    elif tipo_propriedade == "multi_select":
                        # Propriedade multi_select - adicionar o novo valor
                        valores_atuais = []
                        if page["properties"][propriedade_categoria]["multi_select"]:
                            valores_atuais = [item["name"] for item in page["properties"][propriedade_categoria]["multi_select"]]
                        
                        # Remover o valor anterior se existir
                        if tipo_anterior in valores_atuais:
                            valores_atuais.remove(tipo_anterior)
                        
                        # Adicionar o novo valor
                        if tipo_real not in valores_atuais:
                            valores_atuais.append(tipo_real)
                        
                        notion.pages.update(
                            page_id=page_id,
                            properties={
                                propriedade_categoria: {
                                    "multi_select": [{"name": valor} for valor in valores_atuais]
                                }
                            }
                        )
                        print(f"   OK - Propriedade multi_select atualizada para: {', '.join(valores_atuais)}")
                        correcoes_aplicadas += 1
                        
                    elif tipo_propriedade == "rich_text":
                        # Propriedade rich_text - atualizar com o novo valor
                        notion.pages.update(
                            page_id=page_id,
                            properties={
                                propriedade_categoria: {
                                    "rich_text": [{"type": "text", "text": {"content": tipo_real}}]
                                }
                            }
                        )
                        print(f"   OK - Propriedade rich_text atualizada para: {tipo_real}")
                        correcoes_aplicadas += 1
                        
                    elif tipo_propriedade == "title":
                        # Propriedade title - atualizar com o novo valor
                        notion.pages.update(
                            page_id=page_id,
                            properties={
                                propriedade_categoria: {
                                    "title": [{"type": "text", "text": {"content": tipo_real}}]
                                }
                            }
                        )
                        print(f"   OK - Propriedade title atualizada para: {tipo_real}")
                        correcoes_aplicadas += 1
                        
                    else:
                        print(f"   AVISO - Tipo de propriedade nao suportado: {tipo_propriedade}")
                        erros_correcao += 1
                        
                else:
                    # Tentar adicionar uma nova propriedade de categoria
                    print(f"   Tentando adicionar nova propriedade de categoria...")
                    
                    try:
                        # Buscar o database da pagina
                        database_id = page["parent"]["database_id"]
                        
                        # Adicionar nova propriedade ao database
                        notion.databases.update(
                            database_id=database_id,
                            properties={
                                "Categoria": {
                                    "select": {
                                        "options": [
                                            {"name": "Gestao Escolar", "color": "blue"},
                                            {"name": "Educacao", "color": "green"},
                                            {"name": "Tecnologia", "color": "orange"},
                                            {"name": "Financeiro", "color": "red"},
                                            {"name": "Legislacao", "color": "purple"},
                                            {"name": "Formacao", "color": "yellow"},
                                            {"name": "Pedagogico", "color": "pink"},
                                            {"name": "Governanca", "color": "brown"},
                                            {"name": "Outros", "color": "gray"}
                                        ]
                                    }
                                }
                            }
                        )
                        
                        print(f"   OK - Nova propriedade 'Categoria' adicionada ao database")
                        
                        # Atualizar a pagina com a nova propriedade
                        notion.pages.update(
                            page_id=page_id,
                            properties={
                                "Categoria": {
                                    "select": {"name": tipo_real}
                                }
                            }
                        )
                        
                        print(f"   OK - Pagina atualizada com categoria: {tipo_real}")
                        correcoes_aplicadas += 1
                        
                    except Exception as e:
                        print(f"   ERRO ao adicionar propriedade: {str(e)[:50]}...")
                        erros_correcao += 1
                
                # Adicionar detalhes da correcao
                detalhes_correcoes_restantes.append({
                    "page_id": page_id,
                    "titulo": titulo,
                    "database": database,
                    "tipo_anterior": tipo_anterior,
                    "tipo_real": tipo_real,
                    "propriedade_usada": propriedade_categoria,
                    "sucesso": propriedade_categoria is not None,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Pausa entre correcoes
                time.sleep(2)
                
            except Exception as e:
                print(f"   ERRO: {str(e)[:50]}...")
                erros_correcao += 1
                
                # Adicionar detalhes do erro
                detalhes_correcoes_restantes.append({
                    "page_id": page_id,
                    "titulo": titulo,
                    "database": database,
                    "tipo_anterior": tipo_anterior,
                    "tipo_real": tipo_real,
                    "propriedade_usada": None,
                    "sucesso": False,
                    "erro": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        # Calcular estatisticas finais
        total_conteudos_corrigir = len(correcoes_falharam)
        sucessos = len([d for d in detalhes_correcoes_restantes if d["sucesso"]])
        falhas = len([d for d in detalhes_correcoes_restantes if not d["sucesso"]])
        
        print(f"\nRESULTADOS DA CORRECAO DO RESTANTE:")
        print(f"=" * 70)
        print(f"Total de conteudos para corrigir: {total_conteudos_corrigir}")
        print(f"Correcoes aplicadas com sucesso: {sucessos}")
        print(f"Falhas na correcao: {falhas}")
        print(f"Percentual de sucesso: {(sucessos/total_conteudos_corrigir)*100:.1f}%")
        
        # Salvar dados da correcao
        dados_correcao_restante = {
            "data_correcao": datetime.now().isoformat(),
            "total_conteudos_para_corrigir": total_conteudos_corrigir,
            "correcoes_aplicadas": sucessos,
            "falhas_correcao": falhas,
            "percentual_sucesso": (sucessos/total_conteudos_corrigir)*100,
            "detalhes_correcoes": detalhes_correcoes_restantes
        }
        
        with open("correcao_restante_conteudos.json", "w", encoding="utf-8") as f:
            json.dump(dados_correcao_restante, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\nCORRECAO DO RESTANTE CONCLUIDA!")
        print(f"   {sucessos}/{total_conteudos_corrigir} correcoes aplicadas com sucesso")
        print(f"   {falhas} falhas na correcao")
        print(f"   Dados salvos em correcao_restante_conteudos.json")
        
        return sucessos > 0
        
    except Exception as e:
        print(f"Erro na correcao do restante dos conteudos: {e}")
        return False

def main():
    print("CORRECAO DO RESTANTE DOS CONTEUDOS")
    print("=" * 70)
    
    sucesso = corrigir_restante_conteudos()
    
    if sucesso:
        print(f"\nCORRECAO DO RESTANTE CONCLUIDA COM SUCESSO!")
        print(f"   Os conteudos restantes foram corrigidos")
        print(f"   Verificar arquivo correcao_restante_conteudos.json")
    else:
        print(f"\nERRO NA CORRECAO DO RESTANTE!")
        print(f"   Verificar configuracoes e tentar novamente")
    
    return sucesso

if __name__ == "__main__":
    main()
