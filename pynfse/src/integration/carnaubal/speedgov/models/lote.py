"""
Modelos de Lote para SpeedGov - estrutura enviar_lote_rps.xml.
p:LoteRps com filhos p1: (tipos).
"""
from typing import ClassVar, List, Optional

from pydantic import Field, ConfigDict

from pynfse.src.integration.carnaubal.speedgov.constants import ENVIO_NS, TIPOS_NS
from pynfse.src.integration.carnaubal.speedgov.models.base import SpeedGovNode
from pynfse.src.integration.carnaubal.speedgov.models.rps import Rps


class ListaRps(SpeedGovNode):
    model_config = ConfigDict(populate_by_name=True)

    rps: List[Rps] = Field(..., alias="Rps")


class LoteRps(SpeedGovNode):
    """LoteRps - p:LoteRps com filhos em p1: (TIPOS_NS)."""
    model_config = ConfigDict(populate_by_name=True)
    xml_child_namespace: ClassVar[Optional[str]] = TIPOS_NS

    id: Optional[str] = Field("", alias="Id")
    numero_lote: int = Field(..., alias="NumeroLote", ge=0)
    cnpj: str = Field(..., alias="Cnpj", min_length=14, max_length=14)
    inscricao_municipal: str = Field(..., alias="InscricaoMunicipal", min_length=1, max_length=15)
    quantidade_rps: int = Field(..., alias="QuantidadeRps", ge=0, le=9999)
    lista_rps: ListaRps = Field(..., alias="ListaRps")


class EnviarLoteRpsEnvio(SpeedGovNode):
    """EnviarLoteRpsEnvio - p:EnviarLoteRpsEnvio."""
    model_config = ConfigDict(populate_by_name=True)
    xml_child_namespace: ClassVar[Optional[str]] = ENVIO_NS

    lote_rps: LoteRps = Field(..., alias="LoteRps")
