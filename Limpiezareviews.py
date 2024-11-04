import pandas as pd
import ast  
import numpy as np
import re
import nltk
import gzip
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Abrir y leer el archivo .json.gz
with gzip.open('user_reviews.json.gz', 'rt', encoding='utf-8') as file:
    data = []
    for line in file:
        data.append(ast.literal_eval(line.strip()))  # Convertir de string a diccionario

# Eliminar la columna 'user_url' y expandir los datos de 'reviews'
processed_data = []
for entry in data:
    user_id = entry['user_id']
    for review in entry['reviews']:
        review['user_id'] = user_id  # Agregar user_id a cada review
        processed_data.append(review)

# Crear un DataFrame de pandas
df = pd.DataFrame(processed_data)

print (df)

# Eliminar la palabra 'posted' al inicio y luego los espacios o comillas simples al inicio y final
df['posted'] = df['posted'].str.replace('Posted', '', regex=True).str.strip(" '")

# Imprimir el DataFrame para verificar los cambios
print(df['posted'])

# Eliminar la frase 'people found this review funny' y luego los espacios en blanco
df['funny'] = df['funny'].str.replace('people found this review funny', '', regex=False).str.strip()

# Imprimir el DataFrame para verificar los cambios
print(df['funny'])

from nltk.sentiment import SentimentIntensityAnalyzer

# Asegúrate de descargar los recursos requeridos de NLTK solo una vez
nltk.download('vader_lexicon')

# Inicializa el analizador de sentimientos
sia = SentimentIntensityAnalyzer()

def get_sentiment(review):
    # Convertir cualquier valor a cadena
    review = str(review)
    
    if pd.isnull(review) or review.strip() == "":
        return 1  # Valor neutral si no hay reseña
    sentiment_score = sia.polarity_scores(review)['compound']
    if sentiment_score < -0.05:
        return 0  # Malo
    elif sentiment_score > 0.05:
        return 2  # Positivo
    else:
        return 1  # Neutral

# Aplica la función a la columna de reseñas y crea la nueva columna en el DataFrame existente
df['sentiment_analysis'] = df['review'].apply(get_sentiment)

# Elimina la columna review
df = df.drop(columns=['review'])

# Muestra las primeras filas del DataFrame actualizado
print(df.head())

# Función para reemplazar los valores de la columna 'helpful'
def replace_helpful_values(value):
    if value == 'No ratings yet':
        return 0
    # Busca un patrón de porcentaje en la cadena
    match = re.search(r'\((\d+)%\)', value)
    if match:
        return int(match.group(1))  # Devuelve el número encontrado
    else:
        return np.nan  # Valor por defecto si no se encuentra una coincidencia

# Aplica la función a la columna 'helpful'
df['helpful'] = df['helpful'].apply(replace_helpful_values)

# Asegúrate de que los valores sean enteros
df['helpful'] = df['helpful'].fillna(0).astype(int)

df['id_review'] = range(1, len(df) + 1)  # Esto comenzará desde 1

# Eliminar columnas inecesarias del DataFrame
df = df.drop(columns=['posted', 'last_edited','funny'])

print(df)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las credenciales de la base de datos desde las variables de entorno
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')

# URL de conexión
connection_string = f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}'
engine = create_engine(connection_string)

# Escribir el DataFrame en la tabla de MySQL
df.to_sql('reviews', con=engine, index=False, if_exists='append') 

print("Datos subidos exitosamente a MySQL.")

# Guardar el archivo en csv comprimido
df.to_csv('API/Datos/reviews.csv.gz', index=False, compression='gzip')
