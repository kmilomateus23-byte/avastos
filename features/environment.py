import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from abasto import repositories as repos  # noqa: E402
from abasto.auth import AuthService  # noqa: E402
from abasto.inventory import InventoryService  # noqa: E402
from abasto.orders import PurchaseOrderService  # noqa: E402
from abasto.quotations import QuotationService  # noqa: E402
from abasto.suppliers import SupplierService  # noqa: E402


def before_scenario(context, scenario):
    """Cada escenario arranca con un mundo limpio (repositorios y servicios nuevos)."""
    context.supplier_repo = repos.InMemorySupplierRepository()
    context.order_repo = repos.InMemoryPurchaseOrderRepository()
    context.quotation_repo = repos.InMemoryQuotationRepository()
    context.request_repo = repos.InMemoryQuotationRequestRepository()
    context.product_repo = repos.InMemoryProductRepository()

    context.suppliers = SupplierService(context.supplier_repo, context.order_repo)
    context.quotations = QuotationService(context.quotation_repo, context.request_repo)
    context.orders = PurchaseOrderService(context.order_repo)
    context.inventory = InventoryService(context.product_repo)
    context.auth = AuthService()

    context.rol = None
    context.resultado = None
    context.error = None
    context.mensaje = None
    context.contador = 0

    def intentar(fn, mensaje_ok):
        """Ejecuta una acción capturando la excepción como lo haría la interfaz."""
        context.error = None
        try:
            context.resultado = fn()
            context.mensaje = mensaje_ok
        except Exception as e:  # noqa: BLE001
            context.error = e
            context.mensaje = getattr(e, "mensaje_ui", str(e))

    def siguiente_nit():
        context.contador += 1
        return str(900000000 + context.contador)

    context.intentar = intentar
    context.siguiente_nit = siguiente_nit
