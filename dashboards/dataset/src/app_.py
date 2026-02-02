# app.py
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('data.csv', parse_dates=['release_date'])
df['month_order'] = df['month_num']
df_months_order = ['January','February','March','April','May','June','July','August','September','October','November','December']

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server

type_opts = ['All'] + sorted(df['type'].unique().tolist())
year_opts = sorted(df['year'].unique().tolist())
month_opts = ['All'] + df_months_order

sidebar = dbc.Col([
    html.Div([
        html.H4("Soutag", style={'marginTop':'10px','marginBottom':'20px'}),
        html.H6("FILTROS"),
        html.Label("Tipo"),
        dcc.Dropdown(id='filter-type', options=[{'label':t,'value':t} for t in type_opts], value='All', clearable=False),
        html.Br(),
        html.Label("Ano"),
        dcc.Dropdown(id='filter-year', options=[{'label':y,'value':y} for y in year_opts], value=2018, clearable=False),
        html.Br(),
        html.Label("Mês"),
        dcc.Dropdown(id='filter-month', options=[{'label':m,'value':m} for m in month_opts], value='All', clearable=False),
    ], style={'padding': '10px'})
], width=2)

def aggregate_monthly(dff):
    # Count titles per month
    months = dff.groupby('month_num').size().reindex(range(1,13), fill_value=0)
    return pd.DataFrame({'month_num': months.index, 'count': months.values, 'month': [pd.to_datetime(str(m), format='%m').strftime('%B') for m in months.index]})

content = dbc.Col([
    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='chart-monthly')), width=9),
        dbc.Col(html.Div(dcc.Graph(id='chart-donut')), width=3)
    ], style={'marginBottom':'20px'}),
    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='chart-actors')), width=4),
        dbc.Col(html.Div(dcc.Graph(id='chart-treemap')), width=4),
        dbc.Col(html.Div(dcc.Graph(id='chart-countries')), width=4)
    ])
], width=10)

app.layout = dbc.Container([
    dbc.Row([sidebar, content], style={'height':'100vh'})
], fluid=True)

@app.callback(
    Output('chart-monthly','figure'),
    Output('chart-donut','figure'),
    Output('chart-actors','figure'),
    Output('chart-treemap','figure'),
    Output('chart-countries','figure'),
    Input('filter-type','value'),
    Input('filter-year','value'),
    Input('filter-month','value')
)
def update_all(f_type, f_year, f_month):
    dff = df.copy()
    if f_type and f_type != 'All':
        dff = dff[dff['type'] == f_type]
    if f_year:
        dff = dff[dff['year'] == int(f_year)]
    if f_month and f_month != 'All':
        dff = dff[dff['month'] == f_month]

    # Monthly area/line
    monthly = aggregate_monthly(dff)
    fig_month = px.area(monthly, x='month', y='count', line_shape='spline', markers=True)
    fig_month.update_layout(title='Evolução por Lançamento', showlegend=False, margin=dict(t=40,l=20,r=20,b=20))
    fig_month.update_yaxes(range=[0, max(10, monthly['count'].max()+5)])

    # Donut: Movies vs Series
    donut_df = dff['type'].value_counts().reset_index()
    donut_df.columns = ['type','count']
    if donut_df.empty:
        donut_df = pd.DataFrame({'type':['Movie','Series'],'count':[0,0]})
    fig_donut = px.pie(donut_df, names='type', values='count', hole=0.55)
    fig_donut.update_layout(title='Filmes vs Séries', margin=dict(t=40,l=10,r=10,b=10), showlegend=True)

    # Actors ranking
    actors = dff['actor'].value_counts().nlargest(10).reset_index()
    actors.columns = ['actor','count']
    fig_actors = px.bar(actors.sort_values('count'), x='count', y='actor', orientation='h', text='count')
    fig_actors.update_layout(title='Ranking Atores vs Títulos', margin=dict(t=30,l=10,r=10,b=10))

    # Treemap genres
    genres = dff['genre'].value_counts().reset_index()
    genres.columns = ['genre','count']
    fig_tree = px.treemap(genres, path=['genre'], values='count')
    fig_tree.update_layout(title='Analise por Gênero', margin=dict(t=30,l=10,r=10,b=10))

    # Countries ranking
    countries = dff['country'].value_counts().nlargest(8).reset_index()
    countries.columns = ['country','count']
    fig_countries = px.bar(countries.sort_values('count', ascending=True), x='count', y='country', orientation='h', text='count')
    fig_countries.update_layout(title='Ranking Países vs Títulos', margin=dict(t=30,l=10,r=10,b=10))

    return fig_month, fig_donut, fig_actors, fig_tree, fig_countries

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
