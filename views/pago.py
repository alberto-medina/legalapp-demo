from kivy.uix.screenmanager import Screen
from database import get_connection

class PagoScreen(Screen):

    def pagar(self):
        app = self.manager

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO consultas (user_email, abogado, estado) VALUES (?, ?, ?)",
            ("demo@email.com", app.abogado_seleccionado, "pagado")
        )

        conn.commit()
        conn.close()

        self.manager.current = "chat"