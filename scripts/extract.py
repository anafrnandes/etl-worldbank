import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from time import sleep
import os

# Configurar retry + backoff
session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504]
)
session.mount('http://', HTTPAdapter(max_retries=retries))


def get_population(country_code, year):
    url = f'http://api.worldbank.org/v2/country/{country_code}/indicator/SP.POP.TOTL?date={year}&format=json'
    try:
        response = session.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            try:
                return data[1][0]['value']
            except (IndexError, KeyError):
                return None
        return None
    except Exception as e:
        print(f"Erro em {country_code}/{year}: {str(e)}")
        return None


# Carregar dados
df = pd.read_csv('C:\\python\\etlworldbank\\data\\raw\\API_NY.GDP.MKTP.CD_DS2_en_csv_v2_85078.csv', skiprows=4)
df = df[['Country Name', 'Country Code', '2018', '2019', '2020', '2021', '2022']]

# Processar com delays
for year in ['2018', '2019', '2020', '2021', '2022']:
    print(f"Processando ano {year}...")
    df[f'Population_{year}'] = None

    for idx, row in df.iterrows():
        code = row['Country Code']
        df.at[idx, f'Population_{year}'] = get_population(code, year)
        sleep(1)  # Delay crítico para evitar bloqueio

# Criar diretório se não existir
os.makedirs('C:\\python\\etlworldbank\\data\\enriched', exist_ok=True)

# Salvar com nome de arquivo explícito
df.to_csv('C:\\python\\etlworldbank\\data\\enriched\\gdp_population_enriched.csv', index=False)