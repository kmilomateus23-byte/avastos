from behave import given, then, use_step_matcher, when

from abasto.auth import can
from abasto.models import PurchaseOrder


def pesos(texto):
    return int(texto.replace(".", ""))


use_step_matcher("re")


@given(r'que el proveedor "(?P<proveedor>[^"]*)" tiene presupuesto disponible de \$(?P<valor>[\d.]+)')
def step_presupuesto(context, proveedor, valor):
    context.proveedor_id = proveedor
    context.order_repo.set_budget(proveedor, pesos(valor))


@given(r'existe una orden "(?P<id_>[^"]*)" por \$(?P<valor>[\d.]+) en estado "(?P<estado>[^"]*)"')
def step_orden(context, id_, valor, estado):
    context.orden_id = id_
    context.order_repo.save(PurchaseOrder(id_, context.proveedor_id, pesos(valor), estado))


@then(r'el presupuesto del proveedor se reduce a \$(?P<valor>[\d.]+)')
def step_presupuesto_final(context, valor):
    assert context.order_repo.get_budget(context.proveedor_id) == pesos(valor)


use_step_matcher("parse")


@when("el jefe de compras aprueba la orden")
def step_aprobar(context):
    # El jefe de compras actúa con el rol Administrador (único con ordenes:aprobar)
    assert can("administrador", "ordenes:aprobar")
    context.intentar(lambda: context.orders.approve(context.orden_id), "Orden aprobada")


@then('la orden cambia a "{estado}"')
@then('la orden sigue en estado "{estado}"')
def step_estado_orden(context, estado):
    assert context.order_repo.find_by_id(context.orden_id).estado == estado
