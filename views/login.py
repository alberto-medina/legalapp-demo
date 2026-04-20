from kivy.uix.screenmanager import Screen
from database import get_connection
import session


class LoginScreen(Screen):

    def login(self):
        email = self.ids.email.text
        password = self.ids.password.text

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, username, email, rol FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session.current_user = user

            # 🔥 REDIRECCIÓN POR ROL
            if user[3] == "abogado":
                self.manager.current = "abogado_panel"
            else:
                self.manager.current = "dashboard"
        else:
            print("Login incorrecto")