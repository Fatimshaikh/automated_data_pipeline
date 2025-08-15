# app/routes/timeseries.py
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import io, csv
import pandas as pd
from ..database import get_db
from .. import crud

router = APIRouter(prefix="/timeseries", tags=["Time Series"])

@router.get("/series")
def series(
    name: str | None = Query(None, description="Optional series name, e.g., 'NYC Temperature (°C)'"),
    hours: int = Query(48, ge=1, le=100000),
    db: Session = Depends(get_db)
):
    end = datetime.utcnow()
    start = end - timedelta(hours=hours)
    rows = crud.get_series_in_range(db, start, end, name)
    return [
        {"t": r.created_at.isoformat(), "v": r.value, "name": r.name}
        for r in rows
    ]

@router.get("/export.csv")
def export_csv(
    name: str | None = Query(None),
    hours: int = Query(168),
    db: Session = Depends(get_db)
):
    end = datetime.utcnow()
    start = end - timedelta(hours=hours)
    rows = crud.get_series_in_range(db, start, end, name)

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["created_at", "name", "value"])
    for r in rows:
        writer.writerow([r.created_at.isoformat(), r.name, r.value])

    return Response(
        content=buf.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=timeseries.csv"}
    )

@router.get("/forecast")
def forecast(
    name: str | None = Query(None),
    hours: int = Query(48, ge=3),
    window: int = Query(12, ge=3, le=500),  # rolling mean window for forecast
    steps: int = Query(6, ge=1, le=48),     # predict next N steps
    db: Session = Depends(get_db)
):
    end = datetime.utcnow()
    start = end - timedelta(hours=hours)
    rows = crud.get_series_in_range(db, start, end, name)
    if len(rows) < window:
        return {"message": "Not enough data to forecast", "points": []}

    df = pd.DataFrame([{"t": r.created_at, "v": r.value} for r in rows]).set_index("t").sort_index()
    df["ma"] = df["v"].rolling(window=window, min_periods=1).mean()

    # naive forecast: repeat last rolling mean as flat forecast
    last_time = df.index[-1]
    last_ma = float(df["ma"].iloc[-1])
    # assume equal spacing; fallback to 60 minutes
    if len(df.index) >= 2:
        delta = df.index[-1] - df.index[-2]
        freq_mins = max(int(delta.total_seconds() // 60), 1)
    else:
        freq_mins = 60

    preds = []
    for i in range(1, steps + 1):
        preds.append({
            "t": (last_time + pd.Timedelta(minutes=freq_mins * i)).isoformat(),
            "pred": last_ma
        })
    return {"window": window, "steps": steps, "points": preds}

@router.get("/anomalies")
def anomalies(
    name: str | None = Query(None),
    hours: int = Query(48, ge=3),
    window: int = Query(12, ge=3, le=500),
    z_thresh: float = Query(2.0, ge=1.0, le=10.0),
    db: Session = Depends(get_db)
):
    end = datetime.utcnow()
    start = end - timedelta(hours=hours)
    rows = crud.get_series_in_range(db, start, end, name)
    if len(rows) < window:
        return {"message": "Not enough data to detect anomalies", "anomalies": []}

    df = pd.DataFrame([{"t": r.created_at, "v": r.value} for r in rows]).set_index("t").sort_index()
    df["mean"] = df["v"].rolling(window=window, min_periods=window).mean()
    df["std"] = df["v"].rolling(window=window, min_periods=window).std()
    df["z"] = (df["v"] - df["mean"]) / df["std"]
    out = df[df["z"].abs() >= z_thresh].dropna()
    anomalies = [{"t": idx.isoformat(), "v": float(row.v), "z": float(row.z)} for idx, row in out.iterrows()]
    return {"window": window, "z_thresh": z_thresh, "anomalies": anomalies}
