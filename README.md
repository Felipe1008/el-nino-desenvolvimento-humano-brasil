# El Niño e o Desenvolvimento Humano no Brasil (1990–2023)

## 1. Sobre o projeto

Este repositório reúne os códigos-fonte, conjuntos de dados e procedimentos computacionais desenvolvidos para o Trabalho de Conclusão de Curso em Engenharia da Computação, cujo objetivo é investigar a relação entre a ocorrência de fenômeno El Niño e os indicadores de desenvolvimento humano e econômicos no Brasil, no período de 1990 a 2023.

A pesquisa busca analisar possíveis associações entre as variações das condições climáticas relacionadas ao fenômeno El Niño–Oscilação Sul (ENOS) e os indicadores socioeconômicos brasileiros, utilizando dados históricos de diferentes fontes.

O repositório tem como finalidade proporcionar transparência metodológica, documentar os procedimentos de processamento e análise dos dados e permitir a consulta e reprodução das etapas computacionais da pesquisa.

## 2. Objetivos

- Investigar a relação entre o fenômeno El Niño e os indicadores de desenvolvimento humano no Brasil.
- Analisar o comportamento dos indicadores socioeconômicos ao longo do período estudado.
- Organizar, integrar e processar dados provenientes de diferentes bases.
- Aplicar procedimentos de análise de dados para identificar possíveis padrões e associações entre as variáveis estudadas.

## 3. Estrutura do repositório

O projeto está organizado da seguinte forma:

```text
el-nino-desenvolvimento-humano-brasil/
│
├── data/
│   ├── raw/
│   │   ├── idh_e_indicadores_anuais_Brasil.xlsx
│   │   ├── oni.txt
│   │   └── gdp_ppp_brazil.json
│   │
│   └── processed/
│       └── dataset.csv
│
├── src/
│   ├── 01_extract.py
│   ├── 02_transform.py
│   ├── 03_validate.py
│   ├── 04_analysis.py
│   └── config.py
│
├── requirements.txt
└── README.md
```

### Descrição dos diretórios e arquivos

**`data/raw/`**

Armazena os conjuntos de dados originais utilizados na pesquisa, antes das etapas de processamento.

- `idh_e_indicadores_anuais_Brasil.xlsx`: dados de IDH e indicadores anuais do Brasil.
- `oni.txt`: dados referentes ao Oceanic Niño Index (ONI).
- `gdp_ppp_brazil.json`: dados do PIB brasileiro em paridade do poder de compra.

**`data/processed/`**

Contém os dados resultantes das etapas de processamento e integração.

- `dataset.csv`: conjunto de dados consolidado utilizado nas etapas posteriores da pesquisa.

**`src/`**

Contém os scripts desenvolvidos em Python para as etapas computacionais do projeto.

- `01_extract.py`: extração dos dados.
- `02_transform.py`: transformação e preparação dos dados.
- `03_validate.py`: validação dos dados.
- `04_analysis.py`: procedimentos de análise.
- `config.py`: configurações utilizadas pelo projeto.

## 4. Tecnologias e ferramentas

O desenvolvimento do projeto utiliza Python como linguagem de programação, juntamente com bibliotecas voltadas à manipulação, processamento e análise de dados.

As dependências utilizadas estão documentadas no arquivo `requirements.txt`.

## 5. Bases de dados

A pesquisa utiliza diferentes conjuntos de dados históricos, organizados de acordo com suas respectivas variáveis de interesse:

- **Oceanic Niño Index (ONI):** indicador utilizado para caracterizar as condições relacionadas aos fenômenos El Niño e La Niña.
- **Indicadores de desenvolvimento humano:** dados referentes ao IDH e a outros indicadores socioeconômicos do Brasil.
- **Produto Interno Bruto (PIB):** dados econômicos utilizados como variável complementar na investigação.

As fontes originais e os respectivos endereços de acesso devem ser consultados na documentação das bases de dados e no trabalho acadêmico.

## 6. Execução do projeto

Para executar o projeto localmente, é necessário possuir Python instalado.

### 6.1. Clonar o repositório

```bash
git clone https://github.com/SEU-USUARIO/el-nino-desenvolvimento-humano-brasil.git
```

### 6.2. Acessar o diretório

```bash
cd el-nino-desenvolvimento-humano-brasil
```

### 6.3. Criar um ambiente virtual

```bash
python -m venv .venv
```

Ativação no Windows:

```bash
.venv\Scripts\activate
```

### 6.4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6.5. Executar os scripts

Os scripts estão organizados por etapas de processamento. A sequência prevista é:

1. Extração dos dados.
2. Transformação dos dados.
3. Validação dos dados.
4. Análise dos dados.

Os comandos específicos de execução devem seguir as configurações e os caminhos definidos nos respectivos scripts.

## 7. Resultados

Os resultados das análises são apresentados no Trabalho de Conclusão de Curso, juntamente com a discussão dos dados, os procedimentos metodológicos e as interpretações dos resultados obtidos.

Este repositório disponibiliza os recursos computacionais utilizados para apoiar o desenvolvimento da pesquisa.

## 8. Finalidade acadêmica

Este projeto foi desenvolvido como parte dos requisitos para a conclusão do curso de Engenharia da Computação.

O código e os dados disponibilizados têm finalidade acadêmica e científica, visando contribuir para a transparência e a reprodutibilidade dos procedimentos adotados na pesquisa.

## 9. Autores

**Felipe Dias dos Santos**
**Felipe Dias Pigiani**
**Leandro Felipe Carvalho**

Curso: Engenharia da Computação

Instituição: Universidade São Francisco (USF)

Ano: 2026

---

*Repositório desenvolvido como material complementar ao Trabalho de Conclusão de Curso.*
