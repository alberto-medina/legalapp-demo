from kivy.uix.screenmanager import Screen
from database import get_connection
import session


class PagoScreen(Screen):

    def pagar(self):
        conn = get_connection()
        cursor = conn.cursor()

        abogado = (session.abogado_seleccionado or "").strip()

        print("ABOGADO GUARDADO:", abogado)

        cursor.execute("""
            INSERT INTO consultas (user_email, abogado, estado)
            VALUES (?, ?, ?)
        """, (
            session.current_user[2],
            abogado,
            "pagado"
        ))

        consulta_id = cursor.lastrowid
        session.consulta_id = consulta_id

        conn.commit()
        conn.close()

        print("PAGO OK - CONSULTA ID:", consulta_id)

        self.manager.current = "chat"