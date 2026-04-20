from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from database import get_connection
import session


class AbogadoPanelScreen(Screen):

    def on_enter(self):
        self.cargar_consultas()

    def cargar_consultas(self):
        self.ids.lista.clear_widgets()

        if not session.current_user:
            return

        try:
            abogado_nombre = session.current_user[1]
        except:
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, user_email, abogado, estado
            FROM consultas
            WHERE abogado=?
        """, (abogado_nombre,))

        consultas = cursor.fetchall()
        conn.close()

        if not consultas:
            self.ids.lista.add_widget(
                Label(text="No hay consultas aún", size_hint_y=None, height=40)
            )
            return

        for c in consultas:
            consulta_id = c[0]
            cliente = c[1]
            estado = c[3]

            box = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=120,
                spacing=5
            )

            box.add_widget(Label(text=f"Cliente: {cliente}"))
            box.add_widget(Label(text=f"Estado: {estado}"))

            btn = Button(text="Abrir Chat", size_hint_y=None, height=40)
            btn.bind(on_release=lambda x, cid=consulta_id: self.abrir_chat(cid))

            box.add_widget(btn)

            self.ids.lista.add_widget(box)

    def abrir_chat(self, consulta_id):
        print("ABRIENDO CHAT:", consulta_id)

        session.consulta_id = consulta_id
        self.manager.current = "chat"

    def volver(self):
        self.manager.current = "login"