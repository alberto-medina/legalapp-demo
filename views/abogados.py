from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from database import get_connection
import session


class AbogadosScreen(Screen):

    def on_enter(self):
        self.ids.lista.clear_widgets()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT username, email
            FROM users
            WHERE rol='abogado'
        """)

        abogados = cursor.fetchall()
        conn.close()

        for nombre, email in abogados:
            btn = Button(
                text=f"{nombre}",
                size_hint_y=None,
                height=50
            )

            btn.bind(on_release=lambda x, e=email: self.seleccionar(e))
            self.ids.lista.add_widget(btn)

    def seleccionar(self, email):
        print("ABOGADO SELECCIONADO:", email)

        session.abogado_seleccionado = email
        self.manager.current = "pago"