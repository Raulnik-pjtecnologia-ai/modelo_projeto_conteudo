import os
import glob
import re
import json
from datetime import datetime

def limpeza_final_conteudos():
    """Aplica limpeza final nos conteúdos existentes"""
    
    print("================================================================================")
    print("LIMPEZA FINAL DE CONTEÚDOS EXISTENTES")
    print("================================================================================")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Limpeza final e correções nos conteúdos existentes")
    
    # Buscar todos os conteúdos
    conteudos = []
    patterns = [
        "2_conteudo/02_conteudos_prontos/**/*.md",
        "docs/**/*.md"
    ]
    
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)
        conteudos.extend(files)
    
    # Filtrar arquivos de documentação e scripts
    conteudos_filtrados = []
    for conteudo in conteudos:
        if not any(skip in conteudo for skip in [
            "scripts/", "relatorio_", "plano_", "analise_", 
            "regra_", "temp_", "backup_", "README.md"
        ]):
            conteudos_filtrados.append(conteudo)
    
    print(f"📊 Conteúdos para limpeza: {len(conteudos_filtrados)}")
    
    if not conteudos_filtrados:
        print("❌ Nenhum conteúdo encontrado")
        return
    
    # Aplicar limpeza
    processados = 0
    erros = 0
    correcoes = []
    
    for i, filepath in enumerate(conteudos_filtrados, 1):
        print(f"\n🧹 Limpando {i}/{len(conteudos_filtrados)}: {os.path.basename(filepath)}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Aplicar correções
            content_limpo, correcoes_arquivo = aplicar_limpeza_final(content, filepath)
            
            # Salvar conteúdo limpo
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content_limpo)
            
            correcoes.extend(correcoes_arquivo)
            print(f"   ✅ Limpeza concluída ({len(correcoes_arquivo)} correções)")
            processados += 1
            
        except Exception as e:
            print(f"   ❌ Erro: {str(e)}")
            erros += 1
    
    # Relatório final
    print("\n================================================================================")
    print("RELATÓRIO FINAL - LIMPEZA")
    print("================================================================================")
    print(f"📊 Total processados: {len(conteudos_filtrados)}")
    print(f"✅ Limpos com sucesso: {processados}")
    print(f"❌ Erros: {erros}")
    print(f"🔧 Total de correções: {len(correcoes)}")
    
    # Mostrar tipos de correções
    tipos_correcao = {}
    for correcao in correcoes:
        tipo = correcao.get('tipo', 'Outro')
        tipos_correcao[tipo] = tipos_correcao.get(tipo, 0) + 1
    
    print("\n📋 Tipos de correções aplicadas:")
    for tipo, quantidade in tipos_correcao.items():
        print(f"   • {tipo}: {quantidade}")
    
    # Salvar relatório
    relatorio = {
        "timestamp": datetime.now().isoformat(),
        "total_processados": len(conteudos_filtrados),
        "limpos_sucesso": processados,
        "erros": erros,
        "total_correcoes": len(correcoes),
        "tipos_correcao": tipos_correcao,
        "correcoes_detalhadas": correcoes
    }
    
    with open("relatorio_limpeza_final_conteudos.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Relatório salvo em: relatorio_limpeza_final_conteudos.json")
    
    if processados == len(conteudos_filtrados):
        print("\n🎉 TODOS OS CONTEÚDOS LIMPOS COM SUCESSO!")
    else:
        print(f"\n⚠️ {len(conteudos_filtrados) - processados} conteúdos precisam de atenção manual")

def aplicar_limpeza_final(content, filepath):
    """Aplica limpeza final em um conteúdo específico"""
    
    correcoes = []
    
    # 1. CORREÇÃO DE SINTAXE MARKDOWN - Remover |--| e pipes desnecessários
    if "|--|" in content or "|---|---|" in content:
        content_original = content
        
        # Remover linhas de separação de tabela
        content = re.sub(r'^\s*\|-+\|\s*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*\|--\|\s*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*\|-+\|+\s*$', '', content, flags=re.MULTILINE)
        
        # Limpar pipes de início e fim de linha
        content = re.sub(r'^\s*\|\s*', '', content, flags=re.MULTILINE)
        content = re.sub(r'\s*\|\s*$', '', content, flags=re.MULTILINE)
        
        # Substituir pipes internos por espaços
        content = re.sub(r'\s*\|\s*', ' ', content)
        
        if content != content_original:
            correcoes.append({
                "tipo": "Sintaxe Markdown",
                "descricao": "Removida sintaxe de tabela markdown incorreta",
                "arquivo": os.path.basename(filepath)
            })
    
    # 2. REMOÇÃO DE INFORMAÇÕES TÉCNICAS
    info_tecnicas_removidas = 0
    
    # Remover URLs de backup
    if "Backup Local:" in content:
        content = re.sub(r'Backup Local: .*\.jpg', '', content)
        info_tecnicas_removidas += 1
    
    if "Imgur:" in content:
        content = re.sub(r'Imgur: N/A', '', content)
        info_tecnicas_removidas += 1
    
    if "GitHub:" in content:
        content = re.sub(r'GitHub: .*\.jpg', '', content)
        info_tecnicas_removidas += 1
    
    if "Método Atual:" in content:
        content = re.sub(r'Método Atual: .*', '', content)
        info_tecnicas_removidas += 1
    
    if "Local:" in content:
        content = re.sub(r'Local: .*\.jpg', '', content)
        info_tecnicas_removidas += 1
    
    # Remover timestamps
    if re.search(r'\d{4}_\d{2}_\d{2}_\d{6}\.jpg', content):
        content = re.sub(r'\d{4}_\d{2}_\d{2}_\d{6}\.jpg', '', content)
        info_tecnicas_removidas += 1
    
    # Remover metadados
    if "[IMAGEM:" in content:
        content = re.sub(r'\[IMAGEM: .*\]', '', content)
        info_tecnicas_removidas += 1
    
    if info_tecnicas_removidas > 0:
        correcoes.append({
            "tipo": "Informações Técnicas",
            "descricao": f"Removidas {info_tecnicas_removidas} informações técnicas desnecessárias",
            "arquivo": os.path.basename(filepath)
        })
    
    # 3. LIMPEZA DE REFERÊNCIAS EXTERNAS
    ref_externas_removidas = 0
    
    # Remover callouts com referências a arquivos locais
    if "consulte o arquivo local" in content.lower():
        content = re.sub(r'> \*\*.*consulte o arquivo local.*\*\*', '', content, flags=re.IGNORECASE)
        ref_externas_removidas += 1
    
    if "arquivo mencionado acima" in content.lower():
        content = re.sub(r'> \*\*.*arquivo mencionado acima.*\*\*', '', content, flags=re.IGNORECASE)
        ref_externas_removidas += 1
    
    # Remover links para arquivos .md externos
    if "\.md" in content and "assets/" not in content:
        content = re.sub(r'\[.*\]\(.*\.md\)', '', content)
        ref_externas_removidas += 1
    
    if ref_externas_removidas > 0:
        correcoes.append({
            "tipo": "Referências Externas",
            "descricao": f"Removidas {ref_externas_removidas} referências a arquivos externos",
            "arquivo": os.path.basename(filepath)
        })
    
    # 4. CORREÇÃO DE FORMATAÇÃO
    formatacao_corrigida = 0
    
    # Garantir que títulos principais usem H1
    if not content.startswith('#') and content.strip():
        lines = content.split('\n')
        if lines[0].strip():
            lines[0] = f"# {lines[0].strip()}"
            content = '\n'.join(lines)
            formatacao_corrigida += 1
    
    # Corrigir espaçamento excessivo
    if re.search(r'\n\s*\n\s*\n\s*\n', content):
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        formatacao_corrigida += 1
    
    # Corrigir listas mal formatadas
    if re.search(r'^\s*-\s*$', content, re.MULTILINE):
        content = re.sub(r'^\s*-\s*$', '', content, flags=re.MULTILINE)
        formatacao_corrigida += 1
    
    if formatacao_corrigida > 0:
        correcoes.append({
            "tipo": "Formatação",
            "descricao": f"Aplicadas {formatacao_corrigida} correções de formatação",
            "arquivo": os.path.basename(filepath)
        })
    
    # 5. VALIDAÇÃO DE ESTRUTURA
    estrutura_corrigida = 0
    
    # Adicionar seções essenciais se ausentes
    secoes_essenciais = ["Introdução", "Contexto", "Aplicação", "Conclusão"]
    secoes_presentes = sum(1 for secao in secoes_essenciais if secao in content)
    
    if secoes_presentes < 2 and "artigo_" in os.path.basename(filepath):
        # Adicionar estrutura básica para artigos
        estrutura_basica = """
## 📋 Resumo Executivo
Este documento apresenta estratégias e práticas para gestão escolar, oferecendo orientações práticas para implementação em instituições educacionais.

## 🎯 Contexto e Desafios
A gestão escolar moderna enfrenta diversos desafios que exigem abordagens estruturadas e inovadoras.

## 💡 Aplicação Prática
Implementação de estratégias eficazes para melhorar a gestão escolar.

## 🚀 Conclusão
Gestão escolar é um processo contínuo que requer comprometimento e planejamento.
"""
        content = estrutura_basica + content
        estrutura_corrigida += 1
    
    if estrutura_corrigida > 0:
        correcoes.append({
            "tipo": "Estrutura",
            "descricao": f"Aplicadas {estrutura_corrigida} correções de estrutura",
            "arquivo": os.path.basename(filepath)
        })
    
    # 6. LIMPEZA FINAL
    # Remover linhas vazias no início e fim
    content = content.strip()
    
    # Garantir que termine com quebra de linha
    if not content.endswith('\n'):
        content += '\n'
    
    return content, correcoes

if __name__ == "__main__":
    limpeza_final_conteudos()
