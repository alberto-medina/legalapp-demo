import hashlib
from database import get_connection


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, email, password, telefono):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password, rol, telefono, foto) VALUES (?, ?, ?, ?, ?, ?)",
            (username, email, hash_password(password), "cliente", telefono, "")
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password, rol FROM users WHERE email=?", (email,))
    result = cursor.fetchone()

    conn.close()

    if result and result[0] == hash_password(password):
        return result[1]

    return None