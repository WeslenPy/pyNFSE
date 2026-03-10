from datetime import date
from typing import Optional
from pydantic import Field
from pynfse.src.integration.carnaubal.abrasf.models.base import ABRASFNode, tsNumero
from pynfse.src.integration.carnaubal.abrasf.models.rps import IdentificacaoPrestador, IdentificacaoTomador, IdentificacaoIntermediarioServico

class PeriodoEmissao(ABRASFNode):
    data_inicial: date = Field(..., alias="DataInicial")
    data_final: date = Field(..., alias="DataFinal")

class ConsultarNfseEnvio(ABRASFNode):
    prestador: IdentificacaoPrestador = Field(..., alias="Prestador")
    numero_nfse: Optional[tsNumero] = Field(None, alias="NumeroNfse")
    periodo_emissao: Optional[PeriodoEmissao] = Field(None, alias="PeriodoEmissao")
    tomador: Optional[IdentificacaoTomador] = Field(None, alias="Tomador")
    intermediario_servico: Optional[IdentificacaoIntermediarioServico] = Field(None, alias="IntermediarioServico")
