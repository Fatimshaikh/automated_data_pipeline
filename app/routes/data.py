from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.post("/data", response_model=schemas.DataItemResponse)
def create_item(item: schemas.DataItemCreate, db: Session = Depends(get_db)):
    return crud.create_data_item(db, item)

@router.get("/data", response_model=list[schemas.DataItemResponse])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_data_items(db, skip=skip, limit=limit)
