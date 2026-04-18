from kivy.uix.screenmanager import Screen


class ChatScreen(Screen):

    def volver_dashboard(self):
        self.manager.current = "dashboard"