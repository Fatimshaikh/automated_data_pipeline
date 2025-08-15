
from . import models, schemas
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func


def create_data_item(db: Session, item: schemas.DataItemCreate):
    db_item = models.DataItem(name=item.name, value=item.value)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_data_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DataItem).offset(skip).limit(limit).all()


def get_latest_value(db: Session, city: str | None = None):
    query = db.query(models.DataItem)
    if city:
        query = query.filter(models.DataItem.city == city)
    item = query.order_by(models.DataItem.id.desc()).first()
    return item  # Return SQLAlchemy object, not dict



def get_average_value(db: Session):
    return db.query(func.avg(models.DataItem.value)).scalar()

def get_min_value(db: Session):
    return db.query(func.min(models.DataItem.value)).scalar()

def get_max_value(db: Session):
    return db.query(func.max(models.DataItem.value)).scalar()

def get_average_in_range(db: Session, start: datetime, end: datetime):
    return db.query(func.avg(models.DataItem.value))\
             .filter(models.DataItem.created_at >= start)\
             .filter(models.DataItem.created_at <= end)\
             .scalar()

def get_minmax_in_range(db: Session, start: datetime, end: datetime):
    min_val = db.query(func.min(models.DataItem.value))\
                .filter(models.DataItem.created_at >= start)\
                .filter(models.DataItem.created_at <= end)\
                .scalar()
    max_val = db.query(func.max(models.DataItem.value))\
                .filter(models.DataItem.created_at >= start)\
                .filter(models.DataItem.created_at <= end)\
                .scalar()
    return min_val, max_val


def get_series(db: Session, name: str | None = None, limit: int = 500):
    q = db.query(models.DataItem)
    if name:
        q = q.filter(models.DataItem.name == name)
    return q.order_by(models.DataItem.created_at.desc()).limit(limit).all()

def get_series_in_range(db: Session, start: datetime, end: datetime, name: str | None = None):
    q = db.query(models.DataItem).filter(
        models.DataItem.created_at >= start,
        models.DataItem.created_at <= end
    )
    if name:
        q = q.filter(models.DataItem.name == name)
    return q.order_by(models.DataItem.created_at.asc()).all()
