# Sistema de Classificação (Arquivo Histórico)

Esta pasta contém os arquivos históricos do sistema de classificação que foi migrado para a pasta `scripts/`.

## Arquivos Migrados

- `classificador_biblioteca.py` → `scripts/aplicar_taxonomia_simples.ps1`
- `config_classificador.json` → `scripts/classificacao_final_100_porcento.json`
- `executar_classificacao.py` → `scripts/aplicar_taxonomia_simples.ps1`
- `testar_classificacao.py` → Removido (funcionalidade integrada)
- `INSTRUCOES_CLASSIFICACAO.md` → `docs/TAXONOMIA_INDEXACAO.md`

## Status

**ARQUIVO HISTÓRICO** - Esta pasta é mantida apenas para referência histórica. Para usar o sistema de classificação atual, utilize os scripts na pasta `scripts/`.

## Sistema Atual

O sistema de classificação atual está localizado em:
- `scripts/aplicar_taxonomia_simples.ps1` - Script principal
- `docs/TAXONOMIA_INDEXACAO.md` - Documentação completa
- `scripts/classificacao_final_100_porcento.json` - Configuração final
