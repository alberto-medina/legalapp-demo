from kivy.uix.screenmanager import Screen


class ConsultaTipoScreen(Screen):

    def seleccionar_tipo(self):
        self.manager.current = "especialidad"