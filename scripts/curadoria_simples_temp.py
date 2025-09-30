import os
import json
from datetime import datetime

def curadoria_simples():
    """Curadoria simplificada sem emojis."""
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
    
    # Critérios básicos
    criterios_aprovados = 0
    total_criterios = 11
    
    print(f"\nVERIFICANDO ESTRUTURA DO BOILERPLATE:")
    print(f"=" * 50)
    
    # Verificar capa
    if "## 🖼️ Capa" in conteudo and "![Sistemas de Gestão Escolar Modernos 2024]" in conteudo:
        criterios_aprovados += 1
        print(f"OK - Capa: OK")
    else:
        print(f"ERRO - Capa: FALTANDO")
    
    # Verificar resumo executivo
    if "## 📋 Resumo Executivo" in conteudo:
        criterios_aprovados += 1
        print(f"OK - Resumo Executivo: OK")
    else:
        print(f"ERRO - Resumo Executivo: FALTANDO")
    
    # Verificar dados e gráficos
    if "## 📊 Dados e Gráficos" in conteudo and "![Funcionalidades Sistemas Gestão]" in conteudo:
        criterios_aprovados += 1
        print(f"OK - Dados e Graficos: OK")
    else:
        print(f"ERRO - Dados e Graficos: FALTANDO")
    
    # Verificar vídeos relacionados
    if "## 🎥 Vídeos Relacionados" in conteudo and conteudo.count("**Canal:**") >= 3:
        criterios_aprovados += 1
        print(f"OK - Videos Relacionados: OK")
    else:
        print(f"ERRO - Videos Relacionados: FALTANDO")
    
    # Verificar notícias recentes
    if "## 📰 Notícias Recentes" in conteudo and conteudo.count("**Fonte:**") >= 3:
        criterios_aprovados += 1
        print(f"OK - Noticias Recentes: OK")
    else:
        print(f"ERRO - Noticias Recentes: FALTANDO")
    
    # Verificar fontes e referências
    if "## 📚 Fontes e Referências" in conteudo and "**Fonte:**" in conteudo:
        criterios_aprovados += 1
        print(f"OK - Fontes e Referencias: OK")
    else:
        print(f"ERRO - Fontes e Referencias: FALTANDO")
    
    # Verificar conclusão
    if "## 🎯 Conclusão" in conteudo:
        criterios_aprovados += 1
        print(f"OK - Conclusao: OK")
    else:
        print(f"ERRO - Conclusao: FALTANDO")
    
    # Verificar tags
    if "## 🏷️ Tags" in conteudo and "Gestão Escolar" in conteudo:
        criterios_aprovados += 1
        print(f"OK - Tags: OK")
    else:
        print(f"ERRO - Tags: FALTANDO")
    
    # Verificar categoria
    if "## 📂 Categoria" in conteudo and "Gestão Escolar" in conteudo:
        criterios_aprovados += 1
        print(f"OK - Categoria: OK")
    else:
        print(f"ERRO - Categoria: FALTANDO")
    
    # Verificar nível
    if "## 📊 Nível" in conteudo and ("Intermediário" in conteudo or "Básico" in conteudo or "Avançado" in conteudo):
        criterios_aprovados += 1
        print(f"OK - Nivel: OK")
    else:
        print(f"ERRO - Nivel: FALTANDO")
    
    # Verificar função
    if "## 👥 Função" in conteudo and ("Diretor" in conteudo or "Coordenador" in conteudo or "Gestor" in conteudo):
        criterios_aprovados += 1
        print(f"OK - Funcao: OK")
    else:
        print(f"ERRO - Funcao: FALTANDO")
    
    # Verificar enriquecimento MCP
    print(f"\nVERIFICANDO ENRIQUECIMENTO MCP:")
    print(f"=" * 50)
    
    # Verificar gráfico
    if "https://mdn.alipayobjects.com" in conteudo:
        print(f"OK - Grafico MCP: OK")
    else:
        print(f"ERRO - Grafico MCP: FALTANDO")
    
    # Verificar vídeos YouTube
    if conteudo.count("https://youtube.com/watch?v=") >= 3:
        print(f"OK - Videos YouTube: OK")
    else:
        print(f"ERRO - Videos YouTube: FALTANDO")
    
    # Verificar notícias web
    if conteudo.count("**Fonte:**") >= 3:
        print(f"OK - Noticias Web: OK")
    else:
        print(f"ERRO - Noticias Web: FALTANDO")
    
    # Verificar fontes confiáveis
    if "Inep" in conteudo or "MEC" in conteudo or "gov.br" in conteudo:
        print(f"OK - Fontes Confiaveis: OK")
    else:
        print(f"ERRO - Fontes Confiaveis: FALTANDO")
    
    # Calcular pontuação
    pontuacao = (criterios_aprovados / total_criterios) * 100
    
    print(f"\nRESULTADO DA CUradoria:")
    print(f"=" * 70)
    print(f"Criterios aprovados: {criterios_aprovados}/{total_criterios}")
    print(f"Pontuacao: {pontuacao:.1f}%")
    
    # Verificar se passou na curadoria (mínimo 80%)
    aprovado = pontuacao >= 80
    
    if aprovado:
        print(f"APROVADO na curadoria!")
        print(f"   Pontuacao acima do minimo (80%)")
    else:
        print(f"REPROVADO na curadoria!")
        print(f"   Pontuacao abaixo do minimo (80%)")
        print(f"   Necessario: {80 - pontuacao:.1f}% a mais")
    
    # Salvar dados da curadoria
    dados_curadoria = {
        "data_curadoria": datetime.now().isoformat(),
        "arquivo_analisado": arquivo_artigo,
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
    
    aprovado = curadoria_simples()
    
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
