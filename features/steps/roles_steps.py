from behave import given, then, when

from abasto.auth import MODULOS, ROLES, can, can_access
from abasto.errors import DomainError

ROL_POR_ETIQUETA = {v: k for k, v in ROLES.items()}
MODULO_POR_ETIQUETA = {v: k for k, v in MODULOS.items()}


@given('que el usuario tiene el rol "{etiqueta}"')
def step_rol(context, etiqueta):
    context.rol = ROL_POR_ETIQUETA[etiqueta]


@when('intenta abrir el módulo "{etiqueta}"')
def step_modulo(context, etiqueta):
    context.acceso = "permitido" if can_access(context.rol, MODULO_POR_ETIQUETA[etiqueta]) else "denegado"


@when('intenta ejecutar la acción "{accion}"')
def step_accion(context, accion):
    context.acceso = "permitido" if can(context.rol, accion) else "denegado"


@when('intento registrarme con correo "{correo}", contraseña "{password}" y rol "{etiqueta}"')
def step_registro(context, correo, password, etiqueta):
    try:
        context.auth.register(correo, password, ROL_POR_ETIQUETA[etiqueta])
        context.mensaje = "Registro exitoso"
    except DomainError as e:
        context.mensaje = e.message


@then('el acceso es "{esperado}"')
def step_acceso(context, esperado):
    assert context.acceso == esperado
