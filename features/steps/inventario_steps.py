from behave import given, then, when

from abasto.inventory import MENSAJES


def alta(context, codigo, stock, stock_minimo=0):
    return context.inventory.register_product(codigo, codigo, "Insumos", stock, stock_minimo)


@given('que no existe un producto con código "{codigo}"')
def step_no_existe(context, codigo):
    assert context.inventory.exists_by_code(codigo) is False


@given('que el producto "{codigo}" tiene stock actual {stock:d}')
@given('que el producto "{codigo}" tiene stock {stock:d}')
def step_producto(context, codigo, stock):
    context.codigo = codigo
    alta(context, codigo, stock)


@given('que el producto "{codigo}" tiene stock {stock:d} y stock mínimo {minimo:d}')
def step_producto_minimo(context, codigo, stock, minimo):
    context.codigo = codigo
    alta(context, codigo, stock, minimo)


@when('registro el producto con código "{codigo}" y stock inicial {stock:d}')
def step_registrar(context, codigo, stock):
    context.intentar(lambda: alta(context, codigo, stock), MENSAJES["REGISTRADO"])


@when("se registra una entrada de {cantidad:d} unidades")
def step_entrada(context, cantidad):
    context.intentar(lambda: context.inventory.register_entry(context.codigo, cantidad), "Entrada registrada")


@when("se intenta retirar {cantidad:d} unidades")
@when("se retiran {cantidad:d} unidades")
def step_retiro(context, cantidad):
    context.intentar(lambda: context.inventory.withdraw(context.codigo, cantidad), MENSAJES["RETIRO_OK"])


@when("consulto las alertas de existencias")
def step_alertas(context):
    context.alertas = context.inventory.get_low_stock_alerts()


@then('el producto se crea con estado "{estado}"')
def step_creado(context, estado):
    assert context.resultado is not None, "No se creó el producto"
    assert context.resultado.estado == estado


@then("el stock final debe ser {esperado:d}")
@then("el stock final es {esperado:d}")
@then("el stock permanece en {esperado:d}")
def step_stock(context, esperado):
    assert context.inventory.get_stock(context.codigo) == esperado


@then("el movimiento queda registrado en el historial")
def step_historial(context):
    assert "ENTRADA" in [m["tipo"] for m in context.inventory.get_history(context.codigo)]


@then('la alerta incluye el producto "{codigo}"')
def step_alerta(context, codigo):
    assert any(p.codigo == codigo for p in context.alertas)
