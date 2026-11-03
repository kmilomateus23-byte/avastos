# ABASTO Operaciones · TDD, BDD y Calidad Ágil con Python

**Universidad de Cundinamarca · Ingeniería de Software II · R2-A2-S10**
**Grupo:** N1 · **Integrantes:** _(nombres y códigos de los estudiantes)_

Incremento de software para la gestión de **proveedores, cotizaciones, órdenes de compra e inventario**
con control de acceso por roles, construido aplicando pruebas desde el primer minuto.

## Ejecutar

```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest                      # TDD: 77 pruebas unitarias + cobertura (100 %)
PYTHONPATH=src behave       # BDD: 50 escenarios Gherkin en español (Windows: set PYTHONPATH=src)
```

## Qué incluye

| Práctica | Herramienta | Dónde |
|---|---|---|
| **TDD** (pruebas unitarias, mocks, parametrización) | `pytest`, `unittest.mock`, `pytest-cov` | `tests/` |
| **BDD** (Given/When/Then en español) | `behave` + Gherkin | `features/` y `features/steps/` |
| **Calidad continua** | GitHub Actions (cobertura mínima 90 %) | `.github/workflows/ci.yml` |
| **Agilidad** (roles, backlog, iteraciones, DoD, retrospectiva) | Documentos | `docs/` |

## Módulos

- **Proveedores**: NIT único y válido, correo válido, nombre obligatorio; "eliminar" = desactivar, y no se permite con órdenes activas.
- **Cotizaciones**: solo sobre solicitudes `ABIERTA`, monto > 0, sin duplicados del mismo proveedor; cálculo de totales.
- **Órdenes de compra**: aprobación dentro del presupuesto del proveedor, sin re-aprobar, descontando presupuesto.
- **Inventario**: código único, categoría obligatoria, stock ≥ 0, retiros sin stock negativo, historial y alertas de stock mínimo.
- **Roles**: Administrador (todo) · Gestión de proveedores (Resumen, Proveedores, Órdenes) · Gestión de cotizaciones (Resumen, Cotizaciones, Inventario y alertas), con validación de correo/contraseña.

## Estructura

```
src/abasto/        lógica de negocio (services + repositorios en memoria)
tests/             pruebas unitarias pytest
features/          escenarios .feature + steps de behave
docs/              plan ágil, backlog, DoD, ciclo TDD, evidencias
```

Los repositorios en memoria (`repositories.py`) se reemplazan por la base de datos del ERP sin tocar los servicios.

## Referencias (APA 7)

- Behave. (s. f.). *Behave documentation*. https://behave.readthedocs.io/
- Beck, K. (2002). *Test-driven development: By example*. Addison-Wesley.
- North, D. (2006). Introducing BDD. *Better Software*. https://dannorth.net/introducing-bdd/
- pytest. (s. f.). *pytest documentation*. https://docs.pytest.org/
- Schwaber, K., & Sutherland, J. (2020). *La guía de Scrum*. https://scrumguides.org/
