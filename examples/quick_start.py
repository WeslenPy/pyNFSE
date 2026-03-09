"""
Quick Start - Guia rápido de uso da biblioteca pyNFSE.

Este é um exemplo mínimo para começar a usar a biblioteca rapidamente.
"""

from pynfse.schemas.lote import LoteRps
from pynfse.src.integration.carnaubal.abrasf.nfse import CarnaubalNFSe

from datetime import date
from pynfse.schemas.nfse import (
    InfoRPS,
    IdentificationNFSE,
    ValuesNFSE,
    ProviderNFSE,
    ServicesNFSE,
    IdentificationCostumerNFSE,
    AddressNFSE,
    CostumerNFSE,
)


def criar_nfse_rapido():
    """
    Cria uma NFSE rapidamente com o mínimo de informações necessárias.
    
    Este exemplo mostra a forma mais simples de criar uma NFSE válida.
    """
    
    # Passo 1: Criar os valores (campos obrigatórios)
    valores = ValuesNFSE(
        value_services=1000.00,
        value_iss=50.00,
        base_calculation=1000.00,
        aliquot=5.0,
        liquid_value=950.00
    )
    
    # Passo 2: Criar o serviço
    servico = ServicesNFSE(
        description="Desenvolvimento de software",
        code_municipio="2408102",  # Código IBGE do município
        values=valores
    )
    
    # Passo 3: Criar o InfoRPS completo
    nfse = InfoRPS(
        identification=IdentificationNFSE(number=1, serie="A"),
        costumer=CostumerNFSE(
            identification=IdentificationCostumerNFSE(cpf_cnpj="12345678901"),
            social_name="Cliente Exemplo",
            address=AddressNFSE(
                address="Rua Exemplo",
                number="123",
                district="Centro",
                uf="RN",
                zip_code="59000000"
            )
        ),
        services=servico,
        provider=ProviderNFSE(
            cnpj="12345678000190",
            municipal_registration=12345
        ),
        date=date.today()
    )
    
    return nfse



if __name__ == "__main__":
    print("Criando NFSE...")
    nfse = criar_nfse_rapido()
    
    print(f"\n✅ NFSE criada com sucesso!")
    print(f"   Número: {nfse.identification.number}")
    print(f"   Série: {nfse.identification.serie}")
    print(f"   Data: {nfse.date}")
    print(f"   Valor: R$ {nfse.services.values.value_services:.2f}")
    print(f"   Tomador: {nfse.costumer.social_name}")


    lote_rps = LoteRps(
        id="lote_001",
        numero_lote=1,
        cnpj=nfse.provider.cnpj,
        inscricao_municipal=nfse.provider.municipal_registration,
        quantidade_rps=1,
        lista_rps=[nfse]
    )

    nfse_carnaubal = CarnaubalNFSe(URL="http://speedgov.com.br/wsmod/Nfes?wsdl")
    response = nfse_carnaubal.send_nfse(lote_rps)
    print(f"Response: {response.response.content}")




