from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from database import get_connection


class HistorialScreen(Screen):

    def on_enter(self):
        self.ids.lista.clear_widgets()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT abogado, estado FROM consultas")
        data = cursor.fetchall()

        conn.close()

        for abogado, estado in data:
            self.ids.lista.add_widget(Label(text=f"{abogado} - {estado}"))