import sqlite3
import os

# 🔥 RUTA FIJA Y ÚNICA
DB_PATH = os.path.join(os.path.dirname(__file__), "legal_app.db")
print("USANDO DB EN:", DB_PATH)

def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # 👤 USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT UNIQUE,
        password TEXT,
        rol TEXT,
        telefono TEXT,
        foto TEXT,
        matricula TEXT,
        experiencia TEXT,
        descripcion TEXT
    )
    """)

    # 📄 CONSULTAS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consultas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        abogado TEXT,
        estado TEXT,
        tipo_servicio TEXT,
        fecha TEXT
    )
    """)

    # 💬 MENSAJES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mensajes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        consulta_id INTEGER,
        emisor TEXT,
        mensaje TEXT,
        archivo TEXT
    )
    """)

    conn.commit()
    conn.close()


def actualizar_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(mensajes)")
    columnas = [col[1] for col in cursor.fetchall()]

    if "archivo" not in columnas:
        cursor.execute("ALTER TABLE mensajes ADD COLUMN archivo TEXT")

    conn.commit()
    conn.close()


create_tables()
actualizar_db()