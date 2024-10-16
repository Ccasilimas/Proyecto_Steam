# models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, JSON, Float
from sqlalchemy.orm import relationship
from database import Base

class UserPlaytime(Base):
    __tablename__ = "user_playtime"

    user_id = Column(String(50), primary_key=True, nullable=False)                                              # Ajusta el tamaño según tus necesidades
    item_id = Column(Integer, primary_key=True, nullable=False)                                                 # Clave primaria combinada
    playtime_forever = Column(Integer)

    def __repr__(self):
        return f"<UserPlaytime(user_id={self.user_id}, item_id={self.item_id})>"

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)                                                                      # Clave primaria
    title = Column(String(255)) 
    developer = Column(String(255))
    release_date = Column(Date)
    genres = Column(JSON)                                                                                       # Almacena géneros como JSON
    tags = Column(JSON)                                                                                         # Almacena etiquetas como JSON
    price = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Game(id={self.id}, developer={self.developer})>"

class Reviews(Base):
    __tablename__ = "reviews"

    id_review = Column(Integer, primary_key=True, autoincrement=True)                                           # Clave primaria
    item_id = Column(Integer, ForeignKey("games.id"))                                                           # Clave foránea de 'games'
    recommend = Column(Boolean)
    sentiment_analysis = Column(Integer)
    game = relationship("Game", back_populates="reviews")                                                       # Relación inversa

    def __repr__(self):
        return f"<Reviews(id_review={self.id_reviews})>"

# Añadir relación en el modelo Game
Game.reviews = relationship("Reviews", order_by=Reviews.id_review, back_populates="game")