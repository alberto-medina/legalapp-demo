from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from database import get_connection


class AbogadoPanelScreen(Screen):

    def on_enter(self):
        # 🔒 Evita crash si el id no existe
        if "lista" not in self.ids:
            return

        # 🧹 Limpiar lista antes de cargar
        self.ids.lista.clear_widgets()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT user_email, abogado, estado FROM consultas")
        consultas = cursor.fetchall()

        conn.close()

        if consultas:
            for user_email, abogado, estado in consultas:
                item = Label(
                    text=f"[b]{user_email}[/b]\nAbogado: {abogado}\nEstado: {estado}",
                    markup=True,
                    size_hint_y=None,
                    height=90
                )
                self.ids.lista.add_widget(item)
        else:
            self.ids.lista.add_widget(
                Label(
                    text="Sin consultas",
                    size_hint_y=None,
                    height=50
                )
            )

    def volver(self):
        self.manager.current = "login"