from kivy.uix.screenmanager import Screen
from auth_controller import login_user


class LoginScreen(Screen):

    def go_to_dashboard(self):
        email = self.ids.email.text
        password = self.ids.password.text

        if login_user(email, password):
            self.manager.current = "dashboard"
        else:
            print("Login incorrecto")

    def go_to_register(self):
        self.manager.current = "register"