"""
Tipos e estruturas base para SpeedGov (enviar_lote_rps.xml).
Estrutura simplificada conforme referência - sem blocos opcionais ABRASF.
"""
from datetime import date, datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field, ConfigDict, model_validator

# Tipos conforme XSD tipos_v1.xsd
class CpfCnpj(BaseModel):
    """Cpf ou Cnpj - exatamente um."""
    model_config = ConfigDict(populate_by_name=True)

    cpf: Optional[str] = Field(None, alias="Cpf", min_length=11, max_length=11)# CPF
    cnpj: Optional[str] = Field(None, alias="Cnpj", min_length=14, max_length=14)# CNPJ

    @model_validator(mode="after")
    def validate_choice(self):
        if bool(self.cpf) == bool(self.cnpj):
            raise ValueError("CpfCnpj deve conter exatamente um entre Cpf ou Cnpj.")# CpfCnpj deve conter exatamente um entre Cpf ou Cnpj.
        return self


class Endereco(BaseModel):
    """Endereco do Tomador - sem Contato."""
    model_config = ConfigDict(populate_by_name=True)

    endereco: str = Field(..., alias="Endereco", max_length=125)# endereço
    numero: str = Field(..., alias="Numero", max_length=10)# número
    complemento: Optional[str] = Field(None, alias="Complemento", max_length=60)# complemento
    bairro: str = Field(..., alias="Bairro", max_length=60)# bairro
    codigo_municipio: int = Field(..., alias="CodigoMunicipio", ge=0, le=9999999)# código do municipio
    uf: str = Field(..., alias="Uf", min_length=2, max_length=2)# uf
    cep: str = Field(..., alias="Cep", max_length=10)# cep
