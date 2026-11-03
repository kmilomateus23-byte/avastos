from unittest.mock import Mock

import pytest

from abasto.errors import InvalidSupplierError, SupplierHasActiveOrdersError
from abasto.models import Supplier
from abasto.suppliers import SupplierService


def test_crea_proveedor_con_nit_valido_y_estado_activo(supplier_service):
    creado = supplier_service.create_supplier("900123456", "ACME S.A.S.", "contacto@acme.com")
    assert creado.id is not None
    assert creado.estado == "ACTIVO"


def test_llama_una_sola_vez_a_save_con_estado_activo():
    repo = Mock()
    repo.exists_by_nit.return_value = False
    repo.save.side_effect = lambda s: s
    SupplierService(repo).create_supplier("900123456", "ACME", "a@acme.com")
    repo.save.assert_called_once()
    assert repo.save.call_args.args[0].estado == "ACTIVO"


def test_rechaza_nit_duplicado(supplier_service, supplier_repo):
    supplier_service.create_supplier("900123456", "ACME", "a@a.com")
    with pytest.raises(InvalidSupplierError, match="El NIT ya está registrado"):
        supplier_service.create_supplier("900123456", "Otra", "b@b.com")
    assert len(supplier_repo.find_all()) == 1


@pytest.mark.parametrize("correo", ["", " ", "sin-arroba", "usuario@", "sin-arroba.com"])
def test_rechaza_correos_invalidos(supplier_service, correo):
    with pytest.raises(InvalidSupplierError):
        supplier_service.create_supplier("900999999", "Test", correo)


def test_exige_nombre_y_nit_valido(supplier_service):
    with pytest.raises(InvalidSupplierError, match="El nombre es obligatorio"):
        supplier_service.create_supplier("900123456", "", "a@a.com")
    with pytest.raises(InvalidSupplierError, match="El NIT no es válido"):
        supplier_service.create_supplier("12", "X", "a@a.com")


def test_desactiva_proveedor_sin_ordenes_activas(supplier_service):
    supplier_service.create_supplier("900123456", "ACME", "a@a.com")
    assert supplier_service.deactivate_supplier("900123456").estado == "INACTIVO"


def test_no_elimina_proveedor_con_ordenes_activas(supplier_repo):
    orders = Mock()
    orders.has_active_orders.return_value = True
    svc = SupplierService(supplier_repo, orders)
    svc.create_supplier("900123456", "ACME", "a@a.com")
    with pytest.raises(SupplierHasActiveOrdersError):
        svc.deactivate_supplier("900123456")
    assert supplier_repo.find_by_nit("900123456").estado == "ACTIVO"
    orders.has_active_orders.assert_called_once_with("900123456")


def test_actualiza_datos_validando_correo_y_nombre(supplier_service):
    supplier_service.create_supplier("900123456", "ACME", "a@a.com")
    assert supplier_service.update_supplier("900123456", nombre="ACME Nueva").nombre == "ACME Nueva"
    with pytest.raises(InvalidSupplierError, match="Formato de correo inválido"):
        supplier_service.update_supplier("900123456", correo="malo")
    with pytest.raises(InvalidSupplierError, match="El nombre es obligatorio"):
        supplier_service.update_supplier("900123456", nombre=" ")


def test_operaciones_sobre_proveedor_inexistente(supplier_service):
    with pytest.raises(InvalidSupplierError, match="Proveedor no encontrado"):
        supplier_service.update_supplier("999999999", nombre="X")
    with pytest.raises(InvalidSupplierError, match="Proveedor no encontrado"):
        supplier_service.deactivate_supplier("999999999")


def test_exists_by_nit(supplier_service):
    assert supplier_service.exists_by_nit("900123456") is False
    supplier_service.create_supplier("900123456", "ACME", "a@a.com")
    assert supplier_service.exists_by_nit("900123456") is True
