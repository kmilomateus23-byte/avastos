# Evidencia del ciclo TDD (Rojo → Verde → Refactor)

## Ejemplo real: validación del monto de una cotización
1. **Rojo**: se escribió `test_rechaza_montos_no_numericos` con `[None, "100", True, nan]`.
   El caso `nan` **falló**: `float("nan") <= 0` es `False`, así que un monto inválido pasaba la validación.
2. **Verde**: se cambió la condición de `monto <= 0` a `not monto > 0` en `src/abasto/quotations.py`.
3. **Refactor**: se mantuvo el mensaje de negocio ("El monto debe ser mayor que cero") y el mensaje de pantalla ("Monto inválido") en `DomainError.mensaje_ui`.

## Sugerencia de commits (uno por paso)
```
test(proveedores): rojo - rechaza NIT duplicado
feat(proveedores): verde - valida NIT único
refactor(proveedores): extrae constantes de validación
```
Hagan al menos un commit por cada paso del ciclo y por integrante para evidenciar el trabajo individual.

## Comandos
```bash
pytest -x               # detener en el primer fallo (rojo)
pytest --cov-report=html && open htmlcov/index.html
PYTHONPATH=src behave --tags=@wip
```
