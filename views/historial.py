from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from database import get_connection
import session


class HistorialScreen(Screen):

    def on_enter(self):
        self.ids.lista.clear_widgets()

        user = session.current_user
        if not user:
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT abogado, estado
            FROM consultas
            WHERE user_email=?
        """, (user[2],))

        consultas = cursor.fetchall()
        conn.close()

        if not consultas:
            self.ids.lista.add_widget(
                Label(text="Sin consultas", size_hint_y=None, height=40)
            )
            return

        for c in consultas:
            texto = f"Abogado: {c[0]}\nEstado: {c[1]}"

            self.ids.lista.add_widget(
                Label(text=texto, size_hint_y=None, height=60)
            )

    def volver(self):
        self.manager.current = "dashboard"
