from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from database import get_connection
import session

ESTADOS = ["disponible", "guardia", "ocupado"]
ESTADO_CFG = {
    "disponible": {"label": "  DISPONIBLE  ", "bg": (0.10, 0.55, 0.25, 1), "text": (1, 1, 1, 1)},
    "guardia":    {"label": "  EN GUARDIA  ", "bg": (0.65, 0.50, 0.00, 1), "text": (1, 1, 1, 1)},
    "ocupado":    {"label": "  OCUPADO     ", "bg": (0.60, 0.10, 0.10, 1), "text": (1, 1, 1, 1)},
}
TIPO_COLOR = {
    "chat":    (0.10, 0.45, 0.85, 1),
    "video":   (0.10, 0.60, 0.40, 1),
    "urgente": (0.75, 0.18, 0.18, 1),
}


class AbogadoPanelScreen(Screen):

    def on_enter(self):
        user = session.current_user
        if user:
            self.ids.lbl_nombre_abogado.text = user[1] or user[2]
        self.cargar_datos()
        self._actualizar_btn_estado()

    def _get_estado_actual(self):
        user = session.current_user
        if not user:
            return "disponible"
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT estado_abogado FROM users WHERE email=?", (user[2],))
        row = c.fetchone()
        conn.close()
        est = row[0] if row and row[0] else "disponible"
        return est if est in ESTADOS else "disponible"

    def _actualizar_btn_estado(self):
        estado = self._get_estado_actual()
        cfg = ESTADO_CFG[estado]
        self.ids.btn_estado.text             = cfg["label"]
        self.ids.btn_estado.background_color = cfg["bg"]
        self.ids.btn_estado.color            = cfg["text"]

    def cambiar_estado(self):
        user = session.current_user
        if not user:
            return
        actual = self._get_estado_actual()
        nuevo  = ESTADOS[(ESTADOS.index(actual) + 1) % len(ESTADOS)]
        conn = get_connection()
        c = conn.cursor()
        c.execute("UPDATE users SET estado_abogado=? WHERE email=?", (nuevo, user[2]))
        conn.commit()
        conn.close()
        self._actualizar_btn_estado()

    def cargar_datos(self):
        self.ids.lista_consultas.clear_widgets()
        user = session.current_user
        if not user:
            return
        email = user[2]
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM consultas WHERE abogado=?", (email,))
        total = c.fetchone()[0]
        self.ids.lbl_consultas.text  = str(total)
        self.ids.lbl_honorarios.text = f"${total * 1000:,}"

        c.execute("""
            SELECT id, user_email, estado, tipo_servicio
            FROM consultas WHERE abogado=? ORDER BY id DESC
        """, (email,))
        consultas = c.fetchall()
        conn.close()

        if not consultas:
            self.ids.lista_consultas.add_widget(Label(
                text="No hay consultas aun",
                color=(0.50, 0.55, 0.65, 1),
                size_hint_y=None, height=60,
            ))
            return

        for cid, cliente, estado, tipo in consultas:
            card = BoxLayout(
                orientation="horizontal",
                size_hint_y=None, height=76,
                spacing=10, padding=[14, 10],
            )
            with card.canvas.before:
                Color(rgba=(1, 1, 1, 1))
                card._bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[12])
            card.bind(
                pos=lambda w, v: setattr(w._bg, 'pos', v),
                size=lambda w, v: setattr(w._bg, 'size', v),
            )

            tipo_lbl = Label(
                text=(tipo or "?").upper(),
                size_hint_x=None, width=58,
                bold=True, font_size=11,
                color=TIPO_COLOR.get(tipo, (0.5, 0.5, 0.5, 1)),
            )

            info = BoxLayout(orientation="vertical")
            info.add_widget(Label(
                text=cliente, font_size=13, bold=True,
                color=(0.08, 0.12, 0.28, 1),
                halign="left", text_size=(None, None),
            ))
            estado_color = (0.10, 0.55, 0.28, 1) if estado == "finalizado" else (0.75, 0.55, 0.05, 1)
            info.add_widget(Label(
                text=estado.upper(), font_size=11,
                color=estado_color,
                halign="left", text_size=(None, None),
            ))

            btn = Button(
                text="Abrir", size_hint_x=None, width=64,
                bold=True, font_size=12,
                background_color=(0.00, 0.04, 0.22, 1),
                color=(1, 1, 1, 1),
            )
            btn.bind(on_release=lambda x, c=cid: self.abrir_chat(c))

            card.add_widget(tipo_lbl)
            card.add_widget(info)
            card.add_widget(btn)
            self.ids.lista_consultas.add_widget(card)

    def abrir_chat(self, consulta_id):
        session.current_consulta_id = consulta_id
        self.manager.current = "chat"

    def ir_perfil(self):
        self.manager.current = "perfil"

    def logout(self):
        session.current_user = None
        self.manager.current = "login"
