from datetime import datetime

from lxml import etree

from pynfse.integration.carnaubal.abrasf.models.base import ListaMensagemRetorno, MensagemRetorno
from pynfse.integration.carnaubal.abrasf.models.rps import (
    DadosServico,
    DadosTomador,
    IdentificacaoPrestador,
    IdentificacaoRps,
    InfRps,
    Rps,
    Valores,
)
from pynfse.integration.carnaubal.abrasf.models.respostas import (
    CancelarNfseResposta,
    ConsultarLoteRpsResposta,
    ConsultarNfseResposta,
    ConsultarNfseRpsResposta,
    ConsultarSituacaoLoteRpsResposta,
    EnviarLoteRpsResposta,
)
from pynfse.integration.carnaubal.abrasf.nfse import CarnaubalNFSe
from pynfse.integration.carnaubal.abrasf.schema_validation import validate_xml


def _extract_cdata_payload(soap_xml: str, tag_name: str) -> str:
    root = etree.fromstring(soap_xml.encode("utf-8"))
    payload = root.find(f".//{tag_name}")
    assert payload is not None
    return payload.text


def _error_messages() -> ListaMensagemRetorno:
    return ListaMensagemRetorno(
        mensagem_retorno=[
            MensagemRetorno(codigo="E001", mensagem="Erro de validacao", correcao="Corrigir payload")
        ]
    )


def test_header_validates_against_xsd():
    provider = CarnaubalNFSe(URL="http://test.com")
    validate_xml(provider._get_default_header(), "cabecalho_v1.xsd")


def test_enviar_lote_payload_validates_against_xsd():
    provider = CarnaubalNFSe(URL="http://test.com")
    rps = Rps(
        inf_rps=InfRps(
            identificacao_rps=IdentificacaoRps(numero=1, serie="A", tipo=1),
            data_emissao=datetime(2024, 3, 9, 10, 0, 0),
            natureza_operacao=1,
            optante_simples_national=1,
            incentivador_cultural=2,
            status=1,
            servico=DadosServico(
                valores=Valores(valor_servicos=100.0, iss_retido=2),
                item_lista_servico="1.01",
                discriminacao="Teste XSD",
                codigo_municipio=1234567,
            ),
            prestador=IdentificacaoPrestador(cnpj="12345678000199", inscricao_municipal="12345"),
            tomador=DadosTomador(razao_social="Tomador XSD"),
        )
    )
    xml = provider.create_rps_nfse(
        rps_list=[rps],
        numero_lote=1,
        cnpj="12345678000199",
        inscricao_municipal="12345",
    )
    payload = _extract_cdata_payload(xml, "parameters")
    validate_xml(payload, "enviar_lote_rps_envio_v1.xsd")


def test_cancelar_payload_validates_against_xsd():
    provider = CarnaubalNFSe(URL="http://test.com")
    xml = provider.create_cancel_nfse(
        numero_nfse=1,
        cnpj="12345678000199",
        inscricao_municipal="12345",
        codigo_municipio=1234567,
        codigo_cancelamento="1",
    )
    payload = _extract_cdata_payload(xml, "parameters")
    validate_xml(payload, "cancelar_nfse_envio_v1.xsd")


def test_consultar_nfse_payload_validates_against_xsd():
    provider = CarnaubalNFSe(URL="http://test.com")
    xml = provider.create_consult_nfse(
        cnpj="12345678000199",
        inscricao_municipal="12345",
        numero_nfse=10,
    )
    payload = _extract_cdata_payload(xml, "parameters")
    validate_xml(payload, "consultar_nfse_envio_v1.xsd")


def test_consultar_rps_payload_validates_against_xsd():
    provider = CarnaubalNFSe(URL="http://test.com")
    xml = provider.create_consult_rps(
        numero=123,
        serie="A",
        tipo=1,
        cnpj="12345678000199",
        inscricao_municipal="12345",
    )
    payload = _extract_cdata_payload(xml, "parameters")
    validate_xml(payload, "consultar_nfse_rps_envio_v1.xsd")


def test_consultar_lote_payload_validates_against_xsd():
    provider = CarnaubalNFSe(URL="http://test.com")
    xml = provider.create_consult_lote_rps(
        protocolo="PROTOCOLO123",
        cnpj="12345678000199",
        inscricao_municipal="12345",
    )
    payload = _extract_cdata_payload(xml, "parameters")
    validate_xml(payload, "consultar_lote_rps_envio_v1.xsd")


def test_consultar_situacao_lote_payload_validates_against_xsd():
    provider = CarnaubalNFSe(URL="http://test.com")
    xml = provider.create_consult_situacao_lote_rps(
        protocolo="PROTOCOLO123",
        cnpj="12345678000199",
        inscricao_municipal="12345",
    )
    payload = _extract_cdata_payload(xml, "parameters")
    validate_xml(payload, "consultar_situacao_lote_rps_envio_v1.xsd")


def test_enviar_lote_resposta_validates_against_xsd():
    response = EnviarLoteRpsResposta(
        numero_lote=1,
        data_recebimento=datetime(2024, 3, 9, 10, 0, 0),
        protocolo="PROTOCOLO123",
    )
    xml = response.to_xml(
        tag_name="EnviarLoteRpsResposta",
        namespace="http://ws.speedgov.com.br/enviar_lote_rps_resposta_v1.xsd",
        nsmap={None: "http://ws.speedgov.com.br/enviar_lote_rps_resposta_v1.xsd"},
        pretty_print=False,
    )
    validate_xml(xml, "enviar_lote_rps_resposta_v1.xsd")


def test_consultar_nfse_rps_resposta_validates_against_xsd():
    response = ConsultarNfseRpsResposta(lista_mensagem_retorno=_error_messages())
    xml = response.to_xml(
        tag_name="ConsultarNfseRpsResposta",
        namespace="http://ws.speedgov.com.br/consultar_nfse_rps_resposta_v1.xsd",
        nsmap={None: "http://ws.speedgov.com.br/consultar_nfse_rps_resposta_v1.xsd", "tipos": "http://ws.speedgov.com.br/tipos_v1.xsd"},
        pretty_print=False,
    )
    validate_xml(xml, "consultar_nfse_rps_resposta_v1.xsd")


def test_consultar_nfse_resposta_validates_against_xsd():
    response = ConsultarNfseResposta(lista_mensagem_retorno=_error_messages())
    xml = response.to_xml(
        tag_name="ConsultarNfseResposta",
        namespace="http://ws.speedgov.com.br/consultar_nfse_resposta_v1.xsd",
        nsmap={None: "http://ws.speedgov.com.br/consultar_nfse_resposta_v1.xsd", "tipos": "http://ws.speedgov.com.br/tipos_v1.xsd"},
        pretty_print=False,
    )
    validate_xml(xml, "consultar_nfse_resposta_v1.xsd")


def test_cancelar_nfse_resposta_validates_against_xsd():
    response = CancelarNfseResposta(lista_mensagem_retorno=_error_messages())
    xml = response.to_xml(
        tag_name="CancelarNfseResposta",
        namespace="http://ws.speedgov.com.br/cancelar_nfse_resposta_v1.xsd",
        nsmap={None: "http://ws.speedgov.com.br/cancelar_nfse_resposta_v1.xsd", "tipos": "http://ws.speedgov.com.br/tipos_v1.xsd"},
        pretty_print=False,
    )
    validate_xml(xml, "cancelar_nfse_resposta_v1.xsd")


def test_consultar_lote_resposta_validates_against_xsd():
    response = ConsultarLoteRpsResposta(lista_mensagem_retorno=_error_messages())
    xml = response.to_xml(
        tag_name="ConsultarLoteRpsResposta",
        namespace="http://ws.speedgov.com.br/consultar_lote_rps_resposta_v1.xsd",
        nsmap={None: "http://ws.speedgov.com.br/consultar_lote_rps_resposta_v1.xsd", "tipos": "http://ws.speedgov.com.br/tipos_v1.xsd"},
        pretty_print=False,
    )
    validate_xml(xml, "consultar_lote_rps_resposta_v1.xsd")


def test_consultar_situacao_lote_resposta_validates_against_xsd():
    response = ConsultarSituacaoLoteRpsResposta(numero_lote=1, situacao=2)
    xml = response.to_xml(
        tag_name="ConsultarSituacaoLoteRpsResposta",
        namespace="http://ws.speedgov.com.br/consultar_situacao_lote_rps_resposta_v1.xsd",
        nsmap={None: "http://ws.speedgov.com.br/consultar_situacao_lote_rps_resposta_v1.xsd"},
        pretty_print=False,
    )
    validate_xml(xml, "consultar_situacao_lote_rps_resposta_v1.xsd")
