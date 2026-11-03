from unittest.mock import Mock

import pytest

from abasto.errors import OrderError
from abasto.models import PurchaseOrder
from abasto.orders import PurchaseOrderService


@pytest.fixture
def mock_repo():
    repo = Mock()
    repo.save.side_effect = lambda o: o
    return repo


def test_aprueba_orden_dentro_del_presupuesto_y_lo_descuenta(mock_repo):
    mock_repo.find_by_id.return_value = PurchaseOrder(1, 10, 5_000_000, "PENDIENTE")
    mock_repo.get_budget.return_value = 10_000_000
    orden = PurchaseOrderService(mock_repo).approve(1)
    assert orden.estado == "APROBADA"
    mock_repo.save.assert_called_once()
    mock_repo.set_budget.assert_called_once_with(10, 5_000_000)


def test_rechaza_orden_que_excede_el_presupuesto(mock_repo):
    mock_repo.find_by_id.return_value = PurchaseOrder(2, 10, 15_000_000, "PENDIENTE")
    mock_repo.get_budget.return_value = 10_000_000
    with pytest.raises(OrderError, match="Presupuesto insuficiente"):
        PurchaseOrderService(mock_repo).approve(2)
    mock_repo.save.assert_not_called()
    mock_repo.set_budget.assert_not_called()


def test_no_aprueba_orden_ya_aprobada(mock_repo):
    mock_repo.find_by_id.return_value = PurchaseOrder(3, 10, 1_000_000, "APROBADA")
    with pytest.raises(OrderError, match="La orden ya está aprobada"):
        PurchaseOrderService(mock_repo).approve(3)


def test_falla_si_la_orden_no_existe(mock_repo):
    mock_repo.find_by_id.return_value = None
    with pytest.raises(OrderError, match="Orden no encontrada"):
        PurchaseOrderService(mock_repo).approve(99)


def test_crea_ordenes_pendientes_validando_monto_y_proveedor(order_service):
    orden = order_service.create("P1", 500)
    assert orden.estado == "PENDIENTE" and orden.id is not None
    with pytest.raises(OrderError, match="El monto debe ser mayor que cero"):
        order_service.create("P1", 0)
    with pytest.raises(OrderError, match="El proveedor es obligatorio"):
        order_service.create("", 10)


def test_flujo_completo_con_repositorio_en_memoria(order_service, order_repo):
    order_repo.set_budget("P1", 1000)
    orden = order_service.create("P1", 400)
    order_service.approve(orden.id)
    assert order_repo.get_budget("P1") == 600
    assert order_repo.has_active_orders("P1") is True
    assert order_repo.has_active_orders("P2") is False
