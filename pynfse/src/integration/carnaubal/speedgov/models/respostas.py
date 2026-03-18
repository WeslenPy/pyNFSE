"""
Modelos de resposta SpeedGov - XML -> Pydantic.
Reutiliza a estrutura ABRASF (mesmos XSDs) e adiciona helpers para popular via XML.
"""
from typing import Type, TypeVar

from pynfse.src.common.response_parser import parse_resposta_xml
from pynfse.src.integration.carnaubal.abrasf.models.base import (
    ListaMensagemRetorno,
    MensagemRetorno,
)
from pynfse.src.integration.carnaubal.abrasf.models.respostas import (
    CancelarNfseResposta,
    CompNfse,
    ConsultarLoteRpsResposta,
    ConsultarNfseResposta,
    ConsultarNfseRpsResposta,
    ConsultarSituacaoLoteRpsResposta,
    EnviarLoteRpsResposta,
    InfNfse,
    ListaNfse,
    Nfse,
)

__all__ = [
    "EnviarLoteRpsResposta",
    "ConsultarNfseResposta",
    "ConsultarNfseRpsResposta",
    "ConsultarLoteRpsResposta",
    "ConsultarSituacaoLoteRpsResposta",
    "CancelarNfseResposta",
    "CompNfse",
    "ListaNfse",
    "ListaMensagemRetorno",
    "MensagemRetorno",
    "Nfse",
    "InfNfse",
    "RespostasSpeedGov",
]


T = TypeVar("T")


class RespostasSpeedGov:
    """Métodos estáticos para parse de respostas XML -> Pydantic."""

    @staticmethod
    def from_xml_enviar_lote(xml_text: str) -> EnviarLoteRpsResposta:
        """Parse de resposta RecepcionarLoteRps -> EnviarLoteRpsResposta."""
        return parse_resposta_xml(xml_text, EnviarLoteRpsResposta)

    @staticmethod
    def from_xml_consultar_nfse(xml_text: str) -> ConsultarNfseResposta:
        """Parse de resposta ConsultarNfse -> ConsultarNfseResposta."""
        return parse_resposta_xml(xml_text, ConsultarNfseResposta)

    @staticmethod
    def from_xml_consultar_rps(xml_text: str) -> ConsultarNfseRpsResposta:
        """Parse de resposta ConsultarNfsePorRps -> ConsultarNfseRpsResposta."""
        return parse_resposta_xml(xml_text, ConsultarNfseRpsResposta)

    @staticmethod
    def from_xml_consultar_lote_rps(xml_text: str) -> ConsultarLoteRpsResposta:
        """Parse de resposta ConsultarLoteRps -> ConsultarLoteRpsResposta."""
        return parse_resposta_xml(xml_text, ConsultarLoteRpsResposta)

    @staticmethod
    def from_xml_consultar_situacao_lote(xml_text: str) -> ConsultarSituacaoLoteRpsResposta:
        """Parse de resposta ConsultarSituacaoLoteRps -> ConsultarSituacaoLoteRpsResposta."""
        return parse_resposta_xml(xml_text, ConsultarSituacaoLoteRpsResposta)

    @staticmethod
    def from_xml_cancelar(xml_text: str) -> CancelarNfseResposta:
        """Parse de resposta CancelarNfse -> CancelarNfseResposta."""
        return parse_resposta_xml(xml_text, CancelarNfseResposta)

    @staticmethod
    def from_xml(xml_text: str, model_class: Type[T]) -> T:
        """Parse genérico: XML -> instância do modelo informado."""
        return parse_resposta_xml(xml_text, model_class)
