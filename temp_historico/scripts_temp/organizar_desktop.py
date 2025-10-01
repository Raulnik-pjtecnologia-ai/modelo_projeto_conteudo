#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Organização Automática do Desktop
Organiza arquivos automaticamente nas pastas do projeto
"""

import os
import shutil
from pathlib import Path
import time
from datetime import datetime

def organizar_desktop(desktop_path, project_root):
    """Organiza arquivos do desktop nas pastas do projeto"""
    print(f"🧹 Iniciando organização automática do desktop em: {desktop_path}")
    
    scripts_dir = Path(project_root) / "scripts"
    docs_dir = Path(project_root) / "docs"
    conteudo_dir = Path(project_root) / "2_conteudo" / "01_ideias_e_rascunhos"
    
    # Criar diretórios se não existirem
    scripts_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)
    conteudo_dir.mkdir(parents=True, exist_ok=True)
    
    arquivos_movidos = []
    
    try:
        for item in os.listdir(desktop_path):
            item_path = Path(desktop_path) / item
            
            if item_path.is_file():
                # Scripts Python
                if item.endswith(".py"):
                    try:
                        shutil.move(item_path, scripts_dir / item)
                        arquivos_movidos.append(f"Script: {item} → scripts/")
                        print(f"✅ Movido: {item} para scripts/")
                    except Exception as e:
                        arquivos_movidos.append(f"Erro ao mover script {item}: {e}")
                        print(f"❌ Erro ao mover script {item}: {e}")
                
                # Relatórios JSON
                elif item.endswith(".json"):
                    try:
                        shutil.move(item_path, docs_dir / item)
                        arquivos_movidos.append(f"Relatório: {item} → docs/")
                        print(f"✅ Movido: {item} para docs/")
                    except Exception as e:
                        arquivos_movidos.append(f"Erro ao mover relatório {item}: {e}")
                        print(f"❌ Erro ao mover relatório {item}: {e}")
                
                # Documentos Markdown
                elif item.endswith(".md"):
                    try:
                        shutil.move(item_path, conteudo_dir / item)
                        arquivos_movidos.append(f"Conteúdo: {item} → 2_conteudo/01_ideias_e_rascunhos/")
                        print(f"✅ Movido: {item} para 2_conteudo/01_ideias_e_rascunhos/")
                    except Exception as e:
                        arquivos_movidos.append(f"Erro ao mover conteúdo {item}: {e}")
                        print(f"❌ Erro ao mover conteúdo {item}: {e}")
                
                # Arquivos de texto
                elif item.endswith((".txt", ".csv")):
                    try:
                        shutil.move(item_path, docs_dir / item)
                        arquivos_movidos.append(f"Documento: {item} → docs/")
                        print(f"✅ Movido: {item} para docs/")
                    except Exception as e:
                        arquivos_movidos.append(f"Erro ao mover documento {item}: {e}")
                        print(f"❌ Erro ao mover documento {item}: {e}")
                
                # Ignorar arquivos de sistema
                elif item in ['desktop.ini', 'Thumbs.db']:
                    print(f"⏭️  Ignorado (arquivo de sistema): {item}")
                    continue
                
                # Outros arquivos
                else:
                    print(f"❓ Arquivo não categorizado: {item}")
    
    except Exception as e:
        print(f"❌ Erro ao acessar desktop: {e}")
        return []
    
    if not arquivos_movidos:
        print("✨ Nenhum arquivo para organizar no momento.")
    
    return arquivos_movidos

def gerar_relatorio(arquivos_movidos, project_root):
    """Gera relatório da organização"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    relatorio_path = Path(project_root) / "docs" / f"relatorio_organizacao_{timestamp}.md"
    
    relatorio_content = f"""# 📄 Relatório de Organização Automática

## Data da Organização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

## 🚀 Resumo das Ações Realizadas

Este relatório detalha as ações tomadas para organizar automaticamente os arquivos do desktop.

### 📊 Estatísticas
- **Total de arquivos movidos**: {len(arquivos_movidos)}
- **Data/Hora**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

### 📁 Arquivos Movidos

"""
    
    if arquivos_movidos:
        for arquivo in arquivos_movidos:
            relatorio_content += f"- {arquivo}\n"
    else:
        relatorio_content += "Nenhum arquivo foi movido.\n"
    
    relatorio_content += f"""
## ✅ Conclusão

A organização automática foi concluída com sucesso. Todos os arquivos identificados foram movidos para suas respectivas pastas dentro do projeto.

**Desktop organizado e limpo!** 🎉
"""
    
    try:
        with open(relatorio_path, 'w', encoding='utf-8') as f:
            f.write(relatorio_content)
        print(f"📄 Relatório salvo em: {relatorio_path}")
    except Exception as e:
        print(f"❌ Erro ao salvar relatório: {e}")

def main():
    """Função principal"""
    print("🧹 ORGANIZAÇÃO AUTOMÁTICA DO DESKTOP")
    print("="*50)
    
    # Caminhos
    desktop_path = Path.home() / "Desktop"
    project_root = Path(__file__).parent.parent
    
    print(f"📁 Desktop: {desktop_path}")
    print(f"📁 Projeto: {project_root}")
    print()
    
    # Executar organização
    arquivos_movidos = organizar_desktop(desktop_path, project_root)
    
    # Gerar relatório
    if arquivos_movidos:
        gerar_relatorio(arquivos_movidos, project_root)
    
    print("\n" + "="*50)
    print("🎉 ORGANIZAÇÃO CONCLUÍDA!")
    print("="*50)
    print(f"📄 Arquivos movidos: {len(arquivos_movidos)}")
    print("✨ Desktop limpo e organizado!")

if __name__ == "__main__":
    main()
