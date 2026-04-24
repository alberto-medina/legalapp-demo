from kivy.uix.screenmanager import Screen
from database import get_connection
import session
import hashlib


class LoginScreen(Screen):

    def login(self):
        email = self.ids.email.text.strip().lower()
        password = self.ids.password.text.strip()

        # 🔥 HASH DE PASSWORD
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        print("INTENTO LOGIN:", email, password)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users WHERE LOWER(email)=? AND password=?
        """, (email, password_hash))

        user = cursor.fetchone()
        conn.close()

        if user:
            session.current_user = user
            print("LOGIN OK:", user)

            if user[4] == "abogado":
                self.manager.current = "abogado_panel"
            else:
                self.manager.current = "dashboard"
        else:
            print("LOGIN ERROR - password incorrecta o usuario no existe")

    def go_register(self):
        self.manager.current = "register"