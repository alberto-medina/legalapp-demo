from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.clock import Clock


class ChatScreen(Screen):

    def on_enter(self):
        # limpiar chat al entrar (podés cambiar esto luego si querés persistencia)
        self.ids.chat_box.clear_widgets()

        # mensaje inicial
        self.add_message("Sistema", "La consulta fue habilitada. Podés comenzar a chatear.")

    def add_message(self, autor, mensaje):
        texto = f"[b]{autor}:[/b] {mensaje}"

        label = Label(
            text=texto,
            markup=True,
            size_hint_y=None,
            height=30,
            color=(1, 1, 1, 1),
            halign="left",
            valign="middle"
        )

        # ajustar ancho del texto
        label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))

        self.ids.chat_box.add_widget(label)

        # hacer scroll automático hacia abajo
        Clock.schedule_once(lambda dt: self.scroll_bottom(), 0.1)

    def scroll_bottom(self):
        self.ids.scroll.scroll_y = 0

    def enviar(self):
        mensaje = self.ids.input.text.strip()

        if mensaje:
            self.add_message("Vos", mensaje)
            self.ids.input.text = ""

            # respuesta simulada del abogado
            Clock.schedule_once(lambda dt: self.add_message("Abogado", "Recibido, estoy revisando tu caso."), 1)

    def volver(self):
        self.manager.current = "dashboard"