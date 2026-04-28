from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, RoundedRectangle
from database import get_connection
import session

ESTADOS_FILTRO = ["Todos", "pagado", "finalizado"]

TIPO_COLOR = {
    "chat":    (0.20, 0.50, 0.90, 1),
    "video":   (0.20, 0.65, 0.45, 1),
    "urgente": (0.80, 0.22, 0.22, 1),
}
ESTADO_COLOR = {
    "pagado":     (0.95, 0.75, 0.10, 1),
    "finalizado": (0.25, 0.80, 0.45, 1),
}


class HistorialScreen(Screen):

    _filtro = "Todos"

    def on_enter(self):
        self.ids.filtro_spinner.values = ESTADOS_FILTRO
        self.ids.filtro_spinner.text = self._filtro
        self.cargar_historial()

    def aplicar_filtro(self, valor):
        self._filtro = valor
        self.cargar_historial()

    def cargar_historial(self):
        self.ids.lista.clear_widgets()
        if not session.current_user:
            return

        conn = get_connection()
        c = conn.cursor()

        if self._filtro == "Todos":
            c.execute("""
                SELECT id, abogado, estado, tipo_servicio
                FROM consultas WHERE user_email=?
                ORDER BY id DESC
            """, (session.current_user[2],))
        else:
            c.execute("""
                SELECT id, abogado, estado, tipo_servicio
                FROM consultas WHERE user_email=? AND estado=?
                ORDER BY id DESC
            """, (session.current_user[2], self._filtro))

        consultas = c.fetchall()
        conn.close()

        if not consultas:
            self.ids.lista.add_widget(Label(
                text="No hay consultas en este filtro",
                color=(0.50, 0.55, 0.70, 1),
                size_hint_y=None, height=60,
            ))
            return

        for cid, abogado, estado, tipo in consultas:
            self._add_card(cid, abogado, estado or "pagado", tipo or "chat")

    def _add_card(self, cid, abogado, estado, tipo):
        card = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=80,
            spacing=10,
            padding=[12, 8],
        )
        with card.canvas.before:
            Color(rgba=(0.04, 0.06, 0.22, 1))
            card._bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[10])
        card.bind(
            pos=lambda w, v: setattr(w._bg, 'pos', v),
            size=lambda w, v: setattr(w._bg, 'size', v),
        )

        # Tipo badge izquierda
        tipo_lbl = Label(
            text=tipo.upper(),
            size_hint_x=None,
            width=62,
            font_size=11,
            bold=True,
            color=TIPO_COLOR.get(tipo, (0.7, 0.7, 0.7, 1)),
        )

        # Info centro
        info = BoxLayout(orientation="vertical")
        info.add_widget(Label(
            text=abogado,
            font_size=13,
            bold=True,
            color=(0.92, 0.94, 1.00, 1),
            halign="left",
            text_size=(None, None),
        ))
        info.add_widget(Label(
            text=estado.upper(),
            font_size=11,
            color=ESTADO_COLOR.get(estado, (0.70, 0.72, 0.85, 1)),
            halign="left",
            text_size=(None, None),
        ))

        # Botones derecha
        btns = BoxLayout(orientation="vertical", size_hint_x=None, width=72, spacing=4)

        btn_chat = Button(
            text="Chat",
            font_size=12,
            bold=True,
            background_color=(0.99, 0.84, 0.00, 1),
            color=(0.00, 0.02, 0.12, 1),
        )
        btn_chat.bind(on_release=lambda x, c=cid: self.abrir_chat(c))
        btns.add_widget(btn_chat)

        # Boton Resena solo si finalizado y sin resena
        if estado == "finalizado":
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id FROM resenas WHERE consulta_id=?", (cid,))
            tiene = cur.fetchone()
            conn.close()
            if not tiene:
                btn_resena = Button(
                    text="Resena",
                    font_size=11,
                    background_color=(0.20, 0.55, 0.35, 1),
                    color=(1, 1, 1, 1),
                )
                btn_resena.bind(on_release=lambda x, c=cid: self.ir_resena(c))
                btns.add_widget(btn_resena)

        card.add_widget(tipo_lbl)
        card.add_widget(info)
        card.add_widget(btns)
        self.ids.lista.add_widget(card)

    def abrir_chat(self, cid):
        session.current_consulta_id = cid
        self.manager.current = "chat"

    def ir_resena(self, cid):
        session.current_consulta_id = cid
        self.manager.current = "resena"

    def volver(self):
        self.manager.current = "dashboard"
