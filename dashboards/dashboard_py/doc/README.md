# 🎬 Dashboard de Filmes e Séries

Este projeto é um **Dashboard Interativo** construído em **Python** utilizando as bibliotecas **Dash** e **Plotly**, inspirado em uma visualização no estilo **Power BI**.  

O objetivo é fornecer insights sobre a base de dados de filmes e séries, com métricas, KPIs e visualizações dinâmicas.

---

## 📊 Funcionalidades

- **KPIs** principais:
  - Quantidade de Títulos
  - Duração Média de Filmes
  - Duração Média de Séries
  - Taxa de Crescimento
  - Achievement (nível de alcance)

- **Gráficos e Visualizações**:
  - 📈 Evolução de lançamentos ao longo do tempo (barra + linha)
  - 🥧 Distribuição de Filmes vs Séries (Donut Chart)
  - ⭐ Ranking de Atores por quantidade de títulos
  - 🌍 Ranking de Países por número de títulos
  - 🎭 Análise por Gênero (Treemap)

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.8+](https://www.python.org/)
- [Dash](https://dash.plotly.com/)  
- [Plotly](https://plotly.com/python/)  
- [Pandas](https://pandas.pydata.org/)

---

## 📂 Estrutura do Projeto

```m
├── app.py # Código principal do dashboard
├── README.md # Documentação do projeto
└── requirements.txt (opcional)
```


---

## 🚀 Como Rodar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/dashboard-filmes-series.git
   cd dashboard-filmes-series
    ```
2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**
   ```bash
    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows
    ```
3. Instale as dependências:
   ```bash
    pip install dash plotly pandas
    ```
4. Execute o projeto:
   ```bash
    python app.py
    ```
5. Acesse no navegador:
   ```bash
    http://127.0.0.1:8050
    ```

## 📌 Customização

Atualmente, os dados estão simulados no código.

Para conectar à sua base real (CSV, Excel ou SQL):

Substitua os DataFrames no código por leitura de arquivo, por exemplo:

```py
df = pd.read_csv("sua_base.csv")
```

As cores e layouts podem ser ajustados via parâmetros do Plotly.