import pandas as pd
import ast  
import numpy as np
import re
import nltk
import json
import gzip #Importar y descomprimir
from sqlalchemy import create_engine            # Se usa para acceso a MYSQL engine
from sqlalchemy.exc import SQLAlchemyError      # Se usa para determinar errores en el proceso de carga
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables de entorno
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
host = os.getenv('MYSQL_HOST')
port = os.getenv('MYSQL_PORT')
database = os.getenv('MYSQL_DB')
table_name = os.getenv('MYSQL_TABLE2')


# Cargar el archivo .json.gz que contiene los datos en formato de diccionario
with gzip.open('users_items.json.gz', 'rt', encoding='utf-8') as file:
    data = []
    for line in file:
        try:
            data.append(ast.literal_eval(line.strip()))  # Convertir de string a diccionario
        except ValueError:
            pass

# Cargar los datos al DF de pandas
df = pd.DataFrame(data)

# Se eliminan colunmnas inecesarias para analisis
df = df.drop(columns=['user_url', 'steam_id'])

items_list = []

# Iterar sobre cada fila del DataFrame original
for index, row in df.iterrows():
    user_id = row['user_id']
    items = row['items']
    
    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict):
                items_list.append({
                    'user_id': user_id,
                    'item_id': item['item_id'],
                    'playtime_forever': item['playtime_forever'],
                    'playtime_2weeks': item['playtime_2weeks']
                })

# Crear un nuevo DataFrame a partir de la lista de diccionarios
df = pd.DataFrame(items_list)

# Limpia los duplicados de las dos claves
df = df.drop_duplicates(subset=['user_id', 'item_id'])

# Convertir datos a CSV file
df.to_csv('API/Datos/Items.csv.gz', index=False, compression='gzip')

# Asegúrate de que user_id e item_id sean strings
df['user_id'] = df['user_id'].astype(str)
df['item_id'] = df['item_id'].astype(str)

# Comprobar que el DataFrame no esté vacío
if df.empty:
    raise ValueError("El DataFrame está vacío. No se puede insertar en la base de datos.")

# Crea la conexión a la base de datos
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

# Insertar el DataFrame a MySQL en bloques
chunk_size = 50000  

try:
    with engine.connect() as connection:
        trans = connection.begin()  # Inicia la transacción
        try:
            for i in range(0, len(df), chunk_size):
                chunk = df[i:i + chunk_size]
                if not chunk.empty:
                    chunk.to_sql(name=table_name, con=connection, if_exists='append', index=False)
            trans.commit()  # Confirma la transacción
        except Exception:
            trans.rollback()  # Deshacer cambios si ocurre un error
except SQLAlchemyError:
    pass

# Verifica el conteo de filas en la tabla después de la inserción
try:
    with engine.connect() as connection:
        result = connection.execute(f'SELECT COUNT(*) FROM {table_name}')
        count = result.fetchone()[0]
except SQLAlchemyError:
    pass
