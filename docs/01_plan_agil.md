# Plan ágil del equipo (Grupo N1)

Grupo N1 · Ingeniería de Software II · Universidad de Cundinamarca

> Las evidencias (capturas de Trello/Jira/Asana, Slack, reuniones) deben ser las del trabajo real del grupo, en `docs/evidencias/`.

## 1. Roles
| Rol | Integrante | Responsabilidad |
|---|---|---|
| Product Owner | William Camilo Mateus Rueda | Prioriza el backlog y acepta historias |
| Scrum Master | Mateo Esteban Medina Sastoque | Facilita ceremonias y remueve impedimentos |
| Desarrollo / QA | Yeisson David Tinjacá Bolívar | Escribe pruebas (rojo), implementa (verde), refactoriza |

> Los tres integrantes también desarrollan y prueban; los roles de Scrum se rotan entre iteraciones. _(Ajustar si el equipo acordó otra distribución.)_

Herramienta de seguimiento: _(Trello / Jira / Asana: indicar cuál usaron)_ · Comunicación: _(Slack / WhatsApp / Teams: indicar cuál usaron)_

## 2. Product Backlog (priorizado)
| ID | Historia de usuario | Prioridad | Pruebas asociadas |
|---|---|---|---|
| HU-01 | Como administrador quiero registrar proveedores con NIT y correo válidos para mantener la base de aliados | Alta | `tests/test_suppliers.py`, `features/proveedores.feature` |
| HU-02 | Como administrador quiero desactivar proveedores sin órdenes activas | Alta | ídem |
| HU-03 | Como gestor de cotizaciones quiero registrar cotizaciones sobre solicitudes abiertas | Alta | `tests/test_quotations.py`, `features/cotizaciones.feature` |
| HU-04 | Como jefe de compras quiero aprobar órdenes dentro del presupuesto del proveedor | Alta | `tests/test_orders.py`, `features/ordenes.feature` |
| HU-05 | Como responsable de inventario quiero registrar entradas/salidas sin permitir stock negativo | Alta | `tests/test_inventory.py`, `features/inventario.feature` |
| HU-06 | Como gestor quiero alertas de stock bajo el mínimo | Media | ídem |
| HU-07 | Como usuario quiero ver solo los módulos de mi rol | Alta | `tests/test_auth.py`, `features/roles.feature` |

## 3. Iteraciones (Sprints)
| Iteración | Objetivo | Historias | Resultado |
|---|---|---|---|
| 1 | Proveedores y roles | HU-01, HU-02, HU-07 | Completada: validaciones de NIT/correo, desactivación y permisos por rol, con pruebas en verde |
| 2 | Cotizaciones y órdenes | HU-03, HU-04 | Completada: cotizaciones sobre solicitudes abiertas y aprobación de órdenes con control de presupuesto |
| 3 | Inventario y calidad (CI, cobertura) | HU-05, HU-06 | Completada: inventario con historial y alertas; 77 pruebas unitarias (100 % cobertura) y 50 escenarios BDD |

## 4. Definición de Hecho (DoD)
- [ ] Escenario Gherkin escrito y aprobado por el PO
- [ ] Prueba unitaria escrita **antes** del código (rojo → verde → refactor)
- [ ] `pytest` en verde con cobertura ≥ 90 %
- [ ] `behave` en verde
- [ ] CI de GitHub Actions en verde
- [ ] Código revisado por otro integrante (pull request)

## 5. Ceremonias (plantilla de acta)
**Fecha:** · **Tipo:** Planning / Daily / Review / Retrospectiva · **Asistentes:**
**Acuerdos:** · **Impedimentos:** · **Responsables y fechas:**

## 6. Retrospectiva (plantilla)
| Qué hicimos bien | Qué mejorar | Acciones para la próxima iteración |
|---|---|---|
| | | |
