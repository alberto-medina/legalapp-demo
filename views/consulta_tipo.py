from kivy.uix.screenmanager import Screen
import session


class ConsultaTipoScreen(Screen):

    def seleccionar(self, servicio):
        session.tipo_servicio = servicio
        self.manager.current = "especialidad"

    def volver(self):
        self.manager.current = "dashboard"