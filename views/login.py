from kivy.uix.screenmanager import Screen
from auth_controller import login_user


class LoginScreen(Screen):

    def go_to_dashboard(self):
        email = self.ids.email.text
        password = self.ids.password.text

        rol = login_user(email, password)

        if rol == "cliente":
            self.manager.current = "dashboard"
        elif rol == "abogado":
            self.manager.current = "abogado_panel"
        else:
            print("Login incorrecto")

    def go_to_register(self):
        self.manager.current = "register"