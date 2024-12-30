from typing import Optional
from dotenv import load_dotenv
import psycopg2
import os

from fastapi import FastAPI

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

app = FastAPI()


def query_db(query):
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
    )
    with conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
    return rows


@app.get("/rivers")
def get_rivers():
    rows = query_db("SELECT * FROM rivers")
    return [{"id": row[0], "name": row[1]} for row in rows]


@app.get("/devices_in_river/{river_id}")
def get_devices_in_river(river_id: int):
    rows = query_db(f"SELECT device_id FROM devices WHERE river_id = {river_id}")
    return [{"device_id": row[0]} for row in rows]


@app.get("/device_readings/{river_id}_{device_id}")
def get_device_readings(river_id: int, device_id: int):
    rows = query_db(f"SELECT * FROM device_measurements WHERE river_id = {river_id} and device_id = {device_id}")
    return [
        {
            "timestamp": row[2],
            "water_level": row[3],
            "tds": row[4],
            "turbidity": row[5],
            "ph": row[6],
            "temperature": row[7],
        }
        for row in rows
    ]
