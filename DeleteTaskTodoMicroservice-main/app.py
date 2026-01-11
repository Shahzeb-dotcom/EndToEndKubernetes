import pyodbc
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

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
# DELETE TASK BY ID
# ============================
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Tasks WHERE ID = ?", task_id)
    conn.commit()

    return {"message": f"Task {task_id} deleted successfully"}
