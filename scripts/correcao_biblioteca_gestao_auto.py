
import requests
import json
from datetime import datetime
import time

# Configuração do Notion
NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
DATABASE_ID = "2325113a91a381c09b33f826449a218f"  # Biblioteca Gestão

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_all_pages():
    """Busca todas as páginas da biblioteca"""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    
    all_pages = []
    has_more = True
    start_cursor = None
    
    while has_more:
        payload = {"page_size": 100}
        if start_cursor:
            payload["start_cursor"] = start_cursor
            
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            all_pages.extend(data.get("results", []))
            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")
        else:
            print(f"Erro ao buscar páginas: {response.status_code}")
            break
    
    return all_pages

def get_page_content(page_id):
    """Busca conteúdo de uma página"""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return None

def update_page_properties(page_id, properties):
    """Atualiza propriedades de uma página"""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    
    payload = {
        "properties": properties
    }
    
    response = requests.patch(url, headers=headers, json=payload)
    return response.status_code == 200

def fix_page_tags(page_id, current_tags):
    """Corrige tags de uma página"""
    # Remover tags incorretas
    incorrect_tags = ["ENEM2025", "FNFM2025", "Estudos", "Preparação", "Alunos"]
    correct_tags = [tag for tag in current_tags if tag not in incorrect_tags]
    
    # Adicionar tags corretas se necessário
    if not correct_tags:
        correct_tags = ["GestãoEscolar", "Estratégia", "2024"]
    
    # Converter para formato Notion
    multi_select = [{"name": tag} for tag in correct_tags]
    
    return {
        "Tags": {
            "multi_select": multi_select
        }
    }

def fix_page_properties(page):
    """Corrige propriedades de uma página"""
    properties = page.get("properties", {})
    updates = {}
    
    # Corrigir tags
    if "Tags" in properties:
        current_tags = []
        if properties["Tags"].get("multi_select"):
            current_tags = [tag["name"] for tag in properties["Tags"]["multi_select"]]
        
        tag_updates = fix_page_tags(page["id"], current_tags)
        updates.update(tag_updates)
    
    # Garantir que tipo está definido
    if "Tipo" not in properties or not properties["Tipo"].get("select"):
        updates["Tipo"] = {
            "select": {"name": "Artigo"}
        }
    
    # Garantir que status está definido
    if "Status editorial" not in properties or not properties["Status editorial"].get("status"):
        updates["Status editorial"] = {
            "status": {"name": "Aprovado"}
        }
    
    # Garantir que função está definida
    if "Função" not in properties or not properties["Função"].get("multi_select"):
        updates["Função"] = {
            "multi_select": [{"name": "Diretor"}, {"name": "Coordenador"}]
        }
    
    # Garantir que nível está definido
    if "Nível de profundidade" not in properties or not properties["Nível de profundidade"].get("multi_select"):
        updates["Nível de profundidade"] = {
            "multi_select": [{"name": "Estratégico"}]
        }
    
    return updates

def main():
    print("================================================================================")
    print("CORREÇÃO COMPLETA DA BIBLIOTECA GESTÃO ESCOLAR")
    print("================================================================================")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Corrigir tags, propriedades e conformidade")
    
    # Buscar páginas
    print("\n🔍 Buscando páginas...")
    pages = get_all_pages()
    print(f"📊 Total de páginas: {len(pages)}")
    
    if not pages:
        print("❌ Nenhuma página encontrada")
        return
    
    # Processar cada página
    corrected = 0
    errors = 0
    
    for i, page in enumerate(pages, 1):
        print(f"\n📄 Processando página {i}/{len(pages)}: {page.get('id', 'N/A')}")
        
        try:
            # Corrigir propriedades
            updates = fix_page_properties(page)
            
            if updates:
                success = update_page_properties(page["id"], updates)
                if success:
                    print(f"   ✅ Propriedades corrigidas")
                    corrected += 1
                else:
                    print(f"   ❌ Erro ao atualizar propriedades")
                    errors += 1
            else:
                print(f"   ℹ️ Nenhuma correção necessária")
            
            # Pausa para evitar rate limit
            time.sleep(0.1)
            
        except Exception as e:
            print(f"   ❌ Erro: {str(e)}")
            errors += 1
    
    print("\n================================================================================")
    print("RELATÓRIO FINAL")
    print("================================================================================")
    print(f"✅ Páginas corrigidas: {corrected}")
    print(f"❌ Erros: {errors}")
    print(f"📊 Total processado: {len(pages)}")
    print("🎉 CORREÇÃO CONCLUÍDA!")

if __name__ == "__main__":
    main()
