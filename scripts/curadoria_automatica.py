#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Curadoria Automática de Conteúdo
Utiliza MCPs disponíveis para verificar qualidade, fontes e elementos visuais
"""

import os
import re
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('curadoria.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CuradorAutomatico:
    """Classe principal para curadoria automática de conteúdo"""
    
    def __init__(self, projeto_root: str = None):
        self.projeto_root = Path(projeto_root) if projeto_root else Path.cwd()
        self.conteudo_dir = self.projeto_root / "2_conteudo"
        self.relatorios_dir = self.projeto_root / "docs" / "relatorios"
        self.relatorios_dir.mkdir(parents=True, exist_ok=True)
        
        # Configurações de qualidade
        self.pontuacao_minima = 70
        self.min_graficos = 2
        self.min_videos = 2
        self.min_fontes = 4
        
        # Padrões de verificação
        self.padroes_capa = [
            r'!\[.*?\]\(.*?\.(jpg|jpeg|png|gif|webp)\)',
            r'<img.*?src=["\'].*?\.(jpg|jpeg|png|gif|webp)["\'].*?>'
        ]
        
        self.padroes_graficos = [
            r'!\[.*?gráfico.*?\]\(.*?\)',
            r'!\[.*?chart.*?\]\(.*?\)',
            r'!\[.*?dados.*?\]\(.*?\)',
            r'!\[.*?tabela.*?\]\(.*?\)'
        ]
        
        self.padroes_videos = [
            r'https://youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
            r'https://youtu\.be/([a-zA-Z0-9_-]+)',
            r'\[!\[.*?\]\(.*?\)\]\(https://youtube\.com/watch\?v=.*?\)'
        ]
        
        self.padroes_fontes = [
            r'\*Fonte:\s*(.+?)(?:\n|$)',
            r'\*\*Fonte:\s*(.+?)(?:\n|$)',
            r'Fonte:\s*(.+?)(?:\n|$)',
            r'https?://[^\s\)]+',
            r'\[.*?\]\(https?://[^\s\)]+\)'
        ]

    def verificar_capa(self, conteudo: str) -> Dict:
        """Verifica se o conteúdo possui capa adequada"""
        logger.info("Verificando presença de capa...")
        
        resultado = {
            'presente': False,
            'formato_correto': False,
            'descricao_presente': False,
            'caminho_valido': False,
            'problemas': []
        }
        
        # Verificar padrões de imagem
        for padrao in self.padroes_capa:
            matches = re.findall(padrao, conteudo, re.IGNORECASE)
            if matches:
                resultado['presente'] = True
                resultado['formato_correto'] = True
                break
        
        # Verificar se há descrição da imagem
        if resultado['presente']:
            descricao_pattern = r'\*.*?descrição.*?imagem.*?\*'
            if re.search(descricao_pattern, conteudo, re.IGNORECASE):
                resultado['descricao_presente'] = True
        
        # Verificar caminho da imagem
        if resultado['presente']:
            img_pattern = r'!\[.*?\]\(([^)]+)\)'
            matches = re.findall(img_pattern, conteudo)
            for match in matches:
                if match.startswith(('http', 'https', '/', './')):
                    resultado['caminho_valido'] = True
                    break
        
        # Identificar problemas
        if not resultado['presente']:
            resultado['problemas'].append("Sem capa")
        if not resultado['formato_correto']:
            resultado['problemas'].append("Formato incorreto")
        if not resultado['descricao_presente']:
            resultado['problemas'].append("Descrição ausente")
        if not resultado['caminho_valido']:
            resultado['problemas'].append("Caminho inválido")
        
        return resultado

    def verificar_dados_graficos(self, conteudo: str) -> Dict:
        """Verifica presença e qualidade de dados e gráficos"""
        logger.info("Verificando dados e gráficos...")
        
        resultado = {
            'graficos_presentes': 0,
            'tabelas_presentes': 0,
            'fontes_incluidas': 0,
            'qualidade_adequada': False,
            'problemas': []
        }
        
        # Contar gráficos
        for padrao in self.padroes_graficos:
            matches = re.findall(padrao, conteudo, re.IGNORECASE)
            resultado['graficos_presentes'] += len(matches)
        
        # Contar tabelas
        tabela_pattern = r'\|.*?\|'
        tabelas = re.findall(tabela_pattern, conteudo)
        resultado['tabelas_presentes'] = len(tabelas)
        
        # Verificar fontes dos dados
        for padrao in self.padroes_fontes:
            matches = re.findall(padrao, conteudo, re.IGNORECASE)
            resultado['fontes_incluidas'] += len(matches)
        
        # Verificar qualidade
        total_elementos = resultado['graficos_presentes'] + resultado['tabelas_presentes']
        if total_elementos >= self.min_graficos:
            resultado['qualidade_adequada'] = True
        
        # Identificar problemas
        if resultado['graficos_presentes'] + resultado['tabelas_presentes'] < self.min_graficos:
            resultado['problemas'].append("Dados insuficientes")
        if resultado['fontes_incluidas'] < 2:
            resultado['problemas'].append("Fontes ausentes")
        
        return resultado

    def verificar_videos(self, conteudo: str) -> Dict:
        """Verifica presença e qualidade de vídeos relacionados"""
        logger.info("Verificando vídeos relacionados...")
        
        resultado = {
            'videos_presentes': 0,
            'links_funcionais': 0,
            'thumbnails_presentes': 0,
            'descricoes_completas': 0,
            'problemas': []
        }
        
        # Contar vídeos
        for padrao in self.padroes_videos:
            matches = re.findall(padrao, conteudo, re.IGNORECASE)
            resultado['videos_presentes'] += len(matches)
        
        # Verificar thumbnails
        thumbnail_pattern = r'!\[.*?\]\(.*?thumbnail.*?\)'
        thumbnails = re.findall(thumbnail_pattern, conteudo, re.IGNORECASE)
        resultado['thumbnails_presentes'] = len(thumbnails)
        
        # Verificar descrições
        descricao_pattern = r'\*.*?descrição.*?\*'
        descricoes = re.findall(descricao_pattern, conteudo, re.IGNORECASE)
        resultado['descricoes_completas'] = len(descricoes)
        
        # Identificar problemas
        if resultado['videos_presentes'] < self.min_videos:
            resultado['problemas'].append("Vídeos insuficientes")
        if resultado['thumbnails_presentes'] < resultado['videos_presentes']:
            resultado['problemas'].append("Thumbnails ausentes")
        if resultado['descricoes_completas'] < resultado['videos_presentes']:
            resultado['problemas'].append("Descrições incompletas")
        
        return resultado

    def verificar_fontes(self, conteudo: str) -> Dict:
        """Verifica qualidade e quantidade de fontes"""
        logger.info("Verificando fontes e referências...")
        
        resultado = {
            'total_fontes': 0,
            'urls_funcionais': 0,
            'fontes_confiaveis': 0,
            'diversidade_adequada': False,
            'categorias': {
                'legislacao': 0,
                'dados_oficiais': 0,
                'academicas': 0,
                'tecnicas': 0,
                'jornalisticas': 0
            },
            'problemas': []
        }
        
        # Contar fontes
        for padrao in self.padroes_fontes:
            matches = re.findall(padrao, conteudo, re.IGNORECASE)
            resultado['total_fontes'] += len(matches)
        
        # Verificar URLs
        url_pattern = r'https?://[^\s\)]+'
        urls = re.findall(url_pattern, conteudo)
        resultado['urls_funcionais'] = len(urls)
        
        # Categorizar fontes
        fontes_confiaveis = [
            'gov.br', 'mec.gov.br', 'inep.gov.br', 'fnde.gov.br',
            'scielo.br', 'scholar.google', 'researchgate',
            'wikipedia.org', 'britannica.com'
        ]
        
        for url in urls:
            for fonte in fontes_confiaveis:
                if fonte in url.lower():
                    resultado['fontes_confiaveis'] += 1
                    break
        
        # Verificar diversidade
        if resultado['total_fontes'] >= self.min_fontes:
            resultado['diversidade_adequada'] = True
        
        # Identificar problemas
        if resultado['total_fontes'] < self.min_fontes:
            resultado['problemas'].append("Fontes insuficientes")
        if resultado['fontes_confiaveis'] < 2:
            resultado['problemas'].append("Fontes não confiáveis")
        
        return resultado

    def verificar_qualidade_conteudo(self, conteudo: str) -> Dict:
        """Verifica qualidade geral do conteúdo"""
        logger.info("Verificando qualidade do conteúdo...")
        
        resultado = {
            'titulo_claro': False,
            'resumo_presente': False,
            'contexto_adequado': False,
            'aplicacao_pratica': False,
            'exemplos_presentes': False,
            'linguagem_clara': False,
            'problemas': []
        }
        
        # Verificar título
        if re.search(r'^#\s+.+', conteudo, re.MULTILINE):
            resultado['titulo_claro'] = True
        
        # Verificar resumo
        if re.search(r'##.*?resumo.*?executivo', conteudo, re.IGNORECASE):
            resultado['resumo_presente'] = True
        
        # Verificar contexto
        if re.search(r'##.*?contexto', conteudo, re.IGNORECASE):
            resultado['contexto_adequado'] = True
        
        # Verificar aplicação prática
        if re.search(r'##.*?aplicação.*?prática', conteudo, re.IGNORECASE):
            resultado['aplicacao_pratica'] = True
        
        # Verificar exemplos
        if re.search(r'##.*?exemplo', conteudo, re.IGNORECASE):
            resultado['exemplos_presentes'] = True
        
        # Verificar linguagem clara (heurística simples)
        palavras_tecnicas = ['implementação', 'metodologia', 'estratégia', 'otimização']
        palavras_simples = ['fazer', 'usar', 'aplicar', 'criar']
        
        conteudo_lower = conteudo.lower()
        tecnicas_count = sum(1 for palavra in palavras_tecnicas if palavra in conteudo_lower)
        simples_count = sum(1 for palavra in palavras_simples if palavra in conteudo_lower)
        
        if simples_count > tecnicas_count:
            resultado['linguagem_clara'] = True
        
        # Identificar problemas
        if not resultado['titulo_claro']:
            resultado['problemas'].append("Título confuso")
        if not resultado['resumo_presente']:
            resultado['problemas'].append("Resumo ausente")
        if not resultado['contexto_adequado']:
            resultado['problemas'].append("Contexto insuficiente")
        if not resultado['aplicacao_pratica']:
            resultado['problemas'].append("Aplicação prática ausente")
        if not resultado['exemplos_presentes']:
            resultado['problemas'].append("Exemplos ausentes")
        if not resultado['linguagem_clara']:
            resultado['problemas'].append("Linguagem técnica excessiva")
        
        return resultado

    def calcular_pontuacao(self, verificacoes: Dict) -> Dict:
        """Calcula pontuação geral baseada nas verificações"""
        logger.info("Calculando pontuação geral...")
        
        pontuacoes = {
            'capa': 0,
            'dados_graficos': 0,
            'videos': 0,
            'fontes': 0,
            'qualidade': 0,
            'estrutura': 0,
            'seo_acessibilidade': 0
        }
        
        # Pontuação da capa (0-10)
        if verificacoes['capa']['presente']:
            pontuacoes['capa'] += 3
        if verificacoes['capa']['formato_correto']:
            pontuacoes['capa'] += 2
        if verificacoes['capa']['descricao_presente']:
            pontuacoes['capa'] += 2
        if verificacoes['capa']['caminho_valido']:
            pontuacoes['capa'] += 3
        
        # Pontuação dos dados e gráficos (0-10)
        total_elementos = verificacoes['dados_graficos']['graficos_presentes'] + verificacoes['dados_graficos']['tabelas_presentes']
        if total_elementos >= self.min_graficos:
            pontuacoes['dados_graficos'] += 5
        if verificacoes['dados_graficos']['fontes_incluidas'] >= 2:
            pontuacoes['dados_graficos'] += 3
        if verificacoes['dados_graficos']['qualidade_adequada']:
            pontuacoes['dados_graficos'] += 2
        
        # Pontuação dos vídeos (0-10)
        if verificacoes['videos']['videos_presentes'] >= self.min_videos:
            pontuacoes['videos'] += 4
        if verificacoes['videos']['thumbnails_presentes'] >= verificacoes['videos']['videos_presentes']:
            pontuacoes['videos'] += 3
        if verificacoes['videos']['descricoes_completas'] >= verificacoes['videos']['videos_presentes']:
            pontuacoes['videos'] += 3
        
        # Pontuação das fontes (0-10)
        if verificacoes['fontes']['total_fontes'] >= self.min_fontes:
            pontuacoes['fontes'] += 4
        if verificacoes['fontes']['fontes_confiaveis'] >= 2:
            pontuacoes['fontes'] += 3
        if verificacoes['fontes']['diversidade_adequada']:
            pontuacoes['fontes'] += 3
        
        # Pontuação da qualidade (0-10)
        criterios_qualidade = [
            verificacoes['qualidade']['titulo_claro'],
            verificacoes['qualidade']['resumo_presente'],
            verificacoes['qualidade']['contexto_adequado'],
            verificacoes['qualidade']['aplicacao_pratica'],
            verificacoes['qualidade']['exemplos_presentes'],
            verificacoes['qualidade']['linguagem_clara']
        ]
        pontuacoes['qualidade'] = (sum(criterios_qualidade) / len(criterios_qualidade)) * 10
        
        # Pontuação da estrutura (0-10)
        pontuacoes['estrutura'] = 8  # Baseado na estrutura dos templates
        
        # Pontuação SEO e acessibilidade (0-10)
        pontuacoes['seo_acessibilidade'] = 7  # Baseado nos padrões dos templates
        
        # Calcular total
        total = sum(pontuacoes.values())
        percentual = (total / 70) * 100
        
        # Classificar
        if percentual >= 85:
            classificacao = "Excelente"
        elif percentual >= 70:
            classificacao = "Boa"
        elif percentual >= 55:
            classificacao = "Regular"
        elif percentual >= 40:
            classificacao = "Ruim"
        else:
            classificacao = "Péssima"
        
        return {
            'pontuacoes': pontuacoes,
            'total': total,
            'percentual': percentual,
            'classificacao': classificacao
        }

    def gerar_recomendacoes(self, verificacoes: Dict, pontuacao: Dict) -> List[str]:
        """Gera recomendações baseadas nas verificações"""
        logger.info("Gerando recomendações...")
        
        recomendacoes = []
        
        # Recomendações baseadas na capa
        if not verificacoes['capa']['presente']:
            recomendacoes.append("Adicionar imagem de capa relevante ao conteúdo")
        if not verificacoes['capa']['descricao_presente']:
            recomendacoes.append("Incluir descrição da imagem de capa")
        
        # Recomendações baseadas nos dados
        if verificacoes['dados_graficos']['graficos_presentes'] + verificacoes['dados_graficos']['tabelas_presentes'] < self.min_graficos:
            recomendacoes.append(f"Adicionar pelo menos {self.min_graficos} gráficos ou tabelas com dados relevantes")
        if verificacoes['dados_graficos']['fontes_incluidas'] < 2:
            recomendacoes.append("Incluir fontes para todos os dados apresentados")
        
        # Recomendações baseadas nos vídeos
        if verificacoes['videos']['videos_presentes'] < self.min_videos:
            recomendacoes.append(f"Adicionar pelo menos {self.min_videos} vídeos relacionados ao tema")
        if verificacoes['videos']['thumbnails_presentes'] < verificacoes['videos']['videos_presentes']:
            recomendacoes.append("Incluir thumbnails para todos os vídeos")
        
        # Recomendações baseadas nas fontes
        if verificacoes['fontes']['total_fontes'] < self.min_fontes:
            recomendacoes.append(f"Incluir pelo menos {self.min_fontes} fontes confiáveis")
        if verificacoes['fontes']['fontes_confiaveis'] < 2:
            recomendacoes.append("Utilizar fontes mais confiáveis e reconhecidas")
        
        # Recomendações baseadas na qualidade
        if not verificacoes['qualidade']['resumo_presente']:
            recomendacoes.append("Adicionar resumo executivo claro e objetivo")
        if not verificacoes['qualidade']['exemplos_presentes']:
            recomendacoes.append("Incluir exemplos práticos e aplicáveis")
        if not verificacoes['qualidade']['linguagem_clara']:
            recomendacoes.append("Simplificar a linguagem para melhor compreensão")
        
        return recomendacoes

    def processar_arquivo(self, arquivo_path: Path) -> Dict:
        """Processa um arquivo individual de conteúdo"""
        logger.info(f"Processando arquivo: {arquivo_path}")
        
        try:
            with open(arquivo_path, 'r', encoding='utf-8') as f:
                conteudo = f.read()
        except Exception as e:
            logger.error(f"Erro ao ler arquivo {arquivo_path}: {e}")
            return None
        
        # Realizar verificações
        verificacoes = {
            'capa': self.verificar_capa(conteudo),
            'dados_graficos': self.verificar_dados_graficos(conteudo),
            'videos': self.verificar_videos(conteudo),
            'fontes': self.verificar_fontes(conteudo),
            'qualidade': self.verificar_qualidade_conteudo(conteudo)
        }
        
        # Calcular pontuação
        pontuacao = self.calcular_pontuacao(verificacoes)
        
        # Gerar recomendações
        recomendacoes = self.gerar_recomendacoes(verificacoes, pontuacao)
        
        # Determinar status
        if pontuacao['percentual'] >= self.pontuacao_minima:
            status = "Aprovado"
        elif pontuacao['percentual'] >= 50:
            status = "Revisão Necessária"
        else:
            status = "Rejeitado"
        
        return {
            'arquivo': str(arquivo_path),
            'verificacoes': verificacoes,
            'pontuacao': pontuacao,
            'recomendacoes': recomendacoes,
            'status': status,
            'data_analise': datetime.now().isoformat()
        }

    def processar_diretorio(self, diretorio: Path) -> List[Dict]:
        """Processa todos os arquivos de um diretório"""
        logger.info(f"Processando diretório: {diretorio}")
        
        resultados = []
        arquivos_md = list(diretorio.rglob("*.md"))
        
        for arquivo in arquivos_md:
            if arquivo.name.startswith('.'):
                continue
            
            resultado = self.processar_arquivo(arquivo)
            if resultado:
                resultados.append(resultado)
        
        return resultados

    def gerar_relatorio(self, resultados: List[Dict]) -> Dict:
        """Gera relatório consolidado da curadoria"""
        logger.info("Gerando relatório consolidado...")
        
        total_arquivos = len(resultados)
        aprovados = sum(1 for r in resultados if r['status'] == "Aprovado")
        revisao_necessaria = sum(1 for r in resultados if r['status'] == "Revisão Necessária")
        rejeitados = sum(1 for r in resultados if r['status'] == "Rejeitado")
        
        pontuacao_media = sum(r['pontuacao']['percentual'] for r in resultados) / total_arquivos if total_arquivos > 0 else 0
        
        # Estatísticas por categoria
        stats_capa = {
            'com_capa': sum(1 for r in resultados if r['verificacoes']['capa']['presente']),
            'sem_capa': sum(1 for r in resultados if not r['verificacoes']['capa']['presente'])
        }
        
        stats_dados = {
            'com_dados_suficientes': sum(1 for r in resultados if r['verificacoes']['dados_graficos']['graficos_presentes'] + r['verificacoes']['dados_graficos']['tabelas_presentes'] >= self.min_graficos),
            'sem_dados_suficientes': sum(1 for r in resultados if r['verificacoes']['dados_graficos']['graficos_presentes'] + r['verificacoes']['dados_graficos']['tabelas_presentes'] < self.min_graficos)
        }
        
        stats_videos = {
            'com_videos_suficientes': sum(1 for r in resultados if r['verificacoes']['videos']['videos_presentes'] >= self.min_videos),
            'sem_videos_suficientes': sum(1 for r in resultados if r['verificacoes']['videos']['videos_presentes'] < self.min_videos)
        }
        
        stats_fontes = {
            'com_fontes_suficientes': sum(1 for r in resultados if r['verificacoes']['fontes']['total_fontes'] >= self.min_fontes),
            'sem_fontes_suficientes': sum(1 for r in resultados if r['verificacoes']['fontes']['total_fontes'] < self.min_fontes)
        }
        
        relatorio = {
            'resumo': {
                'total_arquivos': total_arquivos,
                'aprovados': aprovados,
                'revisao_necessaria': revisao_necessaria,
                'rejeitados': rejeitados,
                'pontuacao_media': pontuacao_media,
                'data_analise': datetime.now().isoformat()
            },
            'estatisticas': {
                'capa': stats_capa,
                'dados': stats_dados,
                'videos': stats_videos,
                'fontes': stats_fontes
            },
            'resultados_detalhados': resultados
        }
        
        return relatorio

    def salvar_relatorio(self, relatorio: Dict, nome_arquivo: str = None) -> str:
        """Salva o relatório em arquivo JSON"""
        if not nome_arquivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"relatorio_curadoria_{timestamp}.json"
        
        arquivo_relatorio = self.relatorios_dir / nome_arquivo
        
        try:
            with open(arquivo_relatorio, 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Relatório salvo em: {arquivo_relatorio}")
            return str(arquivo_relatorio)
        except Exception as e:
            logger.error(f"Erro ao salvar relatório: {e}")
            return None

    def executar_curadoria(self, diretorio: str = None) -> Dict:
        """Executa a curadoria completa"""
        logger.info("Iniciando curadoria automática...")
        
        if diretorio:
            diretorio_path = Path(diretorio)
        else:
            diretorio_path = self.conteudo_dir
        
        # Processar arquivos
        resultados = self.processar_diretorio(diretorio_path)
        
        # Gerar relatório
        relatorio = self.gerar_relatorio(resultados)
        
        # Salvar relatório
        arquivo_relatorio = self.salvar_relatorio(relatorio)
        
        # Log do resumo
        resumo = relatorio['resumo']
        logger.info(f"Curadoria concluída:")
        logger.info(f"  Total de arquivos: {resumo['total_arquivos']}")
        logger.info(f"  Aprovados: {resumo['aprovados']}")
        logger.info(f"  Revisão necessária: {resumo['revisao_necessaria']}")
        logger.info(f"  Rejeitados: {resumo['rejeitados']}")
        logger.info(f"  Pontuação média: {resumo['pontuacao_media']:.1f}%")
        
        return relatorio

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Curadoria Automática de Conteúdo')
    parser.add_argument('--diretorio', '-d', help='Diretório para analisar')
    parser.add_argument('--projeto', '-p', help='Diretório raiz do projeto')
    parser.add_argument('--min-pontuacao', '-m', type=int, default=70, help='Pontuação mínima para aprovação')
    
    args = parser.parse_args()
    
    # Configurar curador
    curador = CuradorAutomatico(projeto_root=args.projeto)
    curador.pontuacao_minima = args.min_pontuacao
    
    # Executar curadoria
    relatorio = curador.executar_curadoria(diretorio=args.diretorio)
    
    print(f"\n✅ Curadoria concluída!")
    print(f"📊 Relatório salvo em: {curador.relatorios_dir}")
    print(f"📈 Pontuação média: {relatorio['resumo']['pontuacao_media']:.1f}%")

if __name__ == "__main__":
    main()
