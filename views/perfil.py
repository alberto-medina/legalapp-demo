from kivy.uix.screenmanager import Screen
from database import get_connection
import session


class PerfilScreen(Screen):

    def on_enter(self):
        user = session.current_user
        if not user:
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT username, email, telefono, foto, especialidad, descripcion
            FROM users WHERE id=?
        """, (user[0],))

        data = cursor.fetchone()
        conn.close()

        if not data:
            return

        self.ids.nombre.text = data[0] or ""
        self.ids.email.text = data[1] or ""
        self.ids.telefono.text = data[2] or ""
        self.ids.foto.text = data[3] or ""
        self.ids.especialidad.text = data[4] or ""
        self.ids.descripcion.text = data[5] or ""

        # mostrar imagen si existe
        if data[3]:
            self.ids.img.source = data[3]

    def guardar(self):
        user = session.current_user
        if not user:
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users SET
                username=?,
                telefono=?,
                foto=?,
                especialidad=?,
                descripcion=?
            WHERE id=?
        """, (
            self.ids.nombre.text,
            self.ids.telefono.text,
            self.ids.foto.text,
            self.ids.especialidad.text,
            self.ids.descripcion.text,
            user[0]
        ))

        conn.commit()
        conn.close()

        print("Perfil actualizado")

    def volver(self):
        # vuelve según rol
        if session.current_user[3] == "abogado":
            self.manager.current = "abogado_panel"
        else:
            self.manager.current = "dashboard"