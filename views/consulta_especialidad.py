from kivy.uix.screenmanager import Screen


class ConsultaEspecialidadScreen(Screen):

    def seleccionar_especialidad(self):
        self.manager.current = "abogados"