from kivy.uix.screenmanager import Screen
from database import get_connection
import session


class ChatScreen(Screen):

    def on_enter(self):
        print("CHAT ENTRA CON ID:", session.consulta_id)

        self.ids.chat_box.text = ""

        if not session.consulta_id:
            self.ids.chat_box.text = "Error: no hay consulta"
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT emisor, mensaje
            FROM mensajes
            WHERE consulta_id=?
        """, (session.consulta_id,))

        mensajes = cursor.fetchall()
        conn.close()

        for emisor, mensaje in mensajes:
            self.ids.chat_box.text += f"{emisor}: {mensaje}\n"

    def enviar(self):
        mensaje = self.ids.input.text

        if mensaje.strip() == "":
            return

        usuario = session.current_user[1]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO mensajes (consulta_id, emisor, mensaje)
            VALUES (?, ?, ?)
        """, (session.consulta_id, usuario, mensaje))

        conn.commit()
        conn.close()

        self.ids.input.text = ""
        self.on_enter()

    def volver(self):
        if session.current_user and session.current_user[4] == "abogado":
            self.manager.current = "abogado_panel"
        else:
            self.manager.current = "historial"