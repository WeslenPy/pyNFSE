from typing import Optional
from pydantic import Field
from pynfse.integration.carnaubal.abrasf.models.base import ABRASFNode
from pynfse.integration.carnaubal.abrasf.models.rps import IdentificacaoRps, IdentificacaoPrestador

CONSULTAR_NFSE_RPS_ENVIO_NS = "http://ws.speedgov.com.br/consultar_nfse_rps_envio_v1.xsd"

class ConsultarNfseRpsEnvio(ABRASFNode):
    """
    Classe para representar o XML de consulta de NFSe por RPS.
    Baseado no schema consultar_nfse_rps_envio_v1.xsd.
    """
    xml_child_namespace = CONSULTAR_NFSE_RPS_ENVIO_NS

    identificacao_rps: IdentificacaoRps = Field(
        ...,
        alias="IdentificacaoRps",
        json_schema_extra={"xml_namespace": None, "xml_child_namespace": None},
    )
    prestador: IdentificacaoPrestador = Field(
        ...,
        alias="Prestador",
        json_schema_extra={"xml_namespace": None, "xml_child_namespace": None},
    )
