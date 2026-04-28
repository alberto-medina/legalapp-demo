"""
Utilidad compartida para mostrar avatar (foto real o silueta default).
Importar desde cualquier vista que necesite mostrar avatares.
"""
import os

AVATAR_DEFAULT = "assets/avatar_default.png"


def get_avatar_source(foto_path):
    """Devuelve la ruta de imagen correcta: foto propia o silueta default."""
    if foto_path and os.path.isfile(foto_path):
        return foto_path
    return AVATAR_DEFAULT
