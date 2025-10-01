"""
Script para Organizar e Limpar Estrutura do Projeto
Mantém apenas arquivos essenciais e organiza temporários
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime

# Diretórios base
BASE_DIR = Path(__file__).parent.parent
TEMP_DIR = BASE_DIR / "temp_historico"
SCRIPTS_DIR = BASE_DIR / "scripts"

def criar_estrutura_temp():
    """Cria estrutura para arquivos temporários históricos"""
    dirs = [
        TEMP_DIR / "json_historico",
        TEMP_DIR / "scripts_temp",
        TEMP_DIR / "relatorios_antigos",
        TEMP_DIR / "logs"
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    return dirs

def listar_arquivos_raiz():
    """Lista arquivos na raiz do projeto"""
    return [f for f in BASE_DIR.iterdir() if f.is_file()]

def categorizar_arquivos():
    """Categoriza arquivos por tipo"""
    
    categorias = {
        "essenciais": [
            "README.md",
            "requirements.txt",
            ".gitignore",
            "DIAGNOSTICO_MCP.md",
            "RELATORIO_FINAL_4_CONTEUDOS_PRE_ENEM.md",
            "RELATORIO_FINALIZACAO_PRE_ENEM.md"
        ],
        "json_ativos": [
            "sincronizacao_pre_enem.json",
            "analise_editorial_pre_enem.json"
        ],
        "json_historico": [],  # Todos outros .json
        "relatorios_antigos": [],  # relatorios com timestamp
        "logs": []  # .log files
    }
    
    arquivos_raiz = listar_arquivos_raiz()
    
    for arquivo in arquivos_raiz:
        nome = arquivo.name
        
        # Essenciais - manter
        if nome in categorias["essenciais"]:
            continue
        
        # JSON ativos - manter
        if nome in categorias["json_ativos"]:
            continue
        
        # Logs - mover
        if nome.endswith(".log"):
            categorias["logs"].append(arquivo)
        
        # Relatórios com timestamp - mover
        elif "_20250" in nome and (nome.endswith(".json") or nome.endswith(".md")):
            categorias["relatorios_antigos"].append(arquivo)
        
        # JSON histórico - mover
        elif nome.endswith(".json"):
            categorias["json_historico"].append(arquivo)
    
    return categorias

def organizar_scripts():
    """Identifica scripts temporários em /scripts"""
    
    scripts_temp = []
    scripts_manter = [
        "curadoria_automatica.py",
        "curadoria_completa.py",
        "curadoria_e_sincronizacao_pre_enem_temp.py",  # Ativo para PRE-ENEM
        "sincronizar_notion.py",
        "verificar_configuracao.py",
        "buscar_fontes_confiaveis.py",
        "verificar_fontes_mcp.py",
        "setup_projeto.py",
        "README.md"
    ]
    
    for script in SCRIPTS_DIR.glob("*.py"):
        if script.name not in scripts_manter:
            scripts_temp.append(script)
    
    return scripts_temp, scripts_manter

def mover_arquivos(categorias, dirs):
    """Move arquivos para diretórios temporários"""
    
    json_dir, scripts_dir, relatorios_dir, logs_dir = dirs
    
    movidos = {
        "json": 0,
        "relatorios": 0,
        "logs": 0,
        "scripts": 0
    }
    
    # Mover JSON histórico
    for arquivo in categorias["json_historico"]:
        destino = json_dir / arquivo.name
        shutil.move(str(arquivo), str(destino))
        movidos["json"] += 1
    
    # Mover relatórios antigos
    for arquivo in categorias["relatorios_antigos"]:
        destino = relatorios_dir / arquivo.name
        shutil.move(str(arquivo), str(destino))
        movidos["relatorios"] += 1
    
    # Mover logs
    for arquivo in categorias["logs"]:
        destino = logs_dir / arquivo.name
        shutil.move(str(arquivo), str(destino))
        movidos["logs"] += 1
    
    return movidos

def mover_scripts_temp(scripts_temp, scripts_dir):
    """Move scripts temporários"""
    movidos = 0
    for script in scripts_temp:
        destino = scripts_dir / script.name
        shutil.move(str(script), str(destino))
        movidos += 1
    return movidos

def gerar_relatorio():
    """Gera relatório da organização"""
    
    print("="*70)
    print("ORGANIZACAO E LIMPEZA DO PROJETO")
    print("="*70)
    
    # Criar estrutura
    print("\nCriando estrutura temp_historico...")
    dirs = criar_estrutura_temp()
    print("   [OK] Estrutura criada")
    
    # Categorizar arquivos raiz
    print("\nCategorizando arquivos na raiz...")
    categorias = categorizar_arquivos()
    
    print(f"\n   Essenciais (manter na raiz): {len(categorias['essenciais'])}")
    print(f"   JSON ativos (manter na raiz): {len(categorias['json_ativos'])}")
    print(f"   JSON historico (mover): {len(categorias['json_historico'])}")
    print(f"   Relatorios antigos (mover): {len(categorias['relatorios_antigos'])}")
    print(f"   Logs (mover): {len(categorias['logs'])}")
    
    # Organizar scripts
    print("\nCategorizando scripts...")
    scripts_temp, scripts_manter = organizar_scripts()
    print(f"   Scripts essenciais (manter): {len(scripts_manter)}")
    print(f"   Scripts temporarios (mover): {len(scripts_temp)}")
    
    # Mover arquivos
    print("\nMovendo arquivos...")
    movidos = mover_arquivos(categorias, dirs)
    print(f"   JSON movidos: {movidos['json']}")
    print(f"   Relatorios movidos: {movidos['relatorios']}")
    print(f"   Logs movidos: {movidos['logs']}")
    
    # Mover scripts
    scripts_movidos = mover_scripts_temp(scripts_temp, dirs[1])
    print(f"   Scripts temporarios movidos: {scripts_movidos}")
    
    # Resumo final
    print("\n" + "="*70)
    print("ESTRUTURA ORGANIZADA")
    print("="*70)
    
    print("\nRAIZ DO PROJETO (limpa):")
    print("   README.md")
    print("   requirements.txt")
    print("   .gitignore")
    print("   DIAGNOSTICO_MCP.md")
    print("   RELATORIO_FINAL_4_CONTEUDOS_PRE_ENEM.md")
    print("   RELATORIO_FINALIZACAO_PRE_ENEM.md")
    print("   sincronizacao_pre_enem.json (ativo)")
    print("   analise_editorial_pre_enem.json (ativo)")
    
    print("\nDIRETORIOS PRINCIPAIS:")
    print("   /2_conteudo/ - Conteudos organizados por status")
    print("   /scripts/ - Scripts essenciais")
    print("   /assets/ - Imagens e recursos")
    print("   /docs/ - Documentacao")
    print("   /config/ - Configuracoes")
    print("   /templates/ - Templates")
    
    print("\nHISTORICO ARQUIVADO:")
    print("   /temp_historico/json_historico/ - JSONs antigos")
    print("   /temp_historico/scripts_temp/ - Scripts temporarios")
    print("   /temp_historico/relatorios_antigos/ - Relatorios com timestamp")
    print("   /temp_historico/logs/ - Arquivos de log")
    
    print("\n" + "="*70)
    print("ORGANIZACAO CONCLUIDA COM SUCESSO!")
    print("="*70)
    
    # Salvar relatório
    relatorio = {
        "data": datetime.now().isoformat(),
        "arquivos_movidos": {
            "json": movidos["json"],
            "relatorios": movidos["relatorios"],
            "logs": movidos["logs"],
            "scripts": scripts_movidos
        },
        "total_arquivos_organizados": sum(movidos.values()) + scripts_movidos,
        "estrutura_limpa": True
    }
    
    with open(BASE_DIR / "temp_historico" / "relatorio_organizacao.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)
    
    print("\nRelatorio salvo em: temp_historico/relatorio_organizacao.json")

if __name__ == "__main__":
    gerar_relatorio()

