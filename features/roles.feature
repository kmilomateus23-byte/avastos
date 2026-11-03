# language: es
Característica: Roles, permisos y acceso
  Como administrador
  Quiero que cada perfil vea solo los módulos que le corresponden
  Para proteger la información y las acciones del ERP

  Esquema del escenario: Acceso a módulos según el rol
    Dado que el usuario tiene el rol "<rol>"
    Cuando intenta abrir el módulo "<modulo>"
    Entonces el acceso es "<acceso>"

    Ejemplos:
      | rol                     | modulo       | acceso     |
      | Administrador           | Resumen      | permitido  |
      | Administrador           | Proveedores  | permitido  |
      | Administrador           | Cotizaciones | permitido  |
      | Administrador           | Órdenes      | permitido  |
      | Administrador           | Inventario   | permitido  |
      | Gestión de proveedores  | Resumen      | permitido  |
      | Gestión de proveedores  | Proveedores  | permitido  |
      | Gestión de proveedores  | Órdenes      | permitido  |
      | Gestión de proveedores  | Cotizaciones | denegado   |
      | Gestión de proveedores  | Inventario   | denegado   |
      | Gestión de cotizaciones | Resumen      | permitido  |
      | Gestión de cotizaciones | Cotizaciones | permitido  |
      | Gestión de cotizaciones | Inventario   | permitido  |
      | Gestión de cotizaciones | Proveedores  | denegado   |
      | Gestión de cotizaciones | Órdenes      | denegado   |

  Esquema del escenario: Acciones restringidas por permisos
    Dado que el usuario tiene el rol "<rol>"
    Cuando intenta ejecutar la acción "<accion>"
    Entonces el acceso es "<acceso>"

    Ejemplos:
      | rol                     | accion            | acceso    |
      | Gestión de proveedores  | proveedores:crear | permitido |
      | Gestión de proveedores  | ordenes:editar    | permitido |
      | Gestión de proveedores  | ordenes:aprobar   | denegado  |
      | Gestión de cotizaciones | alertas:ver       | permitido |
      | Gestión de cotizaciones | ordenes:crear     | denegado  |
      | Administrador           | ordenes:aprobar   | permitido |

  Esquema del escenario: Validación del formulario de registro
    Cuando intento registrarme con correo "<correo>", contraseña "<password>" y rol "<rol>"
    Entonces el sistema responde "<resultado>"

    Ejemplos:
      | correo           | password  | rol           | resultado                                                     |
      | ana@abasto.co    | Clave2026 | Administrador | Registro exitoso                                              |
      | ana-abasto.co    | Clave2026 | Administrador | Correo inválido                                               |
      | ana@abasto.co    | corta1    | Administrador | La contraseña debe tener mínimo 8 caracteres, letras y números |
