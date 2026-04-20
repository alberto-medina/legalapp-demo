from kivy.uix.screenmanager import Screen


class ConsultaEspecialidadScreen(Screen):

    tipo = ""

    def seleccionar(self, especialidad):
        self.manager.current = "abogados"

    def volver(self):
        self.manager.current = "tipo"