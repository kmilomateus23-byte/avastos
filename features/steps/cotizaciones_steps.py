from behave import given, when

from abasto.models import QuotationRequest
from abasto.quotations import MENSAJES


@given('que existe una solicitud "{id_}" en estado "{estado}"')
def step_solicitud(context, id_, estado):
    context.solicitud_id = id_
    context.request_repo.save(QuotationRequest(id_, estado))


@given('el proveedor ya cotizó la solicitud "{id_}"')
def step_ya_cotizo(context, id_):
    context.quotations.create_quotation(id_, "PROV-1", 100000)


@when("registro una cotización por {monto:d}")
def step_cotizar(context, monto):
    context.intentar(
        lambda: context.quotations.create_quotation(context.solicitud_id, "PROV-1", monto),
        MENSAJES["REGISTRADA"],
    )
