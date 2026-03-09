from datetime import date
from typing import Optional
from pydantic import BaseModel



class IdentificationNFSE(BaseModel):
    number: int
    serie: str
    typer:int = 1

class ValuesNFSE(BaseModel):
    value_services:float
    value_deductions:float = 0.0
    value_pis:float = 0.0
    value_cofins:float = 0.0
    value_inss:float = 0.0
    value_ir:float = 0.0
    value_csll:float = 0.0
    iss_retido:int = 2
    value_iss:float

    value_iss_retido:float = 0.0
    others_retentions:float = 0.0
    base_calculation:float
    aliquot:float
    liquid_value:float
    discount_conditioned:float = 0.0
    discount_unconditioned:float = 0.0

class ProviderNFSE(BaseModel):
    cnpj:str
    municipal_registration:int

class ServicesNFSE(BaseModel):

    item_list_service:int = 106
    code_cnae:str = '6204000'
    code_tributation_municipio:str = '620400000'
    description:str
    code_municipio:str
    values:ValuesNFSE

class IdentificationCostumerNFSE(BaseModel):
    cpf_cnpj:str

class AddressNFSE(BaseModel):
    address:str
    number:str
    complement:Optional[str] = 'casa'
    district:str
    ibge_code:Optional[str] = None
    uf:str
    zip_code:str

class CostumerNFSE(BaseModel):
    identification:IdentificationCostumerNFSE
    social_name:str
    address:AddressNFSE


class InfoRPS(BaseModel):

    identification:IdentificationNFSE
    costumer:CostumerNFSE
    services:ServicesNFSE
    provider:ProviderNFSE
    date:date
    nature_of_operation:int = 1
    regime_special_tributation:int = 6
    optant_simple_national:int = 1  
    incentivator_cultural:int = 2

    status:int = 1 

