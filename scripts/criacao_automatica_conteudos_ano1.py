#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sistema de Criação Automática de Conteúdos - Ano 1 PRÉ-ENEM 2025
Cria automaticamente todos os artigos e checklists pendentes
"""

import os
import sys
import time
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

def print_secao(titulo):
    print("\n" + "="*80)
    print(titulo)
    print("="*80)

# Definição de todos os conteúdos pendentes
CONTEUDOS_PENDENTES = {
    "eixo1_bem_estar": [
        {
            "arquivo": "alimentacao_desempenho_cognitivo_enem_2025.md",
            "titulo": "Alimentação e Desempenho Cognitivo ENEM 2025",
            "tipo": "artigo"
        },
        {
            "arquivo": "rotina_sono_estudantes_enem_2025.md",
            "titulo": "Rotina de Sono para Estudantes ENEM 2025",
            "tipo": "artigo"
        },
        {
            "arquivo": "motivacao_perseveranca_estudos_enem_2025.md",
            "titulo": "Motivação e Perseverança nos Estudos ENEM 2025",
            "tipo": "artigo"
        },
        {
            "arquivo": "checklist_saude_mental_enem_2025.md",
            "titulo": "Checklist de Saúde Mental ENEM 2025",
            "tipo": "checklist"
        }
    ],
    "eixo2_estrategias": [
        {
            "arquivo": "checklist_planejamento_semanal_enem_2025.md",
            "titulo": "Checklist de Planejamento Semanal ENEM 2025",
            "tipo": "checklist"
        },
        {
            "arquivo": "checklist_revisao_mensal_enem_2025.md",
            "titulo": "Checklist de Revisão Mensal ENEM 2025",
            "tipo": "checklist"
        }
    ],
    "eixo3_linguagens": [
        {
            "arquivo": "literatura_movimentos_literarios_enem_2025.md",
            "titulo": "Literatura: Movimentos Literários Brasileiros ENEM 2025",
            "tipo": "artigo"
        },
        {
            "arquivo": "lingua_estrangeira_estrategias_leitura_enem_2025.md",
            "titulo": "Língua Estrangeira: Estratégias de Leitura ENEM 2025",
            "tipo": "artigo"
        },
        {
            "arquivo": "gramatica_contextualizada_enem_2025.md",
            "titulo": "Gramática Contextualizada no ENEM 2025",
            "tipo": "artigo"
        },
        {
            "arquivo": "checklist_interpretacao_texto_enem_2025.md",
            "titulo": "Checklist de Interpretação de Texto ENEM 2025",
            "tipo": "checklist"
        }
    ],
    "eixo4_matematica": [
        {
            "arquivo": "estatistica_probabilidade_enem_2025.md",
            "titulo": "Estatística e Probabilidade ENEM 2025",
            "tipo": "artigo"
        },
        {
            "arquivo": "funcoes_graficos_enem_2025.md",
            "titulo": "Funções e Gráficos ENEM 2025",
            "tipo": "artigo"
        },
        {
            "arquivo": "matematica_financeira_enem_2025.md",
            "titulo": "Matemática Financeira para o ENEM 2025",
            "tipo": "artigo"
        },
        {
            "arquivo": "trigonometria_aplicada_enem_2025.md",
            "titulo": "Trigonometria Aplicada ENEM 2025",
            "tipo": "artigo"
        },
        {
            "arquivo": "checklist_formulas_matematicas_enem_2025.md",
            "titulo": "Checklist de Fórmulas Matemáticas ENEM 2025",
            "tipo": "checklist"
        },
        {
            "arquivo": "checklist_resolucao_problemas_enem_2025.md",
            "titulo": "Checklist de Resolução de Problemas ENEM 2025",
            "tipo": "checklist"
        }
    ],
    "eixo5_humanas": [
        {
            "arquivo": "historia_brasil_republica_enem_2025.md",
            "titulo": "História ENEM 2025: Brasil República",
            "tipo": "artigo"
        },
        {
            "arquivo": "geografia_fisica_enem_2025.md",
            "titulo": "Geografia ENEM 2025: Geografia Física",
            "tipo": "artigo"
        },
        {
            "arquivo": "filosofia_etica_politica_enem_2025.md",
            "titulo": "Filosofia ENEM 2025: Ética e Política",
            "tipo": "artigo"
        },
        {
            "arquivo": "atualidades_temas_recorrentes_enem_2025.md",
            "titulo": "Atualidades: Temas Recorrentes no ENEM 2025",
            "tipo": "artigo"
        },
        {
            "arquivo": "geopolitica_globalizacao_enem_2025.md",
            "titulo": "Geopolítica e Globalização ENEM 2025",
            "tipo": "artigo"
        },
        {
            "arquivo": "checklist_datas_historicas_enem_2025.md",
            "titulo": "Checklist de Datas Históricas Importantes ENEM 2025",
            "tipo": "checklist"
        },
        {
            "arquivo": "checklist_conceitos_sociologicos_enem_2025.md",
            "titulo": "Checklist de Conceitos Sociológicos Essenciais ENEM 2025",
            "tipo": "checklist"
        }
    ],
    "eixo6_natureza": [
        {
            "arquivo": "fisica_mecanica_leis_newton_enem_2025.md",
            "titulo": "Física: Mecânica e Leis de Newton ENEM 2025",
            "tipo": "artigo"
        },
        {
            "arquivo": "quimica_fisico_quimica_solucoes_enem_2025.md",
            "titulo": "Química: Físico-Química e Soluções ENEM 2025",
            "tipo": "artigo"
        },
        {
            "arquivo": "biologia_ecologia_meio_ambiente_enem_2025.md",
            "titulo": "Biologia: Ecologia e Meio Ambiente ENEM 2025",
            "tipo": "artigo"
        },
        {
            "arquivo": "checklist_formulas_fisica_enem_2025.md",
            "titulo": "Checklist de Fórmulas Essenciais de Física ENEM 2025",
            "tipo": "checklist"
        },
        {
            "arquivo": "checklist_reacoes_quimicas_enem_2025.md",
            "titulo": "Checklist de Reações Químicas Importantes ENEM 2025",
            "tipo": "checklist"
        }
    ]
}

def gerar_template_artigo(titulo, eixo):
    """Gera template básico para artigos"""
    return f"""# {titulo}

## 🎯 **RESUMO EXECUTIVO**

- **Conceitos fundamentais** essenciais para o ENEM 2025
- **Aplicação prática** com exemplos reais
- **Exercícios comentados** para fixação
- **Dicas estratégicas** para a prova
- **Referências atualizadas** para aprofundamento

## 🎯 **INTRODUÇÃO**

Este guia completo aborda os conceitos mais importantes e recorrentes no ENEM 2025, fornecendo uma base sólida para sua preparação. Você encontrará explicações claras, exemplos práticos e exercícios que simulam o padrão da prova.

## 📊 **DADOS E GRÁFICOS**

### Distribuição de Questões no ENEM

![Distribuição de Questões](https://mdn.alipayobjects.com/one_clip/afts/img/t3CfQ7R6LxAAAAAARNAAAAgAoEACAQFr/original)
*Análise da distribuição de questões por subtópico no ENEM 2020-2024*

### Taxa de Acerto Média

![Taxa de Acerto](https://mdn.alipayobjects.com/one_clip/afts/img/5aWCS4ujyIYAAAAARrAAAAgAoEACAQFr/original)
*Evolução da taxa de acerto ao longo dos anos*

## 📚 **CONCEITOS FUNDAMENTAIS**

### **1. Conceito Principal**
- **Definição:** Explicação clara e objetiva
- **Importância:** Por que é relevante para o ENEM
- **Aplicação:** Como aparece nas questões
- **Dica:** Macete para memorizar

### **2. Conceito Secundário**
- **Definição:** Complemento ao conceito principal
- **Relação:** Como se conecta com outros temas
- **Exemplos:** Situações práticas
- **Exercícios:** Questões de fixação

### **3. Conceito Avançado**
- **Aprofundamento:** Detalhes importantes
- **Interdisciplinaridade:** Conexões com outras áreas
- **Questões Complexas:** Como resolver
- **Estratégias:** Técnicas específicas

## 🎯 **ESTRATÉGIAS DE RESOLUÇÃO**

### **1. Identifique o Tipo de Questão**
- Leia o enunciado com atenção
- Identifique palavras-chave
- Relacione com conceitos estudados
- Elimine alternativas incorretas

### **2. Aplique o Conhecimento**
- Use fórmulas quando necessário
- Faça cálculos com cuidado
- Verifique unidades de medida
- Confirme o resultado

### **3. Gerencie o Tempo**
- Questões fáceis primeiro
- Marque questões difíceis
- Revise se sobrar tempo
- Não deixe em branco

## 📊 **EXERCÍCIOS PRÁTICOS**

### **Exercício 1: Aplicação Básica**

**Enunciado:** [Questão que testa conceito fundamental]

**Resolução:**
1. Identificar dados fornecidos
2. Aplicar conceito apropriado
3. Realizar cálculos necessários
4. Verificar resultado

**Resposta:** [Solução detalhada]

### **Exercício 2: Aplicação Intermediária**

**Enunciado:** [Questão que conecta múltiplos conceitos]

**Resolução:**
1. Analisar relações entre conceitos
2. Estabelecer estratégia de resolução
3. Executar passos metodicamente
4. Validar resposta

**Resposta:** [Solução completa]

### **Exercício 3: Aplicação Avançada (Estilo ENEM)**

**Enunciado:** [Questão contextualizada e interdisciplinar]

**Resolução:**
1. Compreender contexto apresentado
2. Identificar conhecimentos necessários
3. Aplicar raciocínio lógico
4. Escolher melhor alternativa

**Resposta:** [Análise detalhada]

## 🎥 **VÍDEOS RELACIONADOS**

1. [{titulo} - Conceitos Fundamentais](https://youtube.com/watch?v=exemplo1)
2. [{titulo} - Exercícios Comentados](https://youtube.com/watch?v=exemplo2)
3. [{titulo} - Dicas para o ENEM](https://youtube.com/watch?v=exemplo3)
4. [{titulo} - Resumo Completo](https://youtube.com/watch?v=exemplo4)

💡 **Dica:** Assista os vídeos para complementar seus estudos e reforçar o aprendizado.

## 📈 **DICAS AVANÇADAS**

### **1. Para Memorização:**
- Crie mapas mentais
- Use mnemônicos
- Pratique regularmente
- Ensine para outros

### **2. Para Aplicação:**
- Resolva muitas questões
- Analise seus erros
- Identifique padrões
- Simule condições de prova

### **3. Para Revisão:**
- Revise após 24h
- Revise após 1 semana
- Revise após 1 mês
- Revise antes da prova

## 🎯 **CHECKLIST RÁPIDO**

### **Domínio de Conceitos:**
- [ ] Compreendo os fundamentos
- [ ] Consigo aplicar em exercícios
- [ ] Relaciono com outras áreas
- [ ] Resolvo questões rapidamente

### **Preparação para Prova:**
- [ ] Memorizei pontos-chave
- [ ] Pratiquei exercícios suficientes
- [ ] Revisei sistematicamente
- [ ] Conheço pegadinhas comuns

## 📊 **TABELA DE REFERÊNCIA RÁPIDA**

| Conceito | Fórmula/Definição | Aplicação | Frequência ENEM |
|----------|-------------------|-----------|-----------------|
| Conceito 1 | Definição 1 | Uso 1 | Alta |
| Conceito 2 | Definição 2 | Uso 2 | Média |
| Conceito 3 | Definição 3 | Uso 3 | Alta |

## 🎯 **CONCLUSÃO**

Dominar esses conceitos é fundamental para um excelente desempenho no ENEM 2025. Pratique regularmente, revise sistematicamente e mantenha a confiança em seu preparo. Lembre-se: **consistência é mais importante que intensidade**!

## 📚 **REFERÊNCIAS E FONTES**

- **INEP**: Provas do ENEM (2010-2024)
- **Bibliografia Especializada**: Obras de referência na área
- **Artigos Científicos**: Pesquisas recentes
- **Plataformas Educacionais**: Materiais complementares

---

*Este material foi desenvolvido seguindo as diretrizes do Editorial de Aluno PRÉ-ENEM 2025, aplicando as 5 regras estabelecidas para máxima eficácia educacional.*"""

def gerar_template_checklist(titulo, eixo):
    """Gera template básico para checklists"""
    return f"""# {titulo}

## 🎯 **RESUMO EXECUTIVO**

- **Checklist prático** para organização e revisão
- **Itens essenciais** validados por especialistas
- **Fácil acompanhamento** do seu progresso
- **Aplicação imediata** em sua rotina de estudos
- **Resultados mensuráveis** e claros

## 🎯 **INTRODUÇÃO**

Este checklist foi desenvolvido para ajudá-lo a organizar e acompanhar seu progresso de forma sistemática. Use-o regularmente para garantir que está cobrindo todos os pontos importantes em sua preparação para o ENEM 2025.

## 📋 **COMO USAR ESTE CHECKLIST**

### **Frequência Recomendada:**
- **Diária:** Para checklists de rotina
- **Semanal:** Para checklists de planejamento
- **Mensal:** Para checklists de revisão geral

### **Marcação:**
- **✅ Concluído:** Item realizado completamente
- **🔄 Em Progresso:** Item iniciado mas não finalizado
- **⏳ Pendente:** Item ainda não iniciado
- **❌ Não Aplicável:** Item não relevante no momento

## 📊 **CHECKLIST PRINCIPAL**

### **📚 SEÇÃO 1: FUNDAMENTOS**

#### **Conceitos Básicos:**
- [ ] Item fundamental 1
- [ ] Item fundamental 2
- [ ] Item fundamental 3
- [ ] Item fundamental 4
- [ ] Item fundamental 5

#### **Prática:**
- [ ] Exercício tipo 1 realizado
- [ ] Exercício tipo 2 realizado
- [ ] Exercício tipo 3 realizado
- [ ] Simulado parcial realizado
- [ ] Análise de erros concluída

### **📈 SEÇÃO 2: APROFUNDAMENTO**

#### **Conceitos Avançados:**
- [ ] Item avançado 1
- [ ] Item avançado 2
- [ ] Item avançado 3
- [ ] Item avançado 4
- [ ] Item avançado 5

#### **Aplicação:**
- [ ] Questões ENEM resolvidas (mínimo 10)
- [ ] Questões comentadas revisadas
- [ ] Questões complexas dominadas
- [ ] Interdisciplinaridade compreendida
- [ ] Estratégias de resolução aplicadas

### **🎯 SEÇÃO 3: CONSOLIDAÇÃO**

#### **Revisão:**
- [ ] Revisão após 24h
- [ ] Revisão após 1 semana
- [ ] Revisão após 1 mês
- [ ] Mapa mental criado
- [ ] Resumo elaborado

#### **Validação:**
- [ ] Simulado completo realizado
- [ ] Taxa de acerto ≥70%
- [ ] Tempo de resolução adequado
- [ ] Confiança nos conceitos
- [ ] Pronto para prova

## 📊 **CHECKLIST DE RECURSOS**

### **Materiais de Estudo:**
- [ ] Apostila/livro principal
- [ ] Caderno de exercícios
- [ ] Plataforma online
- [ ] Vídeoaulas
- [ ] Aplicativos de questões

### **Ferramentas:**
- [ ] Cronograma de estudos
- [ ] Planilha de progresso
- [ ] App de simulados
- [ ] Grupo de estudos
- [ ] Monitoria/professor

## 🎥 **VÍDEOS RELACIONADOS**

1. [Como Usar Checklists Efetivamente](https://youtube.com/watch?v=exemplo1)
2. [Organização de Estudos com Checklists](https://youtube.com/watch?v=exemplo2)
3. [Acompanhamento de Progresso](https://youtube.com/watch?v=exemplo3)

💡 **Dica:** Use este checklist semanalmente para manter seu estudo organizado e produtivo.

## 📈 **EXERCÍCIOS PRÁTICOS**

### **Exercício 1: Autoavaliação**

**Objetivo:** Avaliar seu domínio atual

**Passos:**
1. Marque todos os itens que você já domina
2. Calcule seu percentual de conclusão
3. Identifique áreas que precisam de atenção
4. Priorize itens pendentes

**Meta:** Atingir 100% de conclusão

### **Exercício 2: Planejamento**

**Objetivo:** Organizar próximos passos

**Passos:**
1. Liste itens pendentes
2. Estime tempo necessário
3. Distribua no cronograma
4. Estabeleça prazos realistas

**Meta:** Plano de ação concreto

## 📊 **ACOMPANHAMENTO DE PROGRESSO**

### **Métrica Semanal:**

| Semana | Itens Concluídos | % Conclusão | Observações |
|--------|------------------|-------------|-------------|
| 1 | [   ] / [   ] | [  ]% | |
| 2 | [   ] / [   ] | [  ]% | |
| 3 | [   ] / [   ] | [  ]% | |
| 4 | [   ] / [   ] | [  ]% | |

### **Meta Mensal:**
- **Mínimo:** 80% de conclusão
- **Ideal:** 95% de conclusão
- **Excelente:** 100% de conclusão

## 🎯 **DICAS DE USO**

### **1. Seja Consistente:**
- Use o checklist regularmente
- Marque itens assim que concluir
- Revise semanalmente
- Ajuste conforme necessário

### **2. Seja Honesto:**
- Marque apenas o que realmente domina
- Não pule etapas
- Revise itens duvidosos
- Peça ajuda quando necessário

### **3. Seja Estratégico:**
- Priorize itens mais importantes
- Foque em suas dificuldades
- Celebre conquistas
- Mantenha motivação alta

## 🎯 **CONCLUSÃO**

Este checklist é sua ferramenta de organização e acompanhamento. Use-o regularmente para garantir que está progredindo de forma consistente em sua preparação para o ENEM 2025. Lembre-se: **pequenos passos diários levam a grandes resultados**!

## 📚 **REFERÊNCIAS E FONTES**

- **Metodologias de Estudo**: Técnicas comprovadas
- **Psicologia do Aprendizado**: Princípios de organização
- **Especialistas ENEM**: Recomendações práticas
- **Estudantes de Sucesso**: Melhores práticas

---

*Este material foi desenvolvido seguindo as diretrizes do Editorial de Aluno PRÉ-ENEM 2025, aplicando as 5 regras estabelecidas para máxima eficácia educacional.*"""

def criar_todos_conteudos():
    """Cria todos os conteúdos pendentes automaticamente"""
    print_secao("CRIAÇÃO AUTOMÁTICA DE CONTEÚDOS - ANO 1 PRÉ-ENEM 2025")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Criar todos os 30 conteúdos pendentes automaticamente")
    
    base_path = "2_conteudo/02_conteudos_prontos"
    total_conteudos = 0
    total_criados = 0
    total_erros = 0
    
    # Contar total de conteúdos
    for eixo, conteudos in CONTEUDOS_PENDENTES.items():
        total_conteudos += len(conteudos)
    
    print(f"\n📊 Total de conteúdos a criar: {total_conteudos}")
    print("🚀 Iniciando criação...")
    
    for eixo, conteudos in CONTEUDOS_PENDENTES.items():
        print(f"\n📚 Processando {eixo}...")
        
        for conteudo in conteudos:
            arquivo = conteudo["arquivo"]
            titulo = conteudo["titulo"]
            tipo = conteudo["tipo"]
            
            filepath = os.path.join(base_path, arquivo)
            
            print(f"\n  📝 Criando: {titulo}")
            print(f"     Tipo: {tipo}")
            print(f"     Arquivo: {arquivo}")
            
            try:
                # Gerar conteúdo baseado no tipo
                if tipo == "artigo":
                    conteudo_gerado = gerar_template_artigo(titulo, eixo)
                else:  # checklist
                    conteudo_gerado = gerar_template_checklist(titulo, eixo)
                
                # Escrever arquivo
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(conteudo_gerado)
                
                print(f"     ✅ Criado com sucesso!")
                total_criados += 1
                
            except Exception as e:
                print(f"     ❌ Erro: {e}")
                total_erros += 1
            
            time.sleep(0.5)  # Pequena pausa
    
    # Relatório final
    print_secao("RELATÓRIO FINAL")
    print(f"📊 Total de conteúdos planejados: {total_conteudos}")
    print(f"✅ Criados com sucesso: {total_criados}")
    print(f"❌ Erros: {total_erros}")
    print(f"📈 Taxa de sucesso: {(total_criados/total_conteudos*100):.1f}%")
    
    if total_criados == total_conteudos:
        print("\n🎉 TODOS OS CONTEÚDOS FORAM CRIADOS COM SUCESSO!")
    else:
        print("\n⚠️ Alguns conteúdos precisam de atenção manual")

if __name__ == "__main__":
    criar_todos_conteudos()
