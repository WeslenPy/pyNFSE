"""Coerção segura de float para Decimal em IBSCBS (evita lixo binário)."""
from decimal import Decimal

from pynfse.integration.carnaubal.speedgov.models.rps import IBSCBS


def test_ibscbs_base_calculo_float_sem_lixo_binario():
    ib = IBSCBS(ibscbs_base_calculo=15.4)
    assert ib.ibscbs_base_calculo == Decimal("15.40")
    assert str(ib.ibscbs_base_calculo) == "15.40"


def test_ibscbs_arredonda_para_duas_casas_ts_valor():
    ib = IBSCBS(ibscbs_base_calculo=15.456)
    assert ib.ibscbs_base_calculo == Decimal("15.46")
