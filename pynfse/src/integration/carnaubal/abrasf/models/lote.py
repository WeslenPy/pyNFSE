from typing import List, Optional, Annotated
from pydantic import Field, StringConstraints
from pynfse.src.integration.carnaubal.abrasf.models.base import ABRASFNode, tsNumero, tsCnpj, tsInscricaoMunicipal
from pynfse.src.common.signature import Signature
from pynfse.src.integration.carnaubal.abrasf.models.rps import Rps

class ListaRps(ABRASFNode):
    rps: List[Rps] = Field(..., alias="Rps")

class LoteRps(ABRASFNode):
    id: Optional[Annotated[str, StringConstraints(max_length=255)]] = Field(None, alias="Id")
    numero_lote: tsNumero = Field(..., alias="NumeroLote")
    cnpj: tsCnpj = Field(..., alias="Cnpj")
    inscricao_municipal: tsInscricaoMunicipal = Field(..., alias="InscricaoMunicipal")
    quantidade_rps: Annotated[int, Field(ge=0, le=9999)] = Field(..., alias="QuantidadeRps")
    lista_rps: ListaRps = Field(..., alias="ListaRps")
    signature: Optional[Signature] = Field(None, alias="Signature")

class EnviarLoteRpsEnvio(ABRASFNode):
    lote_rps: LoteRps = Field(..., alias="LoteRps")
    signature: Optional[Signature] = Field(None, alias="Signature")
