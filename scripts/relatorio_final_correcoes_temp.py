import os
import json
from datetime import datetime

def gerar_relatorio_final_correcoes():
    """Gerar relatório final consolidado de todas as correções realizadas."""
    print("RELATORIO FINAL DE CORRECOES DA DISTRIBUICAO")
    print("=" * 70)
    
    try:
        # Carregar dados de todas as correções
        dados_verificacao_inicial = {}
        dados_correcao_principal = {}
        dados_verificacao_principal = {}
        dados_correcao_restante = {}
        dados_verificacao_restante = {}
        dados_contagem_final = {}
        
        # Carregar dados da verificação inicial
        try:
            with open("verificacao_distribuicao_conteudos.json", "r", encoding="utf-8") as f:
                dados_verificacao_inicial = json.load(f)
        except FileNotFoundError:
            print("AVISO: Arquivo de verificacao inicial nao encontrado")
        
        # Carregar dados da correção principal
        try:
            with open("correcao_distribuicao_conteudos.json", "r", encoding="utf-8") as f:
                dados_correcao_principal = json.load(f)
        except FileNotFoundError:
            print("AVISO: Arquivo de correcao principal nao encontrado")
        
        # Carregar dados da verificação da correção principal
        try:
            with open("verificacao_correcao_distribuicao.json", "r", encoding="utf-8") as f:
                dados_verificacao_principal = json.load(f)
        except FileNotFoundError:
            print("AVISO: Arquivo de verificacao da correcao principal nao encontrado")
        
        # Carregar dados da correção do restante
        try:
            with open("correcao_restante_conteudos.json", "r", encoding="utf-8") as f:
                dados_correcao_restante = json.load(f)
        except FileNotFoundError:
            print("AVISO: Arquivo de correcao do restante nao encontrado")
        
        # Carregar dados da verificação da correção do restante
        try:
            with open("verificacao_correcao_restante.json", "r", encoding="utf-8") as f:
                dados_verificacao_restante = json.load(f)
        except FileNotFoundError:
            print("AVISO: Arquivo de verificacao da correcao do restante nao encontrado")
        
        # Carregar dados da contagem final
        try:
            with open("contagem_conteudos_banco.json", "r", encoding="utf-8") as f:
                dados_contagem_final = json.load(f)
        except FileNotFoundError:
            print("AVISO: Arquivo de contagem final nao encontrado")
        
        # Gerar relatório consolidado
        relatorio = {
            "data_relatorio": datetime.now().isoformat(),
            "resumo_executivo": {
                "total_conteudos_analisados": dados_verificacao_inicial.get("total_conteudos_analisados", 0),
                "conteudos_com_discrepancia_inicial": dados_verificacao_inicial.get("conteudos_com_discrepancia", 0),
                "percentual_acuracia_inicial": dados_verificacao_inicial.get("percentual_acuracia", 0),
                "correcoes_principais_aplicadas": dados_correcao_principal.get("correcoes_aplicadas", 0),
                "correcoes_restantes_aplicadas": dados_correcao_restante.get("correcoes_aplicadas", 0),
                "total_correcoes_aplicadas": (dados_correcao_principal.get("correcoes_aplicadas", 0) + 
                                            dados_correcao_restante.get("correcoes_aplicadas", 0)),
                "verificacoes_principais_corretas": dados_verificacao_principal.get("verificacoes_corretas", 0),
                "verificacoes_restantes_corretas": dados_verificacao_restante.get("verificacoes_corretas", 0),
                "total_verificacoes_corretas": (dados_verificacao_principal.get("verificacoes_corretas", 0) + 
                                              dados_verificacao_restante.get("verificacoes_corretas", 0)),
                "distribuicao_final": dados_contagem_final.get("tipos_gerais", {})
            },
            "detalhes_por_fase": {
                "fase_1_verificacao_inicial": {
                    "descricao": "Análise inicial da distribuição baseada no título vs conteúdo interno",
                    "total_conteudos": dados_verificacao_inicial.get("total_conteudos_analisados", 0),
                    "conteudos_sem_discrepancia": dados_verificacao_inicial.get("conteudos_sem_discrepancia", 0),
                    "conteudos_com_discrepancia": dados_verificacao_inicial.get("conteudos_com_discrepancia", 0),
                    "percentual_acuracia": dados_verificacao_inicial.get("percentual_acuracia", 0),
                    "distribuicao_anterior": dados_verificacao_inicial.get("distribuicao_anterior", {}),
                    "distribuicao_real": dados_verificacao_inicial.get("distribuicao_real", {})
                },
                "fase_2_correcao_principal": {
                    "descricao": "Correção dos conteúdos com propriedades de categoria existentes",
                    "total_para_corrigir": dados_correcao_principal.get("total_conteudos_para_corrigir", 0),
                    "correcoes_aplicadas": dados_correcao_principal.get("correcoes_aplicadas", 0),
                    "falhas_correcao": dados_correcao_principal.get("falhas_correcao", 0),
                    "percentual_sucesso": dados_correcao_principal.get("percentual_sucesso", 0)
                },
                "fase_3_verificacao_principal": {
                    "descricao": "Verificação das correções principais aplicadas",
                    "total_verificacoes": dados_verificacao_principal.get("total_verificacoes_realizadas", 0),
                    "verificacoes_corretas": dados_verificacao_principal.get("verificacoes_corretas", 0),
                    "verificacoes_incorretas": dados_verificacao_principal.get("verificacoes_incorretas", 0),
                    "percentual_sucesso": dados_verificacao_principal.get("percentual_sucesso", 0)
                },
                "fase_4_correcao_restante": {
                    "descricao": "Correção dos conteúdos restantes (criação de propriedades)",
                    "total_para_corrigir": dados_correcao_restante.get("total_conteudos_para_corrigir", 0),
                    "correcoes_aplicadas": dados_correcao_restante.get("correcoes_aplicadas", 0),
                    "falhas_correcao": dados_correcao_restante.get("falhas_correcao", 0),
                    "percentual_sucesso": dados_correcao_restante.get("percentual_sucesso", 0)
                },
                "fase_5_verificacao_restante": {
                    "descricao": "Verificação das correções restantes aplicadas",
                    "total_verificacoes": dados_verificacao_restante.get("total_verificacoes_realizadas", 0),
                    "verificacoes_corretas": dados_verificacao_restante.get("verificacoes_corretas", 0),
                    "verificacoes_incorretas": dados_verificacao_restante.get("verificacoes_incorretas", 0),
                    "percentual_sucesso": dados_verificacao_restante.get("percentual_sucesso", 0)
                }
            },
            "resultados_finais": {
                "total_conteudos_banco": dados_contagem_final.get("total_conteudos", 0),
                "total_databases": dados_contagem_final.get("total_databases", 0),
                "distribuicao_final_por_tipo": dados_contagem_final.get("tipos_gerais", {}),
                "melhorias_alcancadas": {
                    "gestao_escolar": {
                        "antes": dados_verificacao_inicial.get("distribuicao_anterior", {}).get("Gestao Escolar", 0),
                        "depois": dados_contagem_final.get("tipos_gerais", {}).get("Gestao Escolar", 0),
                        "melhoria": dados_contagem_final.get("tipos_gerais", {}).get("Gestao Escolar", 0) - 
                                  dados_verificacao_inicial.get("distribuicao_anterior", {}).get("Gestao Escolar", 0)
                    },
                    "educacao": {
                        "antes": dados_verificacao_inicial.get("distribuicao_anterior", {}).get("Educacao", 0),
                        "depois": dados_contagem_final.get("tipos_gerais", {}).get("Educacao", 0),
                        "melhoria": dados_contagem_final.get("tipos_gerais", {}).get("Educacao", 0) - 
                                  dados_verificacao_inicial.get("distribuicao_anterior", {}).get("Educacao", 0)
                    }
                }
            }
        }
        
        # Salvar relatório
        with open("relatorio_final_correcoes_distribuicao.json", "w", encoding="utf-8") as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False, default=str)
        
        # Exibir resumo
        print(f"\nRESUMO EXECUTIVO:")
        print(f"=" * 70)
        print(f"Total de conteudos analisados: {relatorio['resumo_executivo']['total_conteudos_analisados']}")
        print(f"Conteudos com discrepancia inicial: {relatorio['resumo_executivo']['conteudos_com_discrepancia_inicial']}")
        print(f"Percentual de acuracia inicial: {relatorio['resumo_executivo']['percentual_acuracia_inicial']:.1f}%")
        print(f"Total de correcoes aplicadas: {relatorio['resumo_executivo']['total_correcoes_aplicadas']}")
        print(f"Total de verificacoes corretas: {relatorio['resumo_executivo']['total_verificacoes_corretas']}")
        
        print(f"\nMELHORIAS ALCANCADAS:")
        print(f"=" * 70)
        gestao_antes = relatorio['resultados_finais']['melhorias_alcancadas']['gestao_escolar']['antes']
        gestao_depois = relatorio['resultados_finais']['melhorias_alcancadas']['gestao_escolar']['depois']
        gestao_melhoria = relatorio['resultados_finais']['melhorias_alcancadas']['gestao_escolar']['melhoria']
        
        educacao_antes = relatorio['resultados_finais']['melhorias_alcancadas']['educacao']['antes']
        educacao_depois = relatorio['resultados_finais']['melhorias_alcancadas']['educacao']['depois']
        educacao_melhoria = relatorio['resultados_finais']['melhorias_alcancadas']['educacao']['melhoria']
        
        print(f"Gestao Escolar: {gestao_antes} -> {gestao_depois} (+{gestao_melhoria})")
        print(f"Educacao: {educacao_antes} -> {educacao_depois} (+{educacao_melhoria})")
        
        print(f"\nDISTRIBUICAO FINAL:")
        print(f"=" * 70)
        for tipo, count in sorted(relatorio['resumo_executivo']['distribuicao_final'].items(), 
                                 key=lambda x: x[1], reverse=True):
            percentual = (count / relatorio['resumo_executivo']['total_conteudos_analisados']) * 100 if relatorio['resumo_executivo']['total_conteudos_analisados'] > 0 else 0
            print(f"   {tipo}: {count} ({percentual:.1f}%)")
        
        print(f"\nRELATORIO FINAL GERADO!")
        print(f"   Arquivo: relatorio_final_correcoes_distribuicao.json")
        print(f"   Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        return True
        
    except Exception as e:
        print(f"Erro ao gerar relatorio final: {e}")
        return False

def main():
    print("RELATORIO FINAL DE CORRECOES DA DISTRIBUICAO")
    print("=" * 70)
    
    sucesso = gerar_relatorio_final_correcoes()
    
    if sucesso:
        print(f"\nRELATORIO FINAL GERADO COM SUCESSO!")
        print(f"   Todas as correcoes foram consolidadas")
        print(f"   Verificar arquivo relatorio_final_correcoes_distribuicao.json")
    else:
        print(f"\nERRO AO GERAR RELATORIO FINAL!")
        print(f"   Verificar arquivos de dados e tentar novamente")
    
    return sucesso

if __name__ == "__main__":
    main()
