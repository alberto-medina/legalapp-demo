import session
from database import get_connection
from kivy.uix.screenmanager import Screen

SERVICIOS_HABILITADOS = {
    "disponible": {"chat", "video", "urgente"},
    "guardia":    {"urgente"},
    "ocupado":    set(),
}

BANNER_CFG = {
    "disponible": ("Abogado DISPONIBLE - todos los servicios activos", (0.30, 0.85, 0.50, 1)),
    "guardia":    ("Abogado EN GUARDIA - solo urgente permitido",      (0.95, 0.75, 0.10, 1)),
    "ocupado":    ("Abogado OCUPADO - sin disponibilidad",             (0.85, 0.25, 0.25, 1)),
}

PRECIOS = {
    "chat":    ("Chat",         "$1.000",  (0.18, 0.45, 0.85, 1)),
    "video":   ("Videollamada", "$3.000",  (0.18, 0.45, 0.85, 1)),
    "urgente": ("URGENTE",      "$5.000",  (0.75, 0.15, 0.15, 1)),
}

DESCRIPCIONES = {
    "chat":    "Consulta por mensajes de texto con el abogado",
    "video":   "Sesion por videollamada con el abogado",
    "urgente": "Atencion inmediata con prioridad maxima",
}


class PagoScreen(Screen):

    def on_enter(self):
        tipo    = getattr(session, "tipo_servicio", "chat") or "chat"
        abogado = session.abogado_seleccionado or ""

        # Mismo ID que antes
        self.ids.lbl_abogado_info.text = f"Abogado: {abogado}"

        # Actualiza el unico boton con el servicio que viene de consulta_tipo
        nombre, precio, color = PRECIOS.get(tipo, PRECIOS["chat"])
        self.ids.btn_pago_unico.text             = f"{nombre}     {precio}"
        self.ids.btn_pago_unico.background_color = color
        self.ids.lbl_tipo_desc.text              = DESCRIPCIONES.get(tipo, "")
        self.ids.lbl_precio_grande.text          = precio

    def pagar(self):
        # Lee el tipo directo de session, igual que antes pero sin argumento desde KV
        tipo    = getattr(session, "tipo_servicio", "chat") or "chat"
        conn    = get_connection()
        cursor  = conn.cursor()
        user    = session.current_user
        abogado = session.abogado_seleccionado
        cursor.execute("""
            INSERT INTO consultas (user_email, abogado, estado, tipo_servicio)
            VALUES (?, ?, ?, ?)
        """, (user[2], abogado, "pagado", tipo))
        session.current_consulta_id = cursor.lastrowid
        conn.commit()
        conn.close()
        print("PAGO OK - CONSULTA ID:", session.current_consulta_id)
        self.manager.current = "chat"
