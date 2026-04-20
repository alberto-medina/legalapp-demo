from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    """
    UPDATE users 
    SET password=?, rol=? 
    WHERE email=?
    """,
    ("1234", "abogado", "abogado@test.com")
)

conn.commit()
conn.close()

print("Abogado corregido correctamente")