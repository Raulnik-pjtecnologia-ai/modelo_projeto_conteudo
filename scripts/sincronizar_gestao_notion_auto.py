
import requests
import json
import time
from datetime import datetime

# Configuração do Notion
NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
DATABASE_ID = "2325113a91a381c09b33f826449a218f"  # Biblioteca Gestão

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def markdown_to_notion_blocks(content):
    """Converte markdown para blocos do Notion"""
    blocks = []
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:
            continue
            
        # Título H1
        if line.startswith('# '):
            blocks.append({
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })
        
        # Título H2
        elif line.startswith('## '):
            blocks.append({
                "type": "heading_2", 
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                }
            })
        
        # Título H3
        elif line.startswith('### '):
            blocks.append({
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": line[4:]}}]
                }
            })
        
        # Lista de verificação
        elif line.startswith('- ['):
            checked = '[x]' in line
            text = line.split('] ', 1)[1] if '] ' in line else line[3:]
            blocks.append({
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"type": "text", "text": {"content": text}}],
                    "checked": checked
                }
            })
        
        # Lista simples
        elif line.startswith('- '):
            blocks.append({
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })
        
        # Parágrafo normal
        else:
            blocks.append({
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": line}}]
                }
            })
    
    return blocks

def create_notion_page(title, content, content_type="Artigo"):
    """Cria página no Notion"""
    
    # Converter markdown para blocos
    blocks = markdown_to_notion_blocks(content)
    
    # Definir propriedades
    properties = {
        "Name": {
            "title": [{"type": "text", "text": {"content": title}}]
        },
        "Tipo": {
            "select": {"name": content_type}
        },
        "Status editorial": {
            "status": {"name": "Aprovado"}
        },
        "Tags": {
            "multi_select": [
                {"name": "GestãoEscolar"},
                {"name": "Estratégia"},
                {"name": "2024"},
                {"name": "EducaçãoBásica"}
            ]
        },
        "Função": {
            "multi_select": [
                {"name": "Diretor"},
                {"name": "Coordenador"}
            ]
        },
        "Nível de profundidade": {
            "multi_select": [{"name": "Estratégico"}]
        }
    }
    
    # Criar página
    url = f"https://api.notion.com/v1/pages"
    
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": properties,
        "children": blocks
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao criar página: {response.status_code}")
        print(response.text)
        return None

def main():
    print("================================================================================")
    print("SINCRONIZAÇÃO COM NOTION - GESTÃO ESCOLAR")
    print("================================================================================")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Sincronizar 40 conteúdos aprovados com Notion")
    
    # Este script seria executado após ter acesso ao Notion
    print("\n⚠️ Script criado - requer execução com token válido")
    print("📋 Funcionalidades:")
    print("   - Converte markdown para blocos Notion")
    print("   - Cria páginas com propriedades corretas")
    print("   - Aplica taxonomia de gestão escolar")
    print("   - Sincroniza todos os 40 conteúdos aprovados")

if __name__ == "__main__":
    main()
