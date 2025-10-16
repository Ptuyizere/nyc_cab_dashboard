import uvicorn
import sqlite3
from typing import List
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from data.models import TripDetail, StatsSummary
from fastapi.middleware.cors import CORSMiddleware

# Database
DB_PATH = Path("data/data.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

app = FastAPI(
    title="NYC Yellow Cab API (2016)",
    description="An API that exposes the NYC Yellow Cab data from 2016",
    version="1.0.0"
)

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/trips/", response_model=List[TripDetail])
def list_paged_trips(limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
    """Returns a pages of trips."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trips ORDER BY numeric_id LIMIT ? OFFSET ?", (limit, offset))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        raise HTTPException(404,"No trips found")
    else:
        detailed_trips_list = []
        for row in rows:
            row_dict = dict(row)
            trip_object = TripDetail(**row_dict)
            detailed_trips_list.append(trip_object)
        return detailed_trips_list

@app.get("/trip/{trip_id}", response_model=TripDetail)
def get_trip(trip_id: str):
    """Returns details of a trip given the trip's numeric id"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trips WHERE numeric_id = ?", (trip_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(404,"Trip not found")
    return TripDetail(**dict(row))

@app.get("/stats", response_model=StatsSummary)
def get_summary_stats():
    """Returns summary of statistics for the dataset"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) AS total_trips,
        AVG(speed_kmph) AS avg_speed_kmph,
        AVG(trip_duration) AS avg_duration_s
        FROM trips
        WHERE trip_distance_km > 0
    """)
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=500, detail="No data available")
    return StatsSummary(**dict(row))

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)