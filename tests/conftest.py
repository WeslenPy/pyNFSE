"""Fixtures compartilhadas para os testes."""
import pytest
from datetime import datetime, date
from unittest.mock import Mock, MagicMock
from requests import Response

from pynfse.src.integration.carnaubal.abrasf.models.rps import (
    InfRps as InfoRPS,
    IdentificacaoRps as IdentificationNFSE,
    Valores as ValuesNFSE,
    IdentificacaoPrestador as ProviderNFSE,
    DadosServico as ServicesNFSE,
    IdentificacaoTomador as IdentificationCostumerNFSE,
    Endereco as AddressNFSE,
    DadosTomador as CostumerNFSE,
)
from pynfse.src.integration.carnaubal.abrasf.models.cancelamento import (
    CancelarNfseEnvio as CancelNFSE,
)
from pynfse.src.integration.carnaubal.abrasf.models.consulta import (
    ConsultarNfseEnvio as ConsultNFSE,
)
from pynfse.src.integration.carnaubal.abrasf.models.consultar_rps import (
    ConsultarNfseRpsEnvio as ConsultLoteRPS,
)
# BaseNFSE, ConsultLoteNFSE não têm equivalentes diretos simples ou não são mais usados assim


@pytest.fixture
def sample_identification_nfse():
    """Fixture para IdentificationNFSE."""
    return IdentificationNFSE(
        numero=123,
        serie="A",
        tipo=1
    )


@pytest.fixture
def sample_values_nfse():
    """Fixture para ValuesNFSE."""
    return ValuesNFSE(
        valor_servicos=1000.0,
        valor_deducoes=0.0,
        valor_pis=0.0,
        valor_cofins=0.0,
        valor_inss=0.0,
        valor_ir=0.0,
        valor_csll=0.0,
        iss_retido=2,
        valor_iss=50.0,
        valor_iss_retido=0.0,
        outras_retencoes=0.0,
        base_calculo=1000.0,
        aliquota=0.05,
        valor_liquido_nfse=950.0,
        desconto_condicionado=0.0,
        desconto_incondicionado=0.0,
    )


@pytest.fixture
def sample_provider_nfse():
    """Fixture para ProviderNFSE."""
    return ProviderNFSE(
        cnpj="12345678000190",
        inscricao_municipal="12345"
    )


@pytest.fixture
def sample_address_nfse():
    """Fixture para AddressNFSE."""
    return AddressNFSE(
        endereco="Rua Teste",
        numero="123",
        complemento="Apto 101",
        bairro="Centro",
        codigo_municipio=2408102,
        uf="RN",
        cep="59000000"
    )


@pytest.fixture
def sample_identification_costumer_nfse():
    """Fixture para IdentificationCostumerNFSE."""
    from pynfse.src.integration.carnaubal.abrasf.models.base import CpfCnpj
    return IdentificationCostumerNFSE(
        cpf_cnpj=CpfCnpj(cpf="12345678901")
    )


@pytest.fixture
def sample_costumer_nfse(sample_identification_costumer_nfse, sample_address_nfse):
    """Fixture para CostumerNFSE."""
    return CostumerNFSE(
        identificacao_tomador=sample_identification_costumer_nfse,
        razao_social="Cliente Teste LTDA",
        endereco=sample_address_nfse
    )


@pytest.fixture
def sample_services_nfse(sample_values_nfse, sample_provider_nfse):
    """Fixture para ServicesNFSE."""
    return ServicesNFSE(
        item_lista_servico="1.06",
        codigo_cnae="6204000",
        codigo_tributacao_municipio="620400000",
        discriminacao="Serviço de desenvolvimento de software",
        codigo_municipio=2408102,
        valores=sample_values_nfse
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
        identificacao_rps=sample_identification_nfse,
        tomador=sample_costumer_nfse,
        servico=sample_services_nfse,
        prestador=sample_provider_nfse,
        data_emissao=datetime(2024, 1, 15),
        natureza_operacao=1,
        regime_special_tributation=6,
        optante_simples_national=1,
        incentivador_cultural=2,
        status=1
    )


@pytest.fixture
def sample_base_nfse():
    """Fixture para BaseNFSE."""
    return {
        "cnpj": "12345678000190",
        "municipal_registration": "12345",
        "municipality_code": 2408102,
        "number": 123
    }


@pytest.fixture
def sample_cancel_nfse():
    """Fixture para CancelNFSE."""
    from pynfse.src.integration.carnaubal.abrasf.models.cancelamento import PedidoCancelamento, InfPedidoCancelamento, IdentificacaoNfse
    return CancelNFSE(
        pedido=PedidoCancelamento(
            inf_pedido_cancelamento=InfPedidoCancelamento(
                identificacao_nfse=IdentificacaoNfse(
                    numero=123,
                    cnpj="12345678000190",
                    inscricao_municipal="12345",
                    codigo_municipio=2408102
                ),
                codigo_cancelamento="1"
            )
        )
    )


@pytest.fixture
def sample_consult_nfse(sample_provider_nfse):
    """Fixture para ConsultNFSE."""
    return ConsultNFSE(
        prestador=sample_provider_nfse,
        numero_nfse=123
    )


@pytest.fixture
def sample_consult_lote_nfse():
    """Fixture para ConsultLoteNFSE."""
    return {
        "cnpj": "12345678000190",
        "municipal_registration": "12345",
        "protocol": "123456789"
    }


@pytest.fixture
def sample_consult_lote_rps(sample_identification_nfse, sample_provider_nfse):
    """Fixture para ConsultLoteRPS."""
    return ConsultLoteRPS(
        identificacao_rps=sample_identification_nfse,
        prestador=sample_provider_nfse
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

