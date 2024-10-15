import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import gzip
import psutil

# Función para calcular el uso de memoria
def memory_usage():
    process = psutil.Process()
    mem = process.memory_info().rss / (1024 ** 2)  # en MB
    return mem

# Cargar los datos y descomprimirlos
df_games = pd.read_csv('app/Datos/games.csv.gz', compression='gzip')  
df_users = pd.read_csv('app/Datos/Items.csv.gz', compression='gzip')  
df_reviews = pd.read_csv('app/Datos/reviews.csv.gz', compression='gzip') 

# Calcular TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df_games['genres'].astype('str'))

# Reducir la dimensionalidad con PCA
n_components = 32  
pca = PCA(n_components=n_components)
reduced_matrix = pca.fit_transform(tfidf_matrix.toarray())

# Calcular similitud del coseno en la matriz reducida
cosine_sim = cosine_similarity(reduced_matrix, reduced_matrix)

def recomendacion_juego(game_id):
    try:
        idx = df_games.index[df_games['id'] == game_id].tolist()[0]
        sim_scores = np.array(list(enumerate(cosine_sim[idx])))  # Usar numpy aquí
        sim_scores = np.array(sorted(sim_scores, key=lambda x: x[1], reverse=True))[:5]  # Top 5
        game_indices = sim_scores[:, 0].astype(int)
        return df_games.iloc[game_indices]['title'].to_list()
    except IndexError:
        return {"error": "game_id no encontrado."}
    except Exception as e:
        return {"error": str(e)}

def recomendacion_usuario(user_id):    
    user_games = df_users[df_users['user_id'] == user_id]['item_id'].tolist()  # Obtener los juegos jugados por el usuario

    recommended_titles = []
    if user_games:
        genres = df_games[df_games['id'].isin(user_games)]['genres'].tolist()
        
        if genres:
            genres_df = pd.DataFrame({'genres': genres})
            tfidf_matrix_user = tfidf_vectorizer.transform(genres_df['genres'].astype('str'))
            reduced_matrix_user = pca.transform(tfidf_matrix_user.toarray())  # Usar np.array si es necesario
            user_cosine_sim = cosine_similarity(reduced_matrix_user, reduced_matrix)  # Similitud con todos los juegos

            recommended_indices = user_cosine_sim.argsort(axis=1)[:, -5:]  # Obtener los índices de los 5 más recomendados
            recommended_titles = []
            
            for idx in recommended_indices.flatten():
                if df_reviews[(df_reviews['item_id'] == df_games.iloc[idx]['id']) & (df_reviews['recommend'] == True)].any().any():
                    recommended_titles.append(df_games.iloc[idx]['title'])
                    if len(recommended_titles) >= 5:
                        break
            
            if len(recommended_titles) < 5:
                remaining_count = 5 - len(recommended_titles)
                other_games = df_games[~df_games['id'].isin(user_games)].sample(n=remaining_count, replace=True)
                recommended_titles.extend(other_games['title'].tolist())

        return list(pd.Series(recommended_titles).drop_duplicates().head(5))

# Medir la memoria después de las funciones
memory_used_after = memory_usage()
memory_used_after