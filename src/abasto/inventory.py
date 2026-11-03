from dataclasses import replace

from .errors import InsufficientStockError, InvalidProductError
from .models import Product

MENSAJES = {
    "REGISTRADO": "Producto registrado",
    "RETIRO_OK": "Retiro exitoso",
    "STOCK_INSUFICIENTE": "Stock insuficiente",
}


class InventoryService:
    def __init__(self, repo):
        self.repo = repo

    def exists_by_code(self, codigo):
        return self.repo.exists_by_code(codigo)

    def register_product(self, codigo, nombre, categoria, stock=0, stock_minimo=0):
        if not codigo or not str(codigo).strip():
            raise InvalidProductError("El código es obligatorio")
        if not categoria or not str(categoria).strip():
            raise InvalidProductError("La categoría es obligatoria")
        if not isinstance(stock, int) or stock < 0:
            raise InvalidProductError("El stock inicial debe ser mayor o igual a cero")
        if self.repo.exists_by_code(codigo):
            raise InvalidProductError("El código ya existe")
        producto = self.repo.save(Product(codigo, nombre, categoria, stock, stock_minimo))
        self.repo.add_movement(codigo, "ALTA", stock)
        return producto

    def register_entry(self, codigo, cantidad):
        self._validar_cantidad(cantidad)
        p = self._get(codigo)
        actualizado = self.repo.save(replace(p, stock=p.stock + cantidad))
        self.repo.add_movement(codigo, "ENTRADA", cantidad)
        return actualizado

    def withdraw(self, codigo, cantidad):
        self._validar_cantidad(cantidad)
        p = self._get(codigo)
        if cantidad > p.stock:
            raise InsufficientStockError(MENSAJES["STOCK_INSUFICIENTE"])
        actualizado = self.repo.save(replace(p, stock=p.stock - cantidad))
        self.repo.add_movement(codigo, "SALIDA", cantidad)
        return actualizado

    def get_stock(self, codigo):
        return self._get(codigo).stock

    def get_history(self, codigo):
        return self.repo.get_movements(codigo)

    def get_low_stock_alerts(self):
        """Productos con stock por debajo del mínimo configurado."""
        return [p for p in self.repo.find_all() if p.stock_minimo > 0 and p.stock < p.stock_minimo]

    @staticmethod
    def _validar_cantidad(cantidad):
        if not cantidad > 0:
            raise InvalidProductError("La cantidad debe ser mayor que cero")

    def _get(self, codigo):
        p = self.repo.find_by_code(codigo)
        if p is None:
            raise InvalidProductError("Producto no encontrado")
        return p
