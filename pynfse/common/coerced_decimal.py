"""
Decimal para campos tsValor (ABRASF): coerção segura a partir de float e
quantização em 2 casas decimais, alinhado a tipos_v1.xsd (fractionDigits=2, totalDigits=15).
"""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import Annotated, Any

from pydantic import BeforeValidator, Field

# tsValor: totalDigits 15, fractionDigits 2, minInclusive 0
_TS_VALOR_QUANT = Decimal("0.01")
_TS_VALOR_MAX = Decimal("9999999999999.99")


def _quantize_ts_valor(d: Decimal) -> Decimal:
    return d.quantize(_TS_VALOR_QUANT, rounding=ROUND_HALF_UP)


def _coerce_decimal(v: Any) -> Any:
    if v is None:
        return None
    if isinstance(v, bool):
        d = Decimal(int(v))
    elif isinstance(v, int):
        d = Decimal(v)
    elif isinstance(v, Decimal):
        d = v
    else:
        d = Decimal(str(v))
    return _quantize_ts_valor(d)


CoercedDecimal = Annotated[
    Decimal,
    BeforeValidator(_coerce_decimal),
    Field(ge=Decimal("0"), le=_TS_VALOR_MAX),
]
