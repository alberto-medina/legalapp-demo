from kivy.uix.screenmanager import Screen
from auth_controller import register_user


class RegisterScreen(Screen):

    def register(self):
        username = self.ids.username.text
        email = self.ids.email.text
        telefono = self.ids.telefono.text
        password = self.ids.password.text

        if register_user(username, email, password, telefono):
            self.manager.current = "login"
        else:
            self.ids.error.text = "Error al registrar (email existente?)"

    def go_back(self):
        self.manager.current = "login"