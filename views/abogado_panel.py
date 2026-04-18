from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from database import get_connection


class AbogadoPanelScreen(Screen):

    def on_enter(self):
        self.ids.lista.clear_widgets()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT user_email, estado FROM consultas")
        data = cursor.fetchall()

        conn.close()

        if data:
            for user, estado in data:
                self.ids.lista.add_widget(
                    Label(
                        text=f"{user} - {estado}",
                        size_hint_y=None,
                        height=40
                    )
                )
        else:
            self.ids.lista.add_widget(
                Label(text="No hay consultas", size_hint_y=None, height=40)
            )