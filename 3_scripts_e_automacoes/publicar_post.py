#!/usr/bin/env python3
"""
Script de Publicação Automática - Modelo Projeto Conteúdo
Automatiza a publicação de conteúdo do pipeline para o Notion
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/publicacao.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PublicadorConteudo:
    """Classe principal para publicação de conteúdo"""
    
    def __init__(self, config_path: str = "config.json"):
        """Inicializa o publicador com configurações"""
        self.config = self._carregar_config(config_path)
        self.setup_diretorios()
    
    def _carregar_config(self, config_path: str) -> Dict:
        """Carrega configurações do arquivo JSON"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Arquivo de configuração {config_path} não encontrado. Usando configurações padrão.")
            return self._config_padrao()
    
    def _config_padrao(self) -> Dict:
        """Retorna configurações padrão"""
        return {
            "notion": {
                "token": os.getenv("NOTION_TOKEN", ""),
                "biblioteca_url": os.getenv("NOTION_BIBLIOTECA_URL", ""),
                "categoria_url": os.getenv("NOTION_CATEGORIA_URL", "")
            },
            "diretorios": {
                "pronto_para_publicar": "2_conteudo/03_pronto_para_publicar",
                "publicado": "2_conteudo/04_publicado",
                "logs": "logs"
            },
            "configuracoes": {
                "backup_enabled": True,
                "notification_enabled": False,
                "auto_publish": False
            }
        }
    
    def setup_diretorios(self):
        """Cria diretórios necessários"""
        dirs = [
            self.config["diretorios"]["logs"],
            "backups"
        ]
        
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            logger.info(f"Diretório criado/verificado: {dir_path}")
    
    def listar_conteudo_pronto(self) -> List[Path]:
        """Lista arquivos prontos para publicação"""
        diretorio = Path(self.config["diretorios"]["pronto_para_publicar"])
        
        if not diretorio.exists():
            logger.error(f"Diretório não encontrado: {diretorio}")
            return []
        
        arquivos = list(diretorio.glob("*.md"))
        logger.info(f"Encontrados {len(arquivos)} arquivos prontos para publicação")
        
        return arquivos
    
    def validar_conteudo(self, arquivo: Path) -> bool:
        """Valida se o conteúdo está pronto para publicação"""
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            # Verificações básicas
            verificacoes = [
                ("Título", "# " in conteudo),
                ("Resumo Executivo", "## Resumo Executivo" in conteudo),
                ("Contexto", "## Contexto" in conteudo),
                ("Aplicação Prática", "## Aplicação Prática" in conteudo),
                ("Taxonomia", "## Taxonomia e Indexação" in conteudo)
            ]
            
            for nome, condicao in verificacoes:
                if not condicao:
                    logger.warning(f"Arquivo {arquivo.name}: Falta seção '{nome}'")
                    return False
            
            logger.info(f"Arquivo {arquivo.name}: Validação bem-sucedida")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao validar {arquivo.name}: {e}")
            return False
    
    def extrair_metadados(self, arquivo: Path) -> Dict:
        """Extrai metadados do arquivo Markdown"""
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            metadados = {
                "titulo": "",
                "tipo": "Artigo",
                "funcao": "Diretor",
                "nivel": "Tático",
                "area_problema": "Operacional",
                "tags": ["Gestão Educacional"],
                "status": "Publicado"
            }
            
            # Extrair título
            linhas = conteudo.split('\n')
            for linha in linhas:
                if linha.startswith('# '):
                    metadados["titulo"] = linha[2:].strip()
                    break
            
            # Extrair taxonomia
            for linha in linhas:
                if linha.startswith('- **Eixo:**'):
                    metadados["eixo"] = linha.split(':', 1)[1].strip()
                elif linha.startswith('- **Função:**'):
                    metadados["funcao"] = linha.split(':', 1)[1].strip()
                elif linha.startswith('- **Nível de profundidade:**'):
                    metadados["nivel"] = linha.split(':', 1)[1].strip()
                elif linha.startswith('- **Tipo de problema:**'):
                    metadados["area_problema"] = linha.split(':', 1)[1].strip()
                elif linha.startswith('- **Tags:**'):
                    tags_str = linha.split(':', 1)[1].strip()
                    metadados["tags"] = [tag.strip() for tag in tags_str.split(',')]
            
            return metadados
            
        except Exception as e:
            logger.error(f"Erro ao extrair metadados de {arquivo.name}: {e}")
            return {}
    
    def criar_backup(self, arquivo: Path) -> Optional[Path]:
        """Cria backup do arquivo antes da publicação"""
        if not self.config["configuracoes"]["backup_enabled"]:
            return None
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = Path("backups") / timestamp
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            backup_file = backup_dir / arquivo.name
            backup_file.write_text(arquivo.read_text(encoding='utf-8'), encoding='utf-8')
            
            logger.info(f"Backup criado: {backup_file}")
            return backup_file
            
        except Exception as e:
            logger.error(f"Erro ao criar backup de {arquivo.name}: {e}")
            return None
    
    def publicar_no_notion(self, arquivo: Path, metadados: Dict) -> bool:
        """Publica o conteúdo no Notion (implementação simulada)"""
        try:
            # Aqui seria implementada a integração real com a API do Notion
            logger.info(f"Simulando publicação no Notion: {arquivo.name}")
            logger.info(f"Metadados: {metadados}")
            
            # Simular sucesso
            return True
            
        except Exception as e:
            logger.error(f"Erro ao publicar {arquivo.name} no Notion: {e}")
            return False
    
    def mover_para_publicado(self, arquivo: Path) -> bool:
        """Move arquivo para diretório de publicado"""
        try:
            diretorio_publicado = Path(self.config["diretorios"]["publicado"])
            arquivo_destino = diretorio_publicado / arquivo.name
            
            # Mover arquivo
            arquivo.rename(arquivo_destino)
            
            logger.info(f"Arquivo movido para publicado: {arquivo_destino}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao mover {arquivo.name} para publicado: {e}")
            return False
    
    def publicar_conteudo(self, arquivo: Path) -> bool:
        """Processo completo de publicação de um arquivo"""
        logger.info(f"Iniciando publicação: {arquivo.name}")
        
        # 1. Validar conteúdo
        if not self.validar_conteudo(arquivo):
            logger.error(f"Conteúdo inválido: {arquivo.name}")
            return False
        
        # 2. Extrair metadados
        metadados = self.extrair_metadados(arquivo)
        if not metadados:
            logger.error(f"Erro ao extrair metadados: {arquivo.name}")
            return False
        
        # 3. Criar backup
        self.criar_backup(arquivo)
        
        # 4. Publicar no Notion
        if not self.publicar_no_notion(arquivo, metadados):
            logger.error(f"Erro na publicação no Notion: {arquivo.name}")
            return False
        
        # 5. Mover para publicado
        if not self.mover_para_publicado(arquivo):
            logger.error(f"Erro ao mover para publicado: {arquivo.name}")
            return False
        
        logger.info(f"Publicação concluída com sucesso: {arquivo.name}")
        return True
    
    def executar_publicacao(self):
        """Executa o processo de publicação para todos os arquivos prontos"""
        logger.info("Iniciando processo de publicação")
        
        arquivos = self.listar_conteudo_pronto()
        if not arquivos:
            logger.info("Nenhum arquivo encontrado para publicação")
            return
        
        sucessos = 0
        falhas = 0
        
        for arquivo in arquivos:
            if self.publicar_conteudo(arquivo):
                sucessos += 1
            else:
                falhas += 1
        
        logger.info(f"Processo concluído: {sucessos} sucessos, {falhas} falhas")

def main():
    """Função principal"""
    try:
        publicador = PublicadorConteudo()
        publicador.executar_publicacao()
    except KeyboardInterrupt:
        logger.info("Processo interrompido pelo usuário")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
