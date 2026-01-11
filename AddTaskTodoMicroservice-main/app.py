import pyodbc
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

# ============================
#   DB CONNECTION STRING
# ============================
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

# Allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# HEALTH CHECK (K8s probes)
# ============================
@app.get("/health")
def health():
    return {"status": "ok"}


# ============================
# CREATE TABLE IF NOT EXISTS
# ============================
@app.on_event("startup")
def create_table():
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Tasks')
            CREATE TABLE Tasks (
                ID INT IDENTITY PRIMARY KEY,
                Title VARCHAR(255),
                Description TEXT
            );
        """)
        conn.commit()
    except Exception as e:
        print("Table creation error:", e)


# ============================
# MODEL
# ============================
class Task(BaseModel):
    title: str
    description: str


# ============================
# ADD NEW TASK
# ============================
@app.post("/tasks")
def create_task(task: Task):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Tasks (Title, Description) VALUES (?, ?)",
        task.title,
        task.description
    )
    conn.commit()
    return {"message": "Task added successfully", "task": task}
