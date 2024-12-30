from dotenv import load_dotenv
from datetime import datetime
from psycopg2.pool import SimpleConnectionPool
import os

from fastapi import FastAPI, HTTPException

load_dotenv()

app = FastAPI()

pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
)


def query_db(query, params=None):
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
        return rows
    finally:
        pool.putconn(conn)


@app.get("/rivers")
def get_rivers():
    rows = query_db("SELECT * FROM rivers")
    return [{"id": row[0], "name": row[1]} for row in rows]


@app.get("/devices_in_river/{river_id}")
def get_devices_in_river(river_id: int):
    rows = query_db(f"SELECT device_id FROM devices WHERE river_id = %s", (river_id,))
    return [{"device_id": row[0]} for row in rows]


@app.get("/device_readings/{river_id}_{device_id}")
def get_device_readings(
    river_id: int,
    device_id: int,
    column: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
):
    sensor_columns = ["water_level", "tds", "turbidity", "ph", "temperature"]
    if column:
        if column not in sensor_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid column. Choose one of {sensor_columns}",
            )
        select_columns = ["recorded_at", column]
    else:
        select_columns = ["recorded_at", *sensor_columns]
    query = f"SELECT {', '.join(select_columns)} FROM device_measurements WHERE river_id = %s AND device_id = %s"
    params = (river_id, device_id)
    if start:
        query += " AND recorded_at > %s"
        params += (start,)
    if end:
        query += " AND recorded_at < %s"
        params += (end,)
    rows = query_db(query, params)
    return [{col: row[idx] for idx, col in enumerate(select_columns)} for row in rows]
