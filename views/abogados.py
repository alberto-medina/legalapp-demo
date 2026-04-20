from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class AbogadosScreen(Screen):

    def on_enter(self):
        # 🔒 evitar crash si no existe el id
        if "lista" not in self.ids:
            return

        self.ids.lista.clear_widgets()

        abogados = [
            "Dr. Juan Pérez",
            "Dra. María Gómez",
            "Dr. Carlos López"
        ]

        for abogado in abogados:

            card = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=120,
                padding=10,
                spacing=5
            )

            nombre = Label(
                text=abogado,
                size_hint_y=None,
                height=30
            )

            boton = Button(
                text="Seleccionar",
                size_hint_y=None,
                height=40
            )

            boton.bind(on_release=lambda x, a=abogado: self.seleccionar(a))

            card.add_widget(nombre)
            card.add_widget(boton)

            self.ids.lista.add_widget(card)

    def seleccionar(self, abogado):
        self.manager.get_screen("pago").abogado = abogado
        self.manager.current = "pago"

    def volver(self):
        self.manager.current = "especialidad"