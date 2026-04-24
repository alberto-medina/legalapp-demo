from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from database import get_connection
import session


class HistorialScreen(Screen):

    def on_enter(self):
        self.cargar_historial()

    def cargar_historial(self):
        self.ids.lista.clear_widgets()

        if not session.current_user:
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, abogado, estado
            FROM consultas
            WHERE user_email=?
            ORDER BY id DESC
        """, (session.current_user[2],))

        consultas = cursor.fetchall()
        conn.close()

        if not consultas:
            self.ids.lista.add_widget(
                Label(text="Sin consultas", size_hint_y=None, height=40)
            )
            return

        for consulta_id, abogado, estado in consultas:

            box = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=120,
                spacing=5
            )

            box.add_widget(Label(text=f"Abogado: {abogado}"))
            box.add_widget(Label(text=f"Estado: {estado}"))

            btn = Button(text="Abrir Chat", size_hint_y=None, height=40)
            btn.bind(on_release=lambda x, cid=consulta_id: self.abrir_chat(cid))

            box.add_widget(btn)

            self.ids.lista.add_widget(box)

    def abrir_chat(self, consulta_id):
        print("CLIENTE ABRE CHAT:", consulta_id)

        session.current_consulta_id = consulta_id
        self.manager.current = "chat"

    def volver(self):
        self.manager.current = "dashboard"