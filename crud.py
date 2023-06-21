from sqlalchemy.orm import Session
from sqlalchemy.sql import compiler
from fastapi.responses import JSONResponse

import schemas, models


def get_all_movies(db:Session, skip: int = 0, limit: int = 100):
    return db.query(models.Movie).offset(skip).limit(limit).all()

def create_movie(movie:schemas.MovieModel, db:Session):
    new_movie = models.Movie(**movie.dict())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

def get_movie(db:Session, id:int):
    return db.query(models.Movie).get(id)

def get_movie_category(db:Session, category: str):
    return db.query(models.Movie).filter(models.Movie.category == category).all()

def put_movie(db:Session, id: int, movie:models.Movie):
    movie_to_put = db.query(models.Movie).filter(models.Movie.id == id).first()
    if not movie_to_put:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    movie_to_put.title = movie.title
    movie_to_put.overview = movie.overview
    movie_to_put.year = movie.year
    movie_to_put.rating = movie.rating
    movie_to_put.category = movie.category
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})

def delete_movie(db: Session, id:int):
    result = db.query(models.Movie).filter(models.Movie.id == id).delete()
    db.commit()
    return result

   

