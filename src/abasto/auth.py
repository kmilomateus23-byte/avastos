import hashlib
import os
import re

from .errors import AuthError
from .suppliers import EMAIL_RE

ROLES = {
    "administrador": "Administrador",
    "gestion_proveedores": "Gestión de proveedores",
    "gestion_cotizaciones": "Gestión de cotizaciones",
}
MODULOS = {
    "resumen": "Resumen", "proveedores": "Proveedores", "cotizaciones": "Cotizaciones",
    "ordenes": "Órdenes", "inventario": "Inventario",
}
PERMISOS = {
    "administrador": {
        "modulos": ["resumen", "proveedores", "cotizaciones", "ordenes", "inventario"],
        "acciones": {"*"},
    },
    "gestion_proveedores": {
        "modulos": ["resumen", "proveedores", "ordenes"],
        "acciones": {"proveedores:ver", "proveedores:crear", "proveedores:editar",
                     "ordenes:ver", "ordenes:crear", "ordenes:editar"},
    },
    "gestion_cotizaciones": {
        "modulos": ["resumen", "cotizaciones", "inventario"],
        "acciones": {"cotizaciones:ver", "cotizaciones:crear", "cotizaciones:editar",
                     "inventario:ver", "alertas:ver"},
    },
}


def validar_correo(correo):
    return bool(EMAIL_RE.match(str(correo or "").strip()))


def validar_password(pw):
    """Mínimo 8 caracteres, al menos una letra y un número."""
    return isinstance(pw, str) and len(pw) >= 8 and bool(re.search(r"[A-Za-z]", pw)) and bool(re.search(r"\d", pw))


def can_access(rol, modulo):
    return rol in PERMISOS and modulo in PERMISOS[rol]["modulos"]


def can(rol, accion):
    p = PERMISOS.get(rol)
    return bool(p) and ("*" in p["acciones"] or accion in p["acciones"])


def menu_for(rol):
    return [MODULOS[m] for m in PERMISOS[rol]["modulos"]] if rol in PERMISOS else []


def _hash(password, salt):
    return hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1).hex()


class AuthService:
    def __init__(self):
        self.users = {}

    def register(self, correo, password, rol):
        if not validar_correo(correo):
            raise AuthError("Correo inválido")
        if not validar_password(password):
            raise AuthError("La contraseña debe tener mínimo 8 caracteres, letras y números")
        if rol not in ROLES:
            raise AuthError("Rol no válido")
        key = correo.strip().lower()
        if key in self.users:
            raise AuthError("El correo ya está registrado")
        salt = os.urandom(8)
        self.users[key] = {"correo": key, "rol": rol, "salt": salt, "hash": _hash(password, salt)}
        return {"correo": key, "rol": rol}

    def login(self, correo, password):
        u = self.users.get(str(correo or "").strip().lower())
        if not u or _hash(str(password), u["salt"]) != u["hash"]:
            raise AuthError("Credenciales inválidas")
        return {"correo": u["correo"], "rol": u["rol"]}
