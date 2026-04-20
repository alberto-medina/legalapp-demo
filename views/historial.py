from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from database import get_connection
import session


class HistorialScreen(Screen):

    def on_enter(self):
        if "lista" not in self.ids:
            return

        self.ids.lista.clear_widgets()

        user = session.current_user
        if not user:
            return

        email = user[2]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT abogado, estado FROM consultas WHERE user_email=?",
            (email,)
        )

        consultas = cursor.fetchall()
        conn.close()

        if consultas:
            for abogado, estado in consultas:
                self.ids.lista.add_widget(
                    Label(text=f"{abogado} - {estado}")
                )
        else:
            self.ids.lista.add_widget(Label(text="Sin consultas"))

    def volver(self):
        self.manager.current = "dashboard"