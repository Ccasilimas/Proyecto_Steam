# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Float
from sqlalchemy import func, case
from sqlalchemy.orm import Session
from database import get_db                                                                         # Conexion a database MYSQL
from models import Game, UserPlaytime, Reviews  
from recommendations import recomendacion_juego, recomendacion_usuario                              # Llamado de funciones ML

app = FastAPI(title="Proyecto Steam")

@app.get("/", response_description="Returns a welcome message")
def read_root():
    return {"Api funcionando"}

# Primera funcion llama a una base de datos MYSQL con hosting en Google Cloud
@app.get("/developer/{developer}", response_description="Consulta la cantidad total de juegos por año según el desarrollador")
def developer(developer: str, db: Session = Depends(get_db)):
    # Consulta la cantidad total de juegos por año según el desarrollador
    results = (
        db.query(
            func.extract('year', Game.release_date).label("release_year"),                          # Extraer el año de release_date
            func.count(Game.id).label("total_items"),
            (func.sum(case((Game.price == "Free To Play", 1), else_=0)) / func.count(Game.id) * 100).label("free_content_percentage"),
        )
        .filter(Game.developer == developer)
        .group_by(func.extract('year', Game.release_date))                                          # Agrupar por el año extraído de release_date
        .order_by(func.extract('year', Game.release_date).desc())
        .all()
    )

    # Formatear la respuesta
    response = []
    for release_year, total_items, free_content_percentage in results:
        response.append({
            "Año": int(release_year),                                                               # Convertir a int para el año
            "Cantidad de Items": total_items,
            "Contenido Free": f"{free_content_percentage:.2f}%"                                     
        })

    return response

# Segunda funcion llama a una base de datos MYSQL con hosting en Google Cloud
@app.get("/userdata/{user_id}", response_description="Get user spending data")
def userdata(user_id: str, db: Session = Depends(get_db)):
    # Cantidad total de dinero gastado
    total_spent = db.query(func.sum(UserPlaytime.playtime_forever)).join(Game, UserPlaytime.item_id == Game.id).filter(UserPlaytime.user_id == user_id).scalar() or 0
    
    # Considerando que los precios son en otra columna
    prices = db.query(func.sum(func.cast(Game.price, Float))).join(UserPlaytime, UserPlaytime.item_id == Game.id).filter(UserPlaytime.user_id == user_id).scalar() or 0
    
    # Porcentaje de recomendación
    recommendation_count = db.query(func.count(Reviews.id_review)).join(Game, Reviews.item_id == Game.id).filter(Reviews.recommend == True).filter(UserPlaytime.user_id == user_id).count()
    total_reviews = db.query(func.count(Reviews.id_review)).join(Game, Reviews.item_id == Game.id).filter(UserPlaytime.user_id == user_id).count()
    recommendation_percentage = (recommendation_count / total_reviews * 100) if total_reviews > 0 else 0

    # Cantidad de ítems
    item_count = db.query(func.count(UserPlaytime.item_id)).filter(UserPlaytime.user_id == user_id).scalar() or 0

    # Formatear la respuesta
    response = {
        "Usuario": user_id,
        "Dinero gastado": f"{prices} USD",
        "% de recomendación": f"{recommendation_percentage:.2f}%",
        "cantidad de items": item_count
    }

    return response


# Tercera funcion llama a una base de datos MYSQL con hosting en Google Cloud
@app.get("/UserForGenre/{genero}", response_description="Obtener el usuario con más horas jugadas por género")
def UserForGenre(genero: str, db: Session = Depends(get_db)):
    # Filtrar los juegos por género
    games = db.query(Game).filter(Game.genres.contains(genero)).all()  

    if not games:
        return {"error": "No se encontraron juegos para este género."}

    # Obtener los IDs de los juegos para hacer la consulta de horas
    game_ids = [game.id for game in games]

    # Agrupar por usuario y año de lanzamiento, sumando horas jugadas
    user_hours = (
        db.query(
            UserPlaytime.user_id,
            func.extract('year', Game.release_date).label("release_year"),
            func.sum(UserPlaytime.playtime_forever).label("total_hours")
        )
        .join(Game, UserPlaytime.item_id == Game.id)                                                # Unir UserPlaytime con Game
        .filter(Game.id.in_(game_ids))                                                              # Filtrar por los IDs de los juegos en el género
        .group_by(UserPlaytime.user_id, "release_year")                                             # Agrupar por usuario y año
        .all()
    )

    # 4. Crear un diccionario para acumular horas por usuario
    hours_by_user = {}
    for user_id, release_year, total_hours in user_hours:
        if user_id not in hours_by_user:
            hours_by_user[user_id] = {}
        hours_by_user[user_id][release_year] = hours_by_user[user_id].get(release_year, 0) + total_hours

    # 5. Encontrar el usuario con más horas en total
    if not hours_by_user:                                                                           # Si no hay horas registradas para usuarios, salir
        return {"error": "No hay horas registradas para usuarios en este género."}

    max_user = max(hours_by_user.items(), key=lambda x: sum(x[1].values()))                         # Obtener el usuario con más horas

    # Formatear los datos a devolver
    hours_per_year = [{"Año": year, "Horas": hours} for year, hours in max_user[1].items()]
    
    response = {
        "Usuario con más horas jugadas para Género": max_user[0],
        "Horas jugadas": hours_per_year
    }

    return response

@app.get("/best_developer_year/{year}")
def best_developer_year(year: int, db: Session = Depends(get_db)):
    # Obtener el top 3 de desarrolladores con juegos recomendados para el año dado
    top_developers = db.query(
        Game.developer,
        func.count(Reviews.id_review).label("recommended_count")
    ).join(Reviews, Game.id == Reviews.item_id) \
     .filter(
         Reviews.recommend.is_(True),
         func.extract('year', Game.release_date) == year
    ) \
     .group_by(Game.developer) \
     .order_by(func.count(Reviews.id_review).desc()) \
     .limit(3) \
     .all()

    # Imprimir los resultados para depuración
    print("Top Developers:", top_developers)

    if not top_developers:
        raise HTTPException(status_code=404, detail="No se encuentran desarrolladores para el año mencionado.")

    # Preparar la respuesta en el formato solicitado
    response = [{"Puesto 1": top_developers[0][0]} if i == 0 else 
                {"Puesto 2": top_developers[1][0]} if i == 1 else 
                {"Puesto 3": top_developers[2][0]} 
                for i in range(len(top_developers))]

    return response


@app.get("/developer_reviews_analysis/{desarrolladora}")
def developer_reviews_analysis(desarrolladora: str, db: Session = Depends(get_db)):
    # Obtener la cantidad de reseñas positivas y negativas para el desarrollador especificado
    positive_count = db.query(func.count(Reviews.id_review)).join(Game, Game.id == Reviews.item_id) \
        .filter(Game.developer == desarrolladora, Reviews.sentiment_analysis == 1).scalar() or 0

    negative_count = db.query(func.count(Reviews.id_review)).join(Game, Game.id == Reviews.item_id) \
        .filter(Game.developer == desarrolladora, Reviews.sentiment_analysis == 0).scalar() or 0

    if positive_count == 0 and negative_count == 0:
        raise HTTPException(status_code=404, detail="Desarrollador no encontrado o sin reseñas.")

    # Preparar la respuesta en el formato solicitado
    response = {
        desarrolladora: {
            "Negative": negative_count,
            "Positive": positive_count
        }
    }

    return response
# llamado a primerda funcion de Machine Learning en recommendations
@app.get("/recomendacion/{game_id}", description="Obtener recomendaciones para un juego específico.")
async def get_recomendacion_juego(game_id: int):
    # Llamar a tu función
    try:
        recomendaciones = recomendacion_juego(game_id)
        return recomendaciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Llamado a segunda funcion de Machine Learning en archivo recommendations
@app.get("/recomendacion_usuario/{user_id}", description="Obtener recomendaciones para un juego específico.")
async def get_recomendacion_usuario(user_id):
    # Llamar a tu función
    try:
        recomendaciones = recomendacion_usuario(user_id)
        return recomendaciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return recomendacion_usuario(user_id, db)


#
# Ejecutar la aplicación
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  