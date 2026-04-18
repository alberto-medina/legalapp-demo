from kivy.uix.screenmanager import Screen
from auth_controller import register_user


class RegisterScreen(Screen):

    def register(self):
        username = self.ids.username.text
        email = self.ids.email.text
        password = self.ids.password.text

        if register_user(username, email, password):
            self.manager.current = "login"
        else:
            print("Error al registrar")

    def go_back(self):
        self.manager.current = "login"