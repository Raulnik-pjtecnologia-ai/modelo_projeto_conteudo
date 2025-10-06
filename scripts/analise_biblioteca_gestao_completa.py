import requests
import json
from datetime import datetime
import os

# Configuração do Notion
NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
DATABASE_ID = "2325113a91a381c09b33f826449a218f"  # Biblioteca Gestão

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_all_pages(database_id):
    """Busca todas as páginas da biblioteca de gestão"""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    all_pages = []
    has_more = True
    start_cursor = None
    
    while has_more:
        payload = {
            "page_size": 100
        }
        
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
            print(response.text)
            break
    
    return all_pages

def analyze_page_properties(page):
    """Analisa as propriedades de uma página"""
    properties = page.get("properties", {})
    
    # Extrair informações básicas
    name = ""
    if "Name" in properties and properties["Name"].get("title"):
        name = properties["Name"]["title"][0]["text"]["content"]
    
    # Analisar tipo de conteúdo
    content_type = ""
    if "Tipo" in properties and properties["Tipo"].get("select"):
        content_type = properties["Tipo"]["select"]["name"]
    
    # Analisar status
    status = ""
    if "Status editorial" in properties and properties["Status editorial"].get("status"):
        status = properties["Status editorial"]["status"]["name"]
    
    # Analisar tags
    tags = []
    if "Tags" in properties and properties["Tags"].get("multi_select"):
        tags = [tag["name"] for tag in properties["Tags"]["multi_select"]]
    
    # Analisar função
    function = []
    if "Função" in properties and properties["Função"].get("multi_select"):
        function = [func["name"] for func in properties["Função"]["multi_select"]]
    
    # Analisar nível
    level = []
    if "Nível de profundidade" in properties and properties["Nível de profundidade"].get("multi_select"):
        level = [lev["name"] for lev in properties["Nível de profundidade"]["multi_select"]]
    
    # Analisar categoria
    category = ""
    if "Categoria" in properties and properties["Categoria"].get("relation"):
        category = f"Relacionada ({len(properties['Categoria']['relation'])} itens)"
    
    return {
        "name": name,
        "content_type": content_type,
        "status": status,
        "tags": tags,
        "function": function,
        "level": level,
        "category": category,
        "url": page.get("url", "")
    }

def check_boilerplate_compliance(page_data):
    """Verifica conformidade com boilerplate"""
    issues = []
    score = 100
    
    # Verificar se tem nome
    if not page_data["name"]:
        issues.append("❌ Sem título/nome")
        score -= 20
    
    # Verificar se tem tipo
    if not page_data["content_type"]:
        issues.append("❌ Tipo de conteúdo não definido")
        score -= 15
    
    # Verificar se tem status
    if not page_data["status"]:
        issues.append("❌ Status editorial não definido")
        score -= 15
    
    # Verificar tags (deve ter pelo menos 1)
    if len(page_data["tags"]) == 0:
        issues.append("❌ Nenhuma tag aplicada")
        score -= 15
    
    # Verificar função (deve ter pelo menos 1)
    if len(page_data["function"]) == 0:
        issues.append("❌ Nenhuma função definida")
        score -= 15
    
    # Verificar nível (deve ter pelo menos 1)
    if len(page_data["level"]) == 0:
        issues.append("❌ Nível de profundidade não definido")
        score -= 10
    
    # Verificar categoria
    if not page_data["category"]:
        issues.append("❌ Categoria não relacionada")
        score -= 10
    
    return {
        "score": max(0, score),
        "issues": issues,
        "status": "✅ Conforme" if score >= 80 else "⚠️ Não conforme" if score >= 60 else "❌ Crítico"
    }

def main():
    print("================================================================================")
    print("ANÁLISE COMPLETA DA BIBLIOTECA GESTÃO ESCOLAR")
    print("================================================================================")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Analisar conformidade com boilerplate e taxonomias")
    
    # Buscar todas as páginas
    print("\n🔍 Buscando páginas da biblioteca...")
    pages = get_all_pages(DATABASE_ID)
    print(f"📊 Total de páginas encontradas: {len(pages)}")
    
    if not pages:
        print("❌ Nenhuma página encontrada. Verifique o token e database ID.")
        return
    
    # Analisar cada página
    print("\n📋 Analisando páginas...")
    analysis_results = []
    total_score = 0
    
    for i, page in enumerate(pages, 1):
        print(f"   📄 Analisando página {i}/{len(pages)}: {page.get('id', 'N/A')}")
        
        page_data = analyze_page_properties(page)
        compliance = check_boilerplate_compliance(page_data)
        
        analysis_results.append({
            "page_data": page_data,
            "compliance": compliance
        })
        
        total_score += compliance["score"]
    
    # Calcular estatísticas
    avg_score = total_score / len(pages) if pages else 0
    conformes = len([r for r in analysis_results if r["compliance"]["score"] >= 80])
    nao_conformes = len([r for r in analysis_results if 60 <= r["compliance"]["score"] < 80])
    criticos = len([r for r in analysis_results if r["compliance"]["score"] < 60])
    
    # Gerar relatório
    print("\n================================================================================")
    print("RELATÓRIO DE ANÁLISE")
    print("================================================================================")
    print(f"📊 Total de páginas analisadas: {len(pages)}")
    print(f"📈 Pontuação média: {avg_score:.1f}/100")
    print(f"✅ Conformes (≥80%): {conformes} ({conformes/len(pages)*100:.1f}%)")
    print(f"⚠️ Não conformes (60-79%): {nao_conformes} ({nao_conformes/len(pages)*100:.1f}%)")
    print(f"❌ Críticos (<60%): {criticos} ({criticos/len(pages)*100:.1f}%)")
    
    # Mostrar problemas mais comuns
    print("\n📋 PROBLEMAS MAIS COMUNS:")
    all_issues = []
    for result in analysis_results:
        all_issues.extend(result["compliance"]["issues"])
    
    issue_counts = {}
    for issue in all_issues:
        issue_counts[issue] = issue_counts.get(issue, 0) + 1
    
    sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)
    for issue, count in sorted_issues[:10]:
        print(f"   {issue}: {count} ocorrências")
    
    # Mostrar páginas críticas
    print("\n🚨 PÁGINAS CRÍTICAS (pontuação < 60%):")
    critical_pages = [r for r in analysis_results if r["compliance"]["score"] < 60]
    for result in critical_pages[:5]:  # Mostrar apenas 5
        page_data = result["page_data"]
        compliance = result["compliance"]
        print(f"   📄 {page_data['name'][:50]}... - {compliance['score']}/100")
        for issue in compliance["issues"][:3]:  # Mostrar apenas 3 issues
            print(f"      {issue}")
    
    # Salvar relatório detalhado
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "total_pages": len(pages),
        "average_score": avg_score,
        "conformes": conformes,
        "nao_conformes": nao_conformes,
        "criticos": criticos,
        "detailed_results": analysis_results
    }
    
    with open("relatorio_analise_biblioteca_gestao.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Relatório detalhado salvo em: relatorio_analise_biblioteca_gestao.json")
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("   1. Corrigir páginas críticas")
    print("   2. Aplicar taxonomias corretas")
    print("   3. Preencher propriedades obrigatórias")
    print("   4. Sincronizar com Notion")

if __name__ == "__main__":
    main()
