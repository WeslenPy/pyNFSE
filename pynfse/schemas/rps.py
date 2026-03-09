from typing import Optional
from pydantic import BaseModel


class BaseNFSE(BaseModel):
    cnpj: str
    municipal_registration:int
    municipality_code:Optional[str] = None
    number: Optional[int] = None


class CancelNFSE(BaseNFSE):
    cancellation_code:str = 'E12'
    municipality_code:str 

class ConsultNFSE(BaseNFSE):
    number: int
    serie: str

class ConsultLoteNFSE(BaseNFSE):
    protocol:str

class ConsultLoteRPS(BaseNFSE):
    protocol:str

