from kivy.uix.screenmanager import Screen
from database import get_connection
import session


class PerfilScreen(Screen):

    def on_enter(self):
        if not session.current_user:
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT username, email, telefono, foto, matricula, experiencia, descripcion, rol
            FROM users
            WHERE email=?
        """, (session.current_user[2],))

        user = cursor.fetchone()
        conn.close()

        if not user:
            return

        try:
            # CAMPOS GENERALES
            if "nombre" in self.ids:
                self.ids.nombre.text = user[0] or ""

            if "telefono" in self.ids:
                self.ids.telefono.text = user[2] or ""

            if "foto" in self.ids:
                self.ids.foto.text = user[3] or ""

            rol = user[7]

            # CAMPOS SOLO ABOGADO
            if rol == "abogado":
                self.ids.matricula.opacity = 1
                self.ids.experiencia.opacity = 1
                self.ids.descripcion.opacity = 1

                self.ids.matricula.disabled = False
                self.ids.experiencia.disabled = False
                self.ids.descripcion.disabled = False

                self.ids.matricula.text = user[4] or ""
                self.ids.experiencia.text = user[5] or ""
                self.ids.descripcion.text = user[6] or ""
            else:
                self.ids.matricula.opacity = 0
                self.ids.experiencia.opacity = 0
                self.ids.descripcion.opacity = 0

                self.ids.matricula.disabled = True
                self.ids.experiencia.disabled = True
                self.ids.descripcion.disabled = True

        except Exception as e:
            print("ERROR PERFIL:", e)

    def guardar(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users SET
                username=?,
                telefono=?,
                foto=?,
                matricula=?,
                experiencia=?,
                descripcion=?
            WHERE email=?
        """, (
            self.ids.nombre.text,
            self.ids.telefono.text,
            self.ids.foto.text,
            self.ids.matricula.text,
            self.ids.experiencia.text,
            self.ids.descripcion.text,
            session.current_user[2]
        ))

        conn.commit()
        conn.close()

        print("PERFIL ACTUALIZADO")

        # 🔥 CORRECCIÓN CLAVE: NO MEZCLAR FLUJOS
        if session.current_user[4] == "abogado":
            self.manager.current = "abogado_panel"
        else:
            self.manager.current = "dashboard"