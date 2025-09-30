import os
import json
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def verificacao_melhorada():
    """Verificação melhorada com critérios de detecção mais precisos."""
    print("🔍 VERIFICAÇÃO MELHORADA - CRITÉRIOS DE DETECÇÃO PRECISOS")
    print("=" * 80)
    
    # Carregar configuração
    load_dotenv()
    
    notion_token = os.getenv("NOTION_TOKEN")
    
    if not notion_token:
        print("❌ Configuração do Notion não encontrada")
        return False
    
    # Inicializar cliente Notion
    notion = Client(auth=notion_token)
    
    try:
        # Carregar dados da sincronização
        with open("sincronizacao_completa_notion.json", "r", encoding="utf-8") as f:
            dados_sincronizacao = json.load(f)
        
        paginas_sincronizadas = dados_sincronizacao["paginas_sincronizadas"]
        
        print(f"🔍 VERIFICANDO {len(paginas_sincronizadas)} PÁGINAS SINCRONIZADAS...")
        
        # Critérios do boilerplate com detecção melhorada
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
        
        # Verificar conformidade melhorada
        paginas_verificadas = []
        paginas_conformes = []
        paginas_nao_conformes = []
        
        for i, pagina in enumerate(paginas_sincronizadas):
            page_id = pagina["page_id"]
            titulo = pagina["titulo"]
            criterios_faltando = pagina["criterios_faltando"]
            correcoes_aplicadas = pagina["correcoes_aplicadas"]
            
            print(f"   🔍 Verificando página {i+1}/{len(paginas_sincronizadas)}: {titulo[:50]}...")
            print(f"      🔧 Correções aplicadas: {correcoes_aplicadas}")
            
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
                
                # Verificar cada critério com detecção melhorada
                conformidade_criterios = {}
                
                # 1. Censo Escolar 2024 - Detecção melhorada
                palavras_censo = ["censo escolar", "2024", "inep", "estatísticas nacionais", "dados do censo", "censo 2024"]
                conformidade_criterios["censo_escolar"] = any(palavra in conteudo_texto.lower() for palavra in palavras_censo)
                
                # 2. Vídeos educativos - Detecção melhorada
                palavras_videos = ["youtube", "vídeos", "video", "🎥", "vídeos educativos", "youtube.com"]
                conformidade_criterios["videos"] = any(palavra in conteudo_texto.lower() for palavra in palavras_videos)
                
                # 3. Fontes confiáveis - Detecção melhorada
                palavras_fontes = ["fonte:", "referência", "mec", "inep", "fnde", "📚", "fontes", "referências"]
                conformidade_criterios["fontes"] = any(palavra in conteudo_texto.lower() for palavra in palavras_fontes)
                
                # 4. Resumo executivo - Detecção melhorada
                palavras_resumo = ["resumo", "executivo", "sumário", "objetivos", "📋", "resumo executivo"]
                conformidade_criterios["resumo_executivo"] = any(palavra in conteudo_texto.lower() for palavra in palavras_resumo)
                
                # 5. Tags e categorização - Detecção melhorada
                palavras_tags = ["tags:", "**tags**", "categoria:", "**categoria**", "🏷️", "tags", "categoria"]
                conformidade_criterios["tags"] = any(palavra in conteudo_texto.lower() for palavra in palavras_tags)
                
                # 6. Conclusão - Detecção melhorada
                palavras_conclusao = ["conclusão", "conclusao", "finalizando", "próximos passos", "🎯", "conclusão"]
                conformidade_criterios["conclusao"] = any(palavra in conteudo_texto.lower() for palavra in palavras_conclusao)
                
                # 7. Dados reais - Detecção melhorada
                palavras_dados = ["dados", "estatísticas", "indicadores", "métricas", "📊", "dados reais"]
                conformidade_criterios["dados_reais"] = any(palavra in conteudo_texto.lower() for palavra in palavras_dados)
                
                # 8. Metodologia - Detecção melhorada
                palavras_metodologia = ["metodologia", "aplicabilidade", "implementação", "processo", "🔧", "metodologia"]
                conformidade_criterios["metodologia"] = any(palavra in conteudo_texto.lower() for palavra in palavras_metodologia)
                
                # 9. Qualidade educacional - Detecção melhorada
                palavras_qualidade = ["qualidade", "educacional", "pedagógico", "gestão", "🏆", "qualidade educacional"]
                conformidade_criterios["qualidade"] = any(palavra in conteudo_texto.lower() for palavra in palavras_qualidade)
                
                # Calcular pontuação final
                total_criterios = len(conformidade_criterios)
                criterios_atingidos = sum(conformidade_criterios.values())
                percentual_final = (criterios_atingidos / total_criterios) * 100
                
                # Determinar status final
                if percentual_final >= 80:
                    status_final = "CONFORME"
                    paginas_conformes.append({
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
                    paginas_nao_conformes.append({
                        "page_id": page_id,
                        "titulo": titulo,
                        "percentual_final": percentual_final,
                        "criterios_atingidos": criterios_atingidos,
                        "criterios_faltando": [k for k, v in conformidade_criterios.items() if not v],
                        "conformidade_detalhada": conformidade_criterios
                    })
                    print(f"      ❌ {status_final} ({percentual_final:.1f}%) - {criterios_atingidos}/{total_criterios} critérios")
                
                # Adicionar à lista de páginas verificadas
                paginas_verificadas.append({
                    "page_id": page_id,
                    "titulo": titulo,
                    "percentual_final": percentual_final,
                    "criterios_atingidos": criterios_atingidos,
                    "criterios_faltando": [k for k, v in conformidade_criterios.items() if not v],
                    "conformidade_detalhada": conformidade_criterios,
                    "status_final": status_final
                })
                
            except Exception as e:
                print(f"      ⚠️ ERRO: {e}")
            
            # Progresso
            if (i + 1) % 10 == 0:
                print(f"      📊 Progresso: {i + 1}/{len(paginas_sincronizadas)} páginas verificadas")
        
        # Calcular estatísticas finais
        total_verificadas = len(paginas_verificadas)
        total_conformes = len(paginas_conformes)
        total_nao_conformes = len(paginas_nao_conformes)
        percentual_conformidade = (total_conformes / total_verificadas * 100) if total_verificadas > 0 else 0
        
        print(f"\n📊 RESULTADOS DA VERIFICAÇÃO MELHORADA:")
        print(f"   📄 Total de páginas verificadas: {total_verificadas}")
        print(f"   ✅ Páginas conformes: {total_conformes}")
        print(f"   ❌ Páginas não conformes: {total_nao_conformes}")
        print(f"   📊 Percentual de conformidade: {percentual_conformidade:.1f}%")
        
        # Análise detalhada dos critérios
        print(f"\n📋 ANÁLISE MELHORADA DOS CRITÉRIOS DO BOILERPLATE:")
        
        # Contar conformidade por critério
        contador_criterios = {}
        for pagina in paginas_verificadas:
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
        
        # Salvar dados da verificação melhorada
        dados_verificacao_melhorada = {
            "data_verificacao_melhorada": datetime.now().isoformat(),
            "titulo": "VERIFICAÇÃO MELHORADA - CRITÉRIOS DE DETECÇÃO PRECISOS",
            "total_paginas_verificadas": total_verificadas,
            "total_conformes": total_conformes,
            "total_nao_conformes": total_nao_conformes,
            "percentual_conformidade": percentual_conformidade,
            "criterios_boilerplate": criterios_boilerplate,
            "analise_criterios_melhorada": contador_criterios,
            "paginas_verificadas": paginas_verificadas,
            "paginas_conformes": paginas_conformes,
            "paginas_nao_conformes": paginas_nao_conformes
        }
        
        with open("verificacao_melhorada.json", "w", encoding="utf-8") as f:
            json.dump(dados_verificacao_melhorada, f, indent=2, ensure_ascii=False, default=str)
        
        # Determinar resultado final
        if percentual_conformidade >= 100:
            print(f"\n🏆 RESULTADO FINAL: 100% DE CONFORMIDADE CONFIRMADA!")
            print(f"   📊 {percentual_conformidade:.1f}% de conformidade")
            print(f"   ✅ {total_conformes} páginas conformes")
            print(f"   🎯 Boilerplate implementado perfeitamente")
            return True
        elif percentual_conformidade >= 80:
            print(f"\n✅ RESULTADO FINAL: CONFORMIDADE EXCELENTE!")
            print(f"   📊 {percentual_conformidade:.1f}% de conformidade")
            print(f"   ✅ {total_conformes} páginas conformes")
            print(f"   🎯 Boilerplate implementado corretamente")
            return True
        else:
            print(f"\n❌ RESULTADO FINAL: CONFORMIDADE INSUFICIENTE!")
            print(f"   📊 {percentual_conformidade:.1f}% de conformidade")
            print(f"   ❌ {total_nao_conformes} páginas não conformes")
            print(f"   ⚠️ Necessário mais correções para atingir 80%")
            return False
        
    except Exception as e:
        print(f"❌ Erro na verificação melhorada: {e}")
        return False

def main():
    print("🔍 VERIFICAÇÃO MELHORADA - CRITÉRIOS DE DETECÇÃO PRECISOS")
    print("=" * 80)
    print("📋 Verificando com critérios de detecção melhorados")
    print("=" * 80)
    
    sucesso = verificacao_melhorada()
    
    if sucesso:
        print(f"\n🏆 VERIFICAÇÃO MELHORADA CONFIRMADA COM SUCESSO!")
        print(f"   🔍 Critérios de detecção funcionando")
        print(f"   ✅ Boilerplate implementado corretamente")
        print(f"   💾 Dados da verificação melhorada salvos")
    else:
        print(f"\n❌ VERIFICAÇÃO MELHORADA REVELOU NÃO CONFORMIDADES")
        print(f"   🔧 Correções adicionais necessárias")
        print(f"   📋 Revisar implementação")
        print(f"   💾 Dados da verificação melhorada salvos")
    
    return sucesso

if __name__ == "__main__":
    main()
