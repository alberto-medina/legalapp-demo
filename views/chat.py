from kivy.uix.screenmanager import Screen
import session


class ChatScreen(Screen):

    def on_enter(self):
        print("ENTRANDO A CHAT:", session.consulta_id)

        if session.consulta_id:
            self.ids.chat_box.text = f"Chat consulta ID: {session.consulta_id}"
        else:
            self.ids.chat_box.text = "Error: sin consulta"

    def enviar(self):
        mensaje = self.ids.input.text

        if mensaje.strip() == "":
            return

        self.ids.chat_box.text += f"\nYo: {mensaje}"
        self.ids.input.text = ""

    def volver(self):
        print("VOLVER DESDE CHAT")

        # 🔒 PROTEGIDO (NO CRASHEA MÁS)
        if session.current_user:
            try:
                if session.current_user[4] == "abogado":
                    self.manager.current = "abogado_panel"
                    return
            except:
                pass

        self.manager.current = "historial"