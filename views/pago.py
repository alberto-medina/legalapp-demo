import sqlite3
import session
from kivy.uix.screenmanager import Screen


class PagoScreen(Screen):

    def pagar(self, tipo):
        conn = sqlite3.connect("legal_app.db")
        cursor = conn.cursor()

        user = session.current_user
        abogado = session.abogado_seleccionado

        precio = 1000
        if tipo == "video":
            precio = 3000
        elif tipo == "urgente":
            precio = 5000

        cursor.execute("""
            INSERT INTO consultas (user_email, abogado, estado, tipo_servicio)
            VALUES (?, ?, ?, ?)
        """, (user[2], abogado, "pagado", tipo))

        consulta_id = cursor.lastrowid
        session.current_consulta_id = consulta_id

        conn.commit()
        conn.close()

        print("PAGO OK - CONSULTA ID:", consulta_id)

        self.manager.current = "chat"