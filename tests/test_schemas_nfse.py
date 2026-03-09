"""Testes para os schemas de NFSE."""
import pytest
from datetime import date
from pydantic import ValidationError

from pynfse.schemas.nfse import (
    IdentificationNFSE,
    ValuesNFSE,
    ProviderNFSE,
    ServicesNFSE,
    IdentificationCostumerNFSE,
    AddressNFSE,
    CostumerNFSE,
    InfoRPS,
)


class TestIdentificationNFSE:
    """Testes para IdentificationNFSE."""

    def test_create_identification_nfse_with_defaults(self):
        """Testa criação de IdentificationNFSE com valores padrão."""
        identification = IdentificationNFSE(number=123, serie="A")
        assert identification.number == 123
        assert identification.serie == "A"
        assert identification.typer == 1

    def test_create_identification_nfse_with_custom_typer(self):
        """Testa criação de IdentificationNFSE com typer customizado."""
        identification = IdentificationNFSE(number=456, serie="B", typer=2)
        assert identification.number == 456
        assert identification.serie == "B"
        assert identification.typer == 2

    def test_identification_nfse_required_fields(self):
        """Testa que campos obrigatórios são necessários."""
        with pytest.raises(ValidationError):
            IdentificationNFSE(serie="A")

        with pytest.raises(ValidationError):
            IdentificationNFSE(number=123)


class TestValuesNFSE:
    """Testes para ValuesNFSE."""

    def test_create_values_nfse_with_defaults(self):
        """Testa criação de ValuesNFSE com valores padrão."""
        values = ValuesNFSE(
            value_services=1000.0,
            value_iss=50.0,
            base_calculation=1000.0,
            aliquot=5.0,
            liquid_value=950.0
        )
        assert values.value_services == 1000.0
        assert values.value_deductions == 0.0
        assert values.value_pis == 0.0
        assert values.value_cofins == 0.0
        assert values.value_inss == 0.0
        assert values.value_ir == 0.0
        assert values.value_csll == 0.0
        assert values.iss_retido == 2
        assert values.value_iss == 50.0
        assert values.value_iss_retido == 0.0
        assert values.others_retentions == 0.0
        assert values.base_calculation == 1000.0
        assert values.aliquot == 5.0
        assert values.liquid_value == 950.0
        assert values.discount_conditioned == 0.0
        assert values.discount_unconditioned == 0.0

    def test_create_values_nfse_with_all_fields(self):
        """Testa criação de ValuesNFSE com todos os campos."""
        values = ValuesNFSE(
            value_services=2000.0,
            value_deductions=100.0,
            value_pis=10.0,
            value_cofins=20.0,
            value_inss=30.0,
            value_ir=40.0,
            value_csll=50.0,
            iss_retido=1,
            value_iss=100.0,
            value_iss_retido=50.0,
            others_retentions=25.0,
            base_calculation=1900.0,
            aliquot=5.0,
            liquid_value=1800.0,
            discount_conditioned=50.0,
            discount_unconditioned=50.0
        )
        assert values.value_services == 2000.0
        assert values.value_deductions == 100.0
        assert values.iss_retido == 1

    def test_values_nfse_required_fields(self):
        """Testa que campos obrigatórios são necessários."""
        with pytest.raises(ValidationError):
            ValuesNFSE(
                value_iss=50.0,
                base_calculation=1000.0,
                aliquot=5.0,
                liquid_value=950.0
            )


class TestProviderNFSE:
    """Testes para ProviderNFSE."""

    def test_create_provider_nfse(self):
        """Testa criação de ProviderNFSE."""
        provider = ProviderNFSE(
            cnpj="12345678000190",
            municipal_registration=12345
        )
        assert provider.cnpj == "12345678000190"
        assert provider.municipal_registration == 12345

    def test_provider_nfse_required_fields(self):
        """Testa que campos obrigatórios são necessários."""
        with pytest.raises(ValidationError):
            ProviderNFSE(cnpj="12345678000190")

        with pytest.raises(ValidationError):
            ProviderNFSE(municipal_registration=12345)


class TestAddressNFSE:
    """Testes para AddressNFSE."""

    def test_create_address_nfse_with_defaults(self):
        """Testa criação de AddressNFSE com valores padrão."""
        address = AddressNFSE(
            address="Rua Teste",
            number="123",
            district="Centro",
            uf="RN",
            zip_code="59000000"
        )
        assert address.address == "Rua Teste"
        assert address.number == "123"
        assert address.complement == "casa"
        assert address.district == "Centro"
        assert address.ibge_code is None
        assert address.uf == "RN"
        assert address.zip_code == "59000000"

    def test_create_address_nfse_with_all_fields(self):
        """Testa criação de AddressNFSE com todos os campos."""
        address = AddressNFSE(
            address="Rua Teste",
            number="123",
            complement="Apto 101",
            district="Centro",
            ibge_code="2408102",
            uf="RN",
            zip_code="59000000"
        )
        assert address.complement == "Apto 101"
        assert address.ibge_code == "2408102"

    def test_address_nfse_required_fields(self):
        """Testa que campos obrigatórios são necessários."""
        with pytest.raises(ValidationError):
            AddressNFSE(
                number="123",
                district="Centro",
                uf="RN",
                zip_code="59000000"
            )


class TestIdentificationCostumerNFSE:
    """Testes para IdentificationCostumerNFSE."""

    def test_create_identification_costumer_nfse(self):
        """Testa criação de IdentificationCostumerNFSE."""
        identification = IdentificationCostumerNFSE(cpf_cnpj="12345678901")
        assert identification.cpf_cnpj == "12345678901"

    def test_identification_costumer_nfse_required_fields(self):
        """Testa que campos obrigatórios são necessários."""
        with pytest.raises(ValidationError):
            IdentificationCostumerNFSE()


class TestCostumerNFSE:
    """Testes para CostumerNFSE."""

    def test_create_costumer_nfse(self, sample_identification_costumer_nfse, sample_address_nfse):
        """Testa criação de CostumerNFSE."""
        costumer = CostumerNFSE(
            identification=sample_identification_costumer_nfse,
            social_name="Cliente Teste LTDA",
            address=sample_address_nfse
        )
        assert costumer.identification.cpf_cnpj == "12345678901"
        assert costumer.social_name == "Cliente Teste LTDA"
        assert costumer.address.address == "Rua Teste"

    def test_costumer_nfse_required_fields(self, sample_address_nfse):
        """Testa que campos obrigatórios são necessários."""
        with pytest.raises(ValidationError):
            CostumerNFSE(
                social_name="Cliente Teste",
                address=sample_address_nfse
            )


class TestServicesNFSE:
    """Testes para ServicesNFSE."""

    def test_create_services_nfse_with_defaults(self, sample_values_nfse):
        """Testa criação de ServicesNFSE com valores padrão."""
        services = ServicesNFSE(
            description="Serviço de desenvolvimento",
            code_municipio="2408102",
            values=sample_values_nfse
        )
        assert services.item_list_service == 106
        assert services.code_cnae == "6204000"
        assert services.code_tributation_municipio == "620400000"
        assert services.description == "Serviço de desenvolvimento"
        assert services.code_municipio == "2408102"

    def test_create_services_nfse_with_all_fields(self, sample_values_nfse):
        """Testa criação de ServicesNFSE com todos os campos."""
        services = ServicesNFSE(
            item_list_service=105,
            code_cnae="6203000",
            code_tributation_municipio="620300000",
            description="Outro serviço",
            code_municipio="2408102",
            values=sample_values_nfse
        )
        assert services.item_list_service == 105
        assert services.code_cnae == "6203000"

    def test_services_nfse_required_fields(self):
        """Testa que campos obrigatórios são necessários."""
        with pytest.raises(ValidationError):
            ServicesNFSE(
                code_municipio="2408102"
            )


class TestInfoRPS:
    """Testes para InfoRPS."""

    def test_create_info_rps_with_defaults(
        self,
        sample_identification_nfse,
        sample_costumer_nfse,
        sample_services_nfse,
        sample_provider_nfse
    ):
        """Testa criação de InfoRPS com valores padrão."""
        info_rps = InfoRPS(
            identification=sample_identification_nfse,
            costumer=sample_costumer_nfse,
            services=sample_services_nfse,
            provider=sample_provider_nfse,
            date=date(2024, 1, 15)
        )
        assert info_rps.identification.number == 123
        assert info_rps.costumer.social_name == "Cliente Teste LTDA"
        assert info_rps.services.description == "Serviço de desenvolvimento de software"
        assert info_rps.provider.cnpj == "12345678000190"
        assert info_rps.date == date(2024, 1, 15)
        assert info_rps.nature_of_operation == 1
        assert info_rps.regime_special_tributation == 6
        assert info_rps.optant_simple_national == 1
        assert info_rps.incentivator_cultural == 2
        assert info_rps.status == 1

    def test_create_info_rps_with_all_fields(
        self,
        sample_identification_nfse,
        sample_costumer_nfse,
        sample_services_nfse,
        sample_provider_nfse
    ):
        """Testa criação de InfoRPS com todos os campos."""
        info_rps = InfoRPS(
            identification=sample_identification_nfse,
            costumer=sample_costumer_nfse,
            services=sample_services_nfse,
            provider=sample_provider_nfse,
            date=date(2024, 1, 15),
            nature_of_operation=2,
            regime_special_tributation=5,
            optant_simple_national=2,
            incentivator_cultural=1,
            status=2
        )
        assert info_rps.nature_of_operation == 2
        assert info_rps.regime_special_tributation == 5
        assert info_rps.optant_simple_national == 2
        assert info_rps.incentivator_cultural == 1
        assert info_rps.status == 2

    def test_info_rps_required_fields(self):
        """Testa que campos obrigatórios são necessários."""
        with pytest.raises(ValidationError):
            InfoRPS(
                date=date(2024, 1, 15)
            )

