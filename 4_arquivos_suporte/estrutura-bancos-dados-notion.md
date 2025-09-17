# Estrutura dos Bancos de Dados - Editorial Gestão Educacional

## Visão Geral

O sistema Editorial Gestão Educacional é composto por 5 bancos de dados interconectados que gerenciam conteúdo educacional, categorização e organização de materiais. Todos os bancos estão localizados na página "Infraestrutura" dentro do workspace "Editorial Gestão Educacional".

## 1. Biblioteca (Principal)

**URL:** [https://www.notion.so/2325113a91a381c09b33f826449a218f](https://www.notion.so/2325113a91a381c09b33f826449a218f)

**Descrição:** Banco de dados principal que armazena todo o conteúdo educacional da biblioteca.

### Propriedades:

#### Propriedades Básicas
- **Name** (Título): Nome do item da biblioteca
- **Description**: Descrição do conteúdo (campo de texto)

#### Propriedades de Classificação
- **Categoria** (Relação): Conecta com o banco "Categoria"
- **Tipo** (Seleção): Tipo de conteúdo
  - Artigo Curto
  - Checklist
  - Lição
  - Link
  - Documento Oficial
  - Vídeo
  - Apresentação
  - Artigo
  - Texto

#### Propriedades de Status e Controle
- **Status editorial** (Status): Status do conteúdo no pipeline editorial
  - Rascunho
  - Em revisão
  - Aprovado
  - Publicado
- **Destaques** (Checkbox): Marcação para conteúdo em destaque
- **Fundacional** (Checkbox): Marcação para conteúdo fundamental

#### Propriedades de Organização
- **Tags** (Multi-seleção): Tags para categorização temática
  - Apresentação
  - Planejamento Financeiro
  - Prestação de Contas
  - RH
  - Jurídico
  - Admissão
  - Controle de Presença
  - Férias Trabalhistas
  - Gestão de Patrimônio
  - Fornecedores
  - Remuneração Estratégica
  - Auditoria
  - Desligamento
  - Fechamento de Folha
  - EVP
  - Módulo 1
  - Módulo 2
  - Video informativo

#### Propriedades de Contexto
- **Função** (Multi-seleção): Função do usuário alvo
  - Mantenedor
  - Secretário
  - Diretor
  - Coordenador
- **Nível de profundidade** (Multi-seleção): Nível organizacional
  - Estratégico
  - Tático
  - Operacional
- **Tipo de problema** (Multi-seleção): Área de problema abordada
  - Financeiro
  - Pedagógico
  - Jurídico
  - Operacional
  - Pessoas
  - Infraestrutura
  - Governança

#### Propriedades de Relacionamento
- **Cursos** (Relação): Conecta com o banco "Cursos"
- **Módulos** (Relação): Conecta com o banco "Módulos"
- **Relacionado** (Relação): Auto-relação para itens relacionados

#### Propriedades de Mídia
- **Thumbnail** (Arquivo): Imagem de capa
- **Link** (Arquivo): Arquivo principal do conteúdo
- **Checklist / URL pública** (URL): Link público para checklists

#### Propriedades de Sistema
- **Editado em** (Data): Timestamp da última edição

### Views Disponíveis:
1. **Tabela Padrão**: Visualização completa de todas as propriedades
2. **Por Eixo**: Agrupamento por categoria (board)
3. **Pipeline por Status**: Agrupamento por status editorial (board)
4. **Artigos Fundacionais**: Filtro para conteúdo fundamental
5. **Checklists**: Filtro para checklists
6. **Produção em Andamento**: Filtro para conteúdo em desenvolvimento

## 2. Categoria

**URL:** [https://www.notion.so/2325113a91a381f4b7a7ddd6fa5575b1](https://www.notion.so/2325113a91a381f4b7a7ddd6fa5575b1)

**Descrição:** Banco de dados simples para categorização dos itens da biblioteca.

### Propriedades:
- **Name** (Título): Nome da categoria
- **Description** (Texto): Descrição da categoria

### Relacionamentos:
- **Relacionado com:** Biblioteca (propriedade "Categoria")

## 3. Módulos

**URL:** [https://www.notion.so/2325113a91a38155bba2dec98a75447b](https://www.notion.so/2325113a91a38155bba2dec98a75447b)

**Descrição:** Banco de dados para organização de módulos educacionais.

### Propriedades:
- **Nome** (Título): Nome do módulo
- **Thumbnail** (Arquivo): Imagem do módulo
- **Cursos** (Relação): Conecta com o banco "Cursos"

### Relacionamentos:
- **Relacionado com:** 
  - Biblioteca (propriedade "Módulos")
  - Cursos (propriedade "Cursos")

## 4. Cursos

**URL:** [https://www.notion.so/2325113a91a3815caca3e00a2b3d8648](https://www.notion.so/2325113a91a3815caca3e00a2b3d8648)

**Descrição:** Banco de dados para organização de cursos.

### Propriedades:
- **Nome** (Título): Nome do curso
- **Thumbnail** (Arquivo): Imagem do curso

### Relacionamentos:
- **Relacionado com:** 
  - Biblioteca (propriedade "Cursos")
  - Módulos (propriedade "Cursos")

## 5. Views info

**URL:** [https://www.notion.so/2325113a91a381e799b2d1b64db53c61](https://www.notion.so/2325113a91a381e799b2d1b64db53c61)

**Descrição:** Banco de dados para documentação das views disponíveis.

### Propriedades:
- **name** (Título): Nome da view
- **view_id** (Texto): ID da view no Notion
- **description** (Texto): Descrição da view

## Diagrama de Relacionamentos

```
Biblioteca (Principal)
├── Categoria (1:N)
├── Cursos (N:N)
├── Módulos (N:N)
└── Relacionado (N:N - Auto-relação)

Módulos
└── Cursos (N:N)

Views info (Documentação)
└── Independente
```

## Características do Sistema

### Hierarquia de Conteúdo
1. **Cursos** → **Módulos** → **Biblioteca**
2. **Categoria** → **Biblioteca**

### Sistema de Status Editorial
- Pipeline de produção com 4 estágios: Rascunho → Em revisão → Aprovado → Publicado
- Controle de qualidade através de status

### Sistema de Classificação Multidimensional
- **Por Função**: Mantenedor, Secretário, Diretor, Coordenador
- **Por Nível**: Estratégico, Tático, Operacional
- **Por Área de Problema**: 7 categorias diferentes
- **Por Tags**: 18 tags temáticas específicas

### Flexibilidade de Conteúdo
- Suporte a 9 tipos diferentes de conteúdo
- Sistema de arquivos para mídia
- URLs públicas para checklists
- Auto-relacionamento para conteúdo relacionado

## Considerações Técnicas

- Todos os bancos utilizam UUIDs para identificação
- Relacionamentos são mantidos através de arrays JSON de URLs
- Sistema de timestamps automático para controle de edição
- Views especializadas para diferentes necessidades de visualização
- Suporte a arquivos e mídia integrado
