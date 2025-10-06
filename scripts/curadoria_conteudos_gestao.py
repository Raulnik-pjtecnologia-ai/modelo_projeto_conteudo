import os
import glob
from datetime import datetime

def avaliar_conteudo(filepath):
    """Avalia conteúdo seguindo critérios de curadoria para Gestão Escolar"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        criterios = {}
        pontuacao = 0
        
        # Critério 1: Estrutura (20 pontos)
        estrutura_score = 0
        
        # Verificar título
        if content.startswith('#'):
            estrutura_score += 5
        
        # Verificar seções obrigatórias
        secoes_obrigatorias = [
            "Resumo Executivo",
            "Contexto e Desafios", 
            "Aplicação Prática",
            "Conclusão",
            "Checklist Inicial"
        ]
        
        secoes_presentes = 0
        for secao in secoes_obrigatorias:
            if secao in content:
                secoes_presentes += 1
        
        estrutura_score += (secoes_presentes / len(secoes_obrigatorias)) * 15
        criterios['Estrutura'] = min(20, estrutura_score)
        pontuacao += criterios['Estrutura']
        
        # Critério 2: Conteúdo (20 pontos)
        conteudo_score = 0
        
        # Verificar tamanho mínimo (deve ter pelo menos 1000 caracteres)
        if len(content) >= 1000:
            conteudo_score += 10
        
        # Verificar presença de exemplos práticos
        if "exemplo" in content.lower() or "caso" in content.lower():
            conteudo_score += 5
        
        # Verificar presença de estratégias
        if "estratégia" in content.lower() or "implementação" in content.lower():
            conteudo_score += 5
        
        criterios['Conteúdo'] = min(20, conteudo_score)
        pontuacao += criterios['Conteúdo']
        
        # Critério 3: Apresentação (20 pontos)
        apresentacao_score = 0
        
        # Verificar formatação markdown
        if "##" in content:  # Subtítulos
            apresentacao_score += 5
        
        # Verificar listas
        if "- [" in content or "1." in content:
            apresentacao_score += 5
        
        # Verificar emojis para organização
        emojis_presentes = content.count("📋") + content.count("🎯") + content.count("💡") + content.count("🚀")
        apresentacao_score += min(10, emojis_presentes * 2)
        
        criterios['Apresentação'] = min(20, apresentacao_score)
        pontuacao += criterios['Apresentação']
        
        # Critério 4: Conformidade Gestão (20 pontos)
        conformidade_score = 0
        
        # Verificar termos específicos de gestão escolar
        termos_gestao = [
            "gestão", "escolar", "educacional", "instituição", 
            "pedagógico", "administrativo", "liderança", "equipe"
        ]
        
        termos_presentes = sum(1 for termo in termos_gestao if termo in content.lower())
        conformidade_score = min(20, (termos_presentes / len(termos_gestao)) * 20)
        
        criterios['Conformidade Gestão'] = conformidade_score
        pontuacao += criterios['Conformidade Gestão']
        
        # Critério 5: Qualidade Técnica (20 pontos)
        qualidade_score = 0
        
        # Verificar referências
        if "referências" in content.lower() or "fontes" in content.lower():
            qualidade_score += 10
        
        # Verificar checklist
        if "checklist" in content.lower() or "- [" in content:
            qualidade_score += 10
        
        criterios['Qualidade Técnica'] = qualidade_score
        pontuacao += criterios['Qualidade Técnica']
        
        return pontuacao, criterios
        
    except Exception as e:
        print(f"Erro ao avaliar {filepath}: {str(e)}")
        return 0, {}

def main():
    print("================================================================================")
    print("CURADORIA AUTOMÁTICA - CONTEÚDOS GESTÃO ESCOLAR")
    print("================================================================================")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Objetivo: Avaliar qualidade de 40 novos conteúdos de gestão")
    
    # Buscar todos os arquivos de gestão
    gestao_files = glob.glob("2_conteudo/02_conteudos_prontos/gestao_escolar/**/*.md", recursive=True)
    
    print(f"\n📊 Total de conteúdos encontrados: {len(gestao_files)}")
    
    if not gestao_files:
        print("❌ Nenhum arquivo de gestão encontrado")
        return
    
    print("🔍 Iniciando avaliação...")
    
    aprovados = 0
    em_revisao = 0
    rejeitados = 0
    total_score = 0
    
    for i, filepath in enumerate(gestao_files, 1):
        filename = os.path.basename(filepath)
        print(f"\n--- Conteúdo {i}/{len(gestao_files)} ---")
        print(f"Arquivo: {filename}")
        
        pontuacao, criterios = avaliar_conteudo(filepath)
        total_score += pontuacao
        
        print(f"   📊 Estrutura: {criterios.get('Estrutura', 0)}/20")
        print(f"   📝 Conteúdo: {criterios.get('Conteúdo', 0)}/20")
        print(f"   🎯 Apresentação: {criterios.get('Apresentação', 0)}/20")
        print(f"   🏫 Conformidade Gestão: {criterios.get('Conformidade Gestão', 0)}/20")
        print(f"   ✅ Qualidade Técnica: {criterios.get('Qualidade Técnica', 0)}/20")
        print(f"   🎯 TOTAL: {pontuacao}/100")
        
        if pontuacao >= 85:
            print(f"   ✅ APROVADO")
            aprovados += 1
        elif pontuacao >= 70:
            print(f"   ⚠️ EM REVISÃO")
            em_revisao += 1
        else:
            print(f"   ❌ REJEITADO")
            rejeitados += 1
    
    # Relatório final
    avg_score = total_score / len(gestao_files) if gestao_files else 0
    
    print("\n================================================================================")
    print("RELATÓRIO FINAL DA CURADORIA")
    print("================================================================================")
    print(f"📊 Total de conteúdos avaliados: {len(gestao_files)}")
    print(f"✅ Aprovados (≥85%): {aprovados}")
    print(f"⚠️ Em Revisão (70-84%): {em_revisao}")
    print(f"❌ Rejeitados (<70%): {rejeitados}")
    print(f"📈 Pontuação média: {avg_score:.1f}/100")
    print(f"🎯 Taxa de aprovação: {(aprovados/len(gestao_files)*100):.1f}%")
    
    # Salvar relatório
    relatorio = {
        "timestamp": datetime.now().isoformat(),
        "total_conteudos": len(gestao_files),
        "aprovados": aprovados,
        "em_revisao": em_revisao,
        "rejeitados": rejeitados,
        "pontuacao_media": avg_score,
        "taxa_aprovacao": (aprovados/len(gestao_files)*100) if gestao_files else 0
    }
    
    with open("relatorio_curadoria_gestao.json", "w", encoding="utf-8") as f:
        import json
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Relatório salvo em: relatorio_curadoria_gestao.json")
    
    if aprovados == len(gestao_files):
        print("\n🎉 TODOS OS CONTEÚDOS APROVADOS! PRONTO PARA SINCRONIZAÇÃO!")
    else:
        print(f"\n⚠️ {len(gestao_files) - aprovados} conteúdos precisam de revisão")

if __name__ == "__main__":
    main()
