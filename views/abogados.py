import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Line
from database import get_connection
import session
from views.utils_avatar import get_avatar_source

ESTADO_COLOR = {
    "disponible": (0.10, 0.72, 0.38, 1),
    "guardia":    (0.85, 0.62, 0.05, 1),
    "ocupado":    (0.80, 0.22, 0.22, 1),
}
ESTADO_LABEL = {
    "disponible": "En linea",
    "guardia":    "En guardia",
    "ocupado":    "Ocupado",
}


class AbogadosScreen(Screen):

    _todos = []

    def on_enter(self):
        import session as s
        self.ids.lbl_area.text = f"Area: {s.area_legal or ''}"
        self.ids.buscador.text = ""
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            SELECT username, email, estado_abogado, foto,
                   matricula, experiencia, descripcion
            FROM users WHERE rol='abogado'
        """)
        self._todos = c.fetchall()
        conn.close()
        self._render(self._todos)

    def filtrar(self, texto):
        texto = texto.strip().lower()
        if not texto:
            self._render(self._todos)
            return
        filtrados = [r for r in self._todos
                     if texto in (r[0] or "").lower()
                     or texto in (r[6] or "").lower()]
        self._render(filtrados)

    def _render(self, abogados):
        self.ids.lista.clear_widgets()
        if not abogados:
            self.ids.lista.add_widget(Label(
                text="No se encontraron abogados",
                color=(0.45, 0.50, 0.60, 1),
                size_hint_y=None, height=60,
            ))
            return
        for row in abogados:
            nombre, email, estado, foto, matricula, experiencia, descripcion = row
            self._add_card(nombre or email, email,
                           estado or "disponible", foto,
                           matricula, experiencia, descripcion)

    def _add_card(self, nombre, email, estado, foto,
                  matricula, experiencia, descripcion):
        # Buscar rating
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT AVG(puntaje), COUNT(*) FROM resenas WHERE abogado_email=?",
                  (email,))
        avg_row = c.fetchone()
        conn.close()
        promedio = avg_row[0] or 0
        total_resenas = avg_row[1] or 0

        card = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=130,
            padding=[14, 12],
            spacing=6,
        )
        with card.canvas.before:
            Color(rgba=(1, 1, 1, 1))
            card._bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[14])
            Color(rgba=(0.88, 0.90, 0.93, 1))
            card._border = Line(
                rounded_rectangle=[card.x+1, card.y+1,
                                   card.width-2, card.height-2, 14],
                width=0.8,
            )
        card.bind(
            pos=lambda w, v: (setattr(w._bg, 'pos', v),
                              setattr(w._border, 'rounded_rectangle',
                                      [v[0]+1, v[1]+1, w.width-2, w.height-2, 14])),
            size=lambda w, v: (setattr(w._bg, 'size', v),
                               setattr(w._border, 'rounded_rectangle',
                                       [w.x+1, w.y+1, v[0]-2, v[1]-2, 14])),
        )

        # Fila superior: avatar + info + btn
        top = BoxLayout(orientation="horizontal", spacing=12, size_hint_y=None, height=70)

        # Avatar
        av_box = BoxLayout(size_hint_x=None, width=60)
        av = AsyncImage(
            source=get_avatar_source(foto),
            allow_stretch=True, keep_ratio=True,
        )
        av_box.add_widget(av)
        top.add_widget(av_box)

        # Info
        info = BoxLayout(orientation="vertical")
        info.add_widget(Label(
            text=nombre, font_size=14, bold=True,
            color=(0.08, 0.12, 0.28, 1),
            halign="left", text_size=(None, None),
        ))
        estado_lbl = Label(
            text=ESTADO_LABEL.get(estado, estado),
            font_size=12,
            color=ESTADO_COLOR.get(estado, (0.5, 0.5, 0.5, 1)),
            halign="left", text_size=(None, None),
        )
        info.add_widget(estado_lbl)

        # Rating
        stars = "*" * round(promedio) + "o" * (5 - round(promedio))
        rating_txt = f"{stars} {promedio:.1f} ({total_resenas})" if total_resenas else "Sin resenas"
        info.add_widget(Label(
            text=rating_txt, font_size=11,
            color=(0.80, 0.60, 0.05, 1),
            halign="left", text_size=(None, None),
        ))
        top.add_widget(info)

        btn = Button(
            text="Elegir",
            size_hint_x=None, width=70,
            bold=True, font_size=13,
            background_color=(0.00, 0.04, 0.22, 1),
            color=(1, 1, 1, 1),
        )
        btn.bind(on_release=lambda x, e=email, est=estado: self.seleccionar(e, est))
        top.add_widget(btn)
        card.add_widget(top)

        # Bio corta
        if descripcion:
            bio = Label(
                text=descripcion[:60] + ("..." if len(descripcion) > 60 else ""),
                font_size=11,
                color=(0.40, 0.45, 0.55, 1),
                halign="left",
                text_size=(None, None),
                size_hint_y=None,
                height=22,
            )
            card.add_widget(bio)

        self.ids.lista.add_widget(card)

    def seleccionar(self, email, estado):
        session.abogado_seleccionado = email
        session.estado_abogado = estado
        self.manager.current = "tipo"

    def volver(self):
        self.manager.current = "especialidad"
