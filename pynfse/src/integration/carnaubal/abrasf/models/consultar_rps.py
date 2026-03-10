from typing import Optional
from pydantic import Field
from pynfse.src.integration.carnaubal.abrasf.models.base import ABRASFNode
from pynfse.src.integration.carnaubal.abrasf.models.rps import IdentificacaoRps, IdentificacaoPrestador

class ConsultarNfseRpsEnvio(ABRASFNode):
    """
    Classe para representar o XML de consulta de NFSe por RPS.
    Baseado no schema consultar_nfse_rps_envio_v1.xsd.
    """
    identificacao_rps: IdentificacaoRps = Field(..., alias="IdentificacaoRps")
    prestador: IdentificacaoPrestador = Field(..., alias="Prestador")
