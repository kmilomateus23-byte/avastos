import re
from dataclasses import replace

from .errors import InvalidSupplierError, SupplierHasActiveOrdersError
from .models import Supplier

MENSAJES = {"CREADO": "Proveedor registrado exitosamente", "DESACTIVADO": "Proveedor desactivado"}
NIT_RE = re.compile(r"^\d{9,10}(-\d)?$")
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class _SinOrdenes:
    def has_active_orders(self, _nit):
        return False


class SupplierService:
    def __init__(self, repo, orders_repo=None):
        self.repo = repo
        self.orders_repo = orders_repo or _SinOrdenes()

    def exists_by_nit(self, nit):
        return self.repo.exists_by_nit(nit)

    def create_supplier(self, nit, nombre, correo):
        if not nombre or not str(nombre).strip():
            raise InvalidSupplierError("El nombre es obligatorio")
        if not NIT_RE.match(str(nit or "")):
            raise InvalidSupplierError("El NIT no es válido")
        if not EMAIL_RE.match(str(correo or "").strip()):
            raise InvalidSupplierError("Formato de correo inválido")
        if self.repo.exists_by_nit(nit):
            raise InvalidSupplierError("El NIT ya está registrado")
        return self.repo.save(Supplier(nit, nombre.strip(), correo.strip()))

    def update_supplier(self, nit, **cambios):
        actual = self.repo.find_by_nit(nit)
        if actual is None:
            raise InvalidSupplierError("Proveedor no encontrado")
        if "correo" in cambios and not EMAIL_RE.match(cambios["correo"]):
            raise InvalidSupplierError("Formato de correo inválido")
        if "nombre" in cambios and not str(cambios["nombre"]).strip():
            raise InvalidSupplierError("El nombre es obligatorio")
        return self.repo.save(replace(actual, **cambios))

    def deactivate_supplier(self, nit):
        """'Eliminar' = desactivar. No se permite con órdenes activas."""
        actual = self.repo.find_by_nit(nit)
        if actual is None:
            raise InvalidSupplierError("Proveedor no encontrado")
        if self.orders_repo.has_active_orders(nit):
            raise SupplierHasActiveOrdersError("El proveedor tiene órdenes de compra activas")
        return self.repo.save(replace(actual, estado="INACTIVO"))
