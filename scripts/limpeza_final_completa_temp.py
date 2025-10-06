#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Limpeza Final Completa
Remove todos os arquivos temporários e obsoletos após otimização completa
"""

import os
import sys
import shutil
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

def print_secao(titulo):
    print("\n" + "="*80)
    print(titulo)
    print("="*80)

def get_temp_files_and_dirs(base_path):
    """Identifica arquivos e diretórios temporários para remoção"""
    temp_items = []
    
    # Padrões de arquivos temporários
    patterns = [
        "_temp.py",
        "temp_historico",
        "markdown_imagens_backup.md",
        "backup_imagens",
        "relatorio_organizacao.json",
        "relatorio_conformidade_final.json",
        "relatorio_conformidade_final_completo.json",
        "relatorio_conformidade_final_corrigida.json",
        "relatorio_conformidade_final_etapa4.json",
        "relatorio_etapa_1_verificacao.json",
        "relatorio_correcao_tags_gestao_escolar.json",
        "relatorio_propriedades_bibliotecas.json",
        "relatorio_verificacao_correcao_videos_final.json",
        "relatorio_correcao_tags_bibliotecas.json",
        "relatorio_verificacao_tags_detalhado.json",
        "relatorio_videos_obrigatorios.json",
        "relatorio_correcao_tags_editorial_aluno.json",
        "relatorio_correcao_robusta_tags_gestao.json",
        "relatorio_correcao_videos_bookmark.json",
        "relatorio_diagnostico_correcao_videos.json",
        "relatorio_limpeza_referencias_externas.json",
        "relatorio_verificacao_sincronizacao_tags.json",
        "relatorio_correcao_videos_funcionais.json",
        "relatorio_correcao_videos_texto.json",
        "relatorio_analise_conteudo_rejeitado.json",
        "relatorio_conformidade_final_2025.json",
        "relatorio_conformidade_final_otimizada.json",
        # Relatórios antigos em docs/relatorios
        os.path.join("docs", "relatorios", "relatorio_adicao_novos_conteudos_20250918_141332.json"),
        os.path.join("docs", "relatorios", "relatorio_adicao_novos_conteudos_20250918_141046.json"),
        os.path.join("docs", "relatorios", "relatorio_sincronizacao_final_20250918_141341.json"),
        os.path.join("docs", "relatorios", "relatorio_final_projeto.json"),
    ]

    for root, dirs, files in os.walk(base_path):
        for name in files:
            file_path = os.path.join(root, name)
            if any(pattern in file_path for pattern in patterns if pattern.startswith('_temp.py') or pattern.endswith('.json') or pattern.endswith('.md')):
                temp_items.append(file_path)
        for name in dirs:
            dir_path = os.path.join(root, name)
            if any(pattern == name for pattern in patterns if not (pattern.startswith('_temp.py') or pattern.endswith('.json') or pattern.endswith('.md'))):
                temp_items.append(dir_path)
    
    return temp_items

def remove_item(path):
    """Remove arquivo ou diretório"""
    try:
        if os.path.isfile(path):
            os.remove(path)
            print(f"   ✅ Removido arquivo: {path}")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print(f"   ✅ Removido diretório: {path}")
        return True
    except Exception as e:
        print(f"   ❌ Erro ao remover {path}: {e}")
        return False

def verify_project_structure(base_path):
    """Verifica estrutura do projeto após limpeza"""
    print("\n================================================================================")
    print("VERIFICAÇÃO PÓS-LIMPEZA")
    print("================================================================================")
    print("🔍 Verificando estrutura do projeto...")
    
    content_dir = os.path.join(base_path, "2_conteudo")
    docs_dir = os.path.join(base_path, "docs")
    scripts_dir = os.path.join(base_path, "scripts")

    # Contar arquivos em 2_conteudo/02_conteudos_prontos
    conteudos_prontos_path = os.path.join(content_dir, "02_conteudos_prontos")
    num_conteudos_prontos = len([f for f in os.listdir(conteudos_prontos_path) if os.path.isfile(os.path.join(conteudos_prontos_path, f))]) if os.path.exists(conteudos_prontos_path) else 0

    print(f"   📁 2_conteudo/02_conteudos_prontos: {num_conteudos_prontos} arquivos")
    print(f"   📁 docs: {len(os.listdir(docs_dir)) if os.path.exists(docs_dir) else 0} arquivos")
    print(f"   📁 scripts: {len(os.listdir(scripts_dir)) if os.path.exists(scripts_dir) else 0} arquivos")
    
    # Verificar se há arquivos temporários restantes
    temp_remaining = get_temp_files_and_dirs(base_path)
    if temp_remaining:
        print(f"   ⚠️ Arquivos temporários restantes: {len(temp_remaining)}")
        for item in temp_remaining:
            print(f"      - {item}")
    else:
        print("   ✅ Nenhum arquivo temporário restante")

def main():
    base_path = os.getcwd()
    print_secao("LIMPEZA FINAL COMPLETA")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Remover todos os arquivos temporários e obsoletos")
    print("🔍 Identificando arquivos temporários...")

    temp_items = get_temp_files_and_dirs(base_path)
    
    if not temp_items:
        print("✅ Nenhum arquivo temporário encontrado para remoção.")
        return

    print(f"📋 Encontrados {len(temp_items)} arquivos temporários")
    print("\n📋 Arquivos que serão removidos:")
    for item in temp_items:
        print(f"   - {item}")

    print("\n🧹 Iniciando limpeza final...")
    removed_count = 0
    error_count = 0
    
    for item in temp_items:
        if remove_item(item):
            removed_count += 1
        else:
            error_count += 1
    
    verify_project_structure(base_path)

    print_secao("RELATÓRIO DE LIMPEZA FINAL")
    print(f"📊 Total de arquivos identificados: {len(temp_items)}")
    print(f"✅ Arquivos removidos com sucesso: {removed_count}")
    print(f"❌ Erros durante remoção: {error_count}")
    print(f"📈 Taxa de sucesso: {(removed_count / len(temp_items) * 100):.1f}%")
    
    if error_count > 0:
        print("⚠️ Alguns arquivos não puderam ser removidos")
    else:
        print("🎉 LIMPEZA FINAL CONCLUÍDA COM SUCESSO!")

    print("\n================================================================================")
    print("PROJETO OTIMIZADO E LIMPO!")
    print("================================================================================")

if __name__ == "__main__":
    main()
