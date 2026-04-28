from kivy.uix.screenmanager import Screen
import session


class ConsultaEspecialidadScreen(Screen):

    def seleccionar(self, area):
        session.area_legal = area
        self.manager.current = "abogados"

    def volver(self):
        self.manager.current = "dashboard"
