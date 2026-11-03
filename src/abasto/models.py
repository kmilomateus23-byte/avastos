from dataclasses import dataclass


@dataclass
class Supplier:
    nit: str
    nombre: str
    correo: str
    estado: str = "ACTIVO"
    id: int | None = None


@dataclass
class QuotationRequest:
    id: str
    estado: str = "ABIERTA"


@dataclass
class Quotation:
    solicitud_id: str
    proveedor_id: str
    monto: float
    estado: str = "REGISTRADA"
    id: int | None = None


@dataclass
class PurchaseOrder:
    id: str | int | None
    proveedor_id: str | int
    monto: float
    estado: str = "PENDIENTE"


@dataclass
class Product:
    codigo: str
    nombre: str
    categoria: str
    stock: int = 0
    stock_minimo: int = 0
    estado: str = "ACTIVO"
