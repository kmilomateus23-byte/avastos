import pytest

from abasto.auth import PERMISOS, can, can_access, menu_for, validar_correo, validar_password
from abasto.errors import AuthError

MODULOS = ["resumen", "proveedores", "cotizaciones", "ordenes", "inventario"]
ESPERADO = {
    "administrador": MODULOS,
    "gestion_proveedores": ["resumen", "proveedores", "ordenes"],
    "gestion_cotizaciones": ["resumen", "cotizaciones", "inventario"],
}


@pytest.mark.parametrize("rol", ESPERADO)
@pytest.mark.parametrize("modulo", MODULOS)
def test_acceso_por_rol_y_modulo(rol, modulo):
    assert can_access(rol, modulo) is (modulo in ESPERADO[rol])


def test_gestion_de_proveedores_crea_y_modifica_pero_no_aprueba_ni_elimina():
    for accion in ("proveedores:crear", "proveedores:editar", "ordenes:crear", "ordenes:editar"):
        assert can("gestion_proveedores", accion)
    assert not can("gestion_proveedores", "ordenes:aprobar")
    assert not can("gestion_proveedores", "proveedores:eliminar")


def test_gestion_de_cotizaciones_ve_inventario_y_alertas():
    assert can("gestion_cotizaciones", "alertas:ver")
    assert can("gestion_cotizaciones", "inventario:ver")
    assert not can("gestion_cotizaciones", "proveedores:crear")


def test_administrador_puede_todo():
    assert can("administrador", "ordenes:aprobar") and can("administrador", "lo-que-sea")


def test_menu_adaptado_a_cada_perfil():
    assert menu_for("administrador") == ["Resumen", "Proveedores", "Cotizaciones", "Órdenes", "Inventario"]
    assert menu_for("gestion_proveedores") == ["Resumen", "Proveedores", "Órdenes"]
    assert menu_for("gestion_cotizaciones") == ["Resumen", "Cotizaciones", "Inventario"]
    assert menu_for("desconocido") == [] and len(PERMISOS) == 3


@pytest.mark.parametrize("correo,ok", [("usuario@abasto.co", True), ("sin-arroba", False), ("usuario@", False), ("", False)])
def test_validar_correo(correo, ok):
    assert validar_correo(correo) is ok


@pytest.mark.parametrize("pw,ok", [("Clave2026", True), ("corta1", False), ("solosletras", False), ("12345678", False)])
def test_validar_password(pw, ok):
    assert validar_password(pw) is ok


def test_registro_y_login_sin_guardar_contrasena_en_texto_plano(auth):
    auth.register("Ana@Abasto.co", "Clave2026", "administrador")
    assert "Clave2026" not in str(auth.users)
    assert auth.login("ana@abasto.co", "Clave2026") == {"correo": "ana@abasto.co", "rol": "administrador"}


def test_rechaza_duplicados_rol_invalido_y_credenciales_erroneas(auth):
    auth.register("ana@abasto.co", "Clave2026", "administrador")
    with pytest.raises(AuthError, match="El correo ya está registrado"):
        auth.register("ana@abasto.co", "Clave2026", "administrador")
    with pytest.raises(AuthError, match="Rol no válido"):
        auth.register("b@abasto.co", "Clave2026", "root")
    with pytest.raises(AuthError, match="Credenciales inválidas"):
        auth.login("ana@abasto.co", "otraClave1")
    with pytest.raises(AuthError, match="Credenciales inválidas"):
        auth.login("nadie@abasto.co", "Clave2026")


def test_registro_rechaza_correo_y_contrasena_invalidos(auth):
    with pytest.raises(AuthError, match="Correo inválido"):
        auth.register("ana-abasto.co", "Clave2026", "administrador")
    with pytest.raises(AuthError, match="La contraseña debe tener"):
        auth.register("ana@abasto.co", "corta1", "administrador")
