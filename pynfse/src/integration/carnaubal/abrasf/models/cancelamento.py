from typing import Optional
from pydantic import Field
from pynfse.src.integration.carnaubal.abrasf.models.base import ABRASFNode, tsCnpj, tsInscricaoMunicipal, tsCodigoMunicipioIbge
from pynfse.src.common.signature import Signature

class IdentificacaoNfse(ABRASFNode):
    numero: int = Field(..., alias="Numero")
    cnpj: tsCnpj = Field(..., alias="Cnpj")
    inscricao_municipal: Optional[tsInscricaoMunicipal] = Field(None, alias="InscricaoMunicipal")
    codigo_municipio: tsCodigoMunicipioIbge = Field(..., alias="CodigoMunicipio")

class InfPedidoCancelamento(ABRASFNode):
    id: Optional[str] = Field(None, alias="Id")
    identificacao_nfse: IdentificacaoNfse = Field(..., alias="IdentificacaoNfse")
    codigo_cancelamento: str = Field(..., alias="CodigoCancelamento")

class PedidoCancelamento(ABRASFNode):
    inf_pedido_cancelamento: InfPedidoCancelamento = Field(..., alias="InfPedidoCancelamento")
    signature: Optional[Signature] = Field(None, alias="Signature")

class CancelarNfseEnvio(ABRASFNode):
    pedido: PedidoCancelamento = Field(..., alias="Pedido")
