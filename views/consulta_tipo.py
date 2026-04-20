from kivy.uix.screenmanager import Screen


class ConsultaTipoScreen(Screen):

    def seleccionar(self, tipo):
        self.manager.get_screen("especialidad").tipo = tipo
        self.manager.current = "especialidad"

    def volver(self):
        self.manager.current = "dashboard"