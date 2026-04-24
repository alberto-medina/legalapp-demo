from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
import sqlite3
import session


class AbogadoPanelScreen(Screen):

    def on_enter(self):
        self.cargar_datos()

    def cargar_datos(self):
        self.ids.lista_consultas.clear_widgets()

        user = session.current_user
        if not user:
            return

        email_abogado = user[2]

        conn = sqlite3.connect("legal_app.db")
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM consultas WHERE abogado = ?", (email_abogado,))
        total = cursor.fetchone()[0]

        ganancia = total * 1000

        self.ids.lbl_consultas.text = str(total)
        self.ids.lbl_ganancia.text = f"${ganancia}"

        cursor.execute("""
            SELECT id, user_email, estado
            FROM consultas
            WHERE abogado = ?
            ORDER BY id DESC
        """, (email_abogado,))

        consultas = cursor.fetchall()
        conn.close()

        if not consultas:
            from kivy.uix.label import Label
            self.ids.lista_consultas.add_widget(Label(text="No hay consultas"))
            return

        for consulta_id, cliente, estado in consultas:

            btn = Button(
                text=f"{cliente}\nEstado: {estado}",
                size_hint_y=None,
                height=100
            )

            btn.bind(on_release=lambda x, cid=consulta_id: self.abrir_chat(cid))

            self.ids.lista_consultas.add_widget(btn)

    def abrir_chat(self, consulta_id):
        print("ABOGADO ABRE CHAT:", consulta_id)

        session.current_consulta_id = consulta_id
        self.manager.current = "chat"

    def ir_perfil(self):
        self.manager.current = "perfil"

    def logout(self):
        session.current_user = None
        self.manager.current = "login"