from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from database import get_connection
import session


class AbogadoPanelScreen(Screen):

    def on_enter(self):
        self.ids.lista.clear_widgets()

        user = session.current_user
        if not user:
            return

        email_abogado = user[2]  # usamos EMAIL (más seguro)

        conn = get_connection()
        cursor = conn.cursor()

        # 🔥 IMPORTANTE: mostramos todas las consultas del sistema
        # (así no falla por nombres distintos)
        cursor.execute("""
            SELECT user_email, abogado, estado
            FROM consultas
        """)

        consultas = cursor.fetchall()
        conn.close()

        if not consultas:
            self.ids.lista.add_widget(
                Label(text="No hay consultas aún", size_hint_y=None, height=40)
            )
            return

        for c in consultas:
            cliente = c[0] or ""
            abogado = c[1] or ""
            estado = c[2] or ""

            texto = f"[b]{cliente}[/b]\nAbogado: {abogado}\nEstado: {estado}"

            self.ids.lista.add_widget(
                Label(
                    text=texto,
                    markup=True,
                    size_hint_y=None,
                    height=90
                )
            )

    def volver(self):
        self.manager.current = "login"