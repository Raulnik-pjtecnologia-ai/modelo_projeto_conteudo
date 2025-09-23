#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Verificação de Fontes Confiáveis usando MCPs
Integra com ferramentas de busca e verificação de credibilidade
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
        logging.FileHandler('verificacao_fontes.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VerificadorFontesMCP:
    """Classe para verificação de fontes usando MCPs disponíveis"""
    
    def __init__(self):
        self.fontes_confiaveis = {
            'governamentais': [
                'gov.br', 'mec.gov.br', 'inep.gov.br', 'fnde.gov.br',
                'ibge.gov.br', 'datasus.gov.br', 'ans.gov.br'
            ],
            'academicas': [
                'scielo.br', 'scholar.google.com', 'researchgate.net',
                'academia.edu', 'jstor.org', 'springer.com'
            ],
            'internacionais': [
                'who.int', 'un.org', 'unesco.org', 'oecd.org',
                'worldbank.org', 'imf.org'
            ],
            'jornalisticas': [
                'g1.globo.com', 'folha.uol.com.br', 'estadao.com.br',
                'bbc.com', 'reuters.com', 'ap.org'
            ],
            'tecnicas': [
                'wikipedia.org', 'britannica.com', 'merriam-webster.com',
                'oxforddictionaries.com'
            ]
        }
        
        self.padroes_url = [
            r'https?://[^\s\)]+',
            r'\[.*?\]\(https?://[^\s\)]+\)'
        ]

    def extrair_urls(self, conteudo: str) -> List[str]:
        """Extrai todas as URLs do conteúdo"""
        urls = []
        
        for padrao in self.padroes_url:
            matches = re.findall(padrao, conteudo, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    urls.append(match[0])
                else:
                    urls.append(match)
        
        return list(set(urls))  # Remove duplicatas

    def categorizar_fonte(self, url: str) -> Dict:
        """Categoriza uma fonte baseada na URL"""
        url_lower = url.lower()
        
        resultado = {
            'url': url,
            'categoria': 'desconhecida',
            'confiabilidade': 'baixa',
            'tipo': 'não identificado',
            'dominio': self.extrair_dominio(url)
        }
        
        # Verificar categorias
        for categoria, dominios in self.fontes_confiaveis.items():
            for dominio in dominios:
                if dominio in url_lower:
                    resultado['categoria'] = categoria
                    resultado['confiabilidade'] = 'alta'
                    break
            if resultado['categoria'] != 'desconhecida':
                break
        
        # Determinar tipo baseado na categoria
        if resultado['categoria'] == 'governamentais':
            resultado['tipo'] = 'oficial'
        elif resultado['categoria'] == 'academicas':
            resultado['tipo'] = 'científica'
        elif resultado['categoria'] == 'internacionais':
            resultado['tipo'] = 'internacional'
        elif resultado['categoria'] == 'jornalisticas':
            resultado['tipo'] = 'jornalística'
        elif resultado['categoria'] == 'tecnicas':
            resultado['tipo'] = 'técnica'
        
        return resultado

    def extrair_dominio(self, url: str) -> str:
        """Extrai o domínio de uma URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return url

    def verificar_acessibilidade(self, url: str) -> Dict:
        """Verifica se uma URL está acessível"""
        resultado = {
            'url': url,
            'acessivel': False,
            'codigo_status': None,
            'tempo_resposta': None,
            'erro': None
        }
        
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            resultado['acessivel'] = True
            resultado['codigo_status'] = response.status_code
            resultado['tempo_resposta'] = response.elapsed.total_seconds()
        except requests.exceptions.Timeout:
            resultado['erro'] = 'Timeout'
        except requests.exceptions.ConnectionError:
            resultado['erro'] = 'Erro de conexão'
        except requests.exceptions.RequestException as e:
            resultado['erro'] = str(e)
        except Exception as e:
            resultado['erro'] = f'Erro inesperado: {str(e)}'
        
        return resultado

    def verificar_credibilidade(self, url: str) -> Dict:
        """Verifica a credibilidade de uma fonte"""
        resultado = {
            'url': url,
            'credibilidade': 'baixa',
            'indicadores': [],
            'pontuacao': 0
        }
        
        url_lower = url.lower()
        
        # Indicadores de credibilidade
        indicadores = {
            'https': 1 if url.startswith('https://') else 0,
            'dominio_gov': 3 if '.gov' in url_lower else 0,
            'dominio_edu': 2 if '.edu' in url_lower else 0,
            'dominio_org': 2 if '.org' in url_lower else 0,
            'dominio_com': 1 if '.com' in url_lower else 0,
            'sem_www': 1 if not url_lower.startswith('www.') else 0,
            'caminho_curto': 1 if len(url.split('/')) <= 4 else 0
        }
        
        resultado['indicadores'] = indicadores
        resultado['pontuacao'] = sum(indicadores.values())
        
        # Determinar credibilidade baseada na pontuação
        if resultado['pontuacao'] >= 5:
            resultado['credibilidade'] = 'alta'
        elif resultado['pontuacao'] >= 3:
            resultado['credibilidade'] = 'media'
        else:
            resultado['credibilidade'] = 'baixa'
        
        return resultado

    def verificar_atualidade(self, url: str) -> Dict:
        """Verifica a atualidade de uma fonte"""
        resultado = {
            'url': url,
            'atualizada': False,
            'data_ultima_modificacao': None,
            'idade_dias': None
        }
        
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            
            if 'last-modified' in response.headers:
                from datetime import datetime
                data_modificacao = datetime.strptime(
                    response.headers['last-modified'],
                    '%a, %d %b %Y %H:%M:%S %Z'
                )
                resultado['data_ultima_modificacao'] = data_modificacao.isoformat()
                
                # Calcular idade em dias
                idade = (datetime.now() - data_modificacao).days
                resultado['idade_dias'] = idade
                
                # Considerar atualizada se modificada nos últimos 2 anos
                resultado['atualizada'] = idade <= 730
                
        except Exception as e:
            logger.warning(f"Erro ao verificar atualidade de {url}: {e}")
        
        return resultado

    def analisar_fonte_completa(self, url: str) -> Dict:
        """Análise completa de uma fonte"""
        logger.info(f"Analisando fonte: {url}")
        
        # Categorizar
        categoria = self.categorizar_fonte(url)
        
        # Verificar acessibilidade
        acessibilidade = self.verificar_acessibilidade(url)
        
        # Verificar credibilidade
        credibilidade = self.verificar_credibilidade(url)
        
        # Verificar atualidade
        atualidade = self.verificar_atualidade(url)
        
        # Compilar resultado
        resultado = {
            'url': url,
            'categoria': categoria,
            'acessibilidade': acessibilidade,
            'credibilidade': credibilidade,
            'atualidade': atualidade,
            'data_analise': datetime.now().isoformat()
        }
        
        return resultado

    def analisar_conteudo(self, conteudo: str) -> Dict:
        """Analisa todas as fontes de um conteúdo"""
        logger.info("Iniciando análise de fontes do conteúdo...")
        
        # Extrair URLs
        urls = self.extrair_urls(conteudo)
        logger.info(f"Encontradas {len(urls)} URLs para análise")
        
        # Analisar cada fonte
        fontes_analisadas = []
        for url in urls:
            try:
                analise = self.analisar_fonte_completa(url)
                fontes_analisadas.append(analise)
            except Exception as e:
                logger.error(f"Erro ao analisar {url}: {e}")
                continue
        
        # Calcular estatísticas
        total_fontes = len(fontes_analisadas)
        fontes_acessiveis = sum(1 for f in fontes_analisadas if f['acessibilidade']['acessivel'])
        fontes_confiaveis = sum(1 for f in fontes_analisadas if f['credibilidade']['credibilidade'] == 'alta')
        fontes_atualizadas = sum(1 for f in fontes_analisadas if f['atualidade']['atualizada'])
        
        # Categorizar por tipo
        categorias = {}
        for fonte in fontes_analisadas:
            cat = fonte['categoria']['categoria']
            if cat not in categorias:
                categorias[cat] = 0
            categorias[cat] += 1
        
        # Calcular pontuação geral
        pontuacao = 0
        if total_fontes > 0:
            pontuacao += (fontes_acessiveis / total_fontes) * 30
            pontuacao += (fontes_confiaveis / total_fontes) * 40
            pontuacao += (fontes_atualizadas / total_fontes) * 30
        
        resultado = {
            'resumo': {
                'total_fontes': total_fontes,
                'fontes_acessiveis': fontes_acessiveis,
                'fontes_confiaveis': fontes_confiaveis,
                'fontes_atualizadas': fontes_atualizadas,
                'pontuacao_geral': pontuacao,
                'data_analise': datetime.now().isoformat()
            },
            'categorias': categorias,
            'fontes_detalhadas': fontes_analisadas
        }
        
        return resultado

    def gerar_relatorio_fontes(self, analise: Dict, arquivo_saida: str = None) -> str:
        """Gera relatório de análise de fontes"""
        if not arquivo_saida:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_saida = f"relatorio_fontes_{timestamp}.json"
        
        try:
            with open(arquivo_saida, 'w', encoding='utf-8') as f:
                json.dump(analise, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Relatório de fontes salvo em: {arquivo_saida}")
            return arquivo_saida
        except Exception as e:
            logger.error(f"Erro ao salvar relatório: {e}")
            return None

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Verificação de Fontes Confiáveis')
    parser.add_argument('--arquivo', '-f', help='Arquivo de conteúdo para analisar')
    parser.add_argument('--diretorio', '-d', help='Diretório para analisar')
    parser.add_argument('--saida', '-s', help='Arquivo de saída para o relatório')
    
    args = parser.parse_args()
    
    verificador = VerificadorFontesMCP()
    
    if args.arquivo:
        # Analisar arquivo específico
        try:
            with open(args.arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            analise = verificador.analisar_conteudo(conteudo)
            arquivo_relatorio = verificador.gerar_relatorio_fontes(analise, args.saida)
            
            print(f"\n✅ Análise de fontes concluída!")
            print(f"📊 Total de fontes: {analise['resumo']['total_fontes']}")
            print(f"🔗 Fontes acessíveis: {analise['resumo']['fontes_acessiveis']}")
            print(f"⭐ Fontes confiáveis: {analise['resumo']['fontes_confiaveis']}")
            print(f"📅 Fontes atualizadas: {analise['resumo']['fontes_atualizadas']}")
            print(f"📈 Pontuação geral: {analise['resumo']['pontuacao_geral']:.1f}%")
            
        except Exception as e:
            logger.error(f"Erro ao analisar arquivo: {e}")
    
    elif args.diretorio:
        # Analisar diretório
        diretorio = Path(args.diretorio)
        arquivos_md = list(diretorio.rglob("*.md"))
        
        print(f"Encontrados {len(arquivos_md)} arquivos para análise...")
        
        for arquivo in arquivos_md:
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                
                analise = verificador.analisar_conteudo(conteudo)
                print(f"\n📄 {arquivo.name}:")
                print(f"  Fontes: {analise['resumo']['total_fontes']}")
                print(f"  Pontuação: {analise['resumo']['pontuacao_geral']:.1f}%")
                
            except Exception as e:
                logger.error(f"Erro ao analisar {arquivo}: {e}")
    
    else:
        print("Use --arquivo ou --diretorio para especificar o que analisar")
        print("Use --help para mais opções")

if __name__ == "__main__":
    main()
