"""Testes para os schemas de RPS."""
import pytest
from pydantic import ValidationError

from pynfse.schemas.rps import (
    BaseNFSE,
    CancelNFSE,
    ConsultNFSE,
    ConsultLoteNFSE,
    ConsultLoteRPS,
)


class TestBaseNFSE:
    """Testes para BaseNFSE."""

    def test_create_base_nfse_with_defaults(self):
        """Testa criação de BaseNFSE com valores padrão."""
        base = BaseNFSE(
            cnpj="12345678000190",
            municipal_registration=12345
        )
        assert base.cnpj == "12345678000190"
        assert base.municipal_registration == 12345
        assert base.municipality_code is None
        assert base.number is None

    def test_create_base_nfse_with_all_fields(self):
        """Testa criação de BaseNFSE com todos os campos."""
        base = BaseNFSE(
            cnpj="12345678000190",
            municipal_registration=12345,
            municipality_code="2408102",
            number=123
        )
        assert base.cnpj == "12345678000190"
        assert base.municipal_registration == 12345
        assert base.municipality_code == "2408102"
        assert base.number == 123

    def test_base_nfse_required_fields(self):
        """Testa que campos obrigatórios são necessários."""
        with pytest.raises(ValidationError):
            BaseNFSE(cnpj="12345678000190")

        with pytest.raises(ValidationError):
            BaseNFSE(municipal_registration=12345)


class TestCancelNFSE:
    """Testes para CancelNFSE."""

    def test_create_cancel_nfse_with_defaults(self):
        """Testa criação de CancelNFSE com valores padrão."""
        cancel = CancelNFSE(
            cnpj="12345678000190",
            municipal_registration=12345,
            municipality_code="2408102"
        )
        assert cancel.cnpj == "12345678000190"
        assert cancel.municipal_registration == 12345
        assert cancel.municipality_code == "2408102"
        assert cancel.cancellation_code == "E12"

    def test_create_cancel_nfse_with_custom_code(self):
        """Testa criação de CancelNFSE com código de cancelamento customizado."""
        cancel = CancelNFSE(
            cnpj="12345678000190",
            municipal_registration=12345,
            municipality_code="2408102",
            cancellation_code="E13"
        )
        assert cancel.cancellation_code == "E13"

    def test_cancel_nfse_required_fields(self):
        """Testa que campos obrigatórios são necessários."""
        with pytest.raises(ValidationError):
            CancelNFSE(
                cnpj="12345678000190",
                municipal_registration=12345
            )

        with pytest.raises(ValidationError):
            CancelNFSE(
                cnpj="12345678000190",
                municipality_code="2408102"
            )


class TestConsultNFSE:
    """Testes para ConsultNFSE."""

    def test_create_consult_nfse(self):
        """Testa criação de ConsultNFSE."""
        consult = ConsultNFSE(
            cnpj="12345678000190",
            municipal_registration=12345,
            number=123,
            serie="A"
        )
        assert consult.cnpj == "12345678000190"
        assert consult.municipal_registration == 12345
        assert consult.number == 123
        assert consult.serie == "A"

    def test_consult_nfse_required_fields(self):
        """Testa que campos obrigatórios são necessários."""
        with pytest.raises(ValidationError):
            ConsultNFSE(
                cnpj="12345678000190",
                municipal_registration=12345,
                number=123
            )

        with pytest.raises(ValidationError):
            ConsultNFSE(
                cnpj="12345678000190",
                municipal_registration=12345,
                serie="A"
            )


class TestConsultLoteNFSE:
    """Testes para ConsultLoteNFSE."""

    def test_create_consult_lote_nfse(self):
        """Testa criação de ConsultLoteNFSE."""
        consult = ConsultLoteNFSE(
            cnpj="12345678000190",
            municipal_registration=12345,
            protocol="123456789"
        )
        assert consult.cnpj == "12345678000190"
        assert consult.municipal_registration == 12345
        assert consult.protocol == "123456789"

    def test_consult_lote_nfse_required_fields(self):
        """Testa que campos obrigatórios são necessários."""
        with pytest.raises(ValidationError):
            ConsultLoteNFSE(
                cnpj="12345678000190",
                municipal_registration=12345
            )

        with pytest.raises(ValidationError):
            ConsultLoteNFSE(
                cnpj="12345678000190",
                protocol="123456789"
            )


class TestConsultLoteRPS:
    """Testes para ConsultLoteRPS."""

    def test_create_consult_lote_rps(self):
        """Testa criação de ConsultLoteRPS."""
        consult = ConsultLoteRPS(
            cnpj="12345678000190",
            municipal_registration=12345,
            protocol="123456789"
        )
        assert consult.cnpj == "12345678000190"
        assert consult.municipal_registration == 12345
        assert consult.protocol == "123456789"

    def test_consult_lote_rps_required_fields(self):
        """Testa que campos obrigatórios são necessários."""
        with pytest.raises(ValidationError):
            ConsultLoteRPS(
                cnpj="12345678000190",
                municipal_registration=12345
            )

        with pytest.raises(ValidationError):
            ConsultLoteRPS(
                cnpj="12345678000190",
                protocol="123456789"
            )

