import pytest

from abasto.auth import AuthService
from abasto.inventory import InventoryService
from abasto.models import QuotationRequest
from abasto.orders import PurchaseOrderService
from abasto.quotations import QuotationService
from abasto.repositories import (
    InMemoryProductRepository, InMemoryPurchaseOrderRepository, InMemoryQuotationRepository,
    InMemoryQuotationRequestRepository, InMemorySupplierRepository,
)
from abasto.suppliers import SupplierService


@pytest.fixture
def supplier_repo():
    return InMemorySupplierRepository()


@pytest.fixture
def supplier_service(supplier_repo):
    return SupplierService(supplier_repo)


@pytest.fixture
def quotation_setup():
    quotes, requests = InMemoryQuotationRepository(), InMemoryQuotationRequestRepository()
    requests.save(QuotationRequest("SC-001", "ABIERTA"))
    requests.save(QuotationRequest("SC-002", "CERRADA"))
    return QuotationService(quotes, requests), quotes


@pytest.fixture
def inventory_service():
    return InventoryService(InMemoryProductRepository())


@pytest.fixture
def order_repo():
    return InMemoryPurchaseOrderRepository()


@pytest.fixture
def order_service(order_repo):
    return PurchaseOrderService(order_repo)


@pytest.fixture
def auth():
    return AuthService()
