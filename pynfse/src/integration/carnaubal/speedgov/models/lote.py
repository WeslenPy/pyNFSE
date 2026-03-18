"""
Modelos de Lote para SpeedGov - estrutura enviar_lote_rps.xml.
p:LoteRps com filhos p1: (tipos).
"""
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict

from pynfse.src.integration.carnaubal.speedgov.models.rps import Rps


class ListaRps(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    rps: List[Rps] = Field(..., alias="Rps")# lista de RPS


class LoteRps(BaseModel):
    """LoteRps - p:LoteRps com filhos em p1:."""
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[str] = Field("", alias="Id")# id do lote
    numero_lote: int = Field(..., alias="NumeroLote", ge=0)# número do lote 
    cnpj: str = Field(..., alias="Cnpj", min_length=14, max_length=14)# CNPJ do prestador
    inscricao_municipal: str = Field(..., alias="InscricaoMunicipal", min_length=1, max_length=15)# inscrição municipal do prestador
    quantidade_rps: int = Field(..., alias="QuantidadeRps", ge=0, le=9999)# quantidade de RPS
    lista_rps: ListaRps = Field(..., alias="ListaRps")# lista de RPS


class EnviarLoteRpsEnvio(BaseModel):
    """EnviarLoteRpsEnvio - p:EnviarLoteRpsEnvio."""
    model_config = ConfigDict(populate_by_name=True)

    lote_rps: LoteRps = Field(..., alias="LoteRps")# lote de RPS
