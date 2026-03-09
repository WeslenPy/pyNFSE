"""Schemas para LoteRps."""
from typing import List
from pydantic import BaseModel

from pynfse.schemas.nfse import InfoRPS


class LoteRps(BaseModel):
    """Schema para LoteRps - container que agrupa múltiplos RPS."""
    numero_lote: int
    cnpj: str
    inscricao_municipal: int
    quantidade_rps: int
    lista_rps: List[InfoRPS]
    id: str = ""  # Identificador único para assinatura digital


