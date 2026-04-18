from database import get_connection
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = get_connection()
cursor = conn.cursor()

# borrar si existe
cursor.execute("DELETE FROM users WHERE email=?", ("abogado@test.com",))

# crear de nuevo
cursor.execute(
    "INSERT INTO users (username, email, password, rol) VALUES (?, ?, ?, ?)",
    ("Dr Test", "abogado@test.com", hash_password("1234"), "abogado")
)

conn.commit()
conn.close()

print("Abogado creado correctamente")