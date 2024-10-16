# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Float, func, case
from sqlalchemy.orm import Session
from database import get_db  # Conexión a la base de datos MYSQL
from models import Game, UserPlaytime, Reviews  
from recommendations import recomendacion_juego, recomendacion_usuario  # Llamado de funciones ML
import uvicorn

app = FastAPI(title="Proyecto Steam")

@app.get("/", response_description="Returns a welcome message")
def read_root():
    return {"Api funcionando"}

# Primera función: consulta la cantidad total de juegos por año según el desarrollador
@app.get("/developer/{developer}", response_description="Consulta la cantidad total de juegos por año según el desarrollador")
def developer(developer: str, db: Session = Depends(get_db)):
    print(f"Consultando juegos del desarrollador: {developer}")
    results = (
        db.query(
            func.extract('year', Game.release_date).label("release_year"),
            func.count(Game.id).label("total_items"),
            (func.sum(case((Game.price == "Free To Play", 1), else_=0)) / func.count(Game.id) * 100).label("free_content_percentage"),
        )
        .filter(Game.developer == developer)
        .group_by(func.extract('year', Game.release_date))
        .order_by(func.extract('year', Game.release_date).desc())
        .all()
    )

    response = []
    for release_year, total_items, free_content_percentage in results:
        response.append({
            "Año": int(release_year),
            "Cantidad de Items": total_items,
            "Contenido Free": f"{free_content_percentage:.2f}%"                                     
        })
    
    print(f"Resultados: {response}")
    return response

# Segunda función: obtiene datos de gasto del usuario
@app.get("/userdata/{user_id}", response_description="Get user spending data")
def userdata(user_id: str, db: Session = Depends(get_db)):
    print(f"Obteniendo datos de gasto para el usuario: {user_id}")
    total_spent = db.query(func.sum(UserPlaytime.playtime_forever)).join(Game, UserPlaytime.item_id == Game.id).filter(UserPlaytime.user_id == user_id).scalar() or 0
    prices = db.query(func.sum(func.cast(Game.price, Float))).join(UserPlaytime, UserPlaytime.item_id == Game.id).filter(UserPlaytime.user_id == user_id).scalar() or 0
    
    recommendation_count = db.query(func.count(Reviews.id_review)).join(Game, Reviews.item_id == Game.id).filter(Reviews.recommend == True).filter(UserPlaytime.user_id == user_id).count()
    total_reviews = db.query(func.count(Reviews.id_review)).join(Game, Reviews.item_id == Game.id).filter(UserPlaytime.user_id == user_id).count()
    recommendation_percentage = (recommendation_count / total_reviews * 100) if total_reviews > 0 else 0

    item_count = db.query(func.count(UserPlaytime.item_id)).filter(UserPlaytime.user_id == user_id).scalar() or 0

    response = {
        "Usuario": user_id,
        "Dinero gastado": f"{prices} USD",
        "% de recomendación": f"{recommendation_percentage:.2f}%",
        "Cantidad de items": item_count
    }

    print(f"Datos de usuario: {response}")
    return response

# Tercera función: obtener el usuario con más horas jugadas por género
@app.get("/UserForGenre/{genero}", response_description="Obtener el usuario con más horas jugadas por género")
def UserForGenre(genero: str, db: Session = Depends(get_db)):
    print(f"Buscando el usuario con más horas jugadas en el género: {genero}")
    games = db.query(Game).filter(Game.genres.contains(genero)).all()

    if not games:
        return {"error": "No se encontraron juegos para este género."}

    game_ids = [game.id for game in games]
    user_hours = (
        db.query(
            UserPlaytime.user_id,
            func.extract('year', Game.release_date).label("release_year"),
            func.sum(UserPlaytime.playtime_forever).label("total_hours")
        )
        .join(Game, UserPlaytime.item_id == Game.id)
        .filter(Game.id.in_(game_ids))
        .group_by(UserPlaytime.user_id, "release_year")
        .all()
    )

    hours_by_user = {}
    for user_id, release_year, total_hours in user_hours:
        if user_id not in hours_by_user:
            hours_by_user[user_id] = {}
        hours_by_user[user_id][release_year] = hours_by_user[user_id].get(release_year, 0) + total_hours

    if not hours_by_user:
        return {"error": "No hay horas registradas para usuarios en este género."}

    max_user = max(hours_by_user.items(), key=lambda x: sum(x[1].values()))
    hours_per_year = [{"Año": year, "Horas": hours} for year, hours in max_user[1].items()]
    
    response = {
        "Usuario con más horas jugadas para Género": max_user[0],
        "Horas jugadas": hours_per_year
    }

    print(f"Usuario máximo: {response}")
    return response

@app.get("/best_developer_year/{year}")
def best_developer_year(year: int, db: Session = Depends(get_db)):
    print(f"Consultando mejores desarrolladores para el año: {year}")
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

    if not top_developers:
        raise HTTPException(status_code=404, detail="No se encuentran desarrolladores para el año mencionado.")

    response = [{"Puesto 1": top_developers[0][0]} if i == 0 else 
                {"Puesto 2": top_developers[1][0]} if i == 1 else 
                {"Puesto 3": top_developers[2][0]} 
                for i in range(len(top_developers))]

    print(f"Desarrolladores mejores: {response}")
    return response

@app.get("/developer_reviews_analysis/{desarrolladora}")
def developer_reviews_analysis(desarrolladora: str, db: Session = Depends(get_db)):
    print(f"Analizando reseñas para la desarrolladora: {desarrolladora}")
    positive_count = db.query(func.count(Reviews.id_review)).join(Game, Game.id == Reviews.item_id) \
        .filter(Game.developer == desarrolladora, Reviews.sentiment_analysis == 1).scalar() or 0

    negative_count = db.query(func.count(Reviews.id_review)).join(Game, Game.id == Reviews.item_id) \
        .filter(Game.developer == desarrolladora, Reviews.sentiment_analysis == 0).scalar() or 0

    if positive_count == 0 and negative_count == 0:
        raise HTTPException(status_code=404, detail="Desarrollador no encontrado o sin reseñas.")

    response = {
        desarrolladora: {
            "Negative": negative_count,
            "Positive": positive_count
        }
    }
    
    print(f"Análisis de reseñas: {response}")
    return response

@app.get("/recomendacion/{game_id}", description="Obtener recomendaciones para un juego específico.")
async def get_recomendacion_juego(game_id: int):
    print(f"Obteniendo recomendaciones para el juego ID: {game_id}")
    try:
        recomendaciones = recomendacion_juego(game_id)
        print(f"Recomendaciones obtenidas: {recomendaciones}")
        return recomendaciones
    except Exception as e:
        print(f"Error al obtener recomendaciones: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recomendacion_usuario/{user_id}", description="Obtener recomendaciones para un usuario específico.")
async def get_recomendacion_usuario(user_id: str):
    print(f"Obteniendo recomendaciones para el usuario ID: {user_id}")
    try:
        recomendaciones = recomendacion_usuario(user_id)
        print(f"Recomendaciones obtenidas: {recomendaciones}")
        return recomendaciones
    except Exception as e:
        print(f"Error al obtener recomendaciones: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Ejecutar la aplicación
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)