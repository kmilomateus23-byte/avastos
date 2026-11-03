from .errors import DuplicateQuotationError, InvalidQuotationError
from .models import Quotation

MENSAJES = {"REGISTRADA": "Cotización registrada"}


def calcular_total(precio_unitario, cantidad):
    """Total = precio unitario × cantidad (ambos deben ser > 0)."""
    if not cantidad > 0:
        raise InvalidQuotationError("La cantidad debe ser mayor que cero")
    if not precio_unitario > 0:
        raise InvalidQuotationError("El precio unitario debe ser mayor que cero")
    return precio_unitario * cantidad


class QuotationService:
    def __init__(self, quotation_repo, request_repo):
        self.quotation_repo = quotation_repo
        self.request_repo = request_repo

    def create_quotation(self, solicitud_id, proveedor_id, monto):
        if isinstance(monto, bool) or not isinstance(monto, (int, float)) or not monto > 0:
            raise InvalidQuotationError("El monto debe ser mayor que cero", "Monto inválido")
        solicitud = self.request_repo.find_by_id(solicitud_id)
        if solicitud is None:
            raise InvalidQuotationError("La solicitud no existe")
        if solicitud.estado != "ABIERTA":
            raise InvalidQuotationError("Solo se cotiza sobre solicitudes abiertas")
        if self.quotation_repo.find_by_solicitud_and_proveedor(solicitud_id, proveedor_id):
            raise DuplicateQuotationError("El proveedor ya cotizó esta solicitud")
        return self.quotation_repo.save(Quotation(solicitud_id, proveedor_id, monto))
