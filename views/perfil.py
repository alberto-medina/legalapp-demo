from kivy.uix.screenmanager import Screen
from database import get_connection
import session


class PerfilScreen(Screen):

    def on_enter(self):
        user = session.current_user

        if not user:
            return

        user_id = user[0]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT username, email, telefono FROM users WHERE id=?",
            (user_id,)
        )

        data = cursor.fetchone()
        conn.close()

        if not data:
            return

        if "nombre" in self.ids:
            self.ids.nombre.text = data[0] or ""

        if "email" in self.ids:
            self.ids.email.text = data[1] or ""

        if "telefono" in self.ids:
            self.ids.telefono.text = data[2] or ""

    def volver(self):
        self.manager.current = "dashboard"