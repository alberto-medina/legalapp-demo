from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from plyer import filechooser
from kivy.clock import Clock
from database import get_connection
import shutil
import os
import time
import session

UPLOAD_DIR = "assets/uploads"


class ChatScreen(Screen):

    def on_enter(self):
        self.cargar_mensajes()

    def cargar_mensajes(self):
        self.ids.chat_box.clear_widgets()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT emisor, mensaje, archivo
            FROM mensajes
            WHERE consulta_id = ?
        """, (session.current_consulta_id,))

        mensajes = cursor.fetchall()
        conn.close()

        for emisor, texto, archivo in mensajes:

            if texto:
                self.ids.chat_box.add_widget(
                    Label(
                        text=f"{emisor}: {texto}",
                        size_hint_y=None,
                        height=40
                    )
                )

            if archivo:
                btn = Button(
                    text=f"📎 {os.path.basename(archivo)}",
                    size_hint_y=None,
                    height=40
                )
                btn.bind(on_release=lambda x, path=archivo: self.abrir_archivo(path))
                self.ids.chat_box.add_widget(btn)

        Clock.schedule_once(lambda dt: self.scroll_abajo(), 0.1)

    def scroll_abajo(self):
        self.ids.chat_box.parent.scroll_y = 0

    def enviar(self):
        texto = self.ids.input_mensaje.text
        if not texto:
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO mensajes (consulta_id, emisor, mensaje)
            VALUES (?, ?, ?)
        """, (
            session.current_consulta_id,
            session.current_user[2],
            texto
        ))

        conn.commit()
        conn.close()

        self.ids.input_mensaje.text = ""
        self.cargar_mensajes()

    def adjuntar(self):
        filechooser.open_file(on_selection=self.seleccionar_archivo)

    def seleccionar_archivo(self, selection):
        if not selection:
            return

        origen = selection[0]

        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        nombre = f"{int(time.time())}_{os.path.basename(origen)}"
        destino = os.path.join(UPLOAD_DIR, nombre)

        shutil.copy(origen, destino)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO mensajes (consulta_id, emisor, archivo)
            VALUES (?, ?, ?)
        """, (
            session.current_consulta_id,
            session.current_user[2],
            destino
        ))

        conn.commit()
        conn.close()

        self.cargar_mensajes()

    def abrir_archivo(self, path):
        print("Abrir archivo:", path)

    def volver(self):
        if session.current_user[4] == "abogado":
            self.manager.current = "abogado_panel"
        else:
            self.manager.current = "historial"