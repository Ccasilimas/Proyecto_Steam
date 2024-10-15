import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import gzip
from database import get_db

def load_data(db: Session):
    df_games = pd.read_sql('SELECT * FROM games', db)
    df_users = pd.read_sql('SELECT * FROM users', db)
    df_reviews = pd.read_sql('SELECT * FROM reviews', db)
    return df_games, df_users, df_reviews

def main():
    # Cargar los datos
    db = next(get_db())
    df_games, df_users, df_reviews = load_data(db)

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
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:6]  # Obtener los 5 más similares
            game_indices = [i[0] for i in sim_scores]
            return df_games.iloc[game_indices]['title'].to_list()
        except IndexError:
            return {"error": "game_id no encontrado."}
        except Exception as e:
            return {"error": str(e)}

    def recomendacion_usuario(user_id):
        user_games = df_users[df_users['user_id'] == user_id]['item_id'].tolist()  # Obtener los juegos jugados por el usuario

        # Inicializamos una lista para recomendaciones
        recommended_titles = []
        if user_games:  # Si el usuario ha jugado juegos
            genres = df_games[df_games['id'].isin(user_games)]['genres'].tolist()  # Get genres
            if genres:
                genres_df = pd.DataFrame({'genres': genres})  # Crear DataFrame para los géneros
                tfidf_matrix_user = tfidf_vectorizer.transform(genres_df['genres'].astype('str'))  # Calcular TF-IDF
                reduced_matrix_user = pca.transform(tfidf_matrix_user.toarray())  # Reducir la dimensionalidad
                user_cosine_sim = cosine_similarity(reduced_matrix_user, reduced_matrix)  # Similitud del coseno

                # Recomendación
                recommended_indices = user_cosine_sim.argsort(axis=1)[:, -5:]  # Índices de los 5 más recomendados
                for idx in recommended_indices.flatten():
                    if df_reviews[(df_reviews['item_id'] == df_games.iloc[idx]['id']) & (df_reviews['recommend'] == True)].any().any():
                        recommended_titles.append(df_games.iloc[idx]['title'])
                    
                    if len(recommended_titles) >= 5:
                        break
                    
                # Completar con otros juegos si no hay suficientes
                if len(recommended_titles) < 5:
                    remaining_count = 5 - len(recommended_titles)
                    other_games = df_games[~df_games['id'].isin(user_games)].sample(n=remaining_count, replace=True)
                    recommended_titles.extend(other_games['title'].tolist())
                
        return list(pd.Series(recommended_titles).drop_duplicates().head(5))

if __name__ == "__main__":
    main()