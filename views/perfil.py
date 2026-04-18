from kivy.uix.screenmanager import Screen
from database import get_connection


class PerfilScreen(Screen):

    def on_enter(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT username, email, telefono FROM users LIMIT 1")
        user = cursor.fetchone()

        conn.close()

        if user:
            self.ids.nombre.text = user[0] or ""
            self.ids.email.text = user[1] or ""
            self.ids.telefono.text = user[2] or ""

    def volver(self):
        self.manager.current = "dashboard"