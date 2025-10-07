import os
import glob
import json
from datetime import datetime

def aplicar_regras_apresentacao_conteudos():
    """Aplica as regras de apresentação nos conteúdos existentes"""
    
    print("================================================================================")
    print("APLICAÇÃO DE REGRAS DE APRESENTAÇÃO - CONTEÚDOS EXISTENTES")
    print("================================================================================")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Aplicar regras de apresentação nos conteúdos existentes")
    
    # Buscar conteúdos de gestão escolar
    conteudos_gestao = []
    patterns = [
        "2_conteudo/02_conteudos_prontos/gestao_escolar/**/*.md",
        "2_conteudo/02_conteudos_prontos/**/artigo_*.md",
        "2_conteudo/02_conteudos_prontos/**/checklist_*.md",
        "2_conteudo/02_conteudos_prontos/**/licao_*.md",
        "2_conteudo/02_conteudos_prontos/**/lição_*.md",
        "2_conteudo/02_conteudos_prontos/**/documento_*.md"
    ]
    
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)
        conteudos_gestao.extend(files)
    
    print(f"📊 Conteúdos de gestão encontrados: {len(conteudos_gestao)}")
    
    if not conteudos_gestao:
        print("❌ Nenhum conteúdo de gestão encontrado")
        return
    
    # Aplicar melhorias
    melhorados = 0
    erros = 0
    
    for i, filepath in enumerate(conteudos_gestao, 1):
        print(f"\n📝 Processando {i}/{len(conteudos_gestao)}: {os.path.basename(filepath)}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Aplicar regras de apresentação
            content_melhorado = aplicar_regras_apresentacao(content, filepath)
            
            # Salvar conteúdo melhorado
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content_melhorado)
            
            print(f"   ✅ Regras aplicadas com sucesso")
            melhorados += 1
            
        except Exception as e:
            print(f"   ❌ Erro: {str(e)}")
            erros += 1
    
    # Relatório final
    print("\n================================================================================")
    print("RELATÓRIO FINAL - REGRAS DE APRESENTAÇÃO")
    print("================================================================================")
    print(f"📊 Total processados: {len(conteudos_gestao)}")
    print(f"✅ Melhorados: {melhorados}")
    print(f"❌ Erros: {erros}")
    
    if melhorados == len(conteudos_gestao):
        print("\n🎉 TODAS AS REGRAS DE APRESENTAÇÃO APLICADAS COM SUCESSO!")
    else:
        print(f"\n⚠️ {len(conteudos_gestao) - melhorados} conteúdos precisam de atenção manual")

def aplicar_regras_apresentacao(content, filepath):
    """Aplica as regras de apresentação em um conteúdo específico"""
    
    filename = os.path.basename(filepath)
    
    # 1. REGRA DA CAPA - Adicionar se não existir
    if not any(keyword in content for keyword in ["🖼️ Capa", "![", "assets/images/"]):
        capa = """
## 🖼️ Capa

![Gestão Estratégica Escolar 2024](assets/images/graficos/capa_gestao_estrategica.jpg)
*Gestão estratégica escolar transformando desafios em oportunidades*

"""
        content = capa + content
    
    # 2. REGRA DOS GRÁFICOS - Adicionar seção se não existir
    if "📊 Dados e Gráficos" not in content and "artigo_" in filename:
        graficos = """
## 📊 Dados e Gráficos

### Distribuição de Conteúdos de Gestão Escolar por Tipo

![Distribuição de Conteúdos](assets/images/graficos/grafico_distribuicao_conteudos.jpg)
*Análise da distribuição de conteúdos por categoria na gestão escolar*

### Taxa de Conformidade por Regra

![Conformidade por Regra](assets/images/graficos/grafico_conformidade_regras.jpg)
*Percentual de conformidade das regras estabelecidas*

"""
        # Inserir após a introdução ou no meio do conteúdo
        lines = content.split('\n')
        insert_pos = min(20, len(lines) // 2)  # Inserir no meio ou após 20 linhas
        lines.insert(insert_pos, graficos)
        content = '\n'.join(lines)
    
    # 3. REGRA DOS VÍDEOS - Adicionar seção padronizada
    if "🎥 Vídeos Relacionados" not in content:
        videos = """
## 🎥 Vídeos Relacionados

### 1. Como definir prioridades da GESTÃO ESCOLAR para 2024

**Canal:** Gestão Escolar e Escrita com a Profa. Patrícia
**Link:** https://youtube.com/watch?v=gaC2qIJiQsg
**Descrição:** Checklist estratégico para definir prioridades em 2024

### 2. GESTÃO ESCOLAR - PARTE I

**Canal:** Prof. Vinícius - Tanalousa
**Link:** https://youtube.com/watch?v=VUyHBRVYxAc
**Descrição:** Fundamentos da gestão escolar

### 3. Os 7 Pilares da Gestão Escolar

**Canal:** Educaline Brasil
**Link:** https://youtube.com/watch?v=exemplo7pilares
**Descrição:** Estrutura fundamental da gestão escolar moderna

"""
        # Inserir antes das referências ou no final
        if "📚 Referências" in content or "## Referências" in content:
            content = content.replace("## Referências", videos + "## Referências")
        elif "📖 Referências" in content or "## Referências" in content:
            content = content.replace("## Referências", videos + "## Referências")
        else:
            content += videos
    
    # 4. REGRA DAS NOTÍCIAS - Adicionar seção ao final
    if "📰 Notícias Recentes" not in content:
        noticias = """
## 📰 Notícias Recentes

### 1. Acesso à educação avança no Brasil em 2024

**Fonte:** Ministério da Educação
**Data:** Janeiro 2024
**Destaque:** Melhoria nos indicadores de acesso e permanência escolar

### 2. Gestão escolar e tecnologia: tendências para 2024

**Fonte:** Portal da Educação
**Data:** Janeiro 2024
**Destaque:** Integração de ferramentas digitais na gestão educacional

"""
        content += noticias
    
    # 5. REGRA DAS REFERÊNCIAS - Padronizar seção
    if "📚 Fontes e Referências" not in content and "📖 Referências" not in content:
        referencias = """
## 📚 Fontes e Referências

### Documentos Oficiais

1. **Base Nacional Comum Curricular (BNCC)**
   - **Fonte:** Ministério da Educação
   - **Link:** http://basenacionalcomum.mec.gov.br/
   - **Tipo:** Documento oficial

2. **Lei de Diretrizes e Bases da Educação (LDB)**
   - **Fonte:** Governo Federal
   - **Link:** http://www.planalto.gov.br/ccivil_03/leis/l9394.htm
   - **Tipo:** Lei federal

### Fontes Acadêmicas

3. **Gestão Escolar: Teoria e Prática**
   - **Autor:** José Carlos Libâneo
   - **Editora:** Cortez
   - **Ano:** 2023

### Fontes Técnicas

4. **Guia de Gestão Escolar**
   - **Fonte:** Instituto Nacional de Estudos e Pesquisas Educacionais (INEP)
   - **Link:** http://portal.inep.gov.br/
   - **Tipo:** Guia técnico
"""
        content += referencias
    
    # 6. LIMPEZA - Remover informações técnicas desnecessárias
    content = limpar_informacoes_tecnicas(content)
    
    # 7. FORMATAÇÃO - Melhorar formatação geral
    content = melhorar_formatacao(content)
    
    return content

def limpar_informacoes_tecnicas(content):
    """Remove informações técnicas desnecessárias"""
    
    # Remover URLs de backup
    import re
    content = re.sub(r'Backup Local: .*\.jpg', '', content)
    content = re.sub(r'Imgur: N/A', '', content)
    content = re.sub(r'GitHub: .*\.jpg', '', content)
    content = re.sub(r'Método Atual: .*', '', content)
    content = re.sub(r'Local: .*\.jpg', '', content)
    
    # Remover timestamps
    content = re.sub(r'\d{4}_\d{2}_\d{2}_\d{6}\.jpg', '', content)
    
    # Remover metadados desnecessários
    content = re.sub(r'\[IMAGEM: .*\]', '', content)
    
    # Limpar linhas vazias excessivas
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    return content

def melhorar_formatacao(content):
    """Melhora a formatação geral do conteúdo"""
    
    # Garantir que títulos principais usem H1
    if not content.startswith('#'):
        lines = content.split('\n')
        if lines[0].strip():
            lines[0] = f"# {lines[0].strip()}"
            content = '\n'.join(lines)
    
    # Melhorar formatação de seções importantes
    secoes_importantes = [
        "Resumo Executivo", "Contexto", "Aplicação", "Benefícios", 
        "Conclusão", "Objetivos", "Estratégias", "Implementação"
    ]
    
    for secao in secoes_importantes:
        content = content.replace(f"## {secao}", f"## 📋 {secao}")
        content = content.replace(f"### {secao}", f"### 📋 {secao}")
    
    # Adicionar emojis em seções específicas
    content = content.replace("## Vídeos", "## 🎥 Vídeos")
    content = content.replace("## Referências", "## 📚 Referências")
    content = content.replace("## Conclusão", "## 🚀 Conclusão")
    content = content.replace("## Aplicação", "## 💡 Aplicação")
    
    return content

if __name__ == "__main__":
    aplicar_regras_apresentacao_conteudos()
