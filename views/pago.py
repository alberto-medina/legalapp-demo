from kivy.uix.screenmanager import Screen
from database import get_connection
import session


class PagoScreen(Screen):

    def on_enter(self):
        servicio = getattr(session, "tipo_servicio", "")

        if servicio == "chat":
            precio = 1000
        elif servicio == "video":
            precio = 3000
        elif servicio == "urgente":
            precio = 5000
        else:
            precio = 0

        self.ids.precio.text = f"Total a pagar: ${precio}"

    def pagar(self):
        user = session.current_user
        abogado = getattr(session, "abogado", "")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO consultas (user_email, abogado, estado)
            VALUES (?, ?, ?)
        """, (
            user[2],
            abogado,
            "pagado"
        ))

        conn.commit()
        conn.close()

        print("Pago registrado")

        self.manager.current = "chat"

    def volver(self):
        self.manager.current = "abogados"