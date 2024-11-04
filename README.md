
# Descripción del Proyecto

Este proyecto desarrolla una API RESTful utilizando FastAPI, que permite consumir información sobre videojuegos, reseñas de usuarios y análisis de sentimiento para mejorar la toma de decisiones de las empresas. La API también soporta un sistema de recomendación basado en la similitud entre ítems o usuarios.

## MVP Incluye

1. **Procesamiento de Datos y Preparación del Dataset**: Limpieza y consolidación de datos.
2. **Análisis de Sentimiento**: Transformación de reseñas de usuarios en una escala de valores (0 = malo, 1 = neutral, 2 = positivo) utilizando técnicas de NLP (Procesamiento de Lenguaje Natural).
3. **Exploratory Data Analysis (EDA)**: Detección de patrones y relaciones entre variables del dataset.
4. **Despliegue de la API**: Creación de endpoints para consultas específicas sobre juegos, usuarios, desarrolladores y análisis de reseñas.
5. **Sistema de Recomendación**: Implementación de dos enfoques de recomendación de videojuegos: 
   - **Item-Item**: Basado en la similitud de coseno entre juegos.
   - **User-Item**: Usando filtro colaborativo basado en la similitud entre usuarios.

## Estructura del Proyecto

### Transformaciones
- Aunque no se requieren transformaciones de datos adicionales en este MVP, se eliminaron columnas innecesarias para optimizar la API y el entrenamiento de modelos de machine learning.
- Implementación de la columna `sentiment_analysis`, que reemplaza el texto de las reseñas (`user_reviews.review`). Si una reseña no tiene texto, se le asigna automáticamente un valor de 1.

### Feature Engineering
- El análisis de sentimiento fue una parte clave, transformando reseñas escritas por usuarios en una columna numérica que facilita la entrada de datos a los modelos.

### Exploratory Data Analysis (EDA)
- Identificación de patrones y outliers en las variables.
- Generación de nubes de palabras para identificar términos frecuentes en títulos de juegos.

### API RESTful
Se desarrollaron varios endpoints con FastAPI, accesibles desde cualquier dispositivo conectado a internet:
- `/developer`: Devuelve la cantidad de ítems y el porcentaje de contenido gratuito por año, según la desarrolladora.
- `/userdata`: Retorna información sobre el gasto total, porcentaje de recomendación basado en reseñas, y cantidad de ítems de un usuario.
- `/UserForGenre`: Devuelve el usuario que ha acumulado más horas jugadas para un género específico y su acumulación de horas por año de lanzamiento.
- `/best_developer_year`: Proporciona el top 3 de desarrolladores con juegos más recomendados por los usuarios en un año determinado.
- `/developer_reviews_analysis`: Devuelve un análisis de las reseñas por sentimiento (positivo/negativo) para un desarrollador en específico.
=======
Descripción del Proyecto
Este proyecto desarrolla una API RESTful utilizando FastAPI, que permite consumir información sobre videojuegos, reseñas de usuarios y análisis de sentimiento para mejorar la toma de decisiones de las empresas. La API también soporta un sistema de recomendación basado en la similitud entre ítems o usuarios.

MVP Incluye
Procesamiento de Datos y Preparación del Dataset: Limpieza y consolidación de datos.

Análisis de Sentimiento: Transformación de reseñas de usuarios en una escala de valores (0 = malo, 1 = neutral, 2 = positivo) utilizando técnicas de NLP (Procesamiento de Lenguaje Natural).

Exploratory Data Analysis (EDA): Detección de patrones y relaciones entre variables del dataset.

Despliegue de la API: Creación de endpoints para consultas específicas sobre juegos, usuarios, desarrolladores y análisis de reseñas.

Sistema de Recomendación: Implementación de dos enfoques de recomendación de videojuegos:

Item-Item: Basado en la similitud de coseno entre juegos.

User-Item: Usando filtro colaborativo basado en la similitud entre usuarios.

Estructura del Proyecto
Transformaciones
Aunque no se requieren transformaciones de datos adicionales en este MVP, se eliminaron columnas innecesarias para optimizar la API y el entrenamiento de modelos de machine learning.

Implementación de la columna sentiment_analysis, que reemplaza el texto de las reseñas (user_reviews.review). Si una reseña no tiene texto, se le asigna automáticamente un valor de 1.

Feature Engineering
El análisis de sentimiento fue una parte clave, transformando reseñas escritas por usuarios en una columna numérica que facilita la entrada de datos a los modelos.

Exploratory Data Analysis (EDA)
Identificación de patrones y outliers en las variables.

Generación de nubes de palabras para identificar términos frecuentes en títulos de juegos.

API RESTful
Se desarrollaron varios endpoints con FastAPI, accesibles desde cualquier dispositivo conectado a internet:

/developer: Devuelve la cantidad de ítems y el porcentaje de contenido gratuito por año, según la desarrolladora.

/userdata: Retorna información sobre el gasto total, porcentaje de recomendación basado en reseñas, y cantidad de ítems de un usuario.
>>>>>>> 1e87374488c2b4866937db1b9236b0f3804595b1

### Sistema de Recomendación
Se implementaron dos enfoques:
- **Recomendación Item-Item**: Basado en la similitud del coseno entre juegos. Ingresando el ID de un producto, se devuelven 5 juegos similares recomendados.
- **Recomendación User-Item**: Usando un filtro colaborativo basado en la similitud entre usuarios. Ingresando el ID de un usuario, se recomiendan 5 juegos que a usuarios similares les han gustado.

### Despliegue
=======
/best_developer_year: Proporciona el top 3 de desarrolladores con juegos más recomendados por los usuarios en un año determinado.

/developer_reviews_analysis: Devuelve un análisis de las reseñas por sentimiento (positivo/negativo) para un desarrollador en específico.

Sistema de Recomendación
Se implementaron dos enfoques:

Recomendación Item-Item: Basado en la similitud del coseno entre juegos. Ingresando el ID de un producto, se devuelven 5 juegos similares recomendados.

Recomendación User-Item: Usando un filtro colaborativo basado en la similitud entre usuarios. Ingresando el ID de un usuario, se recomiendan 5 juegos que a usuarios similares les han gustado.

Despliegue
Se propone el uso de plataformas como Ngrok para el despliegue.
