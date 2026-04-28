from kivy.uix.screenmanager import Screen
import session


class DashboardScreen(Screen):

    def on_enter(self):
        user = session.current_user
        if user:
            self.ids.lbl_bienvenida.text = user[1] or user[2]

    def nueva_consulta(self):
        self.manager.current = "especialidad"

    def ver_historial(self):
        self.manager.current = "historial"

    def ir_perfil(self):
        self.manager.current = "perfil"

    def cerrar_sesion(self):
        session.current_user = None
        try:
            ls = self.manager.get_screen("login")
            ls.ids.email.text = ""
            ls.ids.password.text = ""
            ls.ids.error.text = ""
        except Exception:
            pass
        self.manager.current = "login"
