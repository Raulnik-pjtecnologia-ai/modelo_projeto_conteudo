import os
import json
import re
from datetime import datetime

def curadoria_artigo_sistemas_gestao():
    """Aplicar curadoria obrigatória ao artigo sobre sistemas de gestão escolar."""
    print("CUradoria OBRIGATORIA - ARTIGO SISTEMAS GESTAO ESCOLAR")
    print("=" * 70)
    
    # Ler o arquivo do artigo
    arquivo_artigo = "2_conteudo/01_ideias_e_rascunhos/artigo_sistemas_gestao_escolar_modernos_2024.md"
    
    try:
        with open(arquivo_artigo, "r", encoding="utf-8") as f:
            conteudo = f.read()
        
        print(f"Artigo carregado: {arquivo_artigo}")
        print(f"Tamanho do conteudo: {len(conteudo)} caracteres")
        
    except FileNotFoundError:
        print(f"ERRO: Arquivo {arquivo_artigo} nao encontrado")
        return False
    
    # Critérios de curadoria
    criterios = {
        "estrutura_boilerplate": {
            "capa": False,
            "resumo_executivo": False,
            "dados_graficos": False,
            "videos_relacionados": False,
            "noticias_recentes": False,
            "fontes_referencias": False,
            "conclusao": False,
            "tags": False,
            "categoria": False,
            "nivel": False,
            "funcao": False
        },
        "enriquecimento_mcp": {
            "grafico_incluido": False,
            "videos_youtube": False,
            "noticias_web": False,
            "fontes_confiaveis": False
        },
        "qualidade_conteudo": {
            "titulo_atrativo": False,
            "resumo_claro": False,
            "dados_atuais": False,
            "linguagem_acessivel": False,
            "estrutura_logica": False
        },
        "conformidade_regras": {
            "apresentacao_limpa": False,
            "sem_dados_tecnicos": False,
            "videos_formatados": False,
            "noticias_ao_final": False
        }
    }
    
    # Verificar estrutura do boilerplate
    print(f"\nVERIFICANDO ESTRUTURA DO BOILERPLATE:")
    print(f"=" * 50)
    
    # Verificar capa
    if "## 🖼️ Capa" in conteudo and "![Sistemas de Gestão Escolar Modernos 2024]" in conteudo:
        criterios["estrutura_boilerplate"]["capa"] = True
        print(f"OK - Capa: OK")
    else:
        print(f"ERRO - Capa: FALTANDO")
    
    # Verificar resumo executivo
    if "## 📋 Resumo Executivo" in conteudo and len(conteudo.split("## 📋 Resumo Executivo")[1].split("## 📊 Dados e Gráficos")[0]) > 200:
        criterios["estrutura_boilerplate"]["resumo_executivo"] = True
        print(f"✅ Resumo Executivo: OK")
    else:
        print(f"❌ Resumo Executivo: FALTANDO")
    
    # Verificar dados e gráficos
    if "## 📊 Dados e Gráficos" in conteudo and "![Funcionalidades Sistemas Gestão]" in conteudo:
        criterios["estrutura_boilerplate"]["dados_graficos"] = True
        print(f"✅ Dados e Gráficos: OK")
    else:
        print(f"❌ Dados e Gráficos: FALTANDO")
    
    # Verificar vídeos relacionados
    if "## 🎥 Vídeos Relacionados" in conteudo and conteudo.count("**Canal:**") >= 3:
        criterios["estrutura_boilerplate"]["videos_relacionados"] = True
        print(f"✅ Vídeos Relacionados: OK")
    else:
        print(f"❌ Vídeos Relacionados: FALTANDO")
    
    # Verificar notícias recentes
    if "## 📰 Notícias Recentes" in conteudo and conteudo.count("**Fonte:**") >= 3:
        criterios["estrutura_boilerplate"]["noticias_recentes"] = True
        print(f"✅ Notícias Recentes: OK")
    else:
        print(f"❌ Notícias Recentes: FALTANDO")
    
    # Verificar fontes e referências
    if "## 📚 Fontes e Referências" in conteudo and "**Fonte:**" in conteudo:
        criterios["estrutura_boilerplate"]["fontes_referencias"] = True
        print(f"✅ Fontes e Referências: OK")
    else:
        print(f"❌ Fontes e Referências: FALTANDO")
    
    # Verificar conclusão
    if "## 🎯 Conclusão" in conteudo and len(conteudo.split("## 🎯 Conclusão")[1].split("## 🏷️ Tags")[0]) > 300:
        criterios["estrutura_boilerplate"]["conclusao"] = True
        print(f"✅ Conclusão: OK")
    else:
        print(f"❌ Conclusão: FALTANDO")
    
    # Verificar tags
    if "## 🏷️ Tags" in conteudo and "Gestão Escolar" in conteudo:
        criterios["estrutura_boilerplate"]["tags"] = True
        print(f"✅ Tags: OK")
    else:
        print(f"❌ Tags: FALTANDO")
    
    # Verificar categoria
    if "## 📂 Categoria" in conteudo and "Gestão Escolar" in conteudo:
        criterios["estrutura_boilerplate"]["categoria"] = True
        print(f"✅ Categoria: OK")
    else:
        print(f"❌ Categoria: FALTANDO")
    
    # Verificar nível
    if "## 📊 Nível" in conteudo and ("Intermediário" in conteudo or "Básico" in conteudo or "Avançado" in conteudo):
        criterios["estrutura_boilerplate"]["nivel"] = True
        print(f"✅ Nível: OK")
    else:
        print(f"❌ Nível: FALTANDO")
    
    # Verificar função
    if "## 👥 Função" in conteudo and ("Diretor" in conteudo or "Coordenador" in conteudo or "Gestor" in conteudo):
        criterios["estrutura_boilerplate"]["funcao"] = True
        print(f"✅ Função: OK")
    else:
        print(f"❌ Função: FALTANDO")
    
    # Verificar enriquecimento MCP
    print(f"\nVERIFICANDO ENRIQUECIMENTO MCP:")
    print(f"=" * 50)
    
    # Verificar gráfico
    if "https://mdn.alipayobjects.com" in conteudo:
        criterios["enriquecimento_mcp"]["grafico_incluido"] = True
        print(f"✅ Gráfico MCP: OK")
    else:
        print(f"❌ Gráfico MCP: FALTANDO")
    
    # Verificar vídeos YouTube
    if conteudo.count("https://youtube.com/watch?v=") >= 3:
        criterios["enriquecimento_mcp"]["videos_youtube"] = True
        print(f"✅ Vídeos YouTube: OK")
    else:
        print(f"❌ Vídeos YouTube: FALTANDO")
    
    # Verificar notícias web
    if conteudo.count("**Fonte:**") >= 3:
        criterios["enriquecimento_mcp"]["noticias_web"] = True
        print(f"✅ Notícias Web: OK")
    else:
        print(f"❌ Notícias Web: FALTANDO")
    
    # Verificar fontes confiáveis
    if "Inep" in conteudo or "MEC" in conteudo or "gov.br" in conteudo:
        criterios["enriquecimento_mcp"]["fontes_confiaveis"] = True
        print(f"✅ Fontes Confiáveis: OK")
    else:
        print(f"❌ Fontes Confiáveis: FALTANDO")
    
    # Verificar qualidade do conteúdo
    print(f"\nVERIFICANDO QUALIDADE DO CONTEUDO:")
    print(f"=" * 50)
    
    # Verificar título atrativo
    if "Sistemas de Gestão Escolar Modernos" in conteudo and "2024" in conteudo:
        criterios["qualidade_conteudo"]["titulo_atrativo"] = True
        print(f"✅ Título Atrativo: OK")
    else:
        print(f"❌ Título Atrativo: FALTANDO")
    
    # Verificar resumo claro
    if "resumo" in conteudo.lower() and len(conteudo.split("## 📋 Resumo Executivo")[1].split("## 📊 Dados e Gráficos")[0]) > 200:
        criterios["qualidade_conteudo"]["resumo_claro"] = True
        print(f"✅ Resumo Claro: OK")
    else:
        print(f"❌ Resumo Claro: FALTANDO")
    
    # Verificar dados atuais
    if "2024" in conteudo and ("47,1 milhões" in conteudo or "179,3 mil" in conteudo):
        criterios["qualidade_conteudo"]["dados_atuais"] = True
        print(f"✅ Dados Atuais: OK")
    else:
        print(f"❌ Dados Atuais: FALTANDO")
    
    # Verificar linguagem acessível
    if len(conteudo.split()) > 1000 and "##" in conteudo:
        criterios["qualidade_conteudo"]["linguagem_acessivel"] = True
        print(f"✅ Linguagem Acessível: OK")
    else:
        print(f"❌ Linguagem Acessível: FALTANDO")
    
    # Verificar estrutura lógica
    if conteudo.count("##") >= 8:
        criterios["qualidade_conteudo"]["estrutura_logica"] = True
        print(f"✅ Estrutura Lógica: OK")
    else:
        print(f"❌ Estrutura Lógica: FALTANDO")
    
    # Verificar conformidade com regras
    print(f"\nVERIFICANDO CONFORMIDADE COM REGRAS:")
    print(f"=" * 50)
    
    # Verificar apresentação limpa
    if not ("backup" in conteudo.lower() or "temp" in conteudo.lower() or "temporary" in conteudo.lower()):
        criterios["conformidade_regras"]["apresentacao_limpa"] = True
        print(f"✅ Apresentação Limpa: OK")
    else:
        print(f"❌ Apresentação Limpa: FALTANDO")
    
    # Verificar sem dados técnicos
    if not ("data_uri" in conteudo.lower() or "imgur" in conteudo.lower() or "github" in conteudo.lower()):
        criterios["conformidade_regras"]["sem_dados_tecnicos"] = True
        print(f"✅ Sem Dados Técnicos: OK")
    else:
        print(f"❌ Sem Dados Técnicos: FALTANDO")
    
    # Verificar vídeos formatados
    if conteudo.count("**Canal:**") >= 3 and conteudo.count("**Link:**") >= 3:
        criterios["conformidade_regras"]["videos_formatados"] = True
        print(f"✅ Vídeos Formatados: OK")
    else:
        print(f"❌ Vídeos Formatados: FALTANDO")
    
    # Verificar notícias ao final
    if conteudo.find("## 📰 Notícias Recentes") > conteudo.find("## 🎥 Vídeos Relacionados"):
        criterios["conformidade_regras"]["noticias_ao_final"] = True
        print(f"✅ Notícias ao Final: OK")
    else:
        print(f"❌ Notícias ao Final: FALTANDO")
    
    # Calcular pontuação
    total_criterios = 0
    criterios_aprovados = 0
    
    for categoria in criterios.values():
        for criterio, aprovado in categoria.items():
            total_criterios += 1
            if aprovado:
                criterios_aprovados += 1
    
    pontuacao = (criterios_aprovados / total_criterios) * 100
    
    print(f"\nRESULTADO DA CUradoria:")
    print(f"=" * 70)
    print(f"Criterios aprovados: {criterios_aprovados}/{total_criterios}")
    print(f"Pontuacao: {pontuacao:.1f}%")
    
    # Verificar se passou na curadoria (mínimo 80%)
    aprovado = pontuacao >= 80
    
    if aprovado:
        print(f"✅ APROVADO na curadoria!")
        print(f"   Pontuacao acima do minimo (80%)")
    else:
        print(f"❌ REPROVADO na curadoria!")
        print(f"   Pontuacao abaixo do minimo (80%)")
        print(f"   Necessario: {80 - pontuacao:.1f}% a mais")
    
    # Salvar dados da curadoria
    dados_curadoria = {
        "data_curadoria": datetime.now().isoformat(),
        "arquivo_analisado": arquivo_artigo,
        "criterios": criterios,
        "total_criterios": total_criterios,
        "criterios_aprovados": criterios_aprovados,
        "pontuacao": pontuacao,
        "aprovado": aprovado,
        "necessita_correcao": not aprovado
    }
    
    with open("curadoria_artigo_sistemas_gestao.json", "w", encoding="utf-8") as f:
        json.dump(dados_curadoria, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\nCUradoria CONCLUIDA!")
    print(f"   Dados salvos em curadoria_artigo_sistemas_gestao.json")
    print(f"   Status: {'APROVADO' if aprovado else 'REPROVADO'}")
    
    return aprovado

def main():
    print("CUradoria OBRIGATORIA - ARTIGO SISTEMAS GESTAO ESCOLAR")
    print("=" * 70)
    
    aprovado = curadoria_artigo_sistemas_gestao()
    
    if aprovado:
        print(f"\nARTIGO APROVADO!")
        print(f"   Pronto para sincronizacao com Notion")
        print(f"   Conformidade com boilerplate confirmada")
    else:
        print(f"\nARTIGO REPROVADO!")
        print(f"   Necessario aplicar correcoes")
        print(f"   Re-executar curadoria apos correcoes")
    
    return aprovado

if __name__ == "__main__":
    main()
