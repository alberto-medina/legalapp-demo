from kivy.uix.screenmanager import Screen


class DashboardScreen(Screen):

    def nueva_consulta(self):
        # 🔥 ARRANCA BIEN EL FLUJO
        self.manager.current = "especialidad"

    def ver_historial(self):
        self.manager.current = "historial"

    def ir_perfil(self):
        self.manager.current = "perfil"

    def cerrar_sesion(self):
        # Limpia campos del login al volver (evita datos residuales)
        try:
            login_screen = self.manager.get_screen("login")
            login_screen.ids.email.text = ""
            login_screen.ids.password.text = ""
            login_screen.ids.error.text = ""
        except:
            pass

        self.manager.current = "login"