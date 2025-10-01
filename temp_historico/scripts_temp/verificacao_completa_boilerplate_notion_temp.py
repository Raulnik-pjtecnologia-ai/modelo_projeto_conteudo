import os
import json
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def verificar_conformidade_completa_notion():
    """Verificação completa de conformidade com boilerplate de todo o banco de dados Notion."""
    print("🔍 VERIFICAÇÃO COMPLETA DE CONFORMIDADE COM BOILERPLATE")
    print("=" * 70)
    
    # Carregar configuração
    load_dotenv()
    
    notion_token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("DATABASE_ID")
    
    if not notion_token or not database_id:
        print("❌ Configuração do Notion não encontrada")
        return False
    
    # Inicializar cliente Notion
    notion = Client(auth=notion_token)
    
    try:
        print("📊 Buscando todas as páginas do banco de dados...")
        
        # Buscar todas as páginas (pode ser necessário paginar)
        all_pages = []
        has_more = True
        start_cursor = None
        
        while has_more:
            query_params = {
                "database_id": database_id,
                "page_size": 100
            }
            
            if start_cursor:
                query_params["start_cursor"] = start_cursor
            
            response = notion.databases.query(**query_params)
            pages = response.get("results", [])
            all_pages.extend(pages)
            
            has_more = response.get("has_more", False)
            start_cursor = response.get("next_cursor")
            
            print(f"   📄 {len(all_pages)} páginas carregadas...")
        
        print(f"✅ Total de {len(all_pages)} páginas encontradas no banco de dados")
        
        # Critérios do boilerplate para verificar
        criterios_boilerplate = {
            "capa_titulo_data": "Capa com título e data",
            "resumo_executivo": "Resumo executivo",
            "dados_censo_escolar": "Dados do Censo Escolar 2024",
            "videos_youtube": "Vídeos educativos do YouTube",
            "fontes_confiaveis": "Fontes confiáveis",
            "conclusao": "Conclusão",
            "tags_apropriadas": "Tags apropriadas",
            "categoria_correta": "Categoria correta",
            "nivel_funcao": "Nível de função"
        }
        
        print(f"\n🔍 Analisando conformidade com {len(criterios_boilerplate)} critérios...")
        
        paginas_analisadas = []
        paginas_conformes = []
        paginas_nao_conformes = []
        estatisticas_criterios = {criterio: 0 for criterio in criterios_boilerplate.keys()}
        
        for i, page in enumerate(all_pages):
            page_id = page["id"]
            properties = page.get("properties", {})
            
            # Extrair título
            titulo = ""
            if "Título" in properties:
                titulo_prop = properties["Título"]
                if titulo_prop.get("title"):
                    titulo = titulo_prop["title"][0]["text"]["content"]
            
            # Se não encontrou no Título, tentar buscar no conteúdo
            if not titulo:
                try:
                    blocks_response = notion.blocks.children.list(page_id)
                    blocks = blocks_response.get("results", [])
                    
                    for block in blocks:
                        if block.get("type") == "heading_1":
                            heading = block.get("heading_1", {})
                            rich_text = heading.get("rich_text", [])
                            if rich_text:
                                titulo = rich_text[0]["text"]["content"]
                                break
                except:
                    pass
            
            print(f"📋 Analisando ({i+1}/{len(all_pages)}): {titulo[:50]}...")
            
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
                verificacoes["capa_titulo_data"] = bool(titulo and len(titulo) > 5)
                
                # 2. Resumo executivo
                verificacoes["resumo_executivo"] = any(palavra in conteudo_texto.lower() 
                                                     for palavra in ["resumo", "executivo", "sumário", "sumario"])
                
                # 3. Dados do Censo Escolar 2024
                verificacoes["dados_censo_escolar"] = any(palavra in conteudo_texto.lower() 
                                                        for palavra in ["censo escolar", "2024", "inep", "dados reais"])
                
                # 4. Vídeos educativos do YouTube
                verificacoes["videos_youtube"] = "youtube" in conteudo_texto.lower() or "watch?v=" in conteudo_texto.lower()
                
                # 5. Fontes confiáveis
                verificacoes["fontes_confiaveis"] = any(palavra in conteudo_texto.lower() 
                                                      for palavra in ["fonte:", "referência", "bibliografia", "link", "mec", "inep"])
                
                # 6. Conclusão
                verificacoes["conclusao"] = any(palavra in conteudo_texto.lower() 
                                              for palavra in ["conclusão", "conclusao", "finalizando", "considerações"])
                
                # 7. Tags apropriadas
                verificacoes["tags_apropriadas"] = "tags:" in conteudo_texto.lower() or "**tags**" in conteudo_texto.lower()
                
                # 8. Categoria correta
                verificacoes["categoria_correta"] = any(palavra in conteudo_texto.lower() 
                                                      for palavra in ["categoria:", "**categoria**", "gestão", "escolar", "educacional"])
                
                # 9. Nível de função
                verificacoes["nivel_funcao"] = any(palavra in conteudo_texto.lower() 
                                                 for palavra in ["nível:", "**nível**", "diretor", "coordenador", "gestor"])
                
                # Calcular pontuação
                pontuacao = sum(1 for v in verificacoes.values() if v)
                total_criterios = len(verificacoes)
                percentual = (pontuacao / total_criterios) * 100
                
                # Determinar se está conforme (70% de conformidade)
                conforme = percentual >= 70
                
                # Atualizar estatísticas dos critérios
                for criterio, aprovado in verificacoes.items():
                    if aprovado:
                        estatisticas_criterios[criterio] += 1
                
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
                if (i + 1) % 20 == 0:
                    print(f"   📊 Progresso: {i + 1}/{len(all_pages)} páginas analisadas")
                
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
        
        # Calcular estatísticas gerais
        total_analisadas = len(paginas_analisadas)
        total_conformes = len(paginas_conformes)
        total_nao_conformes = len(paginas_nao_conformes)
        percentual_geral = (total_conformes / total_analisadas * 100) if total_analisadas > 0 else 0
        
        # Calcular estatísticas por critério
        estatisticas_criterios_percentual = {}
        for criterio, total in estatisticas_criterios.items():
            estatisticas_criterios_percentual[criterio] = {
                "total": total,
                "percentual": (total / total_analisadas * 100) if total_analisadas > 0 else 0,
                "descricao": criterios_boilerplate[criterio]
            }
        
        # Salvar dados completos
        dados_completos = {
            "data_analise": datetime.now().isoformat(),
            "titulo": "VERIFICAÇÃO COMPLETA DE CONFORMIDADE COM BOILERPLATE",
            "total_paginas_analisadas": total_analisadas,
            "total_conformes": total_conformes,
            "total_nao_conformes": total_nao_conformes,
            "percentual_geral_conformidade": percentual_geral,
            "criterios_boilerplate": criterios_boilerplate,
            "estatisticas_por_criterio": estatisticas_criterios_percentual,
            "paginas_analisadas": paginas_analisadas,
            "paginas_conformes": paginas_conformes,
            "paginas_nao_conformes": paginas_nao_conformes
        }
        
        with open("verificacao_completa_boilerplate_notion.json", "w", encoding="utf-8") as f:
            json.dump(dados_completos, f, indent=2, ensure_ascii=False, default=str)
        
        # Gerar relatório em markdown
        relatorio_md = f"""# VERIFICAÇÃO COMPLETA DE CONFORMIDADE COM BOILERPLATE

**Data da Verificação:** {datetime.now().strftime('%d/%m/%Y às %H:%M')}

## 📊 RESUMO EXECUTIVO

- **Total de Páginas Analisadas:** {total_analisadas}
- **Páginas Conformes:** {total_conformes}
- **Páginas Não Conformes:** {total_nao_conformes}
- **Percentual Geral de Conformidade:** {percentual_geral:.1f}%

## 📈 ESTATÍSTICAS POR CRITÉRIO

"""
        
        for criterio, dados in estatisticas_criterios_percentual.items():
            relatorio_md += f"""
### {dados['descricao']}
- **Total:** {dados['total']}/{total_analisadas}
- **Percentual:** {dados['percentual']:.1f}%
"""
        
        relatorio_md += f"""
## ✅ PÁGINAS CONFORMES ({total_conformes})

"""
        
        for i, pagina in enumerate(paginas_conformes[:20], 1):
            if "erro" not in pagina:
                relatorio_md += f"{i}. {pagina['titulo'][:60]}... ({pagina['percentual']:.1f}%)\n"
            else:
                relatorio_md += f"{i}. {pagina['titulo'][:60]}... (ERRO)\n"
        
        if len(paginas_conformes) > 20:
            relatorio_md += f"... e mais {len(paginas_conformes) - 20} páginas conformes\n"
        
        relatorio_md += f"""
## ❌ PÁGINAS NÃO CONFORMES ({total_nao_conformes})

"""
        
        for i, pagina in enumerate(paginas_nao_conformes[:20], 1):
            if "erro" not in pagina:
                relatorio_md += f"{i}. {pagina['titulo'][:60]}... ({pagina['percentual']:.1f}%)\n"
            else:
                relatorio_md += f"{i}. {pagina['titulo'][:60]}... (ERRO)\n"
        
        if len(paginas_nao_conformes) > 20:
            relatorio_md += f"... e mais {len(paginas_nao_conformes) - 20} páginas não conformes\n"
        
        relatorio_md += f"""
## 🎯 RECOMENDAÇÕES

1. **Páginas Não Conformes:** {total_nao_conformes} páginas precisam de correção
2. **Critérios Mais Críticos:** Verificar critérios com menor percentual de conformidade
3. **Processo de Correção:** Implementar correção automática para páginas não conformes
4. **Monitoramento Contínuo:** Estabelecer verificação periódica de conformidade

---
*Relatório gerado automaticamente em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*
"""
        
        # Salvar relatório em markdown
        with open("relatorio_verificacao_completa_boilerplate.md", "w", encoding="utf-8") as f:
            f.write(relatorio_md)
        
        print(f"\n📊 RESUMO FINAL:")
        print(f"   📄 Total de páginas analisadas: {total_analisadas}")
        print(f"   ✅ Páginas conformes: {total_conformes}")
        print(f"   ❌ Páginas não conformes: {total_nao_conformes}")
        print(f"   📊 Percentual geral de conformidade: {percentual_geral:.1f}%")
        print(f"   💾 Dados salvos: verificacao_completa_boilerplate_notion.json")
        print(f"   📝 Relatório: relatorio_verificacao_completa_boilerplate.md")
        
        print(f"\n📈 CONFORMIDADE POR CRITÉRIO:")
        for criterio, dados in estatisticas_criterios_percentual.items():
            print(f"   {dados['descricao']}: {dados['percentual']:.1f}% ({dados['total']}/{total_analisadas})")
        
        if paginas_nao_conformes:
            print(f"\n❌ PRINCIPAIS PÁGINAS NÃO CONFORMES:")
            for i, pagina in enumerate(paginas_nao_conformes[:10], 1):
                if "erro" not in pagina:
                    print(f"   {i}. {pagina['titulo'][:60]}... ({pagina['percentual']:.1f}%)")
                else:
                    print(f"   {i}. {pagina['titulo'][:60]}... (ERRO)")
            if len(paginas_nao_conformes) > 10:
                print(f"   ... e mais {len(paginas_nao_conformes) - 10} páginas não conformes")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na verificação completa: {e}")
        return False

def main():
    print("🔍 VERIFICAÇÃO COMPLETA DE CONFORMIDADE COM BOILERPLATE")
    print("======================================================================")
    print("📋 Analisando todo o banco de dados do Notion")
    print("======================================================================")
    
    sucesso = verificar_conformidade_completa_notion()
    
    if sucesso:
        print(f"\n✅ VERIFICAÇÃO COMPLETA CONCLUÍDA COM SUCESSO!")
        print(f"   📊 Todo o banco de dados analisado")
        print(f"   🔍 Conformidade verificada")
        print(f"   📈 Estatísticas geradas")
        print(f"   💾 Relatórios salvos")
    else:
        print(f"\n❌ ERRO NA VERIFICAÇÃO COMPLETA")
        print(f"   🔧 Verificar configuração")
        print(f"   📋 Revisar processo")
    
    return sucesso

if __name__ == "__main__":
    main()
