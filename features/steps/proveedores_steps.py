from behave import given, then, when

from abasto.models import PurchaseOrder
from abasto.suppliers import MENSAJES


@given('que no existe un proveedor con NIT "{nit}"')
def step_no_existe(context, nit):
    assert context.suppliers.exists_by_nit(nit) is False


@given('que ya existe un proveedor con NIT "{nit}"')
def step_ya_existe(context, nit):
    context.nit = nit
    context.suppliers.create_supplier(nit, "Existente S.A.S.", "existente@acme.com")


@given('que existe un proveedor "{nombre}" sin órdenes de compra activas')
def step_sin_ordenes(context, nombre):
    context.nit = "900111222"
    context.suppliers.create_supplier(context.nit, nombre, "ventas@acme.com")


@given('que existe un proveedor "{nombre}" con órdenes de compra activas')
def step_con_ordenes(context, nombre):
    context.nit = "900111222"
    context.suppliers.create_supplier(context.nit, nombre, "ventas@acme.com")
    context.order_repo.save(PurchaseOrder("OC-1", context.nit, 1000, "PENDIENTE"))


@when('registro el proveedor con NIT "{nit}", nombre "{nombre}" y correo "{correo}"')
def step_registrar(context, nit, nombre, correo):
    context.intentar(lambda: context.suppliers.create_supplier(nit, nombre, correo), MENSAJES["CREADO"])


@when("intento registrar otro proveedor con el mismo NIT")
def step_duplicado(context):
    context.intentar(
        lambda: context.suppliers.create_supplier(context.nit, "Duplicado", "dup@acme.com"),
        MENSAJES["CREADO"],
    )


@when('registro un proveedor con correo "{correo}"')
def step_correo(context, correo):
    context.intentar(
        lambda: context.suppliers.create_supplier(context.siguiente_nit(), "Proveedor de prueba", correo),
        "Correo válido",
    )


@when("solicito eliminar el proveedor")
def step_eliminar(context):
    context.intentar(lambda: context.suppliers.deactivate_supplier(context.nit), MENSAJES["DESACTIVADO"])


@then('el proveedor se crea con estado "{estado}"')
def step_creado(context, estado):
    assert context.resultado is not None, "No se creó el proveedor"
    assert context.resultado.estado == estado


@then("no se crea un nuevo proveedor")
def step_no_crea(context):
    assert len(context.supplier_repo.find_all()) == 1


@then('el proveedor cambia a estado "{estado}"')
@then('el proveedor sigue en estado "{estado}"')
def step_estado(context, estado):
    assert context.supplier_repo.find_by_nit(context.nit).estado == estado
