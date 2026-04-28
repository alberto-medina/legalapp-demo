from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from database import get_connection
import session
from datetime import datetime


class ResenaScreen(Screen):

    _puntaje_sel = 5

    def on_enter(self):
        self._puntaje_sel = 5
        self._render_estrellas()
        self.ids.input_comentario.text = ""

        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT abogado FROM consultas WHERE id=?",
                  (session.current_consulta_id,))
        row = c.fetchone()
        conn.close()
        abogado = row[0] if row else ""
        self.ids.lbl_abogado_resena.text = f"Abogado: {abogado}"

    def _render_estrellas(self):
        box = self.ids.estrellas_box
        box.clear_widgets()
        labels = ["1", "2", "3", "4", "5"]
        for i in range(1, 6):
            sel = i <= self._puntaje_sel
            btn = Button(
                text=labels[i - 1],
                font_size=22,
                bold=True,
                background_color=(0.99, 0.84, 0.00, 1) if sel else (0.08, 0.10, 0.28, 1),
                color=(0.00, 0.02, 0.12, 1) if sel else (0.45, 0.50, 0.68, 1),
            )
            btn.bind(on_release=lambda x, v=i: self._set_puntaje(v))
            box.add_widget(btn)

    def _set_puntaje(self, val):
        self._puntaje_sel = val
        self._render_estrellas()

    def enviar_resena(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT abogado, user_email FROM consultas WHERE id=?",
                  (session.current_consulta_id,))
        row = c.fetchone()
        if not row:
            conn.close()
            self.manager.current = "historial"
            return
        abogado_email, cliente_email = row
        comentario = self.ids.input_comentario.text.strip()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        try:
            c.execute("""
                INSERT OR REPLACE INTO resenas
                    (consulta_id, abogado_email, cliente_email, puntaje, comentario, fecha)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (session.current_consulta_id, abogado_email, cliente_email,
                  self._puntaje_sel, comentario, fecha))
            conn.commit()
            print("RESENA GUARDADA:", self._puntaje_sel, comentario)
        except Exception as e:
            print("ERROR RESENA:", e)
        finally:
            conn.close()
        self.manager.current = "historial"

    def omitir(self):
        self.manager.current = "historial"
