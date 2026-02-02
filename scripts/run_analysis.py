import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from src.db import create_engine_postgres
from src.config import load_env

# Inicialização
load_env()
engine = create_engine_postgres()

# Função para plotar barra horizontal
def plot_bar(df, x, y, title, palette='viridis'):
    sns.barplot(data=df, x=x, y=y, palette=palette)
    plt.title(title)
    plt.tight_layout()
    plt.show()

# 1️⃣ Top países
df_countries = pd.read_sql("SELECT * FROM view_top_countries;", engine)
plot_bar(df_countries, x='total_titles', y='country', title="Top 10 Países com Mais Títulos")

# 2️⃣ Evolução de lançamentos
df_trends = pd.read_sql("SELECT DATE_TRUNC('month', date_added) AS month, COUNT(*) AS total_titles FROM titles_clean GROUP BY month ORDER BY month;", engine)
sns.lineplot(data=df_trends, x='month', y='total_titles', marker='o')
plt.title("Evolução Mensal de Lançamentos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3️⃣ Distribuição filmes x séries
df_types = pd.read_sql("SELECT type, COUNT(*) AS total FROM titles_clean GROUP BY type;", engine)
plt.pie(df_types['total'], labels=df_types['type'], autopct='%1.1f%%', startangle=90)
plt.title("Distribuição Filmes x Séries")
plt.show()

# 4️⃣ Top atores/atrizes
df_cast = pd.read_sql("SELECT actor, COUNT(*) AS appearances FROM titles_by_cast GROUP BY actor ORDER BY appearances DESC LIMIT 20;", engine)
plot_bar(df_cast, x='appearances', y='actor', title="Top 20 Atores/Atrizes")
