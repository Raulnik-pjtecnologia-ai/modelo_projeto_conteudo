import os
import json
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def analise_completa_biblioteca():
    """Análise completa de toda a biblioteca para verificar conformidades."""
    print("🔍 ANÁLISE COMPLETA DA BIBLIOTECA - VERIFICAÇÃO DE CONFORMIDADES")
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
        # Buscar todas as páginas da biblioteca
        print("📚 BUSCANDO TODAS AS PÁGINAS DA BIBLIOTECA...")
        
        # Buscar todas as páginas do banco de dados
        database_id = "2695113a-91a3-80f3-be87-ebd8fc6b65eb"  # ID do Editorial Gestão Educacional
        
        # Primeiro, vamos listar todos os bancos de dados para encontrar o correto
        print("   🔍 Listando bancos de dados disponíveis...")
        databases_response = notion.search(filter={"property": "object", "value": "database"})
        databases = databases_response.get("results", [])
        
        print(f"   📊 {len(databases)} bancos de dados encontrados")
        
        # Listar todos os bancos de dados para encontrar o correto
        print("   📋 Bancos de dados disponíveis:")
        for i, db in enumerate(databases):
            title_property = db.get("title", [])
            if title_property and len(title_property) > 0:
                title = title_property[0].get("text", {}).get("content", "")
            else:
                title = "Sem título"
            print(f"      {i+1}. {title} (ID: {db['id']})")
        
        # Procurar pelo banco de dados do Editorial Gestão Educacional
        database_id = None
        for db in databases:
            title_property = db.get("title", [])
            if title_property and len(title_property) > 0:
                title = title_property[0].get("text", {}).get("content", "")
                if "gestão" in title.lower() or "editorial" in title.lower() or "gestao" in title.lower():
                    database_id = db["id"]
                    print(f"   ✅ Banco de dados encontrado: {title} (ID: {database_id})")
                    break
        
        if not database_id:
            print("   ❌ Banco de dados 'Editorial Gestão Educacional' não encontrado")
            print("   🔍 Tentando usar o primeiro banco de dados disponível...")
            if databases:
                database_id = databases[0]["id"]
                title_property = databases[0].get("title", [])
                if title_property and len(title_property) > 0:
                    title = title_property[0].get("text", {}).get("content", "")
                else:
                    title = "Sem título"
                print(f"   📊 Usando: {title} (ID: {database_id})")
            else:
                return False
        
        all_pages = []
        has_more = True
        start_cursor = None
        
        while has_more:
            if start_cursor:
                response = notion.databases.query(
                    database_id=database_id,
                    start_cursor=start_cursor
                )
            else:
                response = notion.databases.query(database_id=database_id)
            
            pages = response.get("results", [])
            all_pages.extend(pages)
            
            has_more = response.get("has_more", False)
            start_cursor = response.get("next_cursor")
            
            print(f"   📄 {len(pages)} páginas encontradas nesta consulta...")
        
        print(f"📊 TOTAL DE PÁGINAS ENCONTRADAS: {len(all_pages)}")
        
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
        
        # Analisar cada página
        print(f"\n🔍 ANALISANDO CONFORMIDADE DE CADA PÁGINA...")
        
        paginas_analisadas = []
        paginas_conformes = []
        paginas_nao_conformes = []
        paginas_com_erro = []
        
        for i, page in enumerate(all_pages):
            page_id = page["id"]
            titulo = ""
            
            # Extrair título da página
            try:
                title_property = page.get("properties", {}).get("title", {})
                if title_property and "title" in title_property:
                    title_array = title_property["title"]
                    if title_array and len(title_array) > 0:
                        titulo = title_array[0].get("text", {}).get("content", "Sem título")
            except:
                titulo = "Sem título"
            
            print(f"   🔍 Analisando página {i+1}/{len(all_pages)}: {titulo[:50]}...")
            
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
                        "titulo": titulo,
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
                        "titulo": titulo,
                        "percentual_conformidade": percentual_conformidade,
                        "criterios_atingidos": criterios_atingidos,
                        "criterios_faltando": [k for k, v in conformidade_criterios.items() if not v],
                        "conformidade_detalhada": conformidade_criterios
                    })
                    print(f"      ❌ {status_conformidade} ({percentual_conformidade:.1f}%) - {criterios_atingidos}/{total_criterios} critérios")
                
                # Adicionar à lista de páginas analisadas
                paginas_analisadas.append({
                    "page_id": page_id,
                    "titulo": titulo,
                    "percentual_conformidade": percentual_conformidade,
                    "criterios_atingidos": criterios_atingidos,
                    "criterios_faltando": [k for k, v in conformidade_criterios.items() if not v],
                    "conformidade_detalhada": conformidade_criterios,
                    "status_conformidade": status_conformidade
                })
                
            except Exception as e:
                print(f"      ⚠️ ERRO: {e}")
                paginas_com_erro.append({
                    "page_id": page_id,
                    "titulo": titulo,
                    "erro": str(e)
                })
            
            # Progresso
            if (i + 1) % 20 == 0:
                print(f"      📊 Progresso: {i + 1}/{len(all_pages)} páginas analisadas")
        
        # Calcular estatísticas finais
        total_analisadas = len(paginas_analisadas)
        total_conformes = len(paginas_conformes)
        total_nao_conformes = len(paginas_nao_conformes)
        total_com_erro = len(paginas_com_erro)
        percentual_conformidade_geral = (total_conformes / total_analisadas * 100) if total_analisadas > 0 else 0
        
        print(f"\n📊 RESULTADOS DA ANÁLISE COMPLETA DA BIBLIOTECA:")
        print(f"   📄 Total de páginas analisadas: {total_analisadas}")
        print(f"   ✅ Páginas conformes: {total_conformes}")
        print(f"   ❌ Páginas não conformes: {total_nao_conformes}")
        print(f"   ⚠️ Páginas com erro: {total_com_erro}")
        print(f"   📊 Percentual de conformidade geral: {percentual_conformidade_geral:.1f}%")
        
        # Análise detalhada dos critérios
        print(f"\n📋 ANÁLISE DETALHADA DOS CRITÉRIOS DO BOILERPLATE:")
        
        # Contar conformidade por critério
        contador_criterios = {}
        for pagina in paginas_analisadas:
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
        
        # Análise por faixas de conformidade
        print(f"\n📊 DISTRIBUIÇÃO POR FAIXAS DE CONFORMIDADE:")
        
        faixas = {
            "100%": 0,
            "90-99%": 0,
            "80-89%": 0,
            "70-79%": 0,
            "60-69%": 0,
            "50-59%": 0,
            "40-49%": 0,
            "30-39%": 0,
            "20-29%": 0,
            "10-19%": 0,
            "0-9%": 0
        }
        
        for pagina in paginas_analisadas:
            percentual = pagina["percentual_conformidade"]
            if percentual == 100:
                faixas["100%"] += 1
            elif percentual >= 90:
                faixas["90-99%"] += 1
            elif percentual >= 80:
                faixas["80-89%"] += 1
            elif percentual >= 70:
                faixas["70-79%"] += 1
            elif percentual >= 60:
                faixas["60-69%"] += 1
            elif percentual >= 50:
                faixas["50-59%"] += 1
            elif percentual >= 40:
                faixas["40-49%"] += 1
            elif percentual >= 30:
                faixas["30-39%"] += 1
            elif percentual >= 20:
                faixas["20-29%"] += 1
            elif percentual >= 10:
                faixas["10-19%"] += 1
            else:
                faixas["0-9%"] += 1
        
        for faixa, quantidade in faixas.items():
            if quantidade > 0:
                print(f"   📊 {faixa}: {quantidade} páginas")
        
        # Salvar dados da análise completa
        dados_analise_completa = {
            "data_analise": datetime.now().isoformat(),
            "titulo": "ANÁLISE COMPLETA DA BIBLIOTECA - VERIFICAÇÃO DE CONFORMIDADES",
            "total_paginas_analisadas": total_analisadas,
            "total_conformes": total_conformes,
            "total_nao_conformes": total_nao_conformes,
            "total_com_erro": total_com_erro,
            "percentual_conformidade_geral": percentual_conformidade_geral,
            "criterios_boilerplate": criterios_boilerplate,
            "analise_criterios": contador_criterios,
            "distribuicao_faixas": faixas,
            "paginas_analisadas": paginas_analisadas,
            "paginas_conformes": paginas_conformes,
            "paginas_nao_conformes": paginas_nao_conformes,
            "paginas_com_erro": paginas_com_erro
        }
        
        with open("analise_completa_biblioteca.json", "w", encoding="utf-8") as f:
            json.dump(dados_analise_completa, f, indent=2, ensure_ascii=False, default=str)
        
        # Determinar resultado final
        if percentual_conformidade_geral >= 80:
            print(f"\n✅ RESULTADO FINAL: BIBLIOTECA CONFORME COM BOILERPLATE!")
            print(f"   📊 {percentual_conformidade_geral:.1f}% de conformidade geral")
            print(f"   ✅ {total_conformes} páginas conformes")
            print(f"   🎯 Padrões de qualidade educacional mantidos")
            return True
        else:
            print(f"\n❌ RESULTADO FINAL: BIBLIOTECA NÃO CONFORME COM BOILERPLATE!")
            print(f"   📊 {percentual_conformidade_geral:.1f}% de conformidade geral")
            print(f"   ❌ {total_nao_conformes} páginas não conformes")
            print(f"   ⚠️ Necessário correções para atingir 80% de conformidade")
            return False
        
    except Exception as e:
        print(f"❌ Erro na análise completa: {e}")
        return False

def main():
    print("🔍 ANÁLISE COMPLETA DA BIBLIOTECA - VERIFICAÇÃO DE CONFORMIDADES")
    print("=" * 80)
    print("📋 Analisando toda a biblioteca para verificar conformidades com boilerplate")
    print("=" * 80)
    
    sucesso = analise_completa_biblioteca()
    
    if sucesso:
        print(f"\n✅ ANÁLISE COMPLETA CONCLUÍDA COM SUCESSO!")
        print(f"   🔍 Biblioteca analisada completamente")
        print(f"   ✅ Conformidade verificada")
        print(f"   💾 Dados da análise salvos")
    else:
        print(f"\n❌ ANÁLISE COMPLETA REVELOU NÃO CONFORMIDADES")
        print(f"   🔧 Correções necessárias identificadas")
        print(f"   📋 Revisar implementação do boilerplate")
        print(f"   💾 Dados da análise salvos")
    
    return sucesso

if __name__ == "__main__":
    main()
