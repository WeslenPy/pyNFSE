from typing import List, Optional, Annotated
from pydantic import Field, StringConstraints
from pynfse.src.integration.carnaubal.abrasf.models.base import (
    ABRASFNode,
    ABRASFTypesNode,
    tsNumero,
    tsCnpj,
    tsInscricaoMunicipal,
)
from pynfse.src.common.signature import Signature
from pynfse.src.integration.carnaubal.abrasf.models.rps import Rps

ENVIAR_LOTE_RPS_ENVIO_NS = "http://ws.speedgov.com.br/enviar_lote_rps_envio_v1.xsd"
XMLDSIG_NS = "http://www.w3.org/2000/09/xmldsig#"

class ListaRps(ABRASFTypesNode):
    rps: List[Rps] = Field(..., alias="Rps")

class LoteRps(ABRASFTypesNode):
    id: Optional[Annotated[str, StringConstraints(max_length=255)]] = Field(None, alias="Id")
    numero_lote: tsNumero = Field(..., alias="NumeroLote")
    cnpj: tsCnpj = Field(..., alias="Cnpj")
    inscricao_municipal: tsInscricaoMunicipal = Field(..., alias="InscricaoMunicipal")
    quantidade_rps: Annotated[int, Field(ge=0, le=9999)] = Field(..., alias="QuantidadeRps")
    lista_rps: ListaRps = Field(..., alias="ListaRps")
    signature: Optional[Signature] = Field(
        None,
        alias="Signature",
        json_schema_extra={
            "xml_namespace": None,
            "xml_child_namespace": None,
            "xml_reset_default_namespace": False,
        },
    )

class EnviarLoteRpsEnvio(ABRASFNode):
    xml_child_namespace = ENVIAR_LOTE_RPS_ENVIO_NS

    # LoteRps e filhos sem namespace (xmlns="") conforme referência
    lote_rps: LoteRps = Field(
        ...,
        alias="LoteRps",
        json_schema_extra={"xml_namespace": None, "xml_child_namespace": None},
    )
    signature: Optional[Signature] = Field(
        None,
        alias="Signature",
        json_schema_extra={
            "xml_namespace": XMLDSIG_NS,
            "xml_child_namespace": None,
            "xml_reset_default_namespace": False,
        },
    )
