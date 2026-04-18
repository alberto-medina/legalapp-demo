from kivy.uix.screenmanager import Screen


class DashboardScreen(Screen):

    def nueva_consulta(self):
        self.manager.current = "tipo"