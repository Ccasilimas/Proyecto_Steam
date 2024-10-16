Descripción del Proyecto
Este proyecto desarrolla una API RESTful utilizando FastAPI que permite consumir información sobre videojuegos, reseñas de usuarios y análisis de sentimiento para mejorar la toma de decisiones de las empresas. La API también soporta un sistema de recomendación basado en la similitud entre ítems o usuarios.

El MVP incluye:

Procesamiento de datos y preparación del dataset.
Análisis de sentimiento de las reseñas de usuarios, transformando la información textual en una escala de valores (0 = malo, 1 = neutral, 2 = positivo).
Exploratory Data Analysis (EDA) para detectar patrones y relaciones entre variables del dataset.
Despliegue de la API con endpoints que responden a consultas específicas sobre juegos, usuarios, desarrolladores y análisis de reseñas.
Sistema de recomendación de videojuegos utilizando dos enfoques: item-item (similitud de coseno) y user-item (filtro colaborativo).
Estructura del Proyecto
1. Transformaciones
Aunque no se requieren transformaciones de datos adicionales en este MVP, se eliminaron columnas innecesarias para optimizar la API y el entrenamiento de modelos de machine learning.

Se implementó la columna sentiment_analysis, que reemplaza el texto de las reseñas (user_reviews.review). Utilizando técnicas de NLP (Procesamiento de Lenguaje Natural), las reseñas se clasifican en una escala de 0 (malo), 1 (neutral) y 2 (positivo). Si una reseña no tiene texto, se le asigna automáticamente un valor de 1.

2. Feature Engineering
El análisis de sentimiento fue una parte clave de la ingeniería de características, transformando reseñas escritas por usuarios en una columna numérica que facilita la entrada de datos a los modelos.

3. Exploratory Data Analysis (EDA)
El análisis exploratorio de datos fue realizado sin el uso de librerías automáticas, siguiendo las buenas prácticas de:

Identificación de patrones y outliers en las variables.
Generación de nubes de palabras para identificar términos frecuentes en títulos de juegos.
4. API RESTful
Se desarrollaron varios endpoints con FastAPI, que pueden ser consumidos desde cualquier dispositivo conectado a internet:

/developer: Devuelve la cantidad de items y el porcentaje de contenido gratuito por año, según la desarrolladora.

/userdata: Retorna información sobre el gasto total, porcentaje de recomendación basado en reseñas, y cantidad de items de un usuario.

/UserForGenre: Devuelve el usuario que ha acumulado más horas jugadas para un género específico y su acumulación de horas por año de lanzamiento.

/best_developer_year: Proporciona el top 3 de desarrolladores con juegos más recomendados por los usuarios en un año determinado.

/developer_reviews_analysis: Devuelve un análisis de las reseñas por sentimiento (positivo/negativo) para un desarrollador en específico.

5. Sistema de Recomendación
Se implementaron dos enfoques de sistemas de recomendación:

Recomendación Item-Item: Basado en la similitud del coseno entre juegos. Ingresando el ID de un producto, se devuelven 5 juegos similares recomendados.

Recomendación User-Item: Usando un filtro colaborativo basado en la similitud entre usuarios. Ingresando el ID de un usuario, se recomiendan 5 juegos que a usuarios similares les han gustado.

Ambos sistemas están disponibles a través de endpoints en la API.

6. Despliegue
Se propone el uso de plataformas como Ngrok.

Instrucciones de Uso
Instalación
Clonar este repositorio:
bash
Copiar código
git clone https://github.com/tu_usuario/repo.git
Instalar las dependencias:
bash
Copiar código
pip install -r requirements.txt
Ejecutar la API en modo local:
bash
Copiar código
uvicorn main:app --reload
Acceder a la API en: http://127.0.0.1:8000
Endpoints
/developer?desarrollador={nombre}: Consulta juegos por desarrolladora.
/userdata?User_id={id_usuario}: Información sobre el gasto y recomendaciones de un usuario.
/UserForGenre?genero={nombre_genero}: Usuario con más horas jugadas en un género.
/best_developer_year?año={año}: Top 3 de desarrolladores por año.
/developer_reviews_analysis?desarrolladora={nombre}: Análisis de reseñas por sentimiento.
Recomendación
/recomendacion_juego?id_producto={id}: Recomendación de juegos similares.
/recomendacion_usuario?id_usuario={id}: Recomendación de juegos basados en usuarios similares.
Herramientas Utilizadas
FastAPI: Para la creación de la API.
NLP: Para análisis de sentimiento.
Python: Para el desarrollo del backend y procesamiento de datos.
Cosine Similarity: Para la recomendación item-item.
Collaborative Filtering: Para la recomendación user-item.
Despliegue
Consulta el tutorial de Render o Railway para desplegar la API en la web.

¡Este README proporciona una descripción clara y detallada de las funcionalidades del proyecto, cómo utilizar la API y los detalles técnicos más importantes!