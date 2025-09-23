#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar se a configuração está correta
Verifica se todas as variáveis de ambiente estão definidas e se não há tokens hardcoded
"""

import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv

def verificar_tokens_hardcoded():
    """
    Verifica se há tokens ou IDs hardcoded nos arquivos
    """
    print("🔍 VERIFICANDO TOKENS HARDCODED...")
    print("=" * 50)
    
    # Padrões para detectar tokens e IDs
    padroes = [
        r'ntn_[a-zA-Z0-9]{32,}',  # Token do Notion
        r'2325113a91a381[a-f0-9]{8,}',  # IDs específicos do projeto
        r'https://www\.notion\.so/[a-f0-9]{32,}',  # URLs com IDs específicos
    ]
    
    arquivos_verificados = 0
    problemas_encontrados = 0
    
    # Arquivos para verificar (excluindo .env e arquivos de template)
    arquivos_para_verificar = [
        'scripts/',
        'docs/',
        'config/',
        'templates/',
        '4_arquivos_suporte/'
    ]
    
    for diretorio in arquivos_para_verificar:
        if not Path(diretorio).exists():
            continue
            
        for arquivo in Path(diretorio).rglob('*'):
            if arquivo.is_file() and arquivo.suffix in ['.py', '.md', '.json', '.txt']:
                # Pular arquivos de template e .env
                if 'template' in arquivo.name.lower() or arquivo.name == '.env':
                    continue
                    
                try:
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        conteudo = f.read()
                    
                    arquivos_verificados += 1
                    
                    for padrao in padroes:
                        matches = re.findall(padrao, conteudo)
                        if matches:
                            print(f"⚠️  {arquivo}: {len(matches)} token(s)/ID(s) encontrado(s)")
                            for match in matches:
                                print(f"   - {match}")
                            problemas_encontrados += 1
                            
                except Exception as e:
                    print(f"❌ Erro ao verificar {arquivo}: {e}")
    
    print(f"\n📊 RESULTADO:")
    print(f"✅ Arquivos verificados: {arquivos_verificados}")
    print(f"⚠️  Problemas encontrados: {problemas_encontrados}")
    
    if problemas_encontrados == 0:
        print("🎉 Nenhum token/ID hardcoded encontrado!")
        return True
    else:
        print("❌ Tokens/IDs hardcoded encontrados. Corrija antes de continuar.")
        return False

def verificar_variaveis_ambiente():
    """
    Verifica se as variáveis de ambiente estão definidas
    """
    print("\n🔍 VERIFICANDO VARIÁVEIS DE AMBIENTE...")
    print("=" * 50)
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Variáveis essenciais
    variaveis_essenciais = [
        'NOTION_TOKEN',
        'DATABASE_ID',
        'CATEGORIA_DATABASE_ID'
    ]
    
    # Variáveis opcionais mas importantes
    variaveis_opcionais = [
        'CATEGORIA_FINANCEIRO_URL',
        'CATEGORIA_FORMACAO_URL',
        'CATEGORIA_GOVERNANCA_URL',
        'CATEGORIA_TECNOLOGIA_URL',
        'CATEGORIA_INFRAESTRUTURA_URL',
        'CATEGORIA_GESTAO_PESSOAS_URL',
        'CATEGORIA_ADMINISTRACAO_URL',
        'CATEGORIA_PEDAGOGICO_URL',
        'CATEGORIA_LEGISLACAO_URL'
    ]
    
    variaveis_ok = []
    variaveis_faltando = []
    variaveis_placeholder = []
    
    # Verificar variáveis essenciais
    for var in variaveis_essenciais:
        valor = os.getenv(var)
        if not valor:
            variaveis_faltando.append(var)
        elif 'seu_' in valor.lower() or 'aqui' in valor.lower():
            variaveis_placeholder.append(var)
        else:
            variaveis_ok.append(var)
    
    # Verificar variáveis opcionais
    for var in variaveis_opcionais:
        valor = os.getenv(var)
        if valor and 'seu_' in valor.lower() or 'aqui' in valor.lower():
            variaveis_placeholder.append(var)
        elif valor:
            variaveis_ok.append(var)
    
    print(f"✅ Variáveis configuradas: {len(variaveis_ok)}")
    for var in variaveis_ok:
        print(f"   - {var}")
    
    if variaveis_faltando:
        print(f"❌ Variáveis faltando: {len(variaveis_faltando)}")
        for var in variaveis_faltando:
            print(f"   - {var}")
    
    if variaveis_placeholder:
        print(f"⚠️  Variáveis com placeholder: {len(variaveis_placeholder)}")
        for var in variaveis_placeholder:
            print(f"   - {var}")
    
    return len(variaveis_faltando) == 0

def verificar_arquivo_env():
    """
    Verifica se o arquivo .env existe e está configurado
    """
    print("\n🔍 VERIFICANDO ARQUIVO .ENV...")
    print("=" * 50)
    
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ Arquivo .env não encontrado!")
        print("💡 Execute: python scripts/configurar_ambiente.py")
        return False
    
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Verificar se há configurações
        linhas_configuradas = 0
        linhas_placeholder = 0
        
        for linha in conteudo.split('\n'):
            if '=' in linha and not linha.strip().startswith('#'):
                if 'seu_' in linha.lower() or 'aqui' in linha.lower():
                    linhas_placeholder += 1
                else:
                    linhas_configuradas += 1
        
        print(f"✅ Linhas configuradas: {linhas_configuradas}")
        print(f"⚠️  Linhas com placeholder: {linhas_placeholder}")
        
        if linhas_configuradas > 0:
            print("✅ Arquivo .env configurado!")
            return True
        else:
            print("⚠️  Arquivo .env existe mas não está configurado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao ler arquivo .env: {e}")
        return False

def verificar_gitignore():
    """
    Verifica se o .gitignore está configurado para ignorar .env
    """
    print("\n🔍 VERIFICANDO .GITIGNORE...")
    print("=" * 50)
    
    gitignore_file = Path('.gitignore')
    
    if not gitignore_file.exists():
        print("❌ Arquivo .gitignore não encontrado!")
        return False
    
    try:
        with open(gitignore_file, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        if '.env' in conteudo:
            print("✅ Arquivo .env está no .gitignore")
            return True
        else:
            print("❌ Arquivo .env NÃO está no .gitignore!")
            print("💡 Adicione '.env' ao arquivo .gitignore")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao ler .gitignore: {e}")
        return False

def main():
    """
    Função principal
    """
    print("🔧 VERIFICAÇÃO DE CONFIGURAÇÃO - MODELO PROJETO CONTEÚDO")
    print("=" * 70)
    
    # Executar todas as verificações
    verificacoes = [
        verificar_tokens_hardcoded(),
        verificar_variaveis_ambiente(),
        verificar_arquivo_env(),
        verificar_gitignore()
    ]
    
    # Resumo final
    print("\n📊 RESUMO FINAL:")
    print("=" * 50)
    
    verificacoes_ok = sum(verificacoes)
    total_verificacoes = len(verificacoes)
    
    print(f"✅ Verificações aprovadas: {verificacoes_ok}/{total_verificacoes}")
    
    if verificacoes_ok == total_verificacoes:
        print("🎉 CONFIGURAÇÃO PERFEITA!")
        print("✅ Todos os checks passaram com sucesso")
        print("✅ Projeto pronto para uso")
        return True
    else:
        print("⚠️  CONFIGURAÇÃO INCOMPLETA!")
        print("❌ Alguns checks falharam")
        print("💡 Corrija os problemas antes de continuar")
        return False

if __name__ == "__main__":
    main()
