# generate_data.py
import pandas as pd
import numpy as np
import random
from datetime import datetime
import calendar

random.seed(42)
np.random.seed(42)

n = 600

years = [2017, 2018, 2019]
months = list(range(1,13))
types = ['Movie', 'Series']
genres = ['Comedies','Dramas','Action','Documentary','Stand-Up Comedy','International Movies','TV Comedy','Adventure','Sci-Fi','Thriller']
actors = ['Stephen','Alex','Amanda','Montana','Naseeruddin','Russell','Suhasini','Tony','Vikram','Amanda2','Chris','Patricia','Lee','Maria','Chen','Ivan','Olga','Jorge','Fatima','Hiro']
countries = ['United States','India','Not_Specified','Canada','Japan','United Kingdom','France','Germany','Brazil','Australia']

rows = []
for i in range(n):
    year = random.choice(years)
    month = random.choice(months)
    day = random.randint(1, min(28, calendar.monthrange(year, month)[1]))
    release_date = datetime(year, month, day)
    t = random.choice(types)
    genre = random.choice(genres)
    actor = random.choice(actors)
    country = random.choice(countries)
    title = f"{t[:3]}_{i}_{genre[:3]}"
    rows.append({
        'id': i+1,
        'title': title,
        'type': t,
        'release_date': release_date.strftime('%Y-%m-%d'),
        'year': year,
        'month': release_date.strftime('%B'),
        'month_num': release_date.month,
        'actor': actor,
        'country': country,
        'genre': genre
    })

df = pd.DataFrame(rows)
df.to_csv('data.csv', index=False)
print("data.csv gerado com", len(df), "linhas")
