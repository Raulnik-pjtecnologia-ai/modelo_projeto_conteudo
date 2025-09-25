import os
import json
import time
from pathlib import Path
from datetime import datetime, timezone
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

if not NOTION_TOKEN or not DATABASE_ID:
    print("Erro: NOTION_TOKEN ou DATABASE_ID não configurados nas variáveis de ambiente.")
    exit()

notion = Client(auth=NOTION_TOKEN)

# IDs das categorias obrigatórias (Regra 2)
CATEGORIAS_OBRIGATORIAS = {
    "Financeiro": "2325113a91a3819f8d12ceeeff041cb7",
    "Formação": "2325113a91a3818fb7e6d8905ae463e2", 
    "Governança": "2655113a91a3807099c0d2027c3c36a3",
    "Tecnologia e Sistemas": "2325113a91a381b9a393fec761b34d1a",
    "Infraestrutura": "2325113a91a381f0b0e1eb04ee60746c",
    "Gestão de Pessoas": "2325113a91a381b9940cc7edf1d86b41",
    "Administração Escolar": "2325113a91a381e7926bdf4edbd9e525",
    "Pedagógico": "2325113a91a381c7a475dc537a11c70c",
    "Legislação": "2325113a91a3810aa7bff6c18e61d662"
}

def carregar_dados_bloco1():
    """Carrega os dados do Bloco 1."""
    try:
        with open("dados_bloco1_analise_notion.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar dados do Bloco 1: {e}")
        return None

def verificar_categorizacao_pagina(page_id, titulo, tipo):
    """Verifica se uma página está adequadamente categorizada."""
    try:
        # Buscar página atual
        page = notion.pages.retrieve(page_id=page_id)
        
        # Verificar categoria (relação)
        categoria_obj = page["properties"].get("Categoria", {}).get("relation", [])
        categoria_ids = [cat["id"] for cat in categoria_obj]
        
        # Verificar tags
        tags_obj = page["properties"].get("Tags", {}).get("multi_select", [])
        tag_names = [tag["name"] for tag in tags_obj]
        
        # Verificar status
        status = page["properties"].get("Status editorial", {}).get("status", {}).get("name", "")
        
        # Análise de conformidade
        conformidade = {
            "tem_categoria": len(categoria_ids) > 0,
            "categoria_valida": any(cat_id in CATEGORIAS_OBRIGATORIAS.values() for cat_id in categoria_ids),
            "tem_tags": len(tag_names) > 0,
            "status_adequado": status in ["Rascunho", "Em Revisão", "Aprovado", "Publicado"],
            "categoria_ids": categoria_ids,
            "tags": tag_names,
            "status": status
        }
        
        # Determinar categoria esperada baseada no título e tipo
        categoria_esperada = determinar_categoria_esperada(titulo, tipo)
        conformidade["categoria_esperada"] = categoria_esperada
        
        # Verificar se a categoria está correta
        categoria_correta = False
        if categoria_esperada and categoria_esperada in CATEGORIAS_OBRIGATORIAS:
            categoria_id_esperada = CATEGORIAS_OBRIGATORIAS[categoria_esperada]
            categoria_correta = categoria_id_esperada in categoria_ids
        
        conformidade["categoria_correta"] = categoria_correta
        
        return conformidade
        
    except Exception as e:
        print(f"Erro ao verificar categorização da página {page_id}: {e}")
        return None

def determinar_categoria_esperada(titulo, tipo):
    """Determina a categoria esperada baseada no título e tipo."""
    titulo_lower = titulo.lower()
    
    # Palavras-chave para cada categoria
    keywords = {
        "Financeiro": ["financeiro", "orçamento", "orcamento", "custo", "receita", "despesa", "fluxo de caixa", "contabilidade", "fiscal", "tributário"],
        "Formação": ["formação", "formacao", "capacitação", "capacitacao", "treinamento", "curso", "aprendizagem", "desenvolvimento"],
        "Governança": ["governança", "governanca", "compliance", "auditoria", "controle", "regulamentação", "normas"],
        "Tecnologia e Sistemas": ["tecnologia", "sistema", "digital", "software", "hardware", "informática", "ti", "automação"],
        "Infraestrutura": ["infraestrutura", "instalação", "instalacao", "manutenção", "manutencao", "predial", "física", "fisica"],
        "Gestão de Pessoas": ["pessoas", "recursos humanos", "rh", "funcionário", "funcionario", "colaborador", "liderança", "lideranca"],
        "Administração Escolar": ["administração", "administracao", "gestão", "gestao", "escolar", "direção", "direcao", "coordenação"],
        "Pedagógico": ["pedagógico", "pedagogico", "ensino", "aprendizagem", "currículo", "curriculo", "didática", "didatica"],
        "Legislação": ["lei", "legislação", "legislacao", "legal", "jurídico", "juridico", "normativo", "regulamentar"]
    }
    
    # Contar ocorrências de cada categoria
    scores = {}
    for categoria, palavras in keywords.items():
        score = sum(1 for palavra in palavras if palavra in titulo_lower)
        if score > 0:
            scores[categoria] = score
    
    # Retornar categoria com maior score
    if scores:
        return max(scores, key=scores.get)
    
    return None

def main():
    print("🔍 BLOCO 2: VERIFICAÇÃO DE CATEGORIZAÇÃO")
    print("======================================================================")
    print("📋 Aplicando Regra 2: Categorização Notion Obrigatória")
    print("======================================================================")
    
    # Carregar dados do Bloco 1
    dados_bloco1 = carregar_dados_bloco1()
    if not dados_bloco1:
        print("❌ Erro: Não foi possível carregar dados do Bloco 1")
        return
    
    conteudos_gestao = dados_bloco1["conteudos_gestao"]
    print(f"📊 Analisando {len(conteudos_gestao)} conteúdos de gestão...\n")
    
    # Verificar categorização de cada conteúdo
    verificacoes = []
    problemas_categorizacao = []
    
    print("🔍 VERIFICANDO CATEGORIZAÇÃO...")
    print("======================================================================\n")
    
    for i, conteudo in enumerate(conteudos_gestao):
        print(f"{i+1}/{len(conteudos_gestao)} - {conteudo['titulo'][:60]}...")
        
        verificacao = verificar_categorizacao_pagina(
            conteudo["id"], 
            conteudo["titulo"], 
            conteudo["tipo"]
        )
        
        if verificacao:
            verificacoes.append({
                "titulo": conteudo["titulo"],
                "tipo": conteudo["tipo"],
                "id": conteudo["id"],
                "verificacao": verificacao
            })
            
            # Identificar problemas
            problemas = []
            if not verificacao["tem_categoria"]:
                problemas.append("Sem categoria")
            if not verificacao["categoria_valida"]:
                problemas.append("Categoria inválida")
            if not verificacao["categoria_correta"]:
                problemas.append("Categoria incorreta")
            if not verificacao["tem_tags"]:
                problemas.append("Sem tags")
            if not verificacao["status_adequado"]:
                problemas.append("Status inadequado")
            
            if problemas:
                problemas_categorizacao.append({
                    "titulo": conteudo["titulo"],
                    "tipo": conteudo["tipo"],
                    "id": conteudo["id"],
                    "problemas": problemas,
                    "categoria_esperada": verificacao["categoria_esperada"],
                    "categoria_atual": verificacao["categoria_ids"],
                    "tags": verificacao["tags"],
                    "status": verificacao["status"]
                })
        
        if (i + 1) % 50 == 0:
            print(f"✅ Verificadas {i + 1}/{len(conteudos_gestao)} páginas...")
    
    print(f"\n📊 RESUMO DO BLOCO 2:")
    print("======================================================================")
    
    total_verificados = len(verificacoes)
    total_problemas = len(problemas_categorizacao)
    taxa_conformidade = ((total_verificados - total_problemas) / total_verificados * 100) if total_verificados > 0 else 0
    
    print(f"📋 Total de conteúdos verificados: {total_verificados}")
    print(f"✅ Conteúdos em conformidade: {total_verificados - total_problemas}")
    print(f"❌ Conteúdos com problemas: {total_problemas}")
    print(f"📊 Taxa de conformidade: {taxa_conformidade:.1f}%")
    
    # Estatísticas dos problemas
    tipos_problemas = {}
    for item in problemas_categorizacao:
        for problema in item["problemas"]:
            tipos_problemas[problema] = tipos_problemas.get(problema, 0) + 1
    
    print(f"\n📊 TIPOS DE PROBLEMAS ENCONTRADOS:")
    for problema, count in sorted(tipos_problemas.items()):
        print(f"   • {problema}: {count}")
    
    # Salvar dados para próximos blocos
    dados_bloco2 = {
        "data_analise": datetime.now().isoformat(),
        "total_verificados": total_verificados,
        "total_problemas": total_problemas,
        "taxa_conformidade": taxa_conformidade,
        "verificacoes": verificacoes,
        "problemas_categorizacao": problemas_categorizacao,
        "tipos_problemas": tipos_problemas
    }
    
    with open("dados_bloco2_analise_notion.json", "w", encoding="utf-8") as f:
        json.dump(dados_bloco2, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Dados do Bloco 2 salvos em: dados_bloco2_analise_notion.json")
    
    if total_problemas > 0:
        print(f"\n⚠️  {total_problemas} conteúdos precisam de correção na categorização")
        print("   Exemplos de problemas:")
        for i, item in enumerate(problemas_categorizacao[:5]):
            print(f"   {i+1}. {item['titulo'][:50]}... - {', '.join(item['problemas'])}")
    else:
        print(f"\n🎉 Todos os conteúdos estão em conformidade com a categorização!")
    
    print("\n✅ BLOCO 2 CONCLUÍDO!")
    print("   Próximo: Bloco 3 - Verificar conformidade com boilerplate")

if __name__ == "__main__":
    main()
