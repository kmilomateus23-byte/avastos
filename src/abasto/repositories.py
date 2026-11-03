"""Repositorios en memoria. Sustituibles por la base de datos real del ERP."""
from dataclasses import replace
from datetime import datetime, timezone

ESTADOS_ORDEN_ACTIVOS = ("PENDIENTE", "APROBADA", "ENVIADA")


class InMemorySupplierRepository:
    def __init__(self):
        self.items, self._seq = {}, 1

    def exists_by_nit(self, nit):
        return nit in self.items

    def find_by_nit(self, nit):
        return self.items.get(nit)

    def save(self, supplier):
        if supplier.id is None:
            supplier = replace(supplier, id=self._seq)
            self._seq += 1
        self.items[supplier.nit] = supplier
        return supplier

    def find_all(self):
        return list(self.items.values())


class InMemoryQuotationRequestRepository:
    def __init__(self):
        self.items = {}

    def find_by_id(self, id_):
        return self.items.get(id_)

    def save(self, request):
        self.items[request.id] = request
        return request


class InMemoryQuotationRepository:
    def __init__(self):
        self.items, self._seq = [], 1

    def find_by_solicitud_and_proveedor(self, solicitud_id, proveedor_id):
        return next(
            (q for q in self.items
             if q.solicitud_id == solicitud_id and q.proveedor_id == proveedor_id),
            None,
        )

    def save(self, quotation):
        saved = replace(quotation, id=self._seq)
        self._seq += 1
        self.items.append(saved)
        return saved

    def find_all(self):
        return list(self.items)


class InMemoryPurchaseOrderRepository:
    def __init__(self):
        self.orders, self.budgets, self._seq = {}, {}, 1

    def find_by_id(self, id_):
        return self.orders.get(id_)

    def save(self, order):
        if order.id is None:
            order = replace(order, id=self._seq)
            self._seq += 1
        self.orders[order.id] = order
        return order

    def get_budget(self, proveedor_id):
        return self.budgets.get(proveedor_id, 0)

    def set_budget(self, proveedor_id, valor):
        self.budgets[proveedor_id] = valor

    def has_active_orders(self, proveedor_id):
        return any(
            o.proveedor_id == proveedor_id and o.estado in ESTADOS_ORDEN_ACTIVOS
            for o in self.orders.values()
        )


class InMemoryProductRepository:
    def __init__(self):
        self.products, self.movements = {}, []

    def exists_by_code(self, codigo):
        return codigo in self.products

    def find_by_code(self, codigo):
        return self.products.get(codigo)

    def save(self, product):
        self.products[product.codigo] = product
        return product

    def find_all(self):
        return list(self.products.values())

    def add_movement(self, codigo, tipo, cantidad):
        self.movements.append({
            "codigo": codigo, "tipo": tipo, "cantidad": cantidad,
            "fecha": datetime.now(timezone.utc).isoformat(),
        })

    def get_movements(self, codigo):
        return [m for m in self.movements if m["codigo"] == codigo]
