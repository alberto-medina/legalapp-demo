import sqlite3

def get_connection():
    return sqlite3.connect("legal_app.db")


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT UNIQUE,
        password TEXT,
        rol TEXT,
        telefono TEXT,
        foto TEXT,
        especialidad TEXT,
        descripcion TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consultas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        abogado TEXT,
        estado TEXT
    )
    """)

    conn.commit()
    conn.close()


def update_schema():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN especialidad TEXT")
    except:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN descripcion TEXT")
    except:
        pass

    conn.commit()
    conn.close()


create_tables()
update_schema()