import os
import json
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def verificar_conformidade_boilerplate_completa():
    """Verificação completa se todo o processo seguiu rigorosamente o boilerplate."""
    print("🔍 VERIFICAÇÃO COMPLETA DE CONFORMIDADE COM BOILERPLATE")
    print("=" * 70)
    
    # Carregar configuração
    load_dotenv()
    
    notion_token = os.getenv("NOTION_TOKEN")
    
    if not notion_token:
        print("❌ Configuração do Notion não encontrada")
        return False
    
    # Inicializar cliente Notion
    notion = Client(auth=notion_token)
    
    try:
        # Carregar dados de todas as correções
        dados_correcoes = {}
        
        # Carregar dados da primeira rodada
        try:
            with open("correcao_completa_boilerplate_100.json", "r", encoding="utf-8") as f:
                dados_correcoes["primeira_rodada"] = json.load(f)
            print("✅ Dados da primeira rodada carregados")
        except FileNotFoundError:
            print("⚠️ Arquivo da primeira rodada não encontrado")
            dados_correcoes["primeira_rodada"] = None
        
        # Carregar dados da segunda rodada
        try:
            with open("segunda_rodada_correcao_100.json", "r", encoding="utf-8") as f:
                dados_correcoes["segunda_rodada"] = json.load(f)
            print("✅ Dados da segunda rodada carregados")
        except FileNotFoundError:
            print("⚠️ Arquivo da segunda rodada não encontrado")
            dados_correcoes["segunda_rodada"] = None
        
        # Carregar dados da correção final
        try:
            with open("correcao_final_paginas_reprovadas.json", "r", encoding="utf-8") as f:
                dados_correcoes["correcao_final"] = json.load(f)
            print("✅ Dados da correção final carregados")
        except FileNotFoundError:
            print("⚠️ Arquivo da correção final não encontrado")
            dados_correcoes["correcao_final"] = None
        
        # Carregar dados da análise de sincronização
        try:
            with open("analise_completa_sincronizacao_notion.json", "r", encoding="utf-8") as f:
                dados_correcoes["sincronizacao"] = json.load(f)
            print("✅ Dados da sincronização carregados")
        except FileNotFoundError:
            print("⚠️ Arquivo da sincronização não encontrado")
            dados_correcoes["sincronizacao"] = None
        
        print(f"\n📊 VERIFICAÇÃO DE CONFORMIDADE COM BOILERPLATE:")
        print(f"   🔄 Primeira rodada: {'✅' if dados_correcoes['primeira_rodada'] else '❌'}")
        print(f"   🔄 Segunda rodada: {'✅' if dados_correcoes['segunda_rodada'] else '❌'}")
        print(f"   🔄 Correção final: {'✅' if dados_correcoes['correcao_final'] else '❌'}")
        print(f"   🔄 Sincronização: {'✅' if dados_correcoes['sincronizacao'] else '❌'}")
        
        # Consolidar todas as páginas processadas
        todas_paginas_processadas = set()
        
        if dados_correcoes["primeira_rodada"]:
            paginas_primeira = [p["page_id"] for p in dados_correcoes["primeira_rodada"]["paginas_corrigidas"]]
            todas_paginas_processadas.update(paginas_primeira)
            print(f"   📄 Primeira rodada: {len(paginas_primeira)} páginas")
        
        if dados_correcoes["segunda_rodada"]:
            paginas_segunda = [p["page_id"] for p in dados_correcoes["segunda_rodada"]["paginas_corrigidas_segunda_rodada"]]
            todas_paginas_processadas.update(paginas_segunda)
            print(f"   📄 Segunda rodada: {len(paginas_segunda)} páginas")
        
        if dados_correcoes["correcao_final"]:
            paginas_final = [p["page_id"] for p in dados_correcoes["correcao_final"]["paginas_corrigidas_final"]]
            todas_paginas_processadas.update(paginas_final)
            print(f"   📄 Correção final: {len(paginas_final)} páginas")
        
        print(f"\n📊 TOTAL DE PÁGINAS PROCESSADAS: {len(todas_paginas_processadas)}")
        
        # Verificar conformidade com boilerplate em cada página
        print(f"\n🔍 VERIFICANDO CONFORMIDADE COM BOILERPLATE...")
        
        paginas_conformes = []
        paginas_nao_conformes = []
        paginas_com_erro = []
        
        # Critérios do boilerplate (9 elementos obrigatórios)
        criterios_boilerplate = {
            "censo_escolar": "Dados do Censo Escolar 2024",
            "videos": "Vídeos educativos do YouTube",
            "fontes": "Fontes confiáveis e referências",
            "resumo_executivo": "Resumo executivo",
            "tags": "Tags e categorização",
            "conclusao": "Conclusão estruturada",
            "dados_reais": "Dados reais e estatísticas",
            "metodologia": "Metodologia e aplicabilidade",
            "qualidade": "Padrões de qualidade educacional"
        }
        
        for i, page_id in enumerate(todas_paginas_processadas):
            print(f"   🔍 Verificando página {i+1}/{len(todas_paginas_processadas)}: {page_id[:8]}...")
            
            try:
                # Buscar página no Notion
                page = notion.pages.retrieve(page_id)
                
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
                
                # Verificar cada critério do boilerplate
                conformidade_criterios = {}
                
                # 1. Censo Escolar 2024
                conformidade_criterios["censo_escolar"] = any(palavra in conteudo_texto.lower() for palavra in ["censo escolar", "2024", "inep", "estatísticas nacionais"])
                
                # 2. Vídeos educativos
                conformidade_criterios["videos"] = "youtube" in conteudo_texto.lower() and "vídeos" in conteudo_texto.lower()
                
                # 3. Fontes confiáveis
                conformidade_criterios["fontes"] = any(palavra in conteudo_texto.lower() for palavra in ["fonte:", "referência", "mec", "inep", "fnde"])
                
                # 4. Resumo executivo
                conformidade_criterios["resumo_executivo"] = any(palavra in conteudo_texto.lower() for palavra in ["resumo", "executivo", "sumário", "objetivos"])
                
                # 5. Tags e categorização
                conformidade_criterios["tags"] = "tags:" in conteudo_texto.lower() or "**tags**" in conteudo_texto.lower() or "categoria:" in conteudo_texto.lower()
                
                # 6. Conclusão
                conformidade_criterios["conclusao"] = any(palavra in conteudo_texto.lower() for palavra in ["conclusão", "conclusao", "finalizando", "próximos passos"])
                
                # 7. Dados reais
                conformidade_criterios["dados_reais"] = any(palavra in conteudo_texto.lower() for palavra in ["dados", "estatísticas", "indicadores", "métricas"])
                
                # 8. Metodologia
                conformidade_criterios["metodologia"] = any(palavra in conteudo_texto.lower() for palavra in ["metodologia", "aplicabilidade", "implementação", "processo"])
                
                # 9. Qualidade educacional
                conformidade_criterios["qualidade"] = any(palavra in conteudo_texto.lower() for palavra in ["qualidade", "educacional", "pedagógico", "gestão"])
                
                # Calcular pontuação
                total_criterios = len(conformidade_criterios)
                criterios_atingidos = sum(conformidade_criterios.values())
                percentual_conformidade = (criterios_atingidos / total_criterios) * 100
                
                # Determinar status
                if percentual_conformidade >= 80:
                    status_conformidade = "CONFORME"
                    paginas_conformes.append({
                        "page_id": page_id,
                        "titulo": page.get("properties", {}).get("title", {}).get("title", [{}])[0].get("text", {}).get("content", "Sem título"),
                        "percentual_conformidade": percentual_conformidade,
                        "criterios_atingidos": criterios_atingidos,
                        "criterios_faltando": [k for k, v in conformidade_criterios.items() if not v],
                        "conformidade_detalhada": conformidade_criterios
                    })
                    print(f"      ✅ {status_conformidade} ({percentual_conformidade:.1f}%) - {criterios_atingidos}/{total_criterios} critérios")
                else:
                    status_conformidade = "NÃO CONFORME"
                    paginas_nao_conformes.append({
                        "page_id": page_id,
                        "titulo": page.get("properties", {}).get("title", {}).get("title", [{}])[0].get("text", {}).get("content", "Sem título"),
                        "percentual_conformidade": percentual_conformidade,
                        "criterios_atingidos": criterios_atingidos,
                        "criterios_faltando": [k for k, v in conformidade_criterios.items() if not v],
                        "conformidade_detalhada": conformidade_criterios
                    })
                    print(f"      ❌ {status_conformidade} ({percentual_conformidade:.1f}%) - {criterios_atingidos}/{total_criterios} critérios")
                
            except Exception as e:
                print(f"      ⚠️ ERRO: {e}")
                paginas_com_erro.append({
                    "page_id": page_id,
                    "erro": str(e)
                })
        
        # Calcular estatísticas finais
        total_verificadas = len(todas_paginas_processadas)
        total_conformes = len(paginas_conformes)
        total_nao_conformes = len(paginas_nao_conformes)
        total_com_erro = len(paginas_com_erro)
        percentual_conformidade_geral = (total_conformes / total_verificadas * 100) if total_verificadas > 0 else 0
        
        print(f"\n📊 RESULTADOS DA VERIFICAÇÃO DE CONFORMIDADE COM BOILERPLATE:")
        print(f"   📄 Total de páginas verificadas: {total_verificadas}")
        print(f"   ✅ Páginas conformes: {total_conformes}")
        print(f"   ❌ Páginas não conformes: {total_nao_conformes}")
        print(f"   ⚠️ Páginas com erro: {total_com_erro}")
        print(f"   📊 Percentual de conformidade geral: {percentual_conformidade_geral:.1f}%")
        
        # Análise detalhada dos critérios
        print(f"\n📋 ANÁLISE DETALHADA DOS CRITÉRIOS DO BOILERPLATE:")
        
        # Contar conformidade por critério
        contador_criterios = {}
        for pagina in paginas_conformes + paginas_nao_conformes:
            for criterio, atingido in pagina["conformidade_detalhada"].items():
                if criterio not in contador_criterios:
                    contador_criterios[criterio] = {"atingido": 0, "total": 0}
                contador_criterios[criterio]["total"] += 1
                if atingido:
                    contador_criterios[criterio]["atingido"] += 1
        
        for criterio, dados in contador_criterios.items():
            percentual_criterio = (dados["atingido"] / dados["total"] * 100) if dados["total"] > 0 else 0
            nome_criterio = criterios_boilerplate.get(criterio, criterio.replace("_", " ").title())
            status_criterio = "✅" if percentual_criterio >= 80 else "❌"
            print(f"   {status_criterio} {nome_criterio}: {dados['atingido']}/{dados['total']} ({percentual_criterio:.1f}%)")
        
        # Salvar dados da verificação
        dados_verificacao = {
            "data_verificacao": datetime.now().isoformat(),
            "titulo": "VERIFICAÇÃO COMPLETA DE CONFORMIDADE COM BOILERPLATE",
            "total_paginas_verificadas": total_verificadas,
            "total_conformes": total_conformes,
            "total_nao_conformes": total_nao_conformes,
            "total_com_erro": total_com_erro,
            "percentual_conformidade_geral": percentual_conformidade_geral,
            "criterios_boilerplate": criterios_boilerplate,
            "analise_criterios": contador_criterios,
            "paginas_conformes": paginas_conformes,
            "paginas_nao_conformes": paginas_nao_conformes,
            "paginas_com_erro": paginas_com_erro
        }
        
        with open("verificacao_boilerplate_completa.json", "w", encoding="utf-8") as f:
            json.dump(dados_verificacao, f, indent=2, ensure_ascii=False, default=str)
        
        # Determinar se o processo seguiu o boilerplate
        if percentual_conformidade_geral >= 80:
            print(f"\n✅ RESULTADO FINAL: O PROCESSO SEGUIU RIGOROSAMENTE O BOILERPLATE!")
            print(f"   📊 {percentual_conformidade_geral:.1f}% de conformidade geral")
            print(f"   ✅ {total_conformes} páginas conformes com boilerplate")
            print(f"   🎯 Padrões de qualidade educacional mantidos")
            return True
        else:
            print(f"\n❌ RESULTADO FINAL: O PROCESSO NÃO SEGUIU COMPLETAMENTE O BOILERPLATE!")
            print(f"   📊 {percentual_conformidade_geral:.1f}% de conformidade geral")
            print(f"   ❌ {total_nao_conformes} páginas não conformes")
            print(f"   ⚠️ Necessário ajustes para atingir 80% de conformidade")
            return False
        
    except Exception as e:
        print(f"❌ Erro na verificação de conformidade: {e}")
        return False

def main():
    print("🔍 VERIFICAÇÃO COMPLETA DE CONFORMIDADE COM BOILERPLATE")
    print("=" * 70)
    print("📋 Verificando se todo o processo seguiu rigorosamente o boilerplate")
    print("=" * 70)
    
    sucesso = verificar_conformidade_boilerplate_completa()
    
    if sucesso:
        print(f"\n✅ VERIFICAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"   🔍 Conformidade com boilerplate verificada")
        print(f"   ✅ Processo seguiu rigorosamente os padrões")
        print(f"   💾 Dados da verificação salvos")
    else:
        print(f"\n❌ VERIFICAÇÃO REVELOU NÃO CONFORMIDADES")
        print(f"   🔧 Ajustes necessários identificados")
        print(f"   📋 Revisar implementação do boilerplate")
        print(f"   💾 Dados da verificação salvos")
    
    return sucesso

if __name__ == "__main__":
    main()

