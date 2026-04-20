from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from database import get_connection
import session


class AbogadosScreen(Screen):

    def on_enter(self):
        self.ids.lista.clear_widgets()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT username FROM users WHERE rol='abogado'")
        abogados = cursor.fetchall()

        conn.close()

        for ab in abogados:
            nombre = ab[0]

            btn = Button(
                text=nombre,
                size_hint_y=None,
                height=50
            )

            btn.bind(on_release=lambda x, n=nombre: self.seleccionar(n))

            self.ids.lista.add_widget(btn)

    def seleccionar(self, abogado):
        session.abogado = abogado
        self.manager.current = "pago"

    def volver(self):
        self.manager.current = "especialidad"