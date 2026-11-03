from behave import given, then


@given("que el usuario administrador ha iniciado sesión")
def step_admin(context):
    context.rol = "administrador"


@then('el sistema responde "{esperado}"')
@then('el sistema muestra "{esperado}"')
@then('el sistema muestra el mensaje "{esperado}"')
@then('el sistema confirma "{esperado}"')
def step_mensaje(context, esperado):
    assert context.mensaje == esperado, f"Se esperaba '{esperado}' y se obtuvo '{context.mensaje}'"


@then('el mensaje de error es "{esperado}"')
def step_error(context, esperado):
    assert context.error is not None, "Se esperaba una excepción y no ocurrió"
    assert context.error.message == esperado, f"Mensaje obtenido: '{context.error.message}'"
