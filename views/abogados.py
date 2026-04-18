from kivy.uix.screenmanager import Screen

class AbogadosScreen(Screen):

    def seleccionar_abogado(self, nombre):
        app = self.manager
        app.abogado_seleccionado = nombre
        self.manager.current = "pago"