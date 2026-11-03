# language: es
Característica: Solicitud de cotizaciones
  Como responsable de cotizaciones
  Quiero registrar cotizaciones de los proveedores sobre solicitudes abiertas
  Para comparar ofertas y negociar ahorros

  Esquema del escenario: Validar monto de cotización
    Dado que existe una solicitud "SC-001" en estado "ABIERTA"
    Cuando registro una cotización por <monto>
    Entonces el sistema responde "<resultado>"

    Ejemplos:
      | monto   | resultado             |
      | 2500000 | Cotización registrada |
      | 0       | Monto inválido        |
      | -1000   | Monto inválido        |

  Escenario: Rechazar cotización con monto cero
    Dado que existe una solicitud "SC-001" en estado "ABIERTA"
    Cuando registro una cotización por 0
    Entonces el mensaje de error es "El monto debe ser mayor que cero"

  Escenario: No cotizar sobre una solicitud cerrada
    Dado que existe una solicitud "SC-002" en estado "CERRADA"
    Cuando registro una cotización por 100000
    Entonces el mensaje de error es "Solo se cotiza sobre solicitudes abiertas"

  Escenario: Un proveedor no puede cotizar dos veces la misma solicitud
    Dado que existe una solicitud "SC-001" en estado "ABIERTA"
    Y el proveedor ya cotizó la solicitud "SC-001"
    Cuando registro una cotización por 300000
    Entonces el mensaje de error es "El proveedor ya cotizó esta solicitud"
