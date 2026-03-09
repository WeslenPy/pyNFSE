"""Fixtures compartilhadas para os testes."""
import pytest
from datetime import date
from unittest.mock import Mock, MagicMock
from requests import Response

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
from pynfse.schemas.rps import (
    BaseNFSE,
    CancelNFSE,
    ConsultNFSE,
    ConsultLoteNFSE,
    ConsultLoteRPS,
)


@pytest.fixture
def sample_identification_nfse():
    """Fixture para IdentificationNFSE."""
    return IdentificationNFSE(
        number=123,
        serie="A",
        typer=1
    )


@pytest.fixture
def sample_values_nfse():
    """Fixture para ValuesNFSE."""
    return ValuesNFSE(
        value_services=1000.0,
        value_deductions=0.0,
        value_pis=0.0,
        value_cofins=0.0,
        value_inss=0.0,
        value_ir=0.0,
        value_csll=0.0,
        iss_retido=2,
        value_iss=50.0,
        value_iss_retido=0.0,
        others_retentions=0.0,
        base_calculation=1000.0,
        aliquot=5.0,
        liquid_value=950.0,
        discount_conditioned=0.0,
        discount_unconditioned=0.0,
    )


@pytest.fixture
def sample_provider_nfse():
    """Fixture para ProviderNFSE."""
    return ProviderNFSE(
        cnpj="12345678000190",
        municipal_registration=12345
    )


@pytest.fixture
def sample_address_nfse():
    """Fixture para AddressNFSE."""
    return AddressNFSE(
        address="Rua Teste",
        number="123",
        complement="Apto 101",
        district="Centro",
        ibge_code="2408102",
        uf="RN",
        zip_code="59000000"
    )


@pytest.fixture
def sample_identification_costumer_nfse():
    """Fixture para IdentificationCostumerNFSE."""
    return IdentificationCostumerNFSE(
        cpf_cnpj="12345678901"
    )


@pytest.fixture
def sample_costumer_nfse(sample_identification_costumer_nfse, sample_address_nfse):
    """Fixture para CostumerNFSE."""
    return CostumerNFSE(
        identification=sample_identification_costumer_nfse,
        social_name="Cliente Teste LTDA",
        address=sample_address_nfse
    )


@pytest.fixture
def sample_services_nfse(sample_values_nfse, sample_provider_nfse):
    """Fixture para ServicesNFSE."""
    return ServicesNFSE(
        item_list_service=106,
        code_cnae="6204000",
        code_tributation_municipio="620400000",
        description="Serviço de desenvolvimento de software",
        code_municipio="2408102",
        values=sample_values_nfse
    )


@pytest.fixture
def sample_info_rps(
    sample_identification_nfse,
    sample_costumer_nfse,
    sample_services_nfse,
    sample_provider_nfse
):
    """Fixture para InfoRPS completo."""
    return InfoRPS(
        identification=sample_identification_nfse,
        costumer=sample_costumer_nfse,
        services=sample_services_nfse,
        provider=sample_provider_nfse,
        date=date(2024, 1, 15),
        nature_of_operation=1,
        regime_special_tributation=6,
        optant_simple_national=1,
        incentivator_cultural=2,
        status=1
    )


@pytest.fixture
def sample_base_nfse():
    """Fixture para BaseNFSE."""
    return BaseNFSE(
        cnpj="12345678000190",
        municipal_registration=12345,
        municipality_code="2408102",
        number=123
    )


@pytest.fixture
def sample_cancel_nfse():
    """Fixture para CancelNFSE."""
    return CancelNFSE(
        cnpj="12345678000190",
        municipal_registration=12345,
        municipality_code="2408102",
        number=123,
        cancellation_code="E12"
    )


@pytest.fixture
def sample_consult_nfse():
    """Fixture para ConsultNFSE."""
    return ConsultNFSE(
        cnpj="12345678000190",
        municipal_registration=12345,
        number=123,
        serie="A"
    )


@pytest.fixture
def sample_consult_lote_nfse():
    """Fixture para ConsultLoteNFSE."""
    return ConsultLoteNFSE(
        cnpj="12345678000190",
        municipal_registration=12345,
        protocol="123456789"
    )


@pytest.fixture
def sample_consult_lote_rps():
    """Fixture para ConsultLoteRPS."""
    return ConsultLoteRPS(
        cnpj="12345678000190",
        municipal_registration=12345,
        protocol="123456789"
    )


@pytest.fixture
def mock_response():
    """Fixture para mock de Response do requests."""
    response = Mock(spec=Response)
    response.status_code = 200
    response.text = "<xml>response</xml>"
    response.json.return_value = {"status": "ok"}
    response.headers = {"Content-Type": "application/json"}
    response.content = b"test content"
    return response


@pytest.fixture
def mock_session():
    """Fixture para mock de Session do requests."""
    session = MagicMock()
    response = Mock(spec=Response)
    response.status_code = 200
    response.text = "<xml>response</xml>"
    response.json.return_value = {"status": "ok"}
    response.headers = {"Content-Type": "application/json"}
    session.post.return_value = response
    return session

