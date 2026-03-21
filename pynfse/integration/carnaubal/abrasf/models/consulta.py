from datetime import date
from typing import Optional
from pydantic import Field
from pynfse.integration.carnaubal.abrasf.models.base import ABRASFNode, ABRASFTypesNode, tsNumero
from pynfse.integration.carnaubal.abrasf.models.rps import IdentificacaoPrestador, IdentificacaoTomador, IdentificacaoIntermediarioServico

CONSULTAR_NFSE_ENVIO_NS = "http://ws.speedgov.com.br/consultar_nfse_envio_v1.xsd"

class PeriodoEmissao(ABRASFTypesNode):
    data_inicial: date = Field(..., alias="DataInicial")
    data_final: date = Field(..., alias="DataFinal")

class ConsultarNfseEnvio(ABRASFNode):
    xml_child_namespace = CONSULTAR_NFSE_ENVIO_NS

    prestador: IdentificacaoPrestador = Field(
        ...,
        alias="Prestador",
        json_schema_extra={"xml_namespace": None, "xml_child_namespace": None},
    )
    numero_nfse: Optional[tsNumero] = Field(None, alias="NumeroNfse")
    periodo_emissao: Optional[PeriodoEmissao] = Field(
        None,
        alias="PeriodoEmissao",
        json_schema_extra={"xml_namespace": None, "xml_child_namespace": None},
    )
    tomador: Optional[IdentificacaoTomador] = Field(
        None,
        alias="Tomador",
        json_schema_extra={"xml_namespace": None, "xml_child_namespace": None},
    )
    intermediario_servico: Optional[IdentificacaoIntermediarioServico] = Field(
        None,
        alias="IntermediarioServico",
        json_schema_extra={"xml_namespace": None, "xml_child_namespace": None},
    )
