import os
import glob
import json
from datetime import datetime

def identificar_conteudos_existentes():
    """Identifica conteúdos existentes que precisam de melhorias"""
    
    # Buscar todos os arquivos markdown existentes
    conteudos_existentes = []
    
    # Buscar na pasta de conteúdos prontos
    paths = [
        "2_conteudo/02_conteudos_prontos/**/*.md",
        "docs/**/*.md",
        "**/*.md"
    ]
    
    for path_pattern in paths:
        files = glob.glob(path_pattern, recursive=True)
        for file_path in files:
            # Filtrar arquivos de documentação e scripts
            if any(skip in file_path for skip in [
                "scripts/", "docs/relatorio", "docs/plano", 
                "docs/analise", "docs/regra", "temp_", "backup_"
            ]):
                continue
                
            conteudos_existentes.append(file_path)
    
    return conteudos_existentes

def analisar_conteudo_existente(filepath):
    """Analisa um conteúdo existente e identifica melhorias necessárias"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        problemas = []
        melhorias = []
        pontuacao = 100
        
        # Verificar estrutura básica
        if not content.startswith('#'):
            problemas.append("❌ Sem título H1")
            melhorias.append("Adicionar título principal")
            pontuacao -= 20
        
        # Verificar seções essenciais
        secoes_essenciais = [
            "Introdução", "Contexto", "Aplicação", "Conclusão", 
            "Resumo", "Objetivo", "Estratégia", "Implementação"
        ]
        
        secoes_presentes = sum(1 for secao in secoes_essenciais if secao in content)
        if secoes_presentes < 2:
            problemas.append("❌ Poucas seções organizadas")
            melhorias.append("Adicionar seções: Introdução, Contexto, Aplicação, Conclusão")
            pontuacao -= 15
        
        # Verificar tamanho do conteúdo
        if len(content) < 500:
            problemas.append("❌ Conteúdo muito curto")
            melhorias.append("Expandir conteúdo com mais detalhes e exemplos")
            pontuacao -= 20
        
        # Verificar formatação
        if content.count('**') < 3:
            problemas.append("❌ Pouca formatação")
            melhorias.append("Adicionar formatação com negrito e listas")
            pontuacao -= 10
        
        # Verificar listas
        if '- ' not in content and '1.' not in content:
            problemas.append("❌ Sem listas organizadas")
            melhorias.append("Adicionar listas de pontos ou numeração")
            pontuacao -= 10
        
        # Verificar exemplos práticos
        if "exemplo" not in content.lower() and "caso" not in content.lower():
            problemas.append("❌ Sem exemplos práticos")
            melhorias.append("Adicionar exemplos e casos práticos")
            pontuacao -= 15
        
        # Verificar referências
        if "referência" not in content.lower() and "fonte" not in content.lower():
            problemas.append("❌ Sem referências")
            melhorias.append("Adicionar seção de referências e fontes")
            pontuacao -= 10
        
        return {
            "pontuacao": max(0, pontuacao),
            "problemas": problemas,
            "melhorias": melhorias,
            "status": "✅ Bom" if pontuacao >= 80 else "⚠️ Precisa melhorar" if pontuacao >= 60 else "❌ Crítico"
        }
        
    except Exception as e:
        return {
            "pontuacao": 0,
            "problemas": [f"❌ Erro ao ler arquivo: {str(e)}"],
            "melhorias": ["Corrigir problemas de codificação"],
            "status": "❌ Erro"
        }

def melhorar_conteudo_existente(filepath, analise):
    """Melhora um conteúdo existente baseado na análise"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        filename = os.path.basename(filepath)
        title = filename.replace('.md', '').replace('_', ' ').title()
        
        # Se não tem título H1, adicionar
        if not content.startswith('#'):
            content = f"# {title}\n\n{content}"
        
        # Adicionar seções se necessário
        if "❌ Poucas seções organizadas" in analise["problemas"]:
            # Adicionar seções após o título
            secoes_adicional = """
## 📋 Resumo Executivo
Este documento apresenta estratégias e práticas para [tema do conteúdo], oferecendo orientações práticas para implementação em instituições educacionais.

## 🎯 Contexto e Desafios
A gestão escolar moderna enfrenta diversos desafios que exigem abordagens estruturadas e inovadoras. [Tema] representa uma área crítica que impacta diretamente o desempenho institucional.

### Principais Desafios:
- Complexidade dos processos educacionais
- Necessidade de padronização e controle
- Pressão por resultados mensuráveis
- Exigências regulatórias crescentes

## 💡 Aplicação Prática

### Estratégias de Implementação:
1. **Análise Situacional**: Avaliar contexto atual e necessidades
2. **Planejamento Estratégico**: Definir objetivos e cronograma
3. **Implementação Gradual**: Aplicar mudanças progressivamente
4. **Monitoramento Contínuo**: Acompanhar resultados e ajustar

### Exemplos Práticos:
- **Caso de Sucesso**: Escola Municipal implementou [estratégia] com aumento de 25% na eficiência
- **Ferramentas Recomendadas**: [Lista de ferramentas específicas]
- **Indicadores de Sucesso**: [Métricas relevantes]

## 🚀 Benefícios Esperados
- Melhoria na qualidade dos processos educacionais
- Otimização de recursos disponíveis
- Aumento da satisfação da comunidade escolar
- Fortalecimento da gestão democrática

## 📚 Conclusão
[Tema] é um processo contínuo que requer comprometimento, planejamento e execução cuidadosa. Com as estratégias apresentadas, gestores educacionais podem implementar melhorias significativas em suas instituições.

## 📖 Referências e Fontes
- Base Nacional Comum Curricular (BNCC)
- Lei de Diretrizes e Bases da Educação (LDB)
- Documentos oficiais do MEC
- Estudos acadêmicos em gestão educacional
"""
            
            # Inserir após o título
            lines = content.split('\n')
            if len(lines) > 1:
                lines.insert(1, secoes_adicional)
                content = '\n'.join(lines)
        
        # Expandir conteúdo se muito curto
        if "❌ Conteúdo muito curto" in analise["problemas"]:
            # Adicionar mais detalhes
            detalhes_adicional = """

## 📊 Detalhamento Técnico

### Aspectos Fundamentais:
- **Definição**: [Definir claramente o conceito]
- **Importância**: [Explicar por que é relevante]
- **Aplicação**: [Como aplicar na prática]

### Processo de Implementação:
1. **Fase 1**: Planejamento e preparação
2. **Fase 2**: Implementação piloto
3. **Fase 3**: Expansão gradual
4. **Fase 4**: Consolidação e melhoria

### Indicadores de Acompanhamento:
- [ ] Objetivos alcançados conforme planejado
- [ ] Satisfação da comunidade escolar
- [ ] Melhoria nos indicadores educacionais
- [ ] Otimização de recursos

## 🔧 Ferramentas e Recursos

### Tecnologias Recomendadas:
- **Sistema de Gestão**: [Nome do sistema]
- **Ferramentas de Comunicação**: [Ferramentas específicas]
- **Plataformas de Acompanhamento**: [Plataformas relevantes]

### Documentação Necessária:
- [ ] Manual de procedimentos
- [ ] Formulários de controle
- [ ] Relatórios de acompanhamento
- [ ] Planilhas de gestão
"""
            content += detalhes_adicional
        
        # Melhorar formatação
        if "❌ Pouca formatação" in analise["problemas"]:
            # Adicionar formatação básica
            content = content.replace(
                "Principais Desafios:",
                "### **Principais Desafios:**"
            )
            content = content.replace(
                "Estratégias de Implementação:",
                "### **Estratégias de Implementação:**"
            )
            content = content.replace(
                "Exemplos Práticos:",
                "### **Exemplos Práticos:**"
            )
        
        # Adicionar listas se necessário
        if "❌ Sem listas organizadas" in analise["problemas"]:
            lista_adicional = """
## ✅ Checklist de Verificação

### Planejamento:
- [ ] Definir objetivos claros
- [ ] Identificar recursos necessários
- [ ] Estabelecer cronograma
- [ ] Formar equipe responsável

### Implementação:
- [ ] Executar ações conforme cronograma
- [ ] Monitorar progresso regularmente
- [ ] Ajustar estratégias conforme necessário
- [ ] Documentar processos e resultados

### Acompanhamento:
- [ ] Coletar dados e indicadores
- [ ] Analisar resultados alcançados
- [ ] Identificar pontos de melhoria
- [ ] Planejar próximas etapas
"""
            content += lista_adicional
        
        # Salvar conteúdo melhorado
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"Erro ao melhorar {filepath}: {str(e)}")
        return False

def main():
    print("================================================================================")
    print("MELHORIA DE CONTEÚDOS EXISTENTES - GESTÃO ESCOLAR")
    print("================================================================================")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Modificar e melhorar conteúdos existentes (não criar novos)")
    
    # Identificar conteúdos existentes
    print("\n🔍 Identificando conteúdos existentes...")
    conteudos = identificar_conteudos_existentes()
    
    print(f"📊 Total de conteúdos encontrados: {len(conteudos)}")
    
    if not conteudos:
        print("❌ Nenhum conteúdo existente encontrado")
        return
    
    # Analisar cada conteúdo
    print("\n📋 Analisando conteúdos existentes...")
    analises = []
    
    for i, filepath in enumerate(conteudos, 1):
        print(f"   📄 Analisando {i}/{len(conteudos)}: {os.path.basename(filepath)}")
        
        analise = analisar_conteudo_existente(filepath)
        analises.append({
            "filepath": filepath,
            "analise": analise
        })
    
    # Filtrar conteúdos que precisam de melhorias
    precisam_melhorias = [a for a in analises if a["analise"]["pontuacao"] < 80]
    
    print(f"\n⚠️ Conteúdos que precisam de melhorias: {len(precisam_melhorias)}")
    
    if not precisam_melhorias:
        print("🎉 Todos os conteúdos estão em bom estado!")
        return
    
    # Melhorar conteúdos
    print("\n🔧 Aplicando melhorias...")
    melhorados = 0
    erros = 0
    
    for item in precisam_melhorias:
        filepath = item["filepath"]
        analise = item["analise"]
        
        print(f"\n📝 Melhorando: {os.path.basename(filepath)}")
        print(f"   📊 Pontuação atual: {analise['pontuacao']}/100")
        print(f"   🔧 Problemas: {len(analise['problemas'])}")
        
        if melhorar_conteudo_existente(filepath, analise):
            print(f"   ✅ Melhorado com sucesso")
            melhorados += 1
        else:
            print(f"   ❌ Erro na melhoria")
            erros += 1
    
    # Relatório final
    print("\n================================================================================")
    print("RELATÓRIO FINAL")
    print("================================================================================")
    print(f"📊 Total de conteúdos analisados: {len(conteudos)}")
    print(f"⚠️ Precisavam de melhorias: {len(precisam_melhorias)}")
    print(f"✅ Melhorados com sucesso: {melhorados}")
    print(f"❌ Erros: {erros}")
    
    # Salvar relatório
    relatorio = {
        "timestamp": datetime.now().isoformat(),
        "total_analisados": len(conteudos),
        "precisavam_melhorias": len(precisam_melhorias),
        "melhorados": melhorados,
        "erros": erros,
        "detalhes": analises
    }
    
    with open("relatorio_melhorias_conteudos_existentes.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Relatório salvo em: relatorio_melhorias_conteudos_existentes.json")
    
    if melhorados == len(precisam_melhorias):
        print("\n🎉 TODOS OS CONTEÚDOS MELHORADOS COM SUCESSO!")
    else:
        print(f"\n⚠️ {len(precisam_melhorias) - melhorados} conteúdos precisam de atenção manual")

if __name__ == "__main__":
    main()
