from kivy.uix.screenmanager import Screen
from auth_controller import register_user


class RegisterScreen(Screen):

    def register(self):
        if register_user(
            self.ids.username.text,
            self.ids.email.text,
            self.ids.password.text
        ):
            self.manager.current = "login"

    def go_back(self):
        self.manager.current = "login"