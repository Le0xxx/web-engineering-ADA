import uuid
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

# База данных SQLite
engine = create_engine("sqlite:///shaurma.db")
Base = declarative_base()

# Модель для SQLAlchemy
class ShaurmaModel(Base):
    __tablename__ = "shaurmas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    ingredients = Column(Text)
    price = Column(Float)
    image_url = Column(String)

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Pydantic модель для запросов и ответов
class Shaurma(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=3, max_length=50)
    ingredients: str = Field(..., min_length=10)
    price: float = Field(..., gt=0)
    image_url: Optional[str] = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="Шаурма API", description="API для управления меню шаурмы")


# CREATE
@app.post("/shaurmas/", response_model=Shaurma, status_code=status.HTTP_201_CREATED)
def create_shaurma(shaurma: Shaurma, db: Session = Depends(get_db)):
    db_shaurma = ShaurmaModel(name=shaurma.name, ingredients=shaurma.ingredients, price=shaurma.price, image_url=shaurma.image_url)
    db.add(db_shaurma)
    db.commit()
    db.refresh(db_shaurma)
    return shaurma


# READ
@app.get("/shaurmas/", response_model=List[Shaurma])
def read_shaurmas(db: Session = Depends(get_db)):
    return [Shaurma.from_orm(shaurma) for shaurma in db.query(ShaurmaModel).all()]


@app.get("/shaurmas/{shaurma_id}", response_model=Shaurma)
def read_shaurma(shaurma_id: int, db: Session = Depends(get_db)):
    shaurma = db.query(ShaurmaModel).get(shaurma_id)
    if not shaurma:
        raise HTTPException(status_code=404, detail="Шаурма не найдена")
    return Shaurma.from_orm(shaurma)


# UPDATE
@app.put("/shaurmas/{shaurma_id}", response_model=Shaurma)
def update_shaurma(shaurma_id: int, shaurma: Shaurma, db: Session = Depends(get_db)):
    db_shaurma = db.query(ShaurmaModel).get(shaurma_id)
    if not db_shaurma:
        raise HTTPException(status_code=404, detail="Шаурма не найдена")
    db_shaurma.name = shaurma.name
    db_shaurma.ingredients = shaurma.ingredients
    db_shaurma.price = shaurma.price
    db_shaurma.image_url = shaurma.image_url
    db.commit()
    db.refresh(db_shaurma)
    return Shaurma.from_orm(db_shaurma)


# DELETE
@app.delete("/shaurmas/{shaurma_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shaurma(shaurma_id: int, db: Session = Depends(get_db)):
    db_shaurma = db.query(ShaurmaModel).get(shaurma_id)
    if not db_shaurma:
        raise HTTPException(status_code=404, detail="Шаурма не найдена")
    db.delete(db_shaurma)
    db.commit()
    return {"message": "Шаурма удалена"}