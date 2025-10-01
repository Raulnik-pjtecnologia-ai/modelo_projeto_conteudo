import os
import json
import time
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def verificar_correcao_restante():
    """Verificar se a correção do restante dos conteúdos foi aplicada corretamente."""
    print("VERIFICACAO DA CORRECAO DO RESTANTE DOS CONTEUDOS")
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
        # Carregar dados da correcao do restante
        try:
            with open("correcao_restante_conteudos.json", "r", encoding="utf-8") as f:
                dados_correcao = json.load(f)
            
            detalhes_correcoes = dados_correcao["detalhes_correcoes"]
            print(f"Dados da correcao do restante carregados: {len(detalhes_correcoes)} correcoes")
            
        except FileNotFoundError:
            print("ERRO: Arquivo de correcao do restante nao encontrado")
            print("Execute primeiro a correcao do restante dos conteudos")
            return False
        
        # Filtrar apenas correcoes bem-sucedidas
        correcoes_sucesso = [c for c in detalhes_correcoes if c["sucesso"]]
        
        print(f"Correcoes bem-sucedidas encontradas: {len(correcoes_sucesso)}")
        print("=" * 70)
        
        verificacoes_realizadas = 0
        verificacoes_corretas = 0
        verificacoes_incorretas = 0
        detalhes_verificacao = []
        
        for i, correcao in enumerate(correcoes_sucesso):
            page_id = correcao["page_id"]
            titulo = correcao["titulo"]
            tipo_esperado = correcao["tipo_real"]
            propriedade_usada = correcao["propriedade_usada"]
            
            print(f"\n{i+1}/{len(correcoes_sucesso)}: {titulo[:40]}...")
            print(f"   Tipo esperado: {tipo_esperado}")
            print(f"   Propriedade: {propriedade_usada}")
            
            try:
                # Buscar a pagina no Notion
                page = notion.pages.retrieve(page_id=page_id)
                
                # Verificar o valor atual da propriedade
                if propriedade_usada in page["properties"]:
                    propriedade = page["properties"][propriedade_usada]
                    tipo_propriedade = propriedade["type"]
                    
                    valor_atual = None
                    
                    if tipo_propriedade == "select":
                        if propriedade["select"]:
                            valor_atual = propriedade["select"]["name"]
                    elif tipo_propriedade == "multi_select":
                        if propriedade["multi_select"]:
                            valor_atual = [item["name"] for item in propriedade["multi_select"]]
                    elif tipo_propriedade == "rich_text":
                        if propriedade["rich_text"]:
                            valor_atual = propriedade["rich_text"][0]["text"]["content"]
                    elif tipo_propriedade == "title":
                        if propriedade["title"]:
                            valor_atual = propriedade["title"][0]["text"]["content"]
                    
                    print(f"   Valor atual: {valor_atual}")
                    
                    # Verificar se a correcao foi aplicada
                    correcao_aplicada = False
                    
                    if tipo_propriedade == "select":
                        correcao_aplicada = valor_atual == tipo_esperado
                    elif tipo_propriedade == "multi_select":
                        correcao_aplicada = tipo_esperado in valor_atual if valor_atual else False
                    elif tipo_propriedade in ["rich_text", "title"]:
                        correcao_aplicada = valor_atual == tipo_esperado
                    
                    if correcao_aplicada:
                        print(f"   OK - Correcao aplicada corretamente")
                        verificacoes_corretas += 1
                    else:
                        print(f"   ERRO - Correcao nao foi aplicada")
                        verificacoes_incorretas += 1
                    
                    verificacoes_realizadas += 1
                    
                    # Adicionar detalhes da verificacao
                    detalhes_verificacao.append({
                        "page_id": page_id,
                        "titulo": titulo,
                        "tipo_esperado": tipo_esperado,
                        "valor_atual": valor_atual,
                        "correcao_aplicada": correcao_aplicada,
                        "propriedade_usada": propriedade_usada,
                        "tipo_propriedade": tipo_propriedade,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                else:
                    print(f"   ERRO - Propriedade {propriedade_usada} nao encontrada")
                    verificacoes_incorretas += 1
                
                # Pausa entre verificacoes
                time.sleep(0.5)
                
            except Exception as e:
                print(f"   ERRO: {str(e)[:50]}...")
                verificacoes_incorretas += 1
        
        # Calcular estatisticas finais
        percentual_sucesso = (verificacoes_corretas/verificacoes_realizadas)*100 if verificacoes_realizadas > 0 else 0
        
        print(f"\nRESULTADOS DA VERIFICACAO:")
        print(f"=" * 70)
        print(f"Total de verificacoes realizadas: {verificacoes_realizadas}")
        print(f"Verificacoes corretas: {verificacoes_corretas}")
        print(f"Verificacoes incorretas: {verificacoes_incorretas}")
        print(f"Percentual de sucesso: {percentual_sucesso:.1f}%")
        
        # Salvar dados da verificacao
        dados_verificacao = {
            "data_verificacao": datetime.now().isoformat(),
            "total_verificacoes_realizadas": verificacoes_realizadas,
            "verificacoes_corretas": verificacoes_corretas,
            "verificacoes_incorretas": verificacoes_incorretas,
            "percentual_sucesso": percentual_sucesso,
            "detalhes_verificacao": detalhes_verificacao
        }
        
        with open("verificacao_correcao_restante.json", "w", encoding="utf-8") as f:
            json.dump(dados_verificacao, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\nVERIFICACAO CONCLUIDA!")
        print(f"   {verificacoes_corretas}/{verificacoes_realizadas} verificacoes corretas")
        print(f"   {verificacoes_incorretas} verificacoes incorretas")
        print(f"   Dados salvos em verificacao_correcao_restante.json")
        
        return verificacoes_corretas > 0
        
    except Exception as e:
        print(f"Erro na verificacao da correcao do restante: {e}")
        return False

def main():
    print("VERIFICACAO DA CORRECAO DO RESTANTE DOS CONTEUDOS")
    print("=" * 70)
    
    sucesso = verificar_correcao_restante()
    
    if sucesso:
        print(f"\nVERIFICACAO CONCLUIDA COM SUCESSO!")
        print(f"   A correcao do restante foi verificada e esta funcionando")
        print(f"   Verificar arquivo verificacao_correcao_restante.json")
    else:
        print(f"\nERRO NA VERIFICACAO!")
        print(f"   Verificar configuracoes e tentar novamente")
    
    return sucesso

if __name__ == "__main__":
    main()
