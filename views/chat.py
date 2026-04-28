from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from database import get_connection
import session
import os, time, shutil

try:
    from plyer import filechooser
    PLYER_OK = True
except Exception:
    PLYER_OK = False

UPLOAD_DIR = "assets/uploads"


class ChatScreen(Screen):

    def on_enter(self):
        self._setup_ui()
        self.cargar_mensajes()

    def _get_estado_consulta(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT estado, abogado, user_email, tipo_servicio FROM consultas WHERE id=?",
                  (session.current_consulta_id,))
        row = c.fetchone()
        conn.close()
        return row

    def _setup_ui(self):
        row = self._get_estado_consulta()
        if not row:
            return
        estado, abogado, cliente, tipo = row
        es_abogado = session.current_user and session.current_user[4] == "abogado"

        # FIX: leer estado FRESCO de la DB cada vez
        finalizado = (estado == "finalizado")

        if es_abogado:
            interlocutor = cliente
            estado_linea = "Cliente"
            color_linea  = (0.85, 0.62, 0.05, 1)
        else:
            interlocutor = abogado
            conn = get_connection()
            c = conn.cursor()
            c.execute("SELECT estado_abogado FROM users WHERE email=?", (abogado,))
            ab_row = c.fetchone()
            conn.close()
            ab_est = (ab_row[0] if ab_row and ab_row[0] else "disponible")
            if ab_est == "disponible":
                estado_linea = "En linea"
                color_linea  = (0.10, 0.72, 0.38, 1)
            elif ab_est == "guardia":
                estado_linea = "En guardia"
                color_linea  = (0.85, 0.62, 0.05, 1)
            else:
                estado_linea = "Ocupado"
                color_linea  = (0.80, 0.22, 0.22, 1)

        self.ids.lbl_chat_titulo.text  = interlocutor
        self.ids.lbl_chat_tipo.text    = f"Consulta {tipo or ''}"
        self.ids.lbl_estado_linea.text  = estado_linea
        self.ids.lbl_estado_linea.color = color_linea

        # Boton finalizar: SOLO abogado Y no finalizado aun
        if es_abogado and not finalizado:
            self.ids.btn_finalizar.opacity  = 1
            self.ids.btn_finalizar.disabled = False
        else:
            self.ids.btn_finalizar.opacity  = 0
            self.ids.btn_finalizar.disabled = True

        # Banner: SOLO si la DB dice finalizado
        if finalizado:
            self.ids.banner_finalizado.height   = 36
            self.ids.lbl_banner_fin.text        = "Esta consulta fue finalizada"
            self.ids.input_area.opacity         = 0.4
            self.ids.input_area.disabled        = True
        else:
            self.ids.banner_finalizado.height   = 0
            self.ids.lbl_banner_fin.text        = ""
            self.ids.input_area.opacity         = 1
            self.ids.input_area.disabled        = False

    def cargar_mensajes(self):
        self.ids.chat_box.clear_widgets()
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT emisor, mensaje, archivo FROM mensajes WHERE consulta_id=?",
                  (session.current_consulta_id,))
        mensajes = c.fetchall()
        conn.close()

        mi_email = session.current_user[2] if session.current_user else ""

        for emisor, texto, archivo in mensajes:
            if emisor == "SISTEMA":
                self.ids.chat_box.add_widget(Label(
                    text=texto, font_size=11, italic=True,
                    color=(0.50, 0.55, 0.65, 1),
                    size_hint_y=None, height=28,
                    halign="center", text_size=(None, None),
                ))
                continue

            es_mio = (emisor == mi_email)
            if texto:
                bubble = BoxLayout(size_hint_y=None, height=42, padding=[10, 4])
                bg = (0.00, 0.04, 0.22, 1) if es_mio else (1, 1, 1, 1)
                with bubble.canvas.before:
                    Color(rgba=bg)
                    bubble._bg = RoundedRectangle(pos=bubble.pos, size=bubble.size, radius=[12])
                bubble.bind(
                    pos=lambda w, v: setattr(w._bg, 'pos', v),
                    size=lambda w, v: setattr(w._bg, 'size', v),
                )
                bubble.add_widget(Label(
                    text=texto, font_size=13,
                    color=(1, 1, 1, 1) if es_mio else (0.10, 0.14, 0.28, 1),
                    halign="right" if es_mio else "left",
                    text_size=(None, None),
                ))
                wrapper = BoxLayout(size_hint_y=None, height=48)
                if es_mio:
                    wrapper.add_widget(BoxLayout())
                wrapper.add_widget(bubble)
                if not es_mio:
                    wrapper.add_widget(BoxLayout())
                self.ids.chat_box.add_widget(wrapper)

            if archivo:
                btn = Button(
                    text=f"Adjunto: {os.path.basename(archivo)}",
                    size_hint_y=None, height=40,
                    background_color=(0.88, 0.90, 0.93, 1),
                    color=(0.10, 0.14, 0.28, 1), font_size=12,
                )
                btn.bind(on_release=lambda x, p=archivo: self.abrir_archivo(p))
                self.ids.chat_box.add_widget(btn)

        Clock.schedule_once(lambda dt: self.scroll_abajo(), 0.1)

    def scroll_abajo(self):
        self.ids.scroll_chat.scroll_y = 0

    def enviar(self):
        texto = self.ids.input_mensaje.text.strip()
        if not texto:
            return
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO mensajes (consulta_id, emisor, mensaje) VALUES (?,?,?)",
                  (session.current_consulta_id, session.current_user[2], texto))
        conn.commit()
        conn.close()
        self.ids.input_mensaje.text = ""
        self.cargar_mensajes()

    def adjuntar(self):
        if PLYER_OK:
            try:
                filechooser.open_file(on_selection=self.seleccionar_archivo)
                return
            except Exception:
                pass
        # fallback tkinter
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk(); root.withdraw()
            path = filedialog.askopenfilename()
            root.destroy()
            if path:
                self.seleccionar_archivo([path])
        except Exception as e:
            print("adjuntar error:", e)

    def seleccionar_archivo(self, selection):
        if not selection:
            return
        origen = selection[0]
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        nombre  = f"{int(time.time())}_{os.path.basename(origen)}"
        destino = os.path.join(UPLOAD_DIR, nombre)
        shutil.copy(origen, destino)
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO mensajes (consulta_id, emisor, archivo) VALUES (?,?,?)",
                  (session.current_consulta_id, session.current_user[2], destino))
        conn.commit()
        conn.close()
        self.cargar_mensajes()

    def abrir_archivo(self, path):
        print("Abrir:", path)

    def finalizar_consulta(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("UPDATE consultas SET estado='finalizado' WHERE id=?",
                  (session.current_consulta_id,))
        c.execute("INSERT INTO mensajes (consulta_id, emisor, mensaje) VALUES (?,?,?)",
                  (session.current_consulta_id, "SISTEMA",
                   "El abogado finalizo esta consulta."))
        conn.commit()
        conn.close()
        print("FINALIZADO:", session.current_consulta_id)
        self._setup_ui()
        self.cargar_mensajes()

    def volver(self):
        if session.current_user and session.current_user[4] == "abogado":
            self.manager.current = "abogado_panel"
        else:
            row = self._get_estado_consulta()
            if row and row[0] == "finalizado":
                conn = get_connection()
                c = conn.cursor()
                c.execute("SELECT id FROM resenas WHERE consulta_id=?",
                          (session.current_consulta_id,))
                tiene = c.fetchone()
                conn.close()
                if not tiene:
                    self.manager.current = "resena"
                    return
            self.manager.current = "historial"
