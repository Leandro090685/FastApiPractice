from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from config.database import Session, engine, Base
import crud, schemas, models



app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

def get_db():
    db = Session()
    try:
        yield db
        # devuelve uno a la vez
    finally:
        db.close()

@app.post('/movies/', tags=['movies'], response_model=schemas.MovieModel, status_code=201)
def create_movie(movie:schemas.MovieModel, db:Session = Depends(get_db)) -> dict:
    return crud.create_movie(movie = movie, db = db)
    
@app.get('/movies/list/all', tags=['movies'], response_model=list[schemas.MovieModel])
def all_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = crud.get_all_movies(db=db,skip=skip,limit=limit)
    return movies

@app.get('/movies/{id}', tags= ['movies'], response_model=schemas.MovieModel)
def movies_id(id: int, db:Session = Depends(get_db)):
    db_movie = crud.get_movie(db, id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_movie

@app.get('/movies/list/{category}/', tags=['movies'], response_model=schemas.MovieModel)
def movie_category(category: str, db:Session = Depends(get_db)):
    result = crud.get_movie_category(db=db,category=category)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(status_code=201, content=jsonable_encoder(result))

@app.put('/movies/load/{id}/', tags=['movies'], response_model=schemas.MovieModel)
def put_one_movie(id: int, movie: schemas.MovieModel,db: Session=Depends(get_db)):
    result = crud.put_movie(db=db,id=id,movie=movie)
    return result

@app.delete('/movies/delete/{id}',tags=['movies'])
def delete_one_movie(id: int, db: Session=Depends(get_db)):
    movie_delete = crud.delete_movie(db=db, id=id)
    if not movie_delete:
        raise HTTPException(status_code=404, detail=f"No hay una pelicula con el id: {id}")
    return JSONResponse(status_code=200, content={"message": f"Se ha eliminado la película id:{id}"})