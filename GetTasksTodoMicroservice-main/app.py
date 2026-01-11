import pyodbc
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# DB connection
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

connection_string = (
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server=tcp:{DB_HOST},1433;"
    f"Database={DB_NAME};"
    f"Uid={DB_USER};"
    f"Pwd={DB_PASSWORD};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}


# ============================
# GET ALL TASKS
# ============================
@app.get("/tasks")
def get_tasks():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("SELECT ID, Title, Description FROM Tasks")
    rows = cursor.fetchall()

    tasks = []
    for r in rows:
        tasks.append({
            "ID": r.ID,
            "Title": r.Title,
            "Description": r.Description
        })
    return tasks
