from typing import Optional
from dotenv import load_dotenv
import psycopg2
import os

from fastapi import FastAPI

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS= os.getenv("DB_PASS")

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
            results = cur.fetchall()
    return results

@app.get("/rivers")
def get_rivers():
    return query_db('SELECT * FROM rivers')