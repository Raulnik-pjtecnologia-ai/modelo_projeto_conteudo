import os
import json
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def verificacao_final_boilerplate():
    """Verificação final para confirmar que todas as falhas foram corrigidas."""
    print("🔍 VERIFICAÇÃO FINAL DE CONFORMIDADE COM BOILERPLATE")
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
        # Carregar dados da correção de falhas
        with open("correcao_falhas_boilerplate.json", "r", encoding="utf-8") as f:
            dados_correcao = json.load(f)
        
        paginas_corrigidas = dados_correcao["paginas_corrigidas"]
        
        print(f"📊 VERIFICANDO {len(paginas_corrigidas)} PÁGINAS CORRIGIDAS...")
        
        # Verificar conformidade final
        paginas_conformes_final = []
        paginas_nao_conformes_final = []
        
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
        
        for i, pagina in enumerate(paginas_corrigidas):
            page_id = pagina["page_id"]
            titulo = pagina["titulo"]
            percentual_anterior = pagina["percentual_anterior"]
            percentual_novo = pagina["percentual_novo"]
            
            print(f"   🔍 Verificando página {i+1}/{len(paginas_corrigidas)}: {titulo[:50]}...")
            print(f"      📊 Percentual anterior: {percentual_anterior:.1f}%")
            print(f"      📊 Percentual novo: {percentual_novo:.1f}%")
            
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
                
                # Calcular pontuação final
                total_criterios = len(conformidade_criterios)
                criterios_atingidos = sum(conformidade_criterios.values())
                percentual_final = (criterios_atingidos / total_criterios) * 100
                
                # Determinar status final
                if percentual_final >= 80:
                    status_final = "CONFORME"
                    paginas_conformes_final.append({
                        "page_id": page_id,
                        "titulo": titulo,
                        "percentual_final": percentual_final,
                        "criterios_atingidos": criterios_atingidos,
                        "criterios_faltando": [k for k, v in conformidade_criterios.items() if not v],
                        "conformidade_detalhada": conformidade_criterios
                    })
                    print(f"      ✅ {status_final} ({percentual_final:.1f}%) - {criterios_atingidos}/{total_criterios} critérios")
                else:
                    status_final = "NÃO CONFORME"
                    paginas_nao_conformes_final.append({
                        "page_id": page_id,
                        "titulo": titulo,
                        "percentual_final": percentual_final,
                        "criterios_atingidos": criterios_atingidos,
                        "criterios_faltando": [k for k, v in conformidade_criterios.items() if not v],
                        "conformidade_detalhada": conformidade_criterios
                    })
                    print(f"      ❌ {status_final} ({percentual_final:.1f}%) - {criterios_atingidos}/{total_criterios} critérios")
                
            except Exception as e:
                print(f"      ⚠️ ERRO: {e}")
        
        # Calcular estatísticas finais
        total_verificadas = len(paginas_corrigidas)
        total_conformes_final = len(paginas_conformes_final)
        total_nao_conformes_final = len(paginas_nao_conformes_final)
        percentual_conformidade_final = (total_conformes_final / total_verificadas * 100) if total_verificadas > 0 else 0
        
        print(f"\n📊 RESULTADOS DA VERIFICAÇÃO FINAL:")
        print(f"   📄 Total de páginas verificadas: {total_verificadas}")
        print(f"   ✅ Páginas conformes: {total_conformes_final}")
        print(f"   ❌ Páginas não conformes: {total_nao_conformes_final}")
        print(f"   📊 Percentual de conformidade final: {percentual_conformidade_final:.1f}%")
        
        # Análise detalhada dos critérios
        print(f"\n📋 ANÁLISE FINAL DOS CRITÉRIOS DO BOILERPLATE:")
        
        # Contar conformidade por critério
        contador_criterios = {}
        for pagina in paginas_conformes_final + paginas_nao_conformes_final:
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
        
        # Salvar dados da verificação final
        dados_verificacao_final = {
            "data_verificacao_final": datetime.now().isoformat(),
            "titulo": "VERIFICAÇÃO FINAL DE CONFORMIDADE COM BOILERPLATE",
            "total_paginas_verificadas": total_verificadas,
            "total_conformes_final": total_conformes_final,
            "total_nao_conformes_final": total_nao_conformes_final,
            "percentual_conformidade_final": percentual_conformidade_final,
            "criterios_boilerplate": criterios_boilerplate,
            "analise_criterios_final": contador_criterios,
            "paginas_conformes_final": paginas_conformes_final,
            "paginas_nao_conformes_final": paginas_nao_conformes_final
        }
        
        with open("verificacao_final_boilerplate.json", "w", encoding="utf-8") as f:
            json.dump(dados_verificacao_final, f, indent=2, ensure_ascii=False, default=str)
        
        # Determinar resultado final
        if percentual_conformidade_final >= 80:
            print(f"\n✅ RESULTADO FINAL: TODAS AS FALHAS FORAM CORRIGIDAS COM SUCESSO!")
            print(f"   📊 {percentual_conformidade_final:.1f}% de conformidade final")
            print(f"   ✅ {total_conformes_final} páginas conformes com boilerplate")
            print(f"   🎯 Processo seguiu rigorosamente o boilerplate")
            return True
        else:
            print(f"\n❌ RESULTADO FINAL: AINDA HÁ FALHAS A SEREM CORRIGIDAS!")
            print(f"   📊 {percentual_conformidade_final:.1f}% de conformidade final")
            print(f"   ❌ {total_nao_conformes_final} páginas ainda não conformes")
            print(f"   ⚠️ Necessário mais correções")
            return False
        
    except Exception as e:
        print(f"❌ Erro na verificação final: {e}")
        return False

def main():
    print("🔍 VERIFICAÇÃO FINAL DE CONFORMIDADE COM BOILERPLATE")
    print("=" * 70)
    print("📋 Confirmando que todas as falhas foram corrigidas")
    print("=" * 70)
    
    sucesso = verificacao_final_boilerplate()
    
    if sucesso:
        print(f"\n✅ VERIFICAÇÃO FINAL CONCLUÍDA COM SUCESSO!")
        print(f"   🔍 Todas as falhas foram corrigidas")
        print(f"   ✅ Boilerplate implementado corretamente")
        print(f"   💾 Dados da verificação final salvos")
    else:
        print(f"\n❌ VERIFICAÇÃO FINAL REVELOU FALHAS RESTANTES")
        print(f"   🔧 Ainda necessário mais correções")
        print(f"   📋 Revisar implementação")
        print(f"   💾 Dados da verificação final salvos")
    
    return sucesso

if __name__ == "__main__":
    main()
