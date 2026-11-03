# language: es
Característica: Aprobación de órdenes de compra
  Como jefe de compras
  Quiero aprobar órdenes dentro del presupuesto del proveedor
  Para controlar el gasto

  Escenario: Aprobar orden dentro del presupuesto
    Dado que el proveedor "ACME" tiene presupuesto disponible de $10.000.000
    Y existe una orden "OC-100" por $5.000.000 en estado "PENDIENTE"
    Cuando el jefe de compras aprueba la orden
    Entonces la orden cambia a "APROBADA"
    Y el presupuesto del proveedor se reduce a $5.000.000

  Escenario: Rechazar orden que excede el presupuesto
    Dado que el proveedor "ACME" tiene presupuesto disponible de $10.000.000
    Y existe una orden "OC-101" por $15.000.000 en estado "PENDIENTE"
    Cuando el jefe de compras aprueba la orden
    Entonces el mensaje de error es "Presupuesto insuficiente"
    Y la orden sigue en estado "PENDIENTE"
    Y el presupuesto del proveedor se reduce a $10.000.000

  Escenario: No re-aprobar una orden ya aprobada
    Dado que el proveedor "ACME" tiene presupuesto disponible de $10.000.000
    Y existe una orden "OC-102" por $1.000.000 en estado "APROBADA"
    Cuando el jefe de compras aprueba la orden
    Entonces el mensaje de error es "La orden ya está aprobada"
