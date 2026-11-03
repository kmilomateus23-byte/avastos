from dataclasses import replace

from .errors import OrderError
from .models import PurchaseOrder


class PurchaseOrderService:
    def __init__(self, repo):
        self.repo = repo

    def create(self, proveedor_id, monto):
        if not proveedor_id:
            raise OrderError("El proveedor es obligatorio")
        if not monto > 0:
            raise OrderError("El monto debe ser mayor que cero")
        return self.repo.save(PurchaseOrder(None, proveedor_id, monto))

    def approve(self, order_id):
        """Aprueba una orden pendiente y descuenta su monto del presupuesto del proveedor."""
        orden = self.repo.find_by_id(order_id)
        if orden is None:
            raise OrderError("Orden no encontrada")
        if orden.estado == "APROBADA":
            raise OrderError("La orden ya está aprobada")
        presupuesto = self.repo.get_budget(orden.proveedor_id)
        if orden.monto > presupuesto:
            raise OrderError("Presupuesto insuficiente")
        aprobada = self.repo.save(replace(orden, estado="APROBADA"))
        self.repo.set_budget(orden.proveedor_id, presupuesto - orden.monto)
        return aprobada
