#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Limpeza de Arquivos Temporários
Remove arquivos temporários criados durante os processos
"""

import os
import sys
import glob
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

def print_secao(titulo):
    print("\n" + "="*80)
    print(titulo)
    print("="*80)

def identificar_arquivos_temporarios():
    """Identifica arquivos temporários para remoção"""
    print("🔍 Identificando arquivos temporários...")
    
    # Padrões de arquivos temporários
    padroes = [
        "**/*_temp.py",
        "**/*_temp.md", 
        "**/*_temp.json",
        "**/temp_*",
        "**/backup_*",
        "**/*_backup.*",
        "**/relatorio_*.json",
        "**/docs/relatorio_*.json"
    ]
    
    arquivos_para_remover = []
    
    for padrao in padroes:
        arquivos = glob.glob(padrao, recursive=True)
        arquivos_para_remover.extend(arquivos)
    
    # Remover duplicatas
    arquivos_para_remover = list(set(arquivos_para_remover))
    
    print(f"📋 Encontrados {len(arquivos_para_remover)} arquivos temporários")
    
    return arquivos_para_remover

def remover_arquivos_temporarios(arquivos):
    """Remove os arquivos temporários identificados"""
    print("🧹 Iniciando limpeza de arquivos temporários...")
    
    removidos = 0
    erros = 0
    
    for arquivo in arquivos:
        try:
            if os.path.exists(arquivo):
                os.remove(arquivo)
                print(f"   ✅ Removido: {arquivo}")
                removidos += 1
            else:
                print(f"   ⚠️ Não encontrado: {arquivo}")
        except Exception as e:
            print(f"   ❌ Erro ao remover {arquivo}: {e}")
            erros += 1
    
    return removidos, erros

def verificar_estrutura_projeto():
    """Verifica se a estrutura do projeto está limpa"""
    print("🔍 Verificando estrutura do projeto...")
    
    diretorios_importantes = [
        "2_conteudo/02_conteudos_prontos",
        "docs",
        "scripts"
    ]
    
    for diretorio in diretorios_importantes:
        if os.path.exists(diretorio):
            arquivos = os.listdir(diretorio)
            print(f"   📁 {diretorio}: {len(arquivos)} arquivos")
        else:
            print(f"   ❌ Diretório não encontrado: {diretorio}")

def gerar_relatorio_limpeza(removidos, erros, total_identificados):
    """Gera relatório da limpeza realizada"""
    print_secao("RELATÓRIO DE LIMPEZA")
    print(f"📊 Total de arquivos identificados: {total_identificados}")
    print(f"✅ Arquivos removidos com sucesso: {removidos}")
    print(f"❌ Erros durante remoção: {erros}")
    print(f"📈 Taxa de sucesso: {(removidos/(removidos+erros)*100) if (removidos+erros) > 0 else 0:.1f}%")
    
    if erros == 0:
        print("🎉 LIMPEZA CONCLUÍDA COM SUCESSO!")
    else:
        print("⚠️ Alguns arquivos não puderam ser removidos")

def main():
    print_secao("LIMPEZA DE ARQUIVOS TEMPORÁRIOS")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Remover arquivos temporários criados durante os processos")
    
    # Identificar arquivos temporários
    arquivos_temporarios = identificar_arquivos_temporarios()
    
    if not arquivos_temporarios:
        print("✅ Nenhum arquivo temporário encontrado")
        return
    
    # Mostrar arquivos que serão removidos
    print("\n📋 Arquivos que serão removidos:")
    for arquivo in arquivos_temporarios:
        print(f"   - {arquivo}")
    
    # Confirmar remoção
    print(f"\n⚠️ ATENÇÃO: {len(arquivos_temporarios)} arquivos serão removidos permanentemente!")
    confirmacao = input("Deseja continuar? (s/N): ").lower().strip()
    
    if confirmacao not in ['s', 'sim', 'y', 'yes']:
        print("❌ Operação cancelada pelo usuário")
        return
    
    # Remover arquivos
    removidos, erros = remover_arquivos_temporarios(arquivos_temporarios)
    
    # Verificar estrutura
    print_secao("VERIFICAÇÃO PÓS-LIMPEZA")
    verificar_estrutura_projeto()
    
    # Gerar relatório
    gerar_relatorio_limpeza(removidos, erros, len(arquivos_temporarios))
    
    print_secao("LIMPEZA CONCLUÍDA!")

if __name__ == "__main__":
    main()
