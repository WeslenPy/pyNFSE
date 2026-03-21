"""
Funções puras de cálculo para NFS-e - Valores e IBSCBS.
Usado pelos model_validators dos modelos Valores e IBSCBS.
"""
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

QUANTIZE = Decimal("0.01")


def _round2(value: Decimal) -> Decimal:
    """Arredonda para 2 casas decimais (moeda)."""
    if value is None:
        return value
    return value.quantize(QUANTIZE, rounding=ROUND_HALF_UP)


def _to_decimal(v) -> Decimal:
    """Converte int/float para Decimal."""
    if v is None:
        return Decimal(0)
    return Decimal(str(v))


def calc_base_calculo(valor_servicos: float, valor_deducoes: float) -> Decimal:
    """BaseCalculo = ValorServicos - ValorDeducoes."""
    vs = _to_decimal(valor_servicos)
    vd = _to_decimal(valor_deducoes)
    return _round2(vs - vd)


def calc_valor_iss(base_calculo: float, aliquota: float) -> Decimal:
    """ValorIss = BaseCalculo * Aliquota."""
    bc = _to_decimal(base_calculo)
    aliq = _to_decimal((aliquota/100))
    return _round2(bc * aliq)


def calc_pis_valor(
    base_calculo_pis_cofins: float,
    aliq_pis: float,
) -> Optional[Decimal]:
    """ValorPis = BaseCalculoPisCofins * AliqPis. Retorna None se aliq_pis <= 0."""
    if not aliq_pis or aliq_pis <= 0:
        return None
    base = _to_decimal(base_calculo_pis_cofins)
    aliq = _to_decimal(aliq_pis)
    return _round2(base * aliq)


def calc_cofins_valor(
    base_calculo_pis_cofins: float,
    aliq_cofins: float,
) -> Optional[Decimal]:
    """ValorCofins = BaseCalculoPisCofins * AliqCofins. Retorna None se aliq_cofins <= 0."""
    if not aliq_cofins or aliq_cofins <= 0:
        return None
    base = _to_decimal(base_calculo_pis_cofins)
    aliq = _to_decimal(aliq_cofins)
    return _round2(base * aliq)


def calc_valor_liquido_nfse(
    base_calculo: float,
    valor_pis: float,
    valor_cofins: float,
    valor_inss: float,
    valor_ir: float,
    valor_csll: float,
    outras_retencoes: float,
    iss_retido: int,
    valor_iss: float,
    valor_iss_retido: float,
) -> Decimal:
    """
    ValorLiquidoNfse = BaseCalculo - Σ(retenções).
    Retenções: PIS, COFINS, INSS, IR, CSLL, OutrasRetencoes,
    + (ValorIssRetido se IssRetido=1, senão ValorIss).
    IssRetido: 1=sim, 2=não.
    Conforme envio_lote.xml de referência.
    """
    bc = _to_decimal(base_calculo)
    total_retencoes = (
        _to_decimal(valor_pis)
        + _to_decimal(valor_cofins)
        + _to_decimal(valor_inss)
        + _to_decimal(valor_ir)
        + _to_decimal(valor_csll)
        + _to_decimal(outras_retencoes)
    )
    if iss_retido == 1:
        total_retencoes += _to_decimal(valor_iss_retido)
    else:
        total_retencoes += _to_decimal(valor_iss)

    liquido = bc - total_retencoes
    return _round2(max(Decimal(0), liquido))


def calc_aliquota_efetiva(aliq: Optional[Decimal], perc_reducao: Optional[Decimal]) -> Optional[Decimal]:
    """AliquotaEfetiva = Aliq * (1 - PercReducao). Não arredonda - alíquota pode ser 0.095."""
    if aliq is None:
        return None
    red = perc_reducao or Decimal(0)
    return aliq * (Decimal(1) - red)


def calc_valor_tributo(base: Decimal, aliq_efetiva: Optional[Decimal]) -> Optional[Decimal]:
    """Valor = Base * AliquotaEfetiva."""
    if base is None or aliq_efetiva is None:
        return None
    return _round2(base * aliq_efetiva)


def calc_diferido(valor: Optional[Decimal], perc_diferimento: Optional[Decimal]) -> Optional[Decimal]:
    """ValorDiferido = Valor * PercDiferimento."""
    if valor is None or perc_diferimento is None:
        return None
    return _round2(valor * perc_diferimento)


def calc_ibscbs(
    base: Decimal,
    aliq_uf: Optional[Decimal],
    aliq_mun: Optional[Decimal],
    aliq_cbs: Optional[Decimal],
    perc_reducao_uf: Optional[Decimal] = None,
    perc_reducao_mun: Optional[Decimal] = None,
    perc_reducao_cbs: Optional[Decimal] = None,
    perc_diferimento_uf: Optional[Decimal] = None,
    perc_diferimento_mun: Optional[Decimal] = None,
    perc_diferimento_cbs: Optional[Decimal] = None,
) -> dict:
    """
    Retorna dict com valores calculados de IBSCBS.
    Não inclui valor_total_com_tributos (requer valor_servicos do pai).
    """
    result = {}

    aliq_uf_ef = calc_aliquota_efetiva(aliq_uf, perc_reducao_uf)
    aliq_mun_ef = calc_aliquota_efetiva(aliq_mun, perc_reducao_mun)
    aliq_cbs_ef = calc_aliquota_efetiva(aliq_cbs, perc_reducao_cbs)

    valor_uf = calc_valor_tributo(base, aliq_uf_ef)
    valor_mun = calc_valor_tributo(base, aliq_mun_ef)
    valor_cbs = calc_valor_tributo(base, aliq_cbs_ef)

    result["ibsu_f_aliquota_efetiva"] = aliq_uf_ef
    result["ibs_mun_aliquota_efetiva"] = aliq_mun_ef
    result["cbs_aliquota_efetiva"] = aliq_cbs_ef
    result["ibsu_f_valor"] = valor_uf
    result["ibs_mun_valor"] = valor_mun
    result["cbs_valor"] = valor_cbs

    result["ibsu_f_valor_diferido"] = calc_diferido(valor_uf, perc_diferimento_uf)
    result["ibs_mun_valor_diferido"] = calc_diferido(valor_mun, perc_diferimento_mun)
    result["cbs_valor_diferido"] = calc_diferido(valor_cbs, perc_diferimento_cbs)

    ibs_total = (valor_uf or Decimal(0)) + (valor_mun or Decimal(0))
    result["ibs_valor_total"] = _round2(ibs_total) if ibs_total else None

    return result


def calc_valor_total_com_tributos(
    valor_servicos: float,
    ibs_valor_total: Decimal,
    cbs_valor: Decimal,
) -> Decimal:
    """ValorTotalComTributos = ValorServicos + IBSValorTotal + CBSValor."""
    vs = _to_decimal(valor_servicos)
    ibs = _to_decimal(ibs_valor_total)
    cbs = _to_decimal(cbs_valor)
    return _round2(vs + ibs + cbs)
