import pytest

from abasto.errors import DuplicateQuotationError, InvalidQuotationError
from abasto.quotations import calcular_total


@pytest.mark.parametrize("precio,cantidad,esperado", [(1000, 3, 3000), (2_500_000, 1, 2_500_000), (150.5, 2, 301)])
def test_calcular_total(precio, cantidad, esperado):
    assert calcular_total(precio, cantidad) == esperado


def test_calcular_total_con_cantidad_cero_lanza_excepcion():
    with pytest.raises(InvalidQuotationError, match="La cantidad debe ser mayor que cero"):
        calcular_total(1000, 0)


def test_calcular_total_con_precio_invalido_lanza_excepcion():
    with pytest.raises(InvalidQuotationError, match="El precio unitario"):
        calcular_total(0, 5)


def test_registra_cotizacion_valida(quotation_setup):
    service, _ = quotation_setup
    assert service.create_quotation("SC-001", "P1", 2_500_000).estado == "REGISTRADA"


@pytest.mark.parametrize("monto,ok", [(2_500_000, True), (0, False), (-1000, False)])
def test_valida_monto(quotation_setup, monto, ok):
    service, quotes = quotation_setup
    if ok:
        assert service.create_quotation("SC-001", "P1", monto).monto == monto
        assert len(quotes.find_all()) == 1
    else:
        with pytest.raises(InvalidQuotationError, match="El monto debe ser mayor que cero"):
            service.create_quotation("SC-001", "P1", monto)
        assert quotes.find_all() == []


@pytest.mark.parametrize("monto", [None, "100", True, float("nan")])
def test_rechaza_montos_no_numericos(quotation_setup, monto):
    service, _ = quotation_setup
    with pytest.raises(InvalidQuotationError):
        service.create_quotation("SC-001", "P1", monto)


def test_rechaza_solicitud_no_abierta_o_inexistente(quotation_setup):
    service, _ = quotation_setup
    with pytest.raises(InvalidQuotationError, match="Solo se cotiza sobre solicitudes abiertas"):
        service.create_quotation("SC-002", "P1", 100)
    with pytest.raises(InvalidQuotationError, match="La solicitud no existe"):
        service.create_quotation("NOPE", "P1", 100)


def test_no_permite_cotizacion_duplicada_del_mismo_proveedor(quotation_setup):
    service, _ = quotation_setup
    service.create_quotation("SC-001", "P1", 100)
    with pytest.raises(DuplicateQuotationError, match="El proveedor ya cotizó esta solicitud"):
        service.create_quotation("SC-001", "P1", 200)
    assert service.create_quotation("SC-001", "P2", 200).proveedor_id == "P2"
