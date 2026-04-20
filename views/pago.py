from kivy.uix.screenmanager import Screen
from database import get_connection
import session


class PagoScreen(Screen):

    abogado = ""

    def pagar(self):
        user = session.current_user

        if not user:
            return

        user_email = user[2]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO consultas (user_email, abogado, estado) VALUES (?, ?, ?)",
            (user_email, self.abogado, "pagado")
        )

        conn.commit()
        conn.close()

        self.manager.current = "chat"

    def volver(self):
        self.manager.current = "abogados"