#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Curadoria Completa de Conteúdo
Integra verificação de capas, dados, vídeos, fontes e busca de fontes confiáveis
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Adicionar o diretório atual ao path para importar módulos locais
sys.path.append(str(Path(__file__).parent))

from curadoria_automatica import CuradorAutomatico
from verificar_fontes_mcp import VerificadorFontesMCP
from buscar_fontes_confiaveis import BuscadorFontesConfiaveis

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('curadoria_completa.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CuradoriaCompleta:
    """Classe principal para curadoria completa de conteúdo"""
    
    def __init__(self, projeto_root: str = None):
        self.projeto_root = Path(projeto_root) if projeto_root else Path.cwd()
        self.conteudo_dir = self.projeto_root / "2_conteudo"
        self.relatorios_dir = self.projeto_root / "docs" / "relatorios"
        self.relatorios_dir.mkdir(parents=True, exist_ok=True)
        
        # Inicializar componentes
        self.curador = CuradorAutomatico(projeto_root)
        self.verificador_fontes = VerificadorFontesMCP()
        self.buscador_fontes = BuscadorFontesConfiaveis()
        
        # Configurações
        self.pontuacao_minima = 70
        self.min_graficos = 2
        self.min_videos = 2
        self.min_fontes = 4

    def extrair_tema_do_conteudo(self, conteudo: str) -> str:
        """Extrai o tema principal do conteúdo"""
        # Buscar título principal
        import re
        titulo_match = re.search(r'^#\s+(.+?)(?:\n|$)', conteudo, re.MULTILINE)
        if titulo_match:
            return titulo_match.group(1).strip()
        
        # Buscar palavras-chave comuns
        palavras_chave = [
            'gestão escolar', 'educação', 'pedagogia', 'ensino',
            'aprendizagem', 'currículo', 'avaliação', 'formação'
        ]
        
        conteudo_lower = conteudo.lower()
        for palavra in palavras_chave:
            if palavra in conteudo_lower:
                return palavra.title()
        
        return "Tema não identificado"

    def verificar_capa_detalhada(self, arquivo_path: Path) -> Dict:
        """Verificação detalhada da capa do conteúdo"""
        logger.info(f"Verificando capa detalhada: {arquivo_path}")
        
        try:
            with open(arquivo_path, 'r', encoding='utf-8') as f:
                conteudo = f.read()
        except Exception as e:
            logger.error(f"Erro ao ler arquivo: {e}")
            return None
        
        # Verificação básica
        verificacao_basica = self.curador.verificar_capa(conteudo)
        
        # Verificação adicional de arquivos
        verificacao_arquivos = self.verificar_arquivos_capa(arquivo_path)
        
        # Combinar resultados
        resultado = {
            'verificacao_basica': verificacao_basica,
            'verificacao_arquivos': verificacao_arquivos,
            'recomendacoes': []
        }
        
        # Gerar recomendações
        if not verificacao_basica['presente']:
            resultado['recomendacoes'].append("Adicionar imagem de capa relevante")
        if not verificacao_basica['descricao_presente']:
            resultado['recomendacoes'].append("Incluir descrição da imagem de capa")
        if not verificacao_arquivos['arquivo_existe']:
            resultado['recomendacoes'].append("Criar arquivo de imagem de capa")
        
        return resultado

    def verificar_arquivos_capa(self, arquivo_path: Path) -> Dict:
        """Verifica se os arquivos de capa existem no sistema de arquivos"""
        resultado = {
            'arquivo_existe': False,
            'caminho_imagem': None,
            'tamanho_arquivo': None,
            'formato_valido': False
        }
        
        # Buscar referências a imagens no conteúdo
        import re
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        img_pattern = r'!\[.*?\]\(([^)]+)\)'
        matches = re.findall(img_pattern, conteudo)
        
        for match in matches:
            if match.startswith(('http', 'https')):
                continue  # URLs externas
            
            # Construir caminho relativo ao arquivo
            caminho_imagem = arquivo_path.parent / match
            
            if caminho_imagem.exists():
                resultado['arquivo_existe'] = True
                resultado['caminho_imagem'] = str(caminho_imagem)
                resultado['tamanho_arquivo'] = caminho_imagem.stat().st_size
                resultado['formato_valido'] = caminho_imagem.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']
                break
        
        return resultado

    def buscar_fontes_para_conteudo(self, conteudo: str, tema: str) -> Dict:
        """Busca fontes confiáveis para um conteúdo específico"""
        logger.info(f"Buscando fontes para tema: {tema}")
        
        # Buscar fontes existentes
        analise_fontes = self.verificador_fontes.analisar_conteudo(conteudo)
        
        # Buscar novas fontes se necessário
        if analise_fontes['resumo']['total_fontes'] < self.min_fontes:
            logger.info("Fontes insuficientes, buscando novas fontes...")
            novas_fontes = self.buscador_fontes.buscar_fontes_completas(tema)
        else:
            novas_fontes = None
        
        return {
            'analise_existente': analise_fontes,
            'novas_fontes': novas_fontes,
            'recomendacoes': self.gerar_recomendacoes_fontes(analise_fontes, novas_fontes)
        }

    def gerar_recomendacoes_fontes(self, analise_existente: Dict, novas_fontes: Dict = None) -> List[str]:
        """Gera recomendações baseadas na análise de fontes"""
        recomendacoes = []
        
        # Recomendações baseadas nas fontes existentes
        if analise_existente['resumo']['total_fontes'] < self.min_fontes:
            recomendacoes.append(f"Adicionar pelo menos {self.min_fontes} fontes confiáveis")
        
        if analise_existente['resumo']['fontes_confiaveis'] < 2:
            recomendacoes.append("Utilizar mais fontes governamentais ou acadêmicas")
        
        if analise_existente['resumo']['fontes_atualizadas'] < 2:
            recomendacoes.append("Incluir fontes mais recentes (últimos 2 anos)")
        
        # Recomendações baseadas nas novas fontes encontradas
        if novas_fontes and novas_fontes['melhores_fontes']:
            recomendacoes.append("Considerar as seguintes fontes adicionais:")
            for fonte in novas_fontes['melhores_fontes'][:3]:
                recomendacoes.append(f"  - {fonte.get('titulo', '')} ({fonte.get('url', '')})")
        
        return recomendacoes

    def processar_conteudo_completo(self, arquivo_path: Path) -> Dict:
        """Processa um conteúdo com curadoria completa"""
        logger.info(f"Processando conteúdo completo: {arquivo_path}")
        
        try:
            with open(arquivo_path, 'r', encoding='utf-8') as f:
                conteudo = f.read()
        except Exception as e:
            logger.error(f"Erro ao ler arquivo: {e}")
            return None
        
        # Extrair tema
        tema = self.extrair_tema_do_conteudo(conteudo)
        
        # Curadoria básica
        curadoria_basica = self.curador.processar_arquivo(arquivo_path)
        
        # Verificação detalhada da capa
        verificacao_capa = self.verificar_capa_detalhada(arquivo_path)
        
        # Análise de fontes
        analise_fontes = self.buscar_fontes_para_conteudo(conteudo, tema)
        
        # Compilar resultado completo
        resultado_completo = {
            'arquivo': str(arquivo_path),
            'tema': tema,
            'data_analise': datetime.now().isoformat(),
            'curadoria_basica': curadoria_basica,
            'verificacao_capa': verificacao_capa,
            'analise_fontes': analise_fontes,
            'recomendacoes_gerais': self.gerar_recomendacoes_gerais(
                curadoria_basica, verificacao_capa, analise_fontes
            )
        }
        
        return resultado_completo

    def gerar_recomendacoes_gerais(self, curadoria_basica: Dict, verificacao_capa: Dict, analise_fontes: Dict) -> List[str]:
        """Gera recomendações gerais baseadas em todas as análises"""
        recomendacoes = []
        
        # Recomendações da curadoria básica
        if curadoria_basica and curadoria_basica['recomendacoes']:
            recomendacoes.extend(curadoria_basica['recomendacoes'])
        
        # Recomendações da verificação de capa
        if verificacao_capa and verificacao_capa['recomendacoes']:
            recomendacoes.extend(verificacao_capa['recomendacoes'])
        
        # Recomendações da análise de fontes
        if analise_fontes and analise_fontes['recomendacoes']:
            recomendacoes.extend(analise_fontes['recomendacoes'])
        
        # Remover duplicatas
        return list(set(recomendacoes))

    def executar_curadoria_completa(self, diretorio: str = None) -> Dict:
        """Executa curadoria completa em um diretório"""
        logger.info("Iniciando curadoria completa...")
        
        if diretorio:
            diretorio_path = Path(diretorio)
        else:
            diretorio_path = self.conteudo_dir
        
        # Encontrar arquivos
        arquivos_md = list(diretorio_path.rglob("*.md"))
        logger.info(f"Encontrados {len(arquivos_md)} arquivos para análise")
        
        # Processar cada arquivo
        resultados_completos = []
        for arquivo in arquivos_md:
            if arquivo.name.startswith('.'):
                continue
            
            logger.info(f"Processando: {arquivo.name}")
            resultado = self.processar_conteudo_completo(arquivo)
            if resultado:
                resultados_completos.append(resultado)
        
        # Gerar relatório consolidado
        relatorio_consolidado = self.gerar_relatorio_consolidado(resultados_completos)
        
        # Salvar relatório
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo_relatorio = self.relatorios_dir / f"curadoria_completa_{timestamp}.json"
        
        with open(arquivo_relatorio, 'w', encoding='utf-8') as f:
            json.dump(relatorio_consolidado, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Relatório consolidado salvo em: {arquivo_relatorio}")
        
        return relatorio_consolidado

    def gerar_relatorio_consolidado(self, resultados: List[Dict]) -> Dict:
        """Gera relatório consolidado de todos os resultados"""
        logger.info("Gerando relatório consolidado...")
        
        total_arquivos = len(resultados)
        
        # Estatísticas gerais
        aprovados = sum(1 for r in resultados if r['curadoria_basica']['status'] == "Aprovado")
        revisao_necessaria = sum(1 for r in resultados if r['curadoria_basica']['status'] == "Revisão Necessária")
        rejeitados = sum(1 for r in resultados if r['curadoria_basica']['status'] == "Rejeitado")
        
        # Estatísticas de capa
        com_capa = sum(1 for r in resultados if r['verificacao_capa']['verificacao_basica']['presente'])
        sem_capa = total_arquivos - com_capa
        
        # Estatísticas de fontes
        fontes_suficientes = sum(1 for r in resultados if r['analise_fontes']['analise_existente']['resumo']['total_fontes'] >= self.min_fontes)
        fontes_insuficientes = total_arquivos - fontes_suficientes
        
        # Pontuação média
        pontuacao_media = sum(r['curadoria_basica']['pontuacao']['percentual'] for r in resultados) / total_arquivos if total_arquivos > 0 else 0
        
        relatorio = {
            'resumo_geral': {
                'total_arquivos': total_arquivos,
                'aprovados': aprovados,
                'revisao_necessaria': revisao_necessaria,
                'rejeitados': rejeitados,
                'pontuacao_media': pontuacao_media,
                'data_analise': datetime.now().isoformat()
            },
            'estatisticas_capa': {
                'com_capa': com_capa,
                'sem_capa': sem_capa,
                'percentual_com_capa': (com_capa / total_arquivos) * 100 if total_arquivos > 0 else 0
            },
            'estatisticas_fontes': {
                'fontes_suficientes': fontes_suficientes,
                'fontes_insuficientes': fontes_insuficientes,
                'percentual_fontes_suficientes': (fontes_suficientes / total_arquivos) * 100 if total_arquivos > 0 else 0
            },
            'resultados_detalhados': resultados,
            'recomendacoes_gerais': self.gerar_recomendacoes_consolidadas(resultados)
        }
        
        return relatorio

    def gerar_recomendacoes_consolidadas(self, resultados: List[Dict]) -> List[str]:
        """Gera recomendações consolidadas baseadas em todos os resultados"""
        recomendacoes = []
        
        # Contar problemas comuns
        problemas_capa = sum(1 for r in resultados if not r['verificacao_capa']['verificacao_basica']['presente'])
        problemas_fontes = sum(1 for r in resultados if r['analise_fontes']['analise_existente']['resumo']['total_fontes'] < self.min_fontes)
        problemas_qualidade = sum(1 for r in resultados if r['curadoria_basica']['pontuacao']['percentual'] < self.pontuacao_minima)
        
        total_arquivos = len(resultados)
        
        if problemas_capa > total_arquivos * 0.5:
            recomendacoes.append("Mais de 50% dos conteúdos não possuem capa - implementar verificação obrigatória")
        
        if problemas_fontes > total_arquivos * 0.3:
            recomendacoes.append("Mais de 30% dos conteúdos têm fontes insuficientes - revisar critérios de qualidade")
        
        if problemas_qualidade > total_arquivos * 0.2:
            recomendacoes.append("Mais de 20% dos conteúdos estão abaixo da pontuação mínima - revisar templates")
        
        # Recomendações específicas
        recomendacoes.extend([
            "Implementar verificação automática de capas em todos os conteúdos",
            "Criar banco de fontes confiáveis para consulta rápida",
            "Desenvolver sistema de busca automática de fontes relevantes",
            "Implementar verificação de links e URLs em tempo real",
            "Criar templates com seções obrigatórias de capa, dados e fontes"
        ])
        
        return recomendacoes

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Curadoria Completa de Conteúdo')
    parser.add_argument('--diretorio', '-d', help='Diretório para analisar')
    parser.add_argument('--projeto', '-p', help='Diretório raiz do projeto')
    parser.add_argument('--min-pontuacao', '-m', type=int, default=70, help='Pontuação mínima para aprovação')
    
    args = parser.parse_args()
    
    # Configurar curadoria completa
    curadoria = CuradoriaCompleta(projeto_root=args.projeto)
    curadoria.pontuacao_minima = args.min_pontuacao
    
    # Executar curadoria
    relatorio = curadoria.executar_curadoria_completa(diretorio=args.diretorio)
    
    # Exibir resumo
    resumo = relatorio['resumo_geral']
    stats_capa = relatorio['estatisticas_capa']
    stats_fontes = relatorio['estatisticas_fontes']
    
    print(f"\n✅ Curadoria completa concluída!")
    print(f"📊 Total de arquivos: {resumo['total_arquivos']}")
    print(f"✅ Aprovados: {resumo['aprovados']}")
    print(f"⚠️ Revisão necessária: {resumo['revisao_necessaria']}")
    print(f"❌ Rejeitados: {resumo['rejeitados']}")
    print(f"📈 Pontuação média: {resumo['pontuacao_media']:.1f}%")
    print(f"🖼️ Conteúdos com capa: {stats_capa['com_capa']} ({stats_capa['percentual_com_capa']:.1f}%)")
    print(f"📚 Conteúdos com fontes suficientes: {stats_fontes['fontes_suficientes']} ({stats_fontes['percentual_fontes_suficientes']:.1f}%)")
    print(f"📁 Relatório salvo em: docs/relatorios/")

if __name__ == "__main__":
    main()
