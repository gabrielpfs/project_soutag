import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Inicializa o app
app = dash.Dash(__name__)
app.title = "Dashboard de Filmes e Séries"

# Dados simulados
dados_top = {
    "Qtd. Títulos": 8807,
    "Duração Média Filmes": "99.58 min",
    "Duração Média Séries": "16.76 temporadas",
    "Taxa de Crescimento": "22.13%",
    "Achievement": "3.30%"
}

lançamentos = pd.DataFrame({
    "Mês": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
    "Filmes": [300, 280, 310, 290, 320, 330, 340],
    "Séries": [120, 110, 130, 125, 140, 150, 160]
})

filmes_vs_series = pd.DataFrame({
    "Tipo": ["Filmes", "Séries"],
    "Percentual": [69.64, 30.36]
})

ranking_atores = pd.DataFrame({
    "Ator": ["Anupam", "Shah", "Naseeruddin", "Om", "Amitabh"],
    "Títulos": [38, 33, 30, 27, 26]
})

ranking_paises = pd.DataFrame({
    "País": ["United States", "India", "United Kingdom", "Canada", "France"],
    "Títulos": [3190, 1681, 646, 444, 336]
})

generos = pd.DataFrame({
    "Gênero": ["International Movies", "Comedies", "Dramas", "Documentaries", "Action & Adventure", "Not_Specified", "Others"],
    "Títulos": [1500, 1200, 1100, 800, 700, 600, 500]
})

# Gráficos
grafico_lancamentos = px.bar(lançamentos, x="Mês", y=["Filmes", "Séries"], barmode="group", title="Evolução por Lançamento")
grafico_pizza = px.pie(filmes_vs_series, names="Tipo", values="Percentual", title="Filmes vs Séries")
grafico_atores = px.bar(ranking_atores, x="Títulos", y="Ator", orientation="h", title="Ranking Atores vs Títulos")
grafico_paises = px.bar(ranking_paises, x="País", y="Títulos", title="Ranking Países vs Títulos")
grafico_generos = px.treemap(generos, path=["Gênero"], values="Títulos", title="Análise por Gênero")

# Layout
app.layout = html.Div([
    html.H1("Dashboard de Filmes e Séries 🎬", style={"textAlign": "center"}),

    html.Div([
        html.Div([html.H4(f"{k}: {v}")], style={"width": "20%", "display": "inline-block", "padding": "10px"})
        for k, v in dados_top.items()
    ], style={"textAlign": "center"}),

    html.Div([
        dcc.Graph(figure=grafico_lancamentos),
        dcc.Graph(figure=grafico_pizza),
    ], style={"display": "flex", "flexWrap": "wrap"}),

    html.Div([
        dcc.Graph(figure=grafico_atores),
        dcc.Graph(figure=grafico_generos),
        dcc.Graph(figure=grafico_paises),
    ], style={"display": "flex", "flexWrap": "wrap"})
])

# Executa o servidor
if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run(debug=True)
