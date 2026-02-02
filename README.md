# Análise de Dados Netflix

## 🎯 Contexto do Projeto

O desafio consistiu em transformar dados brutos da Netflix em insights acionáveis, aplicando técnicas de ETL, modelagem de dados, SQL, análise exploratória e visualização de dados. O objetivo era mostrar capacidade ponta a ponta, raciocínio analítico estruturado, clareza na documentação e entrega de resultados interpretáveis para o negócio.

## Dashboard

![dashboard](assets/step_analysis/dashboard.png)

## 1 Etapa: Banco de Dados (Dataset)

### 📂 Acesso e Download do Dataset

Para iniciar o desenvolvimento do teste técnico, a primeira ação foi acessar o dataset recomendado no enunciado:

- Netflix Movies and TV Shows Dataset (Kaggle)

- Orientacao:

1. Acessar o Link do Kaggle: [Kaggle](https://www.kaggle.com/)
2. Criar uma conta na plataforma
3. Acessar o Dataset: [Netflix Movies and TV Shows – Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)
4. Realizar o Download em: `Download dataset as zip (1 MB).`

- Formato do Dataset: `CSV`.
- Número de Registros do Dataset: 8.807

### 📑 Descrição Geral

Este dataset contém informações detalhadas sobre títulos disponíveis na Netflix, incluindo:

- Filmes e séries
- País de origem
- Ano de lançamento
- Duração
- Gênero (listado em múltiplas categorias)
- Elenco
- Classificação indicativa

### 📋 Analise da Estrutura das Colunas do Dataset

A seguir, um snapshot com as colunas originais presentes no CSV, seus tipos de dados esperados e uma breve explicação:

![snapshot](assets/step_0/snapshot.png)


### ✅ Ações Realizadas nesta Etapa

1. Acesso ao link oficial do Kaggle fornecido no enunciado do teste.

2. Download do arquivo CSV contendo a base completa de 8.807 registros.

3. Verificação inicial do formato do arquivo para assegurar compatibilidade com ferramentas de ingestão (SQL, Python, Power BI).

4. Levantamento da estrutura de colunas do dataset (descrição acima) para embasar as próximas etapas de modelagem e tratamento.

### 🔎 Observações Iniciais

- A base apresenta estrutura em CSV, o que facilita ingestão tanto em linguagens de programação (Python/R) quanto em bancos de dados SQL.

- O tamanho (8.807 registros) é relativamente pequeno, mas o desafio deve ser tratado como se fossem milhões de registros em constante atualização (simulação de cenário real de Big Data).

- Futuras etapas incluirão validação de dados, tratamento de nulos, padronização de colunas e normalização.

### Objetivo da Estruturacao e Organizacao de Pastas

A decisão técnica por separar scripts de execução  em(scripts/) das funções em (src/) permite modularidade, testes independentes e escalabilidade, importante em cenários de produção.

## 2 Etapa – Ingestão de Dados

### 🎯 Objetivo

Realizar o processo de importacao do `Dataset` bruto extraido como Bando de Dados recomendado atraves do Kaggle em formato CSV para o PostgreSQL hospedado na nuvem (Supabase), garantindo:

- Persistência e Escalabilidade;

- Estrutura de dados inicial para transformações subsequentes;

- Validação de integridade (colunas e registros).

### ⚙️ Preparação do Ambiente

1. Configuração do ambiente local de desenvolvimento:

- Editor de código escolhido: Visual Studio Code (VSCode).

- Linguagem de programação principal: Python.

- Instalação das bibliotecas necessárias: pandas, sqlalchemy, psycopg2.

- Criação de um ambiente virtual (venv) para isolamento das dependências.

```shell
python -m venv venv
venv\Scripts\activate # Windows
pip install pandas sqlalchemy psycopg2
pip install psycopg2-binary
```

Python como Ferramenta de Conexão SQL
Vantagens

1. Automação: importar CSVs diretamente para PostgreSQL via scripts.

2. Flexibilidade: manipular dados antes de salvar no banco.

3. Integração: funciona com bibliotecas de análise (pandas, numpy) e visualização (matplotlib, seaborn, plotly).

4. Escalabilidade: você consegue criar pipelines de dados que funcionam para milhares ou milhões de registros.

5. Profissional: é uma prática padrão em Data Science e Analytics.


2. Configuração do Banco de Dados em Nuvem:

0. Serviço escolhido: `Supabase` (`PostgreSQL` hospedado em nuvem).
1. Acessar o Link do Supabase: [Supabase](https://supabase.com/)
2. Criar uma Conta na Plataforma (Gratuito)
3. Criar uma Organizacao e Configurar com Credenciais

- Name
- Type
- Plan

4. Criar um Projeto dentro da Organizacao e Configurar com Credenciais

- Organization
- Project name
- Database password
- Region

5. Apos isso seu Projeto ja estara criado e pronto para adquirir as Credenciais de Conexao.

⚠️ Importante: O Supabase gera uma senha padrão para o usuário postgres. Se você quiser criar usuários adicionais ou senhas específicas, pode fazer isso na aba Authentication > Users ou via SQL.

6. No interior do Project na barra Superior, voce encontra o campo `Connect`.
7. Em Direct Connection voce vai encontrar Credenciais de Conexao

postgresql://postgres:[YOUR-PASSWORD]@yourhost:5432/your_database
- host: your_host
- port: 5432
- database: your_database
- user: your_user

Justificativa da escolha:

- Escalabilidade para bases maiores.
- Facilidade de conexão remota.
- Interface intuitiva para gestão de schemas e tabelas.
- Gratuito no plano inicial, adequado para prototipagem.

Vantagens de usar na nuvem:

- Não precisa se preocupar com instalação, configuração e backup.
- Escalabilidade (cresce conforme aumenta o volume de dados).
- Pode ser acessado de qualquer lugar via internet.
- Fácil integração com Python, BI e outras ferramentas.

Ações realizadas:

- Criação da conta na plataforma Supabase.
- Criação de um novo projeto e provisionamento de instância PostgreSQL.
- Registro de credenciais de conexão (host, user, password, port, database).

### ✅ Ações Realizadas nesta Etapa

Configuração e validação do ambiente Python no VSCode.

Criação da instância PostgreSQL em nuvem (Supabase).

Conexão estabelecida com credenciais seguras.

Ingestão do dataset bruto para a tabela titles_raw no banco de dados.

### 🔎 Observações e Boas Práticas

A ingestão inicial foi realizada na tabela raw, preservando os dados originais sem transformação.

A separação entre camadas (raw, staging, production) será aplicada nas próximas etapas de modelagem.

Esta abordagem facilita reprocessamentos e garante governança sobre os dados.

### 📂 Estrutura de Arquivos Criada

project_soutag_case/
│
├── data/
│ └── netflix_titles.csv
├── env/
│ └── .env
├── scripts/
│ ├── run_ingest.py
│ └── test_connection.py
└── src/
├── config.py
├── db.py
├── ingest.py
└── logger.py

- 🔐 Arquivo .env

```py
DB=your_database
DB_USER=your_database_user
DB_PASSWORD="your_password"
DB_HOST=db.avjflpafvwstzhhmelnn.supabase.co
DB_PORT=5432
DB_NAME=your_database_name
```

### 📜 Principais Scripts de Suporte

- `config.py` → Carregamento e validação de variáveis de ambiente (.env).

- `db.py` → Criação do engine de conexão com PostgreSQL (SQLAlchemy + psycopg2).

- `ingest.py` → Funções de ingestão: leitura do CSV, validação de colunas e carga no banco.

- `logger.py` → Configuração de logging estruturado.

- `run_ingest.py` → Script orquestrador que realiza todo o fluxo de ingestão.

- `test_columns.py` → Testa se as colunas do CSV estão corretas.

- `test_connection.py` → Testa se a conexão com PostgreSQL foi estabelecida com sucesso.

### 🔗 Conexão Python → PostgreSQL

```py
from sqlalchemy import create_engine
engine = create_engine(
f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
```

### 🚀 Execução do Script Principal (run_ingest.py)

1. Carrega variáveis de ambiente.

2. Testa conexão com PostgreSQL.

3. Lê o arquivo netflix_titles.csv.

4. Valida colunas obrigatórias.

5. Ingesta os dados para a tabela netflix_raw.

6. Mostra o total de registros importados e 5 primeiros registros.

Exemplo de saída esperada:

```shell
2025-09-25 11:00:01 [INFO] CSV loaded: 8807 rows, 12 columns
2025-09-25 11:00:01 [INFO] All expected columns are present.
2025-09-25 11:00:05 [INFO] Data ingested into table 'netflix_raw'
2025-09-25 11:00:05 [INFO] Ingestion completed successfully!
✅ Total de registros importados: 8807
✅ Primeiros 5 registros:
('s1', 'Movie', 'Dick Johnson Is Dead', ...)
('s2', 'TV Show', 'Blood & Water', ...)
...
```

Exemplo de saide esperada do test_connection:

```shell
🔹 Iniciando teste de conexão com PostgreSQL...
✅ Variáveis de ambiente carregadas com sucesso
✅ Engine de conexão criada com sucesso
✅ Conexão testada com sucesso! Versão do PostgreSQL: PostgreSQL 15.3 (ou similar)
```

### ✅ Ações Realizadas nesta Etapa

- Configuração e validação do ambiente Python no VSCode.

- Criação da instância PostgreSQL em nuvem (Supabase).

- Organização modular do projeto com scripts de conexão, testes e ingestão.

- Ingestão do dataset bruto para a tabela netflix_raw no banco de dados.

### 🔎 Observações e Boas Práticas

- A ingestão inicial foi realizada na tabela raw, preservando os dados originais sem transformação.

- A separação entre camadas (raw, staging, production) será aplicada nas próximas etapas de modelagem.

- Utilização de .env para proteção de credenciais sensíveis.

- Modularização do código para facilitar manutenção, testes e reuso.

## 3 Etapa - Tratamento e Modelagem de Dados

### 🎯 Objetivo

Realizar o tratamento da tabela netflix_raw para gerar tabelas intermediárias já limpas, normalizadas e estruturadas, atendendo às boas práticas de modelagem de dados.

### ⚙️ Configuração do Ambiente

- Editor de desenvolvimento: VSCode.

- Linguagem de programação: Python (utilizando pandas e sqlalchemy).

- Banco de dados: PostgreSQL (Supabase Cloud).

- Estrutura do projeto expandida:

```
project_soutag_case/
│
├── scripts/
│ └── run_transform.py
└── src/
├── transform.py
├── config.py
├── db.py
└── logger.py
```

### 🛠️ Principais Processos de Transformação

1. Padronização de colunas

- Conversão de nomes para snake_case.

- Conversão da coluna date_added para tipo DATE.

- Separação da coluna duration em:

    - duration_value

    - duration_unit

2. Tratamento de valores

- Preenchimento de valores nulos em country com not_specified.

- Padronização de colunas categóricas (type, listed_in, rating) em letras minúsculas e sem espaços extras.

- Normalização da coluna rating, substituindo valores nulos por not_rated.

3. Normalização de colunas multivalor

- country expandida em tabela auxiliar titles_by_country (relação 1 × N entre show_id e países).

- listed_in expandida em tabela auxiliar titles_by_genre (relação 1 × N entre show_id e gêneros).

- Remoção de duplicados para integridade relacional.

4. Modelagem relacional

- Criação da tabela principal titles_clean (padronizada).

- Criação de chaves primárias em titles_clean(show_id).

- Criação de chaves estrangeiras em titles_by_country e titles_by_genre para garantir integridade referencial.

📜 Scripts Desenvolvidos

1. transform.py → Contém todas as funções de transformação, modelagem e normalização:

- clean_titles(df) → padroniza colunas e trata valores.

- save_clean_table(df) → persiste titles_clean no banco.

- create_primary_key_titles_clean() → adiciona PK.

- create_titles_by_country(df) → gera tabela auxiliar de países.

- create_titles_by_genre(df) → gera tabela auxiliar de gêneros.

- create_foreign_keys() → cria FKs relacionando tabelas auxiliares a titles_clean.

- validate_tables() → valida registros, nulos e duplicados.

- run_transform() → orquestra todo o pipeline.

- run_transform.py → Script orquestrador para executar a transformação completa.

### 🚀 Fluxo de Execução do run_transform.py

- Carrega tabela netflix_raw do PostgreSQL.

- Realiza limpeza e padronização (titles_clean).

- Salva titles_clean no PostgreSQL.

- Cria chave primária na tabela titles_clean.

- Gera tabelas auxiliares titles_by_country e titles_by_genre.

- Cria chaves estrangeiras garantindo integridade referencial.

- Executa validações finais sobre registros, nulos e duplicados.

- Loga primeiros registros das tabelas auxiliares para verificação.

### ✅ Ações Realizadas nesta Etapa

- Configuração do ambiente de transformação no VSCode.

- Criação do script transform.py com funções robustas de ETL.

- Estruturação relacional das tabelas intermediárias (titles_clean, titles_by_country, titles_by_genre).

- Criação de chaves primárias e estrangeiras.

- Implementação de validações pós-transformação.

### 🔎 Observações e Boas Práticas

- O pipeline foi implementado em Python + SQLAlchemy, favorecendo escalabilidade e manutenção.

- Utilização de logs em cada etapa garante rastreabilidade e auditoria.

- A normalização em tabelas auxiliares permite análises mais flexíveis e consistentes.

- Separação clara entre etapas de ingestão e transformação garante organização em camadas (raw → clean → analysis).

## 4 Etapa - Analise de Dados

### 🎯 Objetivo

Transformar os dados tratados e normalizados em insights estratégicos, criando visualizações claras, interpretáveis e prontas para decisões de negócio.

Os principais objetivos desta etapa são:

- Identificar padrões e tendências estratégicas na base de títulos da Netflix.

- Criar visualizações de fácil compreensão para stakeholders e BI.

- Gerar insights relevantes para apoiar decisões estratégicas.

### ⚙️ Ferramentas Utilizadas

- Python: Pandas, Matplotlib, Seaborn.

- SQL: queries no PostgreSQL para agregações e filtragens.

- BI: Power BI para dashboards interativos.

### 📝 Planejamento da Análise

Antes de iniciar a execução, definimos as análises prioritárias:

1. Top países com mais títulos

```sql
SELECT country, COUNT(*) AS total_titles
FROM titles_by_country
GROUP BY country
ORDER BY total_titles DESC
LIMIT 10;
```

Visualização: gráfico de barras mostrando os 6 principais países.

2. Evolução de lançamentos por mês e ano

```py
import pandas as pd
import matplotlib.pyplot as plt


# Dataframe com data_added convertido para datetime
df['date_added'] = pd.to_datetime(df['date_added'])
df.groupby([df['date_added'].dt.year, df['date_added'].dt.month]).size().plot(kind='line')
plt.title('Evolução de lançamentos por mês-ano')
plt.show()
```

3.Distribuição Filmes x Séries

```py
df['type'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Distribuição de Filmes e Séries')
plt.show()
```

4. Análise de elenco

- Explosão da coluna `cast` em linhas separadas.

- Contagem de aparições dos atores/atrizes mais frequentes.

- Identificação de padrões de colaboração entre atores.

- Visualizações em gráficos de barras e redes de colaboração.

5. Análises adicionais sugeridas

- Distribuição por gênero ao longo do tempo.

- Correlação entre país e tipo de título.

- Análise de ratings e sua relação com duração e país.

### 📈 Resultados Esperados

- Gráficos claros e interpretáveis.

- Insights acionáveis, como países com mais lançamentos ou tendências de gênero.

- Relatórios exploratórios que possam ser usados para tomada de decisão.


### ⚙️ Fluxo de trabalho - Hibrido

- Python → análise exploratória inicial, visualizações rápidas, preparação de DataFrames.

- SQL → criação de views e agregações para alimentar Python e Power BI.

- Power BI → dashboards interativos com KPIs estratégicos.

### 📈 Consultas SQL Principais

1. Top países com mais títulos

```sql
CREATE OR REPLACE VIEW view_top_countries AS
SELECT country, COUNT(*) AS total_titles
FROM titles_by_country
GROUP BY country
ORDER BY total_titles DESC;
```

2. Evolução de lançamentos por mês-ano

```sql
CREATE OR REPLACE VIEW view_monthly_trends AS
SELECT DATE_TRUNC('month', date_added) AS month,
       COUNT(*) AS total_titles
FROM titles_clean
WHERE date_added IS NOT NULL
GROUP BY month
ORDER BY month;
```

3. Distribuição filmes x séries

```sql
CREATE OR REPLACE VIEW view_type_distribution AS
SELECT type, COUNT(*) AS total
FROM titles_clean
GROUP BY type;
```

4. Top atores/atrizes

```sql
CREATE OR REPLACE VIEW view_top_cast AS
SELECT actor, COUNT(*) AS appearances
FROM titles_by_cast
GROUP BY actor
ORDER BY appearances DESC
LIMIT 20;
```

5. Títulos por gênero

```sql
CREATE OR REPLACE VIEW view_titles_by_genre AS
SELECT genre, COUNT(*) AS total_titles
FROM titles_by_genre
GROUP BY genre
ORDER BY total_titles DESC;
```

💡 Observação: As views criadas permitem alimentar o dashboard e realizar análises repetíveis sem precisar reprocessar o dataset.


#### 📈 Análise em Python

Pipeline sugerido

- Conectar ao PostgreSQL via SQLAlchemy.

- Executar queries SQL e retornar DataFrames.

- Gerar visualizações com Seaborn/Plotly.


```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Conexão com PostgreSQL
engine = create_engine("postgresql+psycopg2://user:password@host:port/dbname")

# Top países
df_countries = pd.read_sql("SELECT * FROM view_top_countries LIMIT 10;", engine)
sns.barplot(data=df_countries, x='total_titles', y='country', palette='viridis')
plt.title("Top 10 Países com Mais Títulos")
plt.tight_layout()
plt.show()

# Evolução de lançamentos
df_trends = pd.read_sql("SELECT * FROM view_monthly_trends;", engine)
sns.lineplot(data=df_trends, x='month', y='total_titles', marker='o')
plt.title("Evolução Mensal de Lançamentos")
plt.tight_layout()
plt.show()

# Distribuição filmes x séries
df_types = pd.read_sql("SELECT * FROM view_type_distribution;", engine)
plt.pie(df_types['total'], labels=df_types['type'], autopct='%1.1f%%')
plt.title("Distribuição Filmes x Séries")
plt.show()

# Top atores/atrizes
df_cast = pd.read_sql("SELECT * FROM view_top_cast;", engine)
sns.barplot(data=df_cast, y='actor', x='appearances', palette='magma')
plt.title("Top 20 Atores/Atrizes")
plt.tight_layout()
plt.show()
```

💡 Boas práticas profissionais:

- Modularizar o código (analysis.py) para fácil manutenção.

- Documentar cada gráfico e análise no notebook.

- Garantir scripts reprodutíveis e versionáveis.


### 📊 Preparação de Dados para Power BI

1. Views SQL → alimentar diretamente as tabelas no Power BI.

2. Relacionamentos:

- titles_clean.show_id → titles_by_country.show_id (1:N)

- titles_clean.show_id → titles_by_genre.show_id (1:N)

- titles_clean.show_id → titles_by_cast.show_id (1:N)

3. KPIs e Medidas sugeridas (DAX):

```m
Total Titles = COUNT(titles_clean[show_id])
```

```m
Total Movies = CALCULATE(COUNT(titles_clean[show_id]), titles_clean[type] = "Movie")
```

```m
Total Series = CALCULATE(COUNT(titles_clean[show_id]), titles_clean[type] = "TV Show")
```

```m
Top Countries = TOPN(10, SUMMARIZE(titles_by_country, titles_by_country[country], "Total", COUNT(titles_by_country[show_id])), [Total], DESC)
```

### 📊 Visualizações recomendadas:

- Top países → Bar chart horizontal

- Evolução de lançamentos → Line chart

- Distribuição filmes x séries → Pie/Donut chart

- Top atores/atrizes → Bar chart horizontal

- Títulos por gênero → Treemap ou Column chart

### 🔎 Observações Finais da Etapa

A análise combinou SQL para agregações + Python para visualização + Power BI para dashboards interativos, garantindo performance e clareza.

As visualizações permitem identificar padrões estratégicos: mercados prioritários, tendências de lançamentos, foco do catálogo e perfis de elenco.

Scripts e queries criados são reutilizáveis, permitindo atualização periódica da análise sem retrabalho.
