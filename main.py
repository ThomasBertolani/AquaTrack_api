import os
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.pool import SimpleConnectionPool

from utils import *

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
)

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


def rows_to_json(rows, columns):
    return [{col: row[idx] for idx, col in enumerate(columns)} for row in rows]


@app.get("/rivers")
def get_rivers():
    rows = query_db(f"SELECT {', '.join(RIVERS_OUT_COLS)} FROM rivers")
    return rows_to_json(rows, RIVERS_OUT_COLS)


@app.get("/devices_in_river/{river_id}")
def get_devices_in_river(river_id: int):
    rows = query_db(
        f"SELECT {', '.join(DEVICES_OUT_COLS)} FROM devices WHERE river_id = %s",
        (river_id,),
    )
    return rows_to_json(rows, DEVICES_OUT_COLS)


@app.get("/device_readings/{river_id}_{device_id}")
def get_device_readings(
    river_id: int,
    device_id: int,
    sensor: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
):
    if sensor:
        if sensor not in SENSOR_COLUMNS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid sensor. Choose one of {SENSOR_COLUMNS}",
            )
        select_columns = ["recorded_at", sensor]
    else:
        select_columns = ["recorded_at", *SENSOR_COLUMNS]
    query = f"SELECT {', '.join(select_columns)} FROM device_measurements WHERE river_id = %s AND device_id = %s"
    params = (river_id, device_id)
    if start:
        query += " AND recorded_at >= %s"
        params += (start,)
    if end:
        query += " AND recorded_at <= %s"
        params += (end,)
    rows = query_db(query, params)
    return rows_to_json(rows, select_columns)
