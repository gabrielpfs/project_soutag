import os
import pandas as pd

# Caminho absoluto do CSV
csv_path = r"C:\Users\gabri\.project\project_soutag_case\data\netflix_titles.csv"

# Verifica se o arquivo existe
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV não encontrado no caminho: {csv_path}")

# Ler o CSV
df = pd.read_csv(csv_path)

# Imprimir as colunas
print("Colunas do CSV:")
for col in df.columns:
    print(f"- {col}")

# Lista esperada de colunas
expected_columns = [
    'show_id','type','title','director','cast','country',
    'date_added','release_year','rating','duration','listed_in','description'
]

# Comparar com as colunas do CSV
missing_columns = [col for col in expected_columns if col not in df.columns]
extra_columns = [col for col in df.columns if col not in expected_columns]

if not missing_columns and not extra_columns:
    print("\n✅ Todas as colunas estão corretas!")
else:
    if missing_columns:
        print("\n❌ Colunas esperadas não encontradas:")
        print(missing_columns)
    if extra_columns:
        print("\n⚠️ Colunas extras encontradas no CSV:")
        print(extra_columns)
