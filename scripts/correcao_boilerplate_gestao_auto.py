
import requests
import json
from datetime import datetime
import time

# Configuração do Notion
NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
DATABASE_ID = "2325113a91a381c09b33f826449a218f"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_page_blocks(page_id):
    """Busca blocos de uma página"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

def update_page_content(page_id, blocks):
    """Atualiza conteúdo de uma página"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    
    payload = {
        "children": blocks
    }
    
    response = requests.patch(url, headers=headers, json=payload)
    return response.status_code == 200

def fix_markdown_syntax(blocks):
    """Remove sintaxe markdown problemática"""
    fixed_blocks = []
    
    for block in blocks:
        block_type = block.get("type")
        
        if block_type == "paragraph":
            paragraph = block.get("paragraph", {})
            rich_text = paragraph.get("rich_text", [])
            
            # Verificar se contém sintaxe |--|
            for text_obj in rich_text:
                if "text" in text_obj:
                    content = text_obj["text"].get("content", "")
                    if "|--|" in content:
                        # Remover linha com |--|
                        continue
            
            # Se não foi removida, adicionar o bloco
            if rich_text:
                fixed_blocks.append(block)
        else:
            fixed_blocks.append(block)
    
    return fixed_blocks

def add_video_section(blocks):
    """Adiciona seção de vídeos se não existir"""
    # Verificar se já existe seção de vídeos
    has_video_section = False
    for block in blocks:
        if block.get("type") == "paragraph":
            paragraph = block.get("paragraph", {})
            rich_text = paragraph.get("rich_text", [])
            for text_obj in rich_text:
                if "text" in text_obj:
                    content = text_obj["text"].get("content", "")
                    if "vídeos" in content.lower() or "videos" in content.lower():
                        has_video_section = True
                        break
    
    if not has_video_section:
        # Adicionar seção de vídeos
        video_blocks = [
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "🎥 Vídeos Relacionados"
                            }
                        }
                    ]
                }
            },
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "1. [Título do Vídeo]"
                            }
                        }
                    ]
                }
            },
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "   Canal: [Nome do Canal]"
                            }
                        }
                    ]
                }
            },
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "   Link: [URL do YouTube]"
                            }
                        }
                    ]
                }
            }
        ]
        
        # Adicionar no final dos blocos existentes
        blocks.extend(video_blocks)
    
    return blocks

def main():
    print("================================================================================")
    print("CORREÇÃO DE BOILERPLATE - BIBLIOTECA GESTÃO")
    print("================================================================================")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Corrigir sintaxe markdown e adicionar vídeos")
    
    # Este script seria executado após ter acesso ao Notion
    print("\n⚠️ Script criado - requer execução com token válido")
    print("📋 Funcionalidades:")
    print("   - Remove sintaxe |--| de todas as páginas")
    print("   - Adiciona seção de vídeos onde necessário")
    print("   - Corrige formatação markdown")

if __name__ == "__main__":
    main()
