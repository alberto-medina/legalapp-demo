from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT id, username, email FROM users")
rows = cursor.fetchall()

conn.close()

print("USUARIOS EN DB:")
for r in rows:
    print(r)