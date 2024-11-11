from dotenv import load_dotenv
import os
import gzip
import json
import ast
import pandas as pd

load_dotenv()

database_url = os.getenv('DATABASE_URL')
api_key = os.getenv('API_KEY')
secret_key = os.getenv('SECRET_KEY')

# Abrir y leer el archivo .json.gz

with gzip.open('steam_games.json.gz', 'rt', encoding='utf-8') as file:
    data = []
    for line in file:
        try:
            data.append(json.loads(line.strip()))  # Convertir de string a diccionario
        except json.JSONDecodeError as e:
            pass

# Crear un DataFrame de pandas
df = pd.DataFrame(data)

# Eliminar filas completamente vacías
df.dropna(how='all', inplace=True)

# Eliminar filas que tengan NaN en cualquier campo
df.dropna(inplace=True)

# Eliminar las columnas especificadas
columns_to_drop = ['publisher', 'app_name', 'url', 'reviews_url', 'specs','early_access']
df.drop(columns=columns_to_drop, inplace=True)


# %%
# Eliminar filas con fechas inválidas
df = df.dropna(subset=['release_date'])

# Eliminar filas duplicadas en 'id'
df = df.drop_duplicates(subset='id')

# Eliminar las filas con valores nulos en la columna 'release_date'
df = df.dropna(subset=['release_date'])

df = df.dropna(subset=['title'])

# Convertir la columna 'release_date' a formato datetime (si no lo es ya)
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

# %%
# Asegúrate de que la columna sea de tipo string antes de hacer la comparación
df['price'] = df['price'].astype(str)

# Filtra los valores donde la longitud de los datos en 'price' sea menor o igual a 20 caracteres
df_filtrado = df[df['price'].str.len() <= 14]

# Si deseas modificar el DataFrame original, puedes reasignarlo
df = df_filtrado

# Convertimos la columna 'price' a numérica, y donde no pueda convertir, pone un 0
df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)


# Si necesitas que 'price' sea entero:
df['price'] = df['price'].astype(float)

print(df)


# Muestra el DataFrame sin los datos que tenían más de 20 caracteres
print(df)


# %%
# Obtener la lista de valores más comunes
valores_mas_comunes = df['developer'].value_counts()

# Obtener el segundo valor más repetido
segundo_mas_repetido = valores_mas_comunes.index[1]  # El índice [1] es el segundo más repetido
frecuencia_segundo_mas_repetido = valores_mas_comunes.iloc[1]  # Obtener la frecuencia del segundo más repetido

print(f"El segundo valor más repetido es: {segundo_mas_repetido} con una frecuencia de {frecuencia_segundo_mas_repetido}")


# %%
# Buscar el valor de 'title' donde 'id' es igual a 730
title_730 = df.loc[df['id'] == 730, 'title'].values[0]
print(f"El título correspondiente al id 730 es: {title_730}")


# %%
import mysql.connector
import json

# Conexión a la base de datos MySQL
conexion = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST'),
    port=os.getenv('MYSQL_PORT'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DB')
)

# Crear cursor
cursor = conexion.cursor()

# Crear la tabla si no existe
create_table_query = """
CREATE TABLE IF NOT EXISTS games (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    developer VARCHAR(255),
    release_date DATE,
    genres JSON,
    tags JSON,
    price VARCHAR(20)
);
"""
cursor.execute(create_table_query)

# Definir el tamaño del bloque
block_size = 1000  # Cambia esto según tus necesidades

# Insertar datos del DataFrame en la tabla en bloques
for start in range(0, len(df), block_size):
    end = start + block_size
    chunk = df[start:end]  # Obtén el bloque de datos

    # Crear la sentencia de inserción
    insert_query = """
    INSERT INTO games (id, title, developer, release_date, genres, tags, price)
    VALUES (%s, %s, %s, %s, %s, %s,%s)
    """
    
    # Ejecutar inserciones en bloque
    data_to_insert = []
    for index, row in chunk.iterrows():
        data_to_insert.append((
            row['id'],
            row['title'],
            row['developer'],
            row['release_date'],
            json.dumps(row['genres']),  # Convertir la lista a JSON
            json.dumps(row['tags']),     # Convertir la lista a JSON
            row['price']
        ))

    # Ejecutar la inserción de bloque
    cursor.executemany(insert_query, data_to_insert)

    # Confirmar los cambios de cada bloque
    conexion.commit()

# Cerrar la conexión
cursor.close()
conexion.close()

# %%
# Convertir datos a CSV file
df.to_csv('API/Datos/games.csv.gz', index=False, compression='gzip')
