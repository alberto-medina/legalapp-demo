from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.lang import Builder

from views.login import LoginScreen
from views.register import RegisterScreen
from views.dashboard import DashboardScreen
from views.consulta_tipo import ConsultaTipoScreen
from views.consulta_especialidad import ConsultaEspecialidadScreen
from views.abogados import AbogadosScreen
from views.pago import PagoScreen
from views.chat import ChatScreen
from views.historial import HistorialScreen
from views.abogado_panel import AbogadoPanelScreen


class LegalAppPro(App):

    def build(self):
        self.sm = ScreenManager(transition=FadeTransition())

        Builder.load_file("views/login.kv")
        Builder.load_file("views/register.kv")
        Builder.load_file("views/dashboard.kv")
        Builder.load_file("views/consulta_tipo.kv")
        Builder.load_file("views/consulta_especialidad.kv")
        Builder.load_file("views/abogados.kv")
        Builder.load_file("views/pago.kv")
        Builder.load_file("views/chat.kv")
        Builder.load_file("views/historial.kv")
        Builder.load_file("views/abogado_panel.kv")

        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(RegisterScreen(name="register"))
        self.sm.add_widget(DashboardScreen(name="dashboard"))
        self.sm.add_widget(ConsultaTipoScreen(name="tipo"))
        self.sm.add_widget(ConsultaEspecialidadScreen(name="especialidad"))
        self.sm.add_widget(AbogadosScreen(name="abogados"))
        self.sm.add_widget(PagoScreen(name="pago"))
        self.sm.add_widget(ChatScreen(name="chat"))
        self.sm.add_widget(HistorialScreen(name="historial"))
        self.sm.add_widget(AbogadoPanelScreen(name="abogado_panel"))

        return self.sm


if __name__ == "__main__":
    LegalAppPro().run()