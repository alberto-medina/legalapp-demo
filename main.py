from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.lang import Builder

from views.login import LoginScreen
from views.register import RegisterScreen
from views.dashboard import DashboardScreen
from views.consulta_tipo import ConsultaTipoScreen
from views.consulta_especialidad import ConsultaEspecialidadScreen
from views.abogados import AbogadosScreen


class LegalAppPro(App):

    def build(self):
        self.sm = ScreenManager(transition=FadeTransition())

        Builder.load_file("views/login.kv")
        Builder.load_file("views/register.kv")
        Builder.load_file("views/dashboard.kv")
        Builder.load_file("views/consulta_tipo.kv")
        Builder.load_file("views/consulta_especialidad.kv")
        Builder.load_file("views/abogados.kv")

        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(RegisterScreen(name="register"))
        self.sm.add_widget(DashboardScreen(name="dashboard"))
        self.sm.add_widget(ConsultaTipoScreen(name="tipo"))
        self.sm.add_widget(ConsultaEspecialidadScreen(name="especialidad"))
        self.sm.add_widget(AbogadosScreen(name="abogados"))

        return self.sm


if __name__ == "__main__":
    LegalAppPro().run()