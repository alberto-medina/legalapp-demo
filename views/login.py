from kivy.uix.screenmanager import Screen
from database import get_connection
import session


class LoginScreen(Screen):

    def login(self):
        email = self.ids.email.text
        password = self.ids.password.text

        conn = get_connection()
        cursor = conn.cursor()

        # 🔥 TRAEMOS TODAS LAS COLUMNAS (CLAVE)
        cursor.execute("""
            SELECT id, username, email, password, rol, telefono, foto
            FROM users
            WHERE email=? AND password=?
        """, (email, password))

        user = cursor.fetchone()
        conn.close()

        if user:
            session.current_user = user
            print("LOGIN OK:", user)

            # 🔥 REDIRECCIÓN SEGÚN ROL
            try:
                if user[4] == "abogado":
                    self.manager.current = "abogado_panel"
                else:
                    self.manager.current = "dashboard"
            except:
                self.manager.current = "dashboard"

        else:
            print("Login incorrecto")