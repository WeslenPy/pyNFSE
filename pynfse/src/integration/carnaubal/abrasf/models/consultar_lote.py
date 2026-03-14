from typing import Optional

from pydantic import Field

from pynfse.src.common.signature import Signature
from pynfse.src.integration.carnaubal.abrasf.models.base import ABRASFNode, tsNumeroProtocolo, tsIdTag
from pynfse.src.integration.carnaubal.abrasf.models.rps import IdentificacaoPrestador


class ConsultarLoteRpsEnvio(ABRASFNode):
    id: Optional[tsIdTag] = Field(None, alias="Id")
    prestador: IdentificacaoPrestador = Field(..., alias="Prestador")
    protocolo: tsNumeroProtocolo = Field(..., alias="Protocolo")
    signature: Optional[Signature] = Field(None, alias="Signature")


class ConsultarSituacaoLoteRpsEnvio(ABRASFNode):
    id: Optional[tsIdTag] = Field(None, alias="Id")
    prestador: IdentificacaoPrestador = Field(..., alias="Prestador")
    protocolo: tsNumeroProtocolo = Field(..., alias="Protocolo")
    signature: Optional[Signature] = Field(None, alias="Signature")
