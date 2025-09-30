import os
import json
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def verificacao_manual():
    """Verificação manual para confirmar se as correções foram aplicadas."""
    print("🔍 VERIFICAÇÃO MANUAL - CONFIRMAÇÃO DE CORREÇÕES")
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
        # Carregar dados da verificação melhorada
        with open("verificacao_melhorada.json", "r", encoding="utf-8") as f:
            dados_verificacao = json.load(f)
        
        paginas_nao_conformes = dados_verificacao["paginas_nao_conformes"]
        
        print(f"🔍 VERIFICAÇÃO MANUAL DE {len(paginas_nao_conformes)} PÁGINAS NÃO CONFORMES...")
        
        # Verificar apenas as primeiras 5 páginas para análise detalhada
        paginas_amostra = paginas_nao_conformes[:5]
        
        for i, pagina in enumerate(paginas_amostra):
            page_id = pagina["page_id"]
            titulo = pagina["titulo"]
            criterios_faltando = pagina["criterios_faltando"]
            percentual_atual = pagina["percentual_final"]
            
            print(f"\n📄 PÁGINA {i+1}: {titulo[:60]}...")
            print(f"   📊 Percentual atual: {percentual_atual:.1f}%")
            print(f"   🔧 Critérios faltando: {', '.join(criterios_faltando)}")
            print("   " + "="*60)
            
            try:
                # Buscar página no Notion
                page = notion.pages.retrieve(page_id)
                
                # Buscar blocos da página
                blocks_response = notion.blocks.children.list(page_id)
                blocks = blocks_response.get("results", [])
                
                print(f"   📋 Total de blocos encontrados: {len(blocks)}")
                
                # Analisar cada bloco em detalhes
                for j, block in enumerate(blocks):
                    block_type = block.get("type", "unknown")
                    
                    if block_type in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item"]:
                        rich_text = block.get(block_type, {}).get("rich_text", [])
                        if rich_text:
                            texto_bloco = "".join([rt["text"]["content"] for rt in rich_text])
                            
                            # Verificar se contém elementos do boilerplate
                            if any(palavra in texto_bloco.lower() for palavra in ["censo escolar", "2024", "inep"]):
                                print(f"      ✅ Bloco {j+1} ({block_type}): CONTÉM CENSO ESCOLAR")
                                print(f"         📝 Texto: {texto_bloco[:100]}...")
                            
                            if any(palavra in texto_bloco.lower() for palavra in ["youtube", "vídeos", "video", "🎥"]):
                                print(f"      ✅ Bloco {j+1} ({block_type}): CONTÉM VÍDEOS")
                                print(f"         📝 Texto: {texto_bloco[:100]}...")
                            
                            if any(palavra in texto_bloco.lower() for palavra in ["fonte:", "referência", "mec", "inep", "fnde", "📚"]):
                                print(f"      ✅ Bloco {j+1} ({block_type}): CONTÉM FONTES")
                                print(f"         📝 Texto: {texto_bloco[:100]}...")
                            
                            if any(palavra in texto_bloco.lower() for palavra in ["resumo", "executivo", "sumário", "objetivos", "📋"]):
                                print(f"      ✅ Bloco {j+1} ({block_type}): CONTÉM RESUMO EXECUTIVO")
                                print(f"         📝 Texto: {texto_bloco[:100]}...")
                            
                            if any(palavra in texto_bloco.lower() for palavra in ["tags:", "**tags**", "categoria:", "**categoria**", "🏷️"]):
                                print(f"      ✅ Bloco {j+1} ({block_type}): CONTÉM TAGS")
                                print(f"         📝 Texto: {texto_bloco[:100]}...")
                            
                            if any(palavra in texto_bloco.lower() for palavra in ["conclusão", "conclusao", "finalizando", "próximos passos", "🎯"]):
                                print(f"      ✅ Bloco {j+1} ({block_type}): CONTÉM CONCLUSÃO")
                                print(f"         📝 Texto: {texto_bloco[:100]}...")
                            
                            if any(palavra in texto_bloco.lower() for palavra in ["dados", "estatísticas", "indicadores", "métricas", "📊"]):
                                print(f"      ✅ Bloco {j+1} ({block_type}): CONTÉM DADOS REAIS")
                                print(f"         📝 Texto: {texto_bloco[:100]}...")
                            
                            if any(palavra in texto_bloco.lower() for palavra in ["metodologia", "aplicabilidade", "implementação", "processo", "🔧"]):
                                print(f"      ✅ Bloco {j+1} ({block_type}): CONTÉM METODOLOGIA")
                                print(f"         📝 Texto: {texto_bloco[:100]}...")
                            
                            if any(palavra in texto_bloco.lower() for palavra in ["qualidade", "educacional", "pedagógico", "gestão", "🏆"]):
                                print(f"      ✅ Bloco {j+1} ({block_type}): CONTÉM QUALIDADE")
                                print(f"         📝 Texto: {texto_bloco[:100]}...")
                
                # Verificar critérios específicos que estavam faltando
                print(f"\n   🔍 VERIFICAÇÃO ESPECÍFICA DOS CRITÉRIOS FALTANDO:")
                
                # Converter todos os blocos para texto
                conteudo_completo = ""
                for block in blocks:
                    if block.get("type") in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item"]:
                        rich_text = block.get(block["type"], {}).get("rich_text", [])
                        if rich_text:
                            texto_bloco = "".join([rt["text"]["content"] for rt in rich_text])
                            conteudo_completo += texto_bloco + "\n"
                
                for criterio in criterios_faltando:
                    if criterio == "censo_escolar":
                        palavras_censo = ["censo escolar", "2024", "inep", "estatísticas nacionais", "dados do censo", "censo 2024"]
                        encontrado = any(palavra in conteudo_completo.lower() for palavra in palavras_censo)
                        status = "✅ ENCONTRADO" if encontrado else "❌ NÃO ENCONTRADO"
                        print(f"      {status} - Censo Escolar 2024")
                    
                    elif criterio == "videos":
                        palavras_videos = ["youtube", "vídeos", "video", "🎥", "vídeos educativos", "youtube.com"]
                        encontrado = any(palavra in conteudo_completo.lower() for palavra in palavras_videos)
                        status = "✅ ENCONTRADO" if encontrado else "❌ NÃO ENCONTRADO"
                        print(f"      {status} - Vídeos educativos")
                    
                    elif criterio == "fontes":
                        palavras_fontes = ["fonte:", "referência", "mec", "inep", "fnde", "📚", "fontes", "referências"]
                        encontrado = any(palavra in conteudo_completo.lower() for palavra in palavras_fontes)
                        status = "✅ ENCONTRADO" if encontrado else "❌ NÃO ENCONTRADO"
                        print(f"      {status} - Fontes confiáveis")
                    
                    elif criterio == "resumo_executivo":
                        palavras_resumo = ["resumo", "executivo", "sumário", "objetivos", "📋", "resumo executivo"]
                        encontrado = any(palavra in conteudo_completo.lower() for palavra in palavras_resumo)
                        status = "✅ ENCONTRADO" if encontrado else "❌ NÃO ENCONTRADO"
                        print(f"      {status} - Resumo executivo")
                    
                    elif criterio == "tags":
                        palavras_tags = ["tags:", "**tags**", "categoria:", "**categoria**", "🏷️", "tags", "categoria"]
                        encontrado = any(palavra in conteudo_completo.lower() for palavra in palavras_tags)
                        status = "✅ ENCONTRADO" if encontrado else "❌ NÃO ENCONTRADO"
                        print(f"      {status} - Tags e categorização")
                    
                    elif criterio == "conclusao":
                        palavras_conclusao = ["conclusão", "conclusao", "finalizando", "próximos passos", "🎯", "conclusão"]
                        encontrado = any(palavra in conteudo_completo.lower() for palavra in palavras_conclusao)
                        status = "✅ ENCONTRADO" if encontrado else "❌ NÃO ENCONTRADO"
                        print(f"      {status} - Conclusão")
                    
                    elif criterio == "dados_reais":
                        palavras_dados = ["dados", "estatísticas", "indicadores", "métricas", "📊", "dados reais"]
                        encontrado = any(palavra in conteudo_completo.lower() for palavra in palavras_dados)
                        status = "✅ ENCONTRADO" if encontrado else "❌ NÃO ENCONTRADO"
                        print(f"      {status} - Dados reais")
                    
                    elif criterio == "metodologia":
                        palavras_metodologia = ["metodologia", "aplicabilidade", "implementação", "processo", "🔧", "metodologia"]
                        encontrado = any(palavra in conteudo_completo.lower() for palavra in palavras_metodologia)
                        status = "✅ ENCONTRADO" if encontrado else "❌ NÃO ENCONTRADO"
                        print(f"      {status} - Metodologia")
                    
                    elif criterio == "qualidade":
                        palavras_qualidade = ["qualidade", "educacional", "pedagógico", "gestão", "🏆", "qualidade educacional"]
                        encontrado = any(palavra in conteudo_completo.lower() for palavra in palavras_qualidade)
                        status = "✅ ENCONTRADO" if encontrado else "❌ NÃO ENCONTRADO"
                        print(f"      {status} - Qualidade educacional")
                
            except Exception as e:
                print(f"      ❌ ERRO: {e}")
            
            print(f"   " + "="*60)
        
        print(f"\n📊 RESUMO DA VERIFICAÇÃO MANUAL:")
        print(f"   📄 Páginas analisadas: {len(paginas_amostra)}")
        print(f"   🔍 Análise detalhada concluída")
        print(f"   💾 Verificação manual finalizada")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na verificação manual: {e}")
        return False

def main():
    print("🔍 VERIFICAÇÃO MANUAL - CONFIRMAÇÃO DE CORREÇÕES")
    print("=" * 80)
    print("📋 Verificando manualmente se as correções foram aplicadas")
    print("=" * 80)
    
    sucesso = verificacao_manual()
    
    if sucesso:
        print(f"\n🏆 VERIFICAÇÃO MANUAL CONCLUÍDA COM SUCESSO!")
        print(f"   🔍 Análise detalhada realizada")
        print(f"   📊 Correções verificadas")
        print(f"   💾 Verificação manual finalizada")
    else:
        print(f"\n❌ ERRO NA VERIFICAÇÃO MANUAL")
        print(f"   🔧 Verificar configurações")
        print(f"   📋 Revisar implementação")
    
    return sucesso

if __name__ == "__main__":
    main()
