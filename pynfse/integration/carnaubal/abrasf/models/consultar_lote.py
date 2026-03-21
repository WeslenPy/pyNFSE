from typing import Optional, Annotated

from pydantic import Field, StringConstraints

from pynfse.common.signature import Signature
from pynfse.integration.carnaubal.abrasf.models.base import ABRASFNode, tsNumeroProtocolo
from pynfse.integration.carnaubal.abrasf.models.rps import IdentificacaoPrestador

CONSULTAR_LOTE_RPS_ENVIO_NS = "http://ws.speedgov.com.br/consultar_lote_rps_envio_v1.xsd"
CONSULTAR_SITUACAO_LOTE_RPS_ENVIO_NS = "http://ws.speedgov.com.br/consultar_situacao_lote_rps_envio_v1.xsd"


class ConsultarLoteRpsEnvio(ABRASFNode):
    xml_child_namespace = CONSULTAR_LOTE_RPS_ENVIO_NS

    id: Optional[Annotated[str, StringConstraints(max_length=255)]] = Field(None, alias="Id")
    prestador: IdentificacaoPrestador = Field(
        ...,
        alias="Prestador",
        json_schema_extra={"xml_namespace": None, "xml_child_namespace": None},
    )
    protocolo: tsNumeroProtocolo = Field(..., alias="Protocolo")
    signature: Optional[Signature] = Field(
        None,
        alias="Signature",
        json_schema_extra={
            "xml_namespace": None,
            "xml_child_namespace": None,
            "xml_reset_default_namespace": False,
        },
    )


class ConsultarSituacaoLoteRpsEnvio(ABRASFNode):
    xml_child_namespace = CONSULTAR_SITUACAO_LOTE_RPS_ENVIO_NS

    id: Optional[Annotated[str, StringConstraints(max_length=255)]] = Field(None, alias="Id")
    prestador: IdentificacaoPrestador = Field(
        ...,
        alias="Prestador",
        json_schema_extra={"xml_namespace": None, "xml_child_namespace": None},
    )
    protocolo: tsNumeroProtocolo = Field(..., alias="Protocolo")
    signature: Optional[Signature] = Field(
        None,
        alias="Signature",
        json_schema_extra={
            "xml_namespace": None,
            "xml_child_namespace": None,
            "xml_reset_default_namespace": False,
        },
    )
