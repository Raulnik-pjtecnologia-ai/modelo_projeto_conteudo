import os
import json
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def verificar_conformidade_boilerplate():
    """BLOCO 3: Verificar conformidade com boilerplate das páginas de gestão."""
    print("🔍 BLOCO 3: VERIFICANDO CONFORMIDADE COM BOILERPLATE")
    print("=" * 60)
    
    # Carregar configuração
    load_dotenv()
    
    notion_token = os.getenv("NOTION_TOKEN")
    
    if not notion_token:
        print("❌ Configuração do Notion não encontrada")
        return False
    
    # Inicializar cliente Notion
    notion = Client(auth=notion_token)
    
    try:
        # Carregar dados do bloco 2
        with open("dados_analise_bloco2_editorial_gestao.json", "r", encoding="utf-8") as f:
            dados_bloco2 = json.load(f)
        
        paginas_gestao = dados_bloco2["paginas_gestao_detalhadas"]
        
        print(f"📊 Verificando conformidade de {len(paginas_gestao)} páginas de gestão...")
        
        # Critérios do boilerplate para verificar
        criterios_boilerplate = [
            "Capa com título e data",
            "Resumo executivo",
            "Dados do Censo Escolar 2024",
            "Vídeos educativos do YouTube",
            "Fontes confiáveis",
            "Conclusão",
            "Tags apropriadas",
            "Categoria correta",
            "Nível de função"
        ]
        
        paginas_analisadas = []
        paginas_conformes = []
        paginas_nao_conformes = []
        
        for i, pagina in enumerate(paginas_gestao):
            page_id = pagina["page_id"]
            titulo = pagina["titulo"]
            
            print(f"\n📋 Analisando: {titulo[:50]}...")
            
            try:
                # Buscar blocos da página
                blocks_response = notion.blocks.children.list(page_id)
                blocks = blocks_response.get("results", [])
                
                # Converter blocos para texto para análise
                conteudo_texto = ""
                for block in blocks:
                    if block.get("type") in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item"]:
                        rich_text = block.get(block["type"], {}).get("rich_text", [])
                        if rich_text:
                            texto_bloco = "".join([rt["text"]["content"] for rt in rich_text])
                            conteudo_texto += texto_bloco + "\n"
                
                # Verificar cada critério
                verificacoes = {}
                
                # 1. Capa com título e data
                verificacoes["capa"] = bool(titulo and len(titulo) > 10)
                
                # 2. Resumo executivo
                verificacoes["resumo_executivo"] = any(palavra in conteudo_texto.lower() 
                                                     for palavra in ["resumo", "executivo", "sumário"])
                
                # 3. Dados do Censo Escolar 2024
                verificacoes["censo_escolar"] = any(palavra in conteudo_texto.lower() 
                                                  for palavra in ["censo escolar", "2024", "inep", "dados"])
                
                # 4. Vídeos educativos do YouTube
                verificacoes["videos_youtube"] = "youtube" in conteudo_texto.lower() or "watch?v=" in conteudo_texto.lower()
                
                # 5. Fontes confiáveis
                verificacoes["fontes"] = any(palavra in conteudo_texto.lower() 
                                           for palavra in ["fonte:", "referência", "bibliografia", "link"])
                
                # 6. Conclusão
                verificacoes["conclusao"] = any(palavra in conteudo_texto.lower() 
                                              for palavra in ["conclusão", "conclusao", "finalizando", "considerações"])
                
                # 7. Tags apropriadas
                verificacoes["tags"] = "tags:" in conteudo_texto.lower() or "**tags**" in conteudo_texto.lower()
                
                # 8. Categoria correta
                verificacoes["categoria"] = any(palavra in conteudo_texto.lower() 
                                              for palavra in ["categoria:", "**categoria**", "gestão", "escolar"])
                
                # 9. Nível de função
                verificacoes["nivel_funcao"] = any(palavra in conteudo_texto.lower() 
                                                 for palavra in ["nível:", "**nível**", "diretor", "coordenador", "gestor"])
                
                # Calcular pontuação
                pontuacao = sum(1 for v in verificacoes.values() if v)
                total_criterios = len(verificacoes)
                percentual = (pontuacao / total_criterios) * 100
                
                # Determinar se está conforme
                conforme = percentual >= 70  # 70% de conformidade
                
                pagina_analisada = {
                    "page_id": page_id,
                    "titulo": titulo,
                    "verificacoes": verificacoes,
                    "pontuacao": pontuacao,
                    "total_criterios": total_criterios,
                    "percentual": percentual,
                    "conforme": conforme
                }
                
                paginas_analisadas.append(pagina_analisada)
                
                if conforme:
                    paginas_conformes.append(pagina_analisada)
                    print(f"   ✅ CONFORME ({percentual:.1f}%) - {pontuacao}/{total_criterios} critérios")
                else:
                    paginas_nao_conformes.append(pagina_analisada)
                    print(f"   ❌ NÃO CONFORME ({percentual:.1f}%) - {pontuacao}/{total_criterios} critérios")
                
                # Progresso
                if (i + 1) % 5 == 0:
                    print(f"   📊 Progresso: {i + 1}/{len(paginas_gestao)} páginas analisadas")
                
            except Exception as e:
                print(f"   ⚠️ Erro ao analisar página {page_id}: {e}")
                # Adicionar página com erro
                pagina_erro = {
                    "page_id": page_id,
                    "titulo": titulo,
                    "erro": str(e),
                    "conforme": False
                }
                paginas_analisadas.append(pagina_erro)
                paginas_nao_conformes.append(pagina_erro)
        
        # Calcular estatísticas
        total_analisadas = len(paginas_analisadas)
        total_conformes = len(paginas_conformes)
        total_nao_conformes = len(paginas_nao_conformes)
        percentual_geral = (total_conformes / total_analisadas * 100) if total_analisadas > 0 else 0
        
        # Salvar dados do bloco 3
        dados_bloco3 = {
            "data_analise": datetime.now().isoformat(),
            "bloco": 3,
            "total_paginas_analisadas": total_analisadas,
            "total_conformes": total_conformes,
            "total_nao_conformes": total_nao_conformes,
            "percentual_geral_conformidade": percentual_geral,
            "criterios_boilerplate": criterios_boilerplate,
            "paginas_analisadas": paginas_analisadas,
            "paginas_conformes": paginas_conformes,
            "paginas_nao_conformes": paginas_nao_conformes
        }
        
        with open("dados_analise_bloco3_editorial_gestao.json", "w", encoding="utf-8") as f:
            json.dump(dados_bloco3, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n📊 RESUMO BLOCO 3:")
        print(f"   📄 Total de páginas analisadas: {total_analisadas}")
        print(f"   ✅ Páginas conformes: {total_conformes}")
        print(f"   ❌ Páginas não conformes: {total_nao_conformes}")
        print(f"   📊 Percentual geral de conformidade: {percentual_geral:.1f}%")
        print(f"   💾 Dados salvos: dados_analise_bloco3_editorial_gestao.json")
        
        if paginas_nao_conformes:
            print(f"\n❌ PÁGINAS NÃO CONFORMES (precisam correção):")
            for i, pagina in enumerate(paginas_nao_conformes[:10], 1):
                if "erro" not in pagina:
                    print(f"   {i}. {pagina['titulo'][:60]}... ({pagina['percentual']:.1f}%)")
                else:
                    print(f"   {i}. {pagina['titulo'][:60]}... (ERRO)")
            if len(paginas_nao_conformes) > 10:
                print(f"   ... e mais {len(paginas_nao_conformes) - 10} páginas não conformes")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no Bloco 3: {e}")
        return False

def main():
    print("🔍 ANÁLISE EDITORIAL DE GESTÃO - BLOCO 3")
    print("======================================================================")
    print("📋 Verificando conformidade com boilerplate")
    print("======================================================================")
    
    sucesso = verificar_conformidade_boilerplate()
    
    if sucesso:
        print(f"\n✅ BLOCO 3 CONCLUÍDO COM SUCESSO!")
        print(f"   📊 Conformidade verificada")
        print(f"   ✅ Páginas conformes identificadas")
        print(f"   ❌ Páginas não conformes identificadas")
        print(f"   💾 Dados salvos para próximos blocos")
    else:
        print(f"\n❌ ERRO NO BLOCO 3")
        print(f"   🔧 Verificar configuração")
        print(f"   📋 Revisar processo")
    
    return sucesso

if __name__ == "__main__":
    main()
