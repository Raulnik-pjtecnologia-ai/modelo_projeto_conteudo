import os
import json
import time
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

def verificacao_final_conformidade():
    """Verificacao final de conformidade com boilerplate."""
    print("VERIFICACAO FINAL DE CONFORMIDADE - BOILERPLATE")
    print("=" * 60)
    
    # Carregar configuracao
    load_dotenv()
    
    notion_token = os.getenv("NOTION_TOKEN")
    
    if not notion_token:
        print("ERRO: Configuracao do Notion nao encontrada")
        return False
    
    # Inicializar cliente Notion
    notion = Client(auth=notion_token)
    
    try:
        # Carregar dados da sincronizacao
        with open("sincronizacao_simples_final.json", "r", encoding="utf-8") as f:
            dados_sincronizacao = json.load(f)
        
        paginas_sincronizadas = dados_sincronizacao["paginas_sincronizadas"]
        
        print(f"VERIFICANDO CONFORMIDADE DE {len(paginas_sincronizadas)} PAGINAS...")
        
        paginas_conformes = []
        paginas_nao_conformes = []
        
        # Criterios do boilerplate
        criterios_boilerplate = [
            "censo_escolar",
            "videos", 
            "fontes",
            "resumo_executivo",
            "tags",
            "conclusao",
            "dados_reais",
            "metodologia",
            "qualidade"
        ]
        
        for i, pagina in enumerate(paginas_sincronizadas):
            page_id = pagina["page_id"]
            titulo = pagina["titulo"]
            
            print(f"   {i+1}/{len(paginas_sincronizadas)}: {titulo[:30]}...")
            
            try:
                # Buscar conteudo da pagina
                page_blocks = notion.blocks.children.list(block_id=page_id)
                
                # Verificar presenca dos criterios
                criterios_encontrados = []
                criterios_faltando = []
                
                # Converter blocos para texto
                texto_completo = ""
                for block in page_blocks["results"]:
                    if block["type"] == "paragraph" and "rich_text" in block["paragraph"]:
                        for rt in block["paragraph"]["rich_text"]:
                            texto_completo += rt["text"]["content"].lower()
                
                # Verificar cada criterio
                for criterio in criterios_boilerplate:
                    if criterio == "censo_escolar":
                        if "censo escolar" in texto_completo or "179.533" in texto_completo:
                            criterios_encontrados.append(criterio)
                        else:
                            criterios_faltando.append(criterio)
                    elif criterio == "videos":
                        if "videos" in texto_completo or "youtube" in texto_completo:
                            criterios_encontrados.append(criterio)
                        else:
                            criterios_faltando.append(criterio)
                    elif criterio == "fontes":
                        if "mec" in texto_completo or "inep" in texto_completo:
                            criterios_encontrados.append(criterio)
                        else:
                            criterios_faltando.append(criterio)
                    elif criterio == "resumo_executivo":
                        if "resumo executivo" in texto_completo:
                            criterios_encontrados.append(criterio)
                        else:
                            criterios_faltando.append(criterio)
                    elif criterio == "tags":
                        if "tags" in texto_completo or "gestao escolar" in texto_completo:
                            criterios_encontrados.append(criterio)
                        else:
                            criterios_faltando.append(criterio)
                    elif criterio == "conclusao":
                        if "conclusao" in texto_completo:
                            criterios_encontrados.append(criterio)
                        else:
                            criterios_faltando.append(criterio)
                    elif criterio == "dados_reais":
                        if "dados reais" in texto_completo or "89.2%" in texto_completo:
                            criterios_encontrados.append(criterio)
                        else:
                            criterios_faltando.append(criterio)
                    elif criterio == "metodologia":
                        if "metodologia" in texto_completo:
                            criterios_encontrados.append(criterio)
                        else:
                            criterios_faltando.append(criterio)
                    elif criterio == "qualidade":
                        if "qualidade" in texto_completo:
                            criterios_encontrados.append(criterio)
                        else:
                            criterios_faltando.append(criterio)
                
                # Calcular percentual de conformidade
                percentual = (len(criterios_encontrados) / len(criterios_boilerplate)) * 100
                
                if percentual >= 80:
                    paginas_conformes.append({
                        "page_id": page_id,
                        "titulo": titulo,
                        "percentual": percentual,
                        "criterios_encontrados": criterios_encontrados,
                        "criterios_faltando": criterios_faltando
                    })
                    print(f"      CONFORME - {percentual:.1f}%")
                else:
                    paginas_nao_conformes.append({
                        "page_id": page_id,
                        "titulo": titulo,
                        "percentual": percentual,
                        "criterios_encontrados": criterios_encontrados,
                        "criterios_faltando": criterios_faltando
                    })
                    print(f"      NAO CONFORME - {percentual:.1f}%")
                
                # Pausa entre verificacoes
                time.sleep(1)
                
            except Exception as e:
                print(f"      ERRO: {str(e)[:30]}...")
        
        # Calcular estatisticas finais
        total_paginas = len(paginas_sincronizadas)
        total_conformes = len(paginas_conformes)
        total_nao_conformes = len(paginas_nao_conformes)
        percentual_geral = (total_conformes / total_paginas) * 100 if total_paginas > 0 else 0
        
        print(f"\nRESULTADOS DA VERIFICACAO FINAL:")
        print(f"   Total de paginas verificadas: {total_paginas}")
        print(f"   Paginas conformes (>=80%): {total_conformes}")
        print(f"   Paginas nao conformes (<80%): {total_nao_conformes}")
        print(f"   Percentual geral de conformidade: {percentual_geral:.1f}%")
        
        # Salvar resultados da verificacao
        dados_verificacao = {
            "data_verificacao": datetime.now().isoformat(),
            "total_paginas_verificadas": total_paginas,
            "total_conformes": total_conformes,
            "total_nao_conformes": total_nao_conformes,
            "percentual_geral_conformidade": percentual_geral,
            "paginas_conformes": paginas_conformes,
            "paginas_nao_conformes": paginas_nao_conformes
        }
        
        with open("verificacao_final_conformidade.json", "w", encoding="utf-8") as f:
            json.dump(dados_verificacao, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\nVERIFICACAO FINAL CONCLUIDA!")
        print(f"   {total_conformes}/{total_paginas} paginas conformes")
        print(f"   {percentual_geral:.1f}% de conformidade geral")
        print(f"   Dados salvos em verificacao_final_conformidade.json")
        
        return percentual_geral >= 80
        
    except Exception as e:
        print(f"Erro na verificacao: {e}")
        return False

def main():
    print("VERIFICACAO FINAL DE CONFORMIDADE - BOILERPLATE")
    print("=" * 60)
    
    sucesso = verificacao_final_conformidade()
    
    if sucesso:
        print(f"\nVERIFICACAO FINAL REALIZADA COM SUCESSO!")
        print(f"   Conformidade >= 80% alcancada")
        print(f"   Boilerplate implementado corretamente")
    else:
        print(f"\nVERIFICACAO FINAL - CONFORMIDADE INSUFICIENTE")
        print(f"   Conformidade < 80%")
        print(f"   Necessario aplicar mais correcoes")
    
    return sucesso

if __name__ == "__main__":
    main()
