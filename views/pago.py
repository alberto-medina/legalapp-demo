import sqlite3
import session
from kivy.uix.screenmanager import Screen
from database import get_connection


class PagoScreen(Screen):

    def on_enter(self):
        self.cargar_resumen()

    def cargar_resumen(self):
        # 🔹 Especialidad
        area = getattr(session, "area_legal", "-")
        self.ids.lbl_area.text = area

        # 🔹 Tipo de servicio
        tipo = session.tipo_servicio or "-"
        texto_tipo = tipo.capitalize() if tipo else "-"
        self.ids.lbl_tipo.text = texto_tipo

        # 🔹 Precio
        precio = 1000
        if tipo == "video":
            precio = 3000
        elif tipo == "urgente":
            precio = 5000

        self.ids.lbl_precio.text = f"${precio}"

        # 🔹 Abogado (nombre desde DB)
        abogado_email = session.abogado_seleccionado

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT username FROM users WHERE email=?", (abogado_email,))
        result = cursor.fetchone()

        conn.close()

        if result:
            self.ids.lbl_abogado.text = result[0]
        else:
            self.ids.lbl_abogado.text = abogado_email or "-"

    def pagar(self):
        conn = get_connection()
        cursor = conn.cursor()

        user = session.current_user
        abogado = session.abogado_seleccionado
        tipo = session.tipo_servicio

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