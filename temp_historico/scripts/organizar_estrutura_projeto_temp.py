#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Organização da Estrutura do Projeto
Move arquivos temporários e relatórios para pastas apropriadas
"""

import os
import sys
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def print_secao(titulo):
    print("\n" + "="*60)
    print(titulo.upper())
    print("="*60)

def organizar_relatorios():
    """Move relatórios para pasta apropriada"""
    print_secao("Organizando Relatorios")
    
    pasta_relatorios = Path("docs/relatorios")
    pasta_relatorios.mkdir(exist_ok=True)
    
    relatorios_raiz = [
        "relatorio_analise_completa_sincronizacao.md",
        "relatorio_analise_editorial_gestao_final.md",
        "relatorio_correcao_completa_boilerplate_100.md",
        "relatorio_correcao_final_paginas_reprovadas.md",
        "relatorio_verificacao_completa_boilerplate.md"
    ]
    
    movidos = 0
    for relatorio in relatorios_raiz:
        if os.path.exists(relatorio):
            destino = pasta_relatorios / relatorio
            shutil.move(relatorio, destino)
            print(f"  Movido: {relatorio} -> docs/relatorios/")
            movidos += 1
    
    print(f"\nTotal movido: {movidos} relatorios")

def organizar_arquivos_finalizacao():
    """Move arquivos de finalização para pasta de documentação"""
    print_secao("Organizando Arquivos de Finalizacao")
    
    arquivos_finalizacao = [
        "RELATORIO_FINALIZACAO_PRE_ENEM.md",
        "RELATORIO_FINAL_4_CONTEUDOS_PRE_ENEM.md",
        "DIAGNOSTICO_MCP.md"
    ]
    
    pasta_docs = Path("docs")
    
    movidos = 0
    for arquivo in arquivos_finalizacao:
        if os.path.exists(arquivo):
            destino = pasta_docs / arquivo
            shutil.move(arquivo, destino)
            print(f"  Movido: {arquivo} -> docs/")
            movidos += 1
    
    print(f"\nTotal movido: {movidos} arquivos")

def limpar_arquivos_json_temporarios():
    """Move JSONs de análise para temp_historico"""
    print_secao("Organizando Arquivos JSON")
    
    jsons_raiz = [
        "analise_editorial_pre_enem.json",
        "sincronizacao_pre_enem.json"
    ]
    
    pasta_temp = Path("temp_historico")
    pasta_temp.mkdir(exist_ok=True)
    
    movidos = 0
    for json_file in jsons_raiz:
        if os.path.exists(json_file):
            destino = pasta_temp / json_file
            shutil.move(json_file, destino)
            print(f"  Movido: {json_file} -> temp_historico/")
            movidos += 1
    
    print(f"\nTotal movido: {movidos} arquivos JSON")

def organizar_backup_imagens():
    """Verifica organização de backups de imagem"""
    print_secao("Verificando Backup de Imagens")
    
    pasta_backup = Path("backup_imagens")
    
    if pasta_backup.exists():
        arquivos = list(pasta_backup.glob("*"))
        print(f"\nBackup de imagens: {len(arquivos)} arquivos")
        print("  Status: OK")
    else:
        print("\nPasta backup_imagens nao encontrada")

def verificar_scripts_temp():
    """Lista scripts temporários"""
    print_secao("Verificando Scripts Temporarios")
    
    pasta_scripts = Path("scripts")
    scripts_temp = list(pasta_scripts.glob("*_temp.py"))
    
    print(f"\nScripts temporarios encontrados: {len(scripts_temp)}")
    for script in scripts_temp:
        print(f"  - {script.name}")
    
    if scripts_temp:
        print("\nRecomendacao: Manter apenas scripts ativos em uso")
        print("Scripts _temp.py podem ser movidos para temp_historico/")
    
    return scripts_temp

def mover_scripts_temp_para_historico(scripts_temp):
    """Move scripts temporários para histórico"""
    print_secao("Movendo Scripts Temporarios")
    
    pasta_historico = Path("temp_historico/scripts")
    pasta_historico.mkdir(parents=True, exist_ok=True)
    
    # Scripts a MANTER (em uso ativo)
    scripts_ativos = [
        "analisar_editorial_pre_enem_temp.py",
        "curadoria_e_sincronizacao_pre_enem_temp.py",
        "reverter_publicacao_notion_temp.py"
    ]
    
    movidos = 0
    mantidos = 0
    
    for script in scripts_temp:
        if script.name in scripts_ativos:
            print(f"  Mantido (em uso): {script.name}")
            mantidos += 1
        else:
            destino = pasta_historico / script.name
            if not destino.exists():
                shutil.move(script, destino)
                print(f"  Movido: {script.name} -> temp_historico/scripts/")
                movidos += 1
    
    print(f"\nMovidos: {movidos} | Mantidos: {mantidos}")

def criar_estrutura_limpa():
    """Cria/verifica estrutura organizada"""
    print_secao("Verificando Estrutura de Pastas")
    
    estrutura = {
        "2_conteudo/01_ideias_e_rascunhos/pre_enem": "Rascunhos PRE-ENEM",
        "2_conteudo/02_em_revisao/pre_enem": "Em revisao PRE-ENEM",
        "2_conteudo/03_aprovado_publicacao/pre_enem": "Aprovados PRE-ENEM",
        "docs/relatorios": "Relatorios",
        "temp_historico/scripts": "Scripts antigos",
        "temp_historico/json": "Arquivos JSON antigos"
    }
    
    for pasta, descricao in estrutura.items():
        path = Path(pasta)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"  Criada: {pasta} ({descricao})")
        else:
            print(f"  OK: {pasta}")

def gerar_relatorio_final():
    """Gera relatório da organização"""
    print_secao("Relatorio de Organizacao")
    
    # Contar arquivos
    total_md = len(list(Path(".").rglob("*.md")))
    total_py = len(list(Path("scripts").glob("*.py")))
    total_json = len(list(Path(".").rglob("*.json")))
    
    print(f"\nArquivos no projeto:")
    print(f"  Markdown (.md): {total_md}")
    print(f"  Python (.py): {total_py}")
    print(f"  JSON (.json): {total_json}")
    
    print("\nEstrutura principal:")
    print("  /2_conteudo/")
    print("    /01_ideias_e_rascunhos/ - Rascunhos e ideias")
    print("    /02_em_revisao/ - Em revisao editorial")
    print("    /03_aprovado_publicacao/ - Aprovados")
    print("    /04_publicado/ - Ja publicados")
    print("  /scripts/ - Scripts ativos")
    print("  /docs/ - Documentacao e relatorios")
    print("  /temp_historico/ - Arquivos temporarios/antigos")
    print("  /templates/ - Templates de conteudo")
    print("  /config/ - Arquivos de configuracao")

def main():
    print("="*60)
    print("ORGANIZACAO DA ESTRUTURA DO PROJETO")
    print("="*60)
    
    # 1. Criar estrutura organizada
    criar_estrutura_limpa()
    
    # 2. Organizar relatórios
    organizar_relatorios()
    
    # 3. Organizar arquivos de finalização
    organizar_arquivos_finalizacao()
    
    # 4. Organizar JSONs
    limpar_arquivos_json_temporarios()
    
    # 5. Verificar scripts temporários
    scripts_temp = verificar_scripts_temp()
    
    # 6. Mover scripts antigos
    if scripts_temp:
        mover_scripts_temp_para_historico(scripts_temp)
    
    # 7. Verificar backups
    organizar_backup_imagens()
    
    # 8. Relatório final
    gerar_relatorio_final()
    
    print("\n" + "="*60)
    print("ORGANIZACAO CONCLUIDA COM SUCESSO!")
    print("="*60)
    print("\nEstrutura limpa e organizada.")
    print("Scripts ativos mantidos em /scripts/")
    print("Arquivos temporarios em /temp_historico/")
    print("Documentacao em /docs/")

if __name__ == "__main__":
    main()

