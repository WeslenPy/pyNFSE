from typing import Optional, Annotated
from pydantic import Field, StringConstraints
from pynfse.integration.carnaubal.abrasf.models.base import (
    ABRASFNode,
    ABRASFTypesNode,
    tsCnpj,
    tsInscricaoMunicipal,
    tsCodigoMunicipioIbge,
    tsNumeroNfse,
    tsCodigoCancelamentoNfse,
    tsIdTag,
)
from pynfse.common.signature import Signature

class IdentificacaoNfse(ABRASFTypesNode):
    numero: tsNumeroNfse = Field(..., alias="Numero")
    cnpj: tsCnpj = Field(..., alias="Cnpj")
    inscricao_municipal: Optional[tsInscricaoMunicipal] = Field(None, alias="InscricaoMunicipal")
    codigo_municipio: tsCodigoMunicipioIbge = Field(..., alias="CodigoMunicipio")

class InfPedidoCancelamento(ABRASFTypesNode):
    id: Optional[Annotated[str, StringConstraints(max_length=255)]] = Field(None, alias="Id")
    identificacao_nfse: IdentificacaoNfse = Field(..., alias="IdentificacaoNfse")
    codigo_cancelamento: tsCodigoCancelamentoNfse = Field(..., alias="CodigoCancelamento")

class PedidoCancelamento(ABRASFTypesNode):
    inf_pedido_cancelamento: InfPedidoCancelamento = Field(..., alias="InfPedidoCancelamento")
    signature: Optional[Signature] = Field(
        None,
        alias="Signature",
        json_schema_extra={
            "xml_namespace": None,
            "xml_child_namespace": None,
            "xml_reset_default_namespace": False,
        },
    )

class CancelarNfseEnvio(ABRASFNode):
    pedido: PedidoCancelamento = Field(
        ...,
        alias="Pedido",
        json_schema_extra={"xml_namespace": None, "xml_child_namespace": None},
    )
