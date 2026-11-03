# language: es
Característica: Inventario de productos, materia prima e insumos
  Como responsable de inventario
  Quiero registrar productos y controlar su stock
  Para evitar quiebres de existencias

  Escenario: Registrar un producto válido
    Dado que no existe un producto con código "PROD-010"
    Cuando registro el producto con código "PROD-010" y stock inicial 8
    Entonces el producto se crea con estado "ACTIVO"

  Escenario: Rechazar producto con código duplicado
    Dado que no existe un producto con código "PROD-011"
    Cuando registro el producto con código "PROD-011" y stock inicial 1
    Y registro el producto con código "PROD-011" y stock inicial 5
    Entonces el mensaje de error es "El código ya existe"

  Esquema del escenario: Actualizar stock con cantidad válida
    Dado que el producto "<codigo>" tiene stock actual <stock_actual>
    Cuando se registra una entrada de <cantidad> unidades
    Entonces el stock final debe ser <stock_final>
    Y el movimiento queda registrado en el historial

    Ejemplos:
      | codigo   | stock_actual | cantidad | stock_final |
      | PROD-001 | 10           | 5        | 15          |
      | PROD-002 | 0            | 20       | 20          |
      | PROD-003 | 50           | 10       | 60          |

  Escenario: Rechazar salida que deja stock negativo
    Dado que el producto "PROD-001" tiene stock 5
    Cuando se intenta retirar 10 unidades
    Entonces el sistema muestra "Stock insuficiente"
    Y el stock permanece en 5

  Esquema del escenario: Retiro de inventario
    Dado que el producto "<codigo>" tiene stock <stock>
    Cuando se retiran <retiro> unidades
    Entonces el stock final es <final>
    Y el sistema responde "<mensaje>"

    Ejemplos:
      | codigo   | stock | retiro | final | mensaje            |
      | PROD-001 | 10    | 3      | 7     | Retiro exitoso     |
      | PROD-002 | 5     | 5      | 0     | Retiro exitoso     |
      | PROD-003 | 2     | 5      | 2     | Stock insuficiente |

  Escenario: Alerta de existencias por debajo del mínimo
    Dado que el producto "TON-HP-410A" tiene stock 3 y stock mínimo 12
    Cuando consulto las alertas de existencias
    Entonces la alerta incluye el producto "TON-HP-410A"
