import pandas as pd
import sqlite3
import os

# Caminhos RELATIVOS à raiz do projeto (não dentro da pasta scripts!)
csv_path = os.path.join('C:\\python\\etlworldbank\\data\\transformed\\gdp_population_transformed.csv')
db_path = os.path.join('C:\\python\\etlworldbank\\data\\etl_worldbank.db')

# Garante que a pasta data existe (opcional, mas seguro)
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Carrega o CSV transformado
df = pd.read_csv(csv_path)

# Conecta ao banco SQLite (cria se não existir)
conn = sqlite3.connect(db_path)

# Carrega os dados para a tabela (substitui se já existir)
df.to_sql('indicadores_pais', conn, if_exists='replace', index=False)

# Fecha a conexão
conn.close()
print("Dados carregados com sucesso no banco SQLite!")
