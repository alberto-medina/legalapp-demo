from kivy.uix.screenmanager import Screen
from kivy.app import App
import session


# Reglas por estado del abogado:
#   disponible -> chat, video, urgente  (todo habilitado)
#   guardia    -> solo urgente
#   ocupado    -> nada habilitado
SERVICIOS_HABILITADOS = {
    "disponible": {"chat", "video", "urgente"},
    "guardia":    {"urgente"},
    "ocupado":    set(),
}


class ConsultaTipoScreen(Screen):

    def on_enter(self):
        """Refresca los botones segun el estado del abogado seleccionado."""
        estado = getattr(session, "estado_abogado", "disponible") or "disponible"
        habilitados = SERVICIOS_HABILITADOS.get(estado, set())

        ids = self.ids

        # --- Chat ---
        chat_ok = "chat" in habilitados
        ids.btn_chat.disabled = not chat_ok
        ids.btn_chat.opacity = 1.0 if chat_ok else 0.35
        ids.lbl_chat_estado.text = (
            "Disponible" if chat_ok else "Bloqueado - abogado no disponible"
        )
        ids.lbl_chat_estado.color = (
            (0.40, 0.80, 0.40, 1) if chat_ok else (0.85, 0.30, 0.30, 1)
        )

        # --- Video ---
        video_ok = "video" in habilitados
        ids.btn_video.disabled = not video_ok
        ids.btn_video.opacity = 1.0 if video_ok else 0.35
        ids.lbl_video_estado.text = (
            "Disponible" if video_ok else "Bloqueado - abogado no disponible"
        )
        ids.lbl_video_estado.color = (
            (0.40, 0.80, 0.40, 1) if video_ok else (0.85, 0.30, 0.30, 1)
        )

        # --- Urgente ---
        urgente_ok = "urgente" in habilitados
        ids.btn_urgente.disabled = not urgente_ok
        ids.btn_urgente.opacity = 1.0 if urgente_ok else 0.35
        ids.lbl_urgente_estado.text = (
            "Disponible" if urgente_ok else "Bloqueado - abogado ocupado"
        )
        ids.lbl_urgente_estado.color = (
            (0.40, 0.80, 0.40, 1) if urgente_ok else (0.85, 0.30, 0.30, 1)
        )

        # Banner informativo
        if estado == "guardia":
            ids.lbl_banner.text = (
                "Abogado en GUARDIA: solo consultas urgentes permitidas"
            )
            ids.lbl_banner.color = (0.90, 0.70, 0.10, 1)
        elif estado == "ocupado":
            ids.lbl_banner.text = (
                "Abogado OCUPADO: no acepta consultas en este momento"
            )
            ids.lbl_banner.color = (0.85, 0.30, 0.30, 1)
        else:
            ids.lbl_banner.text = "Abogado DISPONIBLE: todos los servicios activos"
            ids.lbl_banner.color = (0.40, 0.80, 0.40, 1)

    def seleccionar(self, servicio):
        session.tipo_servicio = servicio
        self.manager.current = "pago"

    def volver(self):
        self.manager.current = "abogados"
