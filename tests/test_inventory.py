from unittest.mock import Mock

import pytest

from abasto.errors import InsufficientStockError, InvalidProductError
from abasto.inventory import InventoryService


def test_rechaza_producto_con_codigo_duplicado(inventory_service):
    inventory_service.register_product("PROD-001", "Papel", "Insumos")
    with pytest.raises(InvalidProductError, match="El código ya existe"):
        inventory_service.register_product("PROD-001", "Otro", "Insumos")


def test_llama_una_sola_vez_a_save_cuando_el_producto_es_valido():
    repo = Mock()
    repo.exists_by_code.return_value = False
    repo.save.side_effect = lambda p: p
    InventoryService(repo).register_product("X-1", "X", "Insumos", stock=5)
    repo.save.assert_called_once()


def test_valida_codigo_categoria_y_stock_inicial(inventory_service):
    with pytest.raises(InvalidProductError, match="El código es obligatorio"):
        inventory_service.register_product("", "A", "C")
    with pytest.raises(InvalidProductError, match="La categoría es obligatoria"):
        inventory_service.register_product("A", "A", "")
    with pytest.raises(InvalidProductError, match="El stock inicial"):
        inventory_service.register_product("A", "A", "Insumos", stock=-1)


@pytest.mark.parametrize("codigo,stock,cantidad,final", [
    ("PROD-001", 10, 5, 15), ("PROD-002", 0, 20, 20), ("PROD-003", 50, 10, 60),
])
def test_entrada_actualiza_stock_y_historial(inventory_service, codigo, stock, cantidad, final):
    inventory_service.register_product(codigo, codigo, "Insumos", stock=stock)
    inventory_service.register_entry(codigo, cantidad)
    assert inventory_service.get_stock(codigo) == final
    assert any(m["tipo"] == "ENTRADA" and m["cantidad"] == cantidad for m in inventory_service.get_history(codigo))


@pytest.mark.parametrize("codigo,stock,retiro,final,error", [
    ("PROD-001", 10, 3, 7, None),
    ("PROD-002", 5, 5, 0, None),
    ("PROD-003", 2, 5, 2, "Stock insuficiente"),
])
def test_retiro_de_inventario(inventory_service, codigo, stock, retiro, final, error):
    inventory_service.register_product(codigo, codigo, "Insumos", stock=stock)
    if error:
        with pytest.raises(InsufficientStockError, match=error):
            inventory_service.withdraw(codigo, retiro)
    else:
        inventory_service.withdraw(codigo, retiro)
    assert inventory_service.get_stock(codigo) == final


def test_alertas_de_stock_bajo(inventory_service):
    inventory_service.register_product("TON-HP-410A", "Tóner HP 410A negro", "Insumos", stock=3, stock_minimo=12)
    inventory_service.register_product("PAP-A4", "Papel A4", "Insumos", stock=100, stock_minimo=20)
    assert [p.codigo for p in inventory_service.get_low_stock_alerts()] == ["TON-HP-410A"]


def test_rechaza_cantidades_no_positivas_y_productos_inexistentes(inventory_service):
    with pytest.raises(InvalidProductError, match="Producto no encontrado"):
        inventory_service.register_entry("NOPE", 5)
    inventory_service.register_product("A", "A", "C", stock=1)
    with pytest.raises(InvalidProductError, match="La cantidad debe ser mayor que cero"):
        inventory_service.withdraw("A", 0)


def test_exists_by_code(inventory_service):
    assert inventory_service.exists_by_code("A") is False
    inventory_service.register_product("A", "A", "C")
    assert inventory_service.exists_by_code("A") is True
