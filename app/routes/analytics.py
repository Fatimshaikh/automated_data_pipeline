from ..database import get_db
from .. import crud
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/latest")
def latest_value(db: Session = Depends(get_db)):
    item = crud.get_latest_value(db)
    if not item:
        return {"message": "No data found"}
    # Access ORM object attributes using dot notation
    return {"latest_value": item.value, "name": item.name}


@router.get("/average")
def average_value(db: Session = Depends(get_db)):
    avg = crud.get_average_value(db)
    return {"average_value": avg}

@router.get("/minmax")
def min_max_value(db: Session = Depends(get_db)):
    min_val = crud.get_min_value(db)
    max_val = crud.get_max_value(db)
    return {"min_value": min_val, "max_value": max_val}


@router.get("/average-range")
def average_in_range(
    start: datetime = Query(..., description="Start datetime in ISO format"),
    end: datetime = Query(..., description="End datetime in ISO format"),
    db: Session = Depends(get_db)
):
    avg = crud.get_average_in_range(db, start, end)
    return {"average_value": avg, "start": start, "end": end}

@router.get("/minmax-range")
def minmax_in_range(
    start: datetime = Query(..., description="Start datetime in ISO format"),
    end: datetime = Query(..., description="End datetime in ISO format"),
    db: Session = Depends(get_db)
):
    min_val, max_val = crud.get_minmax_in_range(db, start, end)
    return {"min_value": min_val, "max_value": max_val, "start": start, "end": end}

@router.get("/average-last-24h")
def average_last_24h(db: Session = Depends(get_db)):
    end = datetime.utcnow()
    start = end - timedelta(hours=24)
    avg = crud.get_average_in_range(db, start, end)
    return {"average_last_24h": avg}

