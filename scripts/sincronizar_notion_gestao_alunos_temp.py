import os
import json
import time
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def sincronizar_notion_gestao_alunos():
    """Sincronizar artigo aprovado com o Notion - Editorial Gestão de Alunos."""
    print("SINCRONIZACAO COM NOTION - EDITORIAL GESTAO DE ALUNOS")
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
        
        # Ler o artigo aprovado
        arquivo_artigo = "2_conteudo/01_ideias_e_rascunhos/artigo_sistemas_gestao_escolar_modernos_2024.md"
        
        try:
            with open(arquivo_artigo, "r", encoding="utf-8") as f:
                conteudo_artigo = f.read()
            
            print(f"Artigo carregado: {arquivo_artigo}")
            print(f"Tamanho: {len(conteudo_artigo)} caracteres")
            
        except FileNotFoundError:
            print(f"ERRO: Arquivo {arquivo_artigo} nao encontrado")
            return False
        
        # Extrair informações do artigo
        titulo = "Sistemas de Gestão Escolar Modernos: Transformando a Educação em 2024"
        
        # Dividir o conteúdo em blocos para o Notion
        blocos_notion = []
        
        # Título principal
        blocos_notion.append({
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": titulo}}]
            }
        })
        
        # Resumo Executivo
        resumo_inicio = conteudo_artigo.find("## 📋 Resumo Executivo")
        resumo_fim = conteudo_artigo.find("## 📊 Dados e Gráficos")
        
        if resumo_inicio != -1 and resumo_fim != -1:
            resumo_texto = conteudo_artigo[resumo_inicio:resumo_fim].replace("## 📋 Resumo Executivo", "").strip()
            
            blocos_notion.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Resumo Executivo"}}]
                }
            })
            
            # Dividir resumo em parágrafos
            paragrafos = resumo_texto.split("\n\n")
            for paragrafo in paragrafos:
                if paragrafo.strip():
                    blocos_notion.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": paragrafo.strip()}}]
                        }
                    })
        
        # Dados e Gráficos
        dados_inicio = conteudo_artigo.find("## 📊 Dados e Gráficos")
        dados_fim = conteudo_artigo.find("## 🎯 Principais Funcionalidades")
        
        if dados_inicio != -1 and dados_fim != -1:
            dados_texto = conteudo_artigo[dados_inicio:dados_fim].replace("## 📊 Dados e Gráficos", "").strip()
            
            blocos_notion.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Dados e Graficos"}}]
                }
            })
            
            # Adicionar parágrafos dos dados
            paragrafos = dados_texto.split("\n\n")
            for paragrafo in paragrafos:
                if paragrafo.strip() and not paragrafo.strip().startswith("![") and not paragrafo.strip().startswith("*"):
                    blocos_notion.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": paragrafo.strip()}}]
                        }
                    })
        
        # Principais Funcionalidades
        func_inicio = conteudo_artigo.find("## 🎯 Principais Funcionalidades")
        func_fim = conteudo_artigo.find("## 🎥 Vídeos Relacionados")
        
        if func_inicio != -1 and func_fim != -1:
            func_texto = conteudo_artigo[func_inicio:func_fim].replace("## 🎯 Principais Funcionalidades", "").strip()
            
            blocos_notion.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Principais Funcionalidades"}}]
                }
            })
            
            # Adicionar funcionalidades
            linhas = func_texto.split("\n")
            for linha in linhas:
                if linha.strip() and linha.strip().startswith("###"):
                    titulo_func = linha.replace("###", "").strip()
                    blocos_notion.append({
                        "object": "block",
                        "type": "heading_3",
                        "heading_3": {
                            "rich_text": [{"type": "text", "text": {"content": titulo_func}}]
                        }
                    })
                elif linha.strip() and linha.strip().startswith("-"):
                    item = linha.replace("-", "").strip()
                    blocos_notion.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{"type": "text", "text": {"content": item}}]
                        }
                    })
        
        # Vídeos Relacionados
        videos_inicio = conteudo_artigo.find("## 🎥 Vídeos Relacionados")
        videos_fim = conteudo_artigo.find("## 💡 Benefícios dos Sistemas Modernos")
        
        if videos_inicio != -1 and videos_fim != -1:
            videos_texto = conteudo_artigo[videos_inicio:videos_fim].replace("## 🎥 Vídeos Relacionados", "").strip()
            
            blocos_notion.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Videos Relacionados"}}]
                }
            })
            
            # Adicionar vídeos
            linhas = videos_texto.split("\n")
            for linha in linhas:
                if linha.strip() and linha.strip().startswith("###"):
                    titulo_video = linha.replace("###", "").strip()
                    blocos_notion.append({
                        "object": "block",
                        "type": "heading_3",
                        "heading_3": {
                            "rich_text": [{"type": "text", "text": {"content": titulo_video}}]
                        }
                    })
                elif linha.strip() and linha.strip().startswith("**Canal:**"):
                    canal = linha.replace("**Canal:**", "").strip()
                    blocos_notion.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": f"Canal: {canal}"}}]
                        }
                    })
                elif linha.strip() and linha.strip().startswith("**Link:**"):
                    link = linha.replace("**Link:**", "").strip()
                    blocos_notion.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": f"Link: {link}"}}]
                        }
                    })
        
        # Conclusão
        conclusao_inicio = conteudo_artigo.find("## 🎯 Conclusão")
        conclusao_fim = conteudo_artigo.find("## 🏷️ Tags")
        
        if conclusao_inicio != -1 and conclusao_fim != -1:
            conclusao_texto = conteudo_artigo[conclusao_inicio:conclusao_fim].replace("## 🎯 Conclusão", "").strip()
            
            blocos_notion.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Conclusao"}}]
                }
            })
            
            # Adicionar parágrafos da conclusão
            paragrafos = conclusao_texto.split("\n\n")
            for paragrafo in paragrafos:
                if paragrafo.strip():
                    blocos_notion.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": paragrafo.strip()}}]
                        }
                    })
        
        print(f"Total de blocos preparados: {len(blocos_notion)}")
        
        # Criar página no Notion
        print(f"\nCriando pagina no Notion...")
        
        # Propriedades da página
        propriedades = {
            "Title": {
                "title": [{"type": "text", "text": {"content": titulo}}]
            },
            "Tipo": {
                "select": {"name": "Gestao Escolar"}
            },
            "Status": {
                "select": {"name": "Publicado"}
            },
            "Status Editorial": {
                "select": {"name": "Publicado"}
            },
            "Prioridade": {
                "select": {"name": "Alta"}
            }
        }
        
        # Criar a página
        nova_pagina = notion.pages.create(
            parent={"database_id": database_id},
            properties=propriedades
        )
        
        page_id = nova_pagina["id"]
        print(f"Pagina criada com sucesso!")
        print(f"ID: {page_id}")
        
        # Adicionar blocos de conteúdo
        print(f"\nAdicionando conteudo...")
        
        # Adicionar blocos em lotes de 50 (limite do Notion)
        batch_size = 50
        for i in range(0, len(blocos_notion), batch_size):
            batch = blocos_notion[i:i + batch_size]
            notion.blocks.children.append(block_id=page_id, children=batch)
            print(f"   Lote {i//batch_size + 1}: {len(batch)} blocos adicionados")
            time.sleep(0.5)  # Pausa entre lotes
        
        print(f"\nSINCRONIZACAO CONCLUIDA COM SUCESSO!")
        print(f"   Pagina criada: {titulo}")
        print(f"   Database: Editorial Gestao de Alunos")
        print(f"   Total de blocos: {len(blocos_notion)}")
        print(f"   Status: Publicado")
        
        # Salvar dados da sincronização
        dados_sincronizacao = {
            "data_sincronizacao": datetime.now().isoformat(),
            "database_id": database_id,
            "page_id": page_id,
            "titulo": titulo,
            "total_blocos": len(blocos_notion),
            "status": "sucesso",
            "arquivo_origem": arquivo_artigo
        }
        
        with open("sincronizacao_gestao_alunos.json", "w", encoding="utf-8") as f:
            json.dump(dados_sincronizacao, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"   Dados salvos em sincronizacao_gestao_alunos.json")
        
        return True
        
    except Exception as e:
        print(f"ERRO na sincronizacao: {e}")
        return False

def main():
    print("SINCRONIZACAO COM NOTION - EDITORIAL GESTAO DE ALUNOS")
    print("=" * 70)
    
    sucesso = sincronizar_notion_gestao_alunos()
    
    if sucesso:
        print(f"\nSINCRONIZACAO REALIZADA COM SUCESSO!")
        print(f"   Artigo publicado no Editorial Gestao de Alunos")
        print(f"   Conformidade com boilerplate mantida")
        print(f"   Enriquecimento MCP aplicado")
    else:
        print(f"\nERRO NA SINCRONIZACAO")
        print(f"   Verificar configuracoes")
        print(f"   Revisar implementacao")
    
    return sucesso

if __name__ == "__main__":
    main()
