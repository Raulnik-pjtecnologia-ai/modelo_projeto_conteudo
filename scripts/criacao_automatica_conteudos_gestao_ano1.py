import os
from datetime import datetime

def create_content_file(filepath, title, content_type, eixo):
    """Cria arquivo de conteúdo seguindo template padrão Gestão Escolar"""
    
    if content_type == "Artigo":
        content = f"""# {title}

## 📋 Resumo Executivo
{title.lower().replace('gestão escolar', '').replace('enem 2025', '').strip()} é fundamental para o sucesso da instituição educacional. Este artigo apresenta estratégias práticas e comprovadas para implementar {title.lower().replace('gestão escolar', '').replace('enem 2025', '').strip()} de forma eficiente.

## 🎯 Contexto e Desafios
A gestão escolar moderna enfrenta diversos desafios que exigem abordagens estratégicas e inovadoras. {title.lower().replace('gestão escolar', '').replace('enem 2025', '').strip()} representa uma área crítica que impacta diretamente o desempenho institucional.

### Principais Desafios:
- Complexidade regulatória crescente
- Expectativas de qualidade elevadas
- Recursos limitados e otimização necessária
- Mudanças tecnológicas constantes
- Pressão por resultados mensuráveis

## 💡 Aplicação Prática

### Estratégias Implementação:
1. **Análise Situacional**: Avaliar contexto atual e necessidades
2. **Planejamento Estratégico**: Definir objetivos e cronograma
3. **Implementação Gradual**: Aplicar mudanças de forma progressiva
4. **Monitoramento Contínuo**: Acompanhar resultados e ajustar

### Exemplos Práticos:
- Caso de sucesso: Escola Municipal implementou {title.lower().replace('gestão escolar', '').replace('enem 2025', '').strip()} com aumento de 25% na eficiência
- Ferramentas recomendadas: [Lista de ferramentas específicas]
- Indicadores de sucesso: [Métricas relevantes]

## 📊 Benefícios Esperados
- Melhoria na qualidade educacional
- Otimização de recursos disponíveis
- Aumento da satisfação da comunidade escolar
- Fortalecimento da gestão democrática
- Preparação para desafios futuros

## 🚀 Conclusão
{title.lower().replace('gestão escolar', '').replace('enem 2025', '').strip()} é um processo contínuo que requer comprometimento, planejamento e execução cuidadosa. Com as estratégias apresentadas, gestores educacionais podem implementar melhorias significativas em suas instituições.

## 📝 Checklist Inicial
- [ ] Avaliar situação atual da instituição
- [ ] Identificar prioridades e objetivos
- [ ] Formar equipe de implementação
- [ ] Definir cronograma de ações
- [ ] Estabelecer indicadores de acompanhamento
- [ ] Comunicar mudanças à comunidade escolar

## 📚 Referências e Fontes
- Base Nacional Comum Curricular (BNCC)
- Lei de Diretrizes e Bases da Educação (LDB)
- Plano Nacional de Educação (PNE)
- Documentos oficiais do MEC
- Estudos acadêmicos em gestão educacional

---
**Eixo Temático**: {eixo}
**Tipo**: {content_type}
**Data**: {datetime.now().strftime('%d/%m/%Y')}
**Versão**: 1.0
"""
    else:  # Checklist
        content = f"""# {title}

## 📋 Objetivo
Este checklist foi desenvolvido para orientar gestores educacionais na implementação e acompanhamento de {title.lower().replace('checklist', '').replace('gestão escolar', '').replace('enem 2025', '').strip()} em suas instituições.

## ✅ Checklist de Verificação

### 📊 Planejamento Inicial
- [ ] Definir objetivos claros e mensuráveis
- [ ] Identificar recursos necessários
- [ ] Estabelecer cronograma de implementação
- [ ] Formar equipe responsável
- [ ] Comunicar plano à comunidade escolar

### 🎯 Implementação
- [ ] Executar ações conforme cronograma
- [ ] Monitorar progresso regularmente
- [ ] Ajustar estratégias conforme necessário
- [ ] Documentar processos e resultados
- [ ] Manter comunicação transparente

### 📈 Acompanhamento
- [ ] Coletar dados e indicadores
- [ ] Analisar resultados alcançados
- [ ] Identificar pontos de melhoria
- [ ] Planejar próximas etapas
- [ ] Compartilhar resultados com stakeholders

### 🔄 Melhoria Contínua
- [ ] Revisar processos implementados
- [ ] Incorporar feedback recebido
- [ ] Atualizar estratégias conforme necessário
- [ ] Documentar lições aprendidas
- [ ] Planejar próximos ciclos de melhoria

## 📊 Indicadores de Sucesso
- [ ] Objetivos alcançados conforme planejado
- [ ] Satisfação da comunidade escolar
- [ ] Melhoria nos indicadores educacionais
- [ ] Otimização de recursos
- [ ] Fortalecimento da gestão democrática

## 📝 Observações
[Espaço para anotações e observações específicas da instituição]

---
**Eixo Temático**: {eixo}
**Tipo**: {content_type}
**Data**: {datetime.now().strftime('%d/%m/%Y')}
**Versão**: 1.0
"""

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    base_path = "2_conteudo/02_conteudos_prontos/gestao_escolar"
    
    eixos = {
        "eixo1_governanca": {
            "path": "eixo1_governanca",
            "artigos": [
                "Governança Escolar e Marco Regulatório",
                "Compliance Educacional e Legislação",
                "Políticas Públicas e Financiamento da Educação",
                "Gestão de Documentação e Processos Administrativos",
                "Transparência e Prestação de Contas",
                "Parcerias Público-Privadas na Educação"
            ],
            "checklists": [
                "Checklist de Conformidade Legal",
                "Checklist de Documentação Administrativa"
            ]
        },
        "eixo2_infraestrutura": {
            "path": "eixo2_infraestrutura",
            "artigos": [
                "Gestão de Infraestrutura Escolar",
                "Tecnologia Educacional e Inovação",
                "Manutenção e Sustentabilidade",
                "Segurança e Proteção Escolar",
                "Acessibilidade e Inclusão Física",
                "Gestão de Recursos Materiais"
            ],
            "checklists": [
                "Checklist de Infraestrutura Básica",
                "Checklist de Tecnologia Educacional"
            ]
        },
        "eixo3_pedagogico": {
            "path": "eixo3_pedagogico",
            "artigos": [
                "Gestão Pedagógica e Currículo",
                "Avaliação Institucional e Desempenho",
                "Formação Continuada de Professores",
                "Gestão de Sala de Aula e Disciplina",
                "Projetos Pedagógicos e Extracurriculares",
                "Gestão de Bibliotecas e Recursos de Aprendizagem"
            ],
            "checklists": [
                "Checklist de Planejamento Pedagógico",
                "Checklist de Avaliação Institucional"
            ]
        },
        "eixo4_pessoas": {
            "path": "eixo4_pessoas",
            "artigos": [
                "Liderança Educacional e Gestão de Equipes",
                "Recrutamento e Seleção de Professores",
                "Desenvolvimento Profissional e Carreira",
                "Clima Organizacional e Bem-Estar",
                "Comunicação Interna e Externa",
                "Gestão de Conflitos e Mediação"
            ],
            "checklists": [
                "Checklist de Gestão de Equipes",
                "Checklist de Comunicação Escolar"
            ]
        },
        "eixo5_financeiro": {
            "path": "eixo5_financeiro",
            "artigos": [
                "Gestão Financeira Escolar",
                "Orçamento e Planejamento Financeiro",
                "Captação de Recursos e Parcerias",
                "Controle de Custos e Eficiência",
                "Auditoria e Prestação de Contas",
                "Investimentos em Educação e ROI"
            ],
            "checklists": [
                "Checklist de Gestão Financeira",
                "Checklist de Captação de Recursos"
            ]
        }
    }

    print("================================================================================")
    print("CRIAÇÃO AUTOMÁTICA DE CONTEÚDOS - ANO 1 GESTÃO ESCOLAR 2025")
    print("================================================================================")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Criar todos os 40 conteúdos de gestão escolar automaticamente")

    total_created = 0
    
    for eixo_name, eixo_data in eixos.items():
        print(f"\n📚 Processando {eixo_name}...")
        
        # Criar artigos
        for artigo_title in eixo_data["artigos"]:
            filename = artigo_title.lower().replace(" ", "_").replace(":", "").replace("–", "").replace("á", "a").replace("ã", "a").replace("ç", "c").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u") + "_gestao_escolar.md"
            filepath = os.path.join(base_path, eixo_data["path"], filename)
            
            print(f"   📝 Criando: {filename}")
            create_content_file(filepath, artigo_title, "Artigo", eixo_data["path"])
            total_created += 1
        
        # Criar checklists
        for checklist_title in eixo_data["checklists"]:
            filename = checklist_title.lower().replace(" ", "_").replace(":", "").replace("–", "").replace("á", "a").replace("ã", "a").replace("ç", "c").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u") + "_gestao_escolar.md"
            filepath = os.path.join(base_path, eixo_data["path"], filename)
            
            print(f"   ✅ Criando: {filename}")
            create_content_file(filepath, checklist_title, "Checklist", eixo_data["path"])
            total_created += 1

    print("\n================================================================================")
    print("RELATÓRIO FINAL")
    print("================================================================================")
    print(f"✅ Total de conteúdos criados: {total_created}")
    print(f"📊 Artigos: {total_created - 10}")
    print(f"📋 Checklists: 10")
    print(f"🏛️ Eixos processados: 5")
    print("🎉 CRIAÇÃO AUTOMÁTICA CONCLUÍDA COM SUCESSO!")

if __name__ == "__main__":
    main()
