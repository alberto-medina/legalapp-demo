from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    "UPDATE users SET password=? WHERE email=?",
    ("1234", "cliente@test.com")
)

conn.commit()
conn.close()

print("Password actualizada correctamente")