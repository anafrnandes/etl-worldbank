import pandas as pd
import os

# Carregar o arquivo enriquecido
input_path = os.path.join('C:\\python\\etlworldbank\\data\\enriched\\gdp_population_enriched.csv')
df = pd.read_csv(input_path)

#print(df.head())
# Remover linhas sem PIB ou população em algum ano (exemplo: 2022)
df = df.dropna(subset=['2022', 'Population_2022'])

# Remover duplicatas de país (não deve ter, mas por segurança)
df = df.drop_duplicates(subset=['Country Name', 'Country Code'])
anos = ['2018', '2019', '2020', '2021', '2022']

for ano in anos:
    pib_col = ano
    pop_col = f'Population_{ano}'
    per_capita_col = f'gdp_per_capita_{ano}'
    # Cálculo do PIB per capita
    df[per_capita_col] = df[pib_col] / df[pop_col]

for ano in anos:
    per_capita_col = f'gdp_per_capita_{ano}'
    norm_col = f'gdp_per_capita_norm_{ano}'
    max_value = df[per_capita_col].max()
    df[norm_col] = df[per_capita_col] / max_value
# Salvar o DataFrame transformado
output_path = os.path.join('C:\\python\\etlworldbank\\data\\transformed\\gdp_population_transformed.csv')
df.to_csv(output_path, index=False)

import os
print(os.path.abspath('data/etl_worldbank.db'))
print(os.path.exists('data/etl_worldbank.db'))
