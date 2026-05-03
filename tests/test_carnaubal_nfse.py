import asyncio
import pytest
import httpx
from datetime import datetime
from unittest.mock import AsyncMock, patch
from lxml import etree
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

from pynfse.integration.carnaubal.abrasf.nfse import CarnaubalNFSe
from pynfse.integration.carnaubal.abrasf.models.rps import Rps, InfRps, IdentificacaoRps, DadosServico, Valores, IdentificacaoPrestador, DadosTomador
from pynfse.common.signature import (
    Signature,
    SignedInfo,
    CanonicalizationMethod,
    SignatureMethod,
    Reference,
    Transforms,
    Transform,
    DigestMethod,
    KeyInfo,
    X509Data,
)

@pytest.fixture
def mock_certificate():
    """Gera um certificado e chave privada fake para testes."""
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "BR"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "RN"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Carnaubal"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "PyNFSe Test"),
        x509.NameAttribute(NameOID.COMMON_NAME, "pynfse.test"),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow()
    ).sign(key, hashes.SHA256())
    
    cert_pem = cert.public_bytes(serialization.Encoding.PEM)
    key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    return cert_pem + key_pem

@pytest.fixture
def carnaubal_provider():
    p = CarnaubalNFSe(URL="http://test.com")
    yield p
    asyncio.run(p.aclose())


def _parse_xml(xml: str) -> etree._Element:
    return etree.fromstring(xml.encode("utf-8"))


def _parse_soap_request(xml: str, method_name: str) -> tuple[etree._Element, etree._Element]:
    envelope = _parse_xml(xml)
    method = envelope.find(f".//{{http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd}}{method_name}")
    assert method is not None

    header_text = method.findtext("header")
    params_text = method.findtext("parameters")
    assert header_text is not None
    assert params_text is not None

    return _parse_xml(header_text), _parse_xml(params_text)


def _text(element: etree._Element, local_name: str) -> str:
    return element.xpath(f"string(.//*[local-name()='{local_name}'][1])")

def test_get_default_header(carnaubal_provider):
    header = carnaubal_provider._get_default_header()
    header_xml = _parse_xml(header)
    assert header_xml.tag == "{http://ws.speedgov.com.br/cabecalho_v1.xsd}cabecalho"
    assert header_xml.get("versao") == "1"
    assert header_xml.xpath("string(.//*[local-name()='versaoDados'])") == "1"

def test_generate_signature(carnaubal_provider, mock_certificate):
    # Criar um elemento XML simples para assinar
    root = etree.Element("Teste", Id="root1")
    etree.SubElement(root, "Dados").text = "Conteudo para assinar"
    
    signature = carnaubal_provider.generate_signature(root, mock_certificate)
    
    assert isinstance(signature, Signature)
    assert signature.signature_value is not None
    assert signature.signed_info.signature_method.algorithm == "http://www.w3.org/2000/09/xmldsig#rsa-sha1"
    assert signature.signed_info.reference[0].digest_method.algorithm == "http://www.w3.org/2000/09/xmldsig#sha1"
    assert signature.key_info.x509_data.x509_certificate is not None

def test_create_rps_nfse_xml(carnaubal_provider):
    rps = Rps(inf_rps=InfRps(
        identificacao_rps=IdentificacaoRps(numero=1, serie="A", tipo=1),
        data_emissao=datetime.now(),
        natureza_operacao=1,
        optante_simples_national=1,
        incentivador_cultural=2,
        status=1,
        servico=DadosServico(
            valores=Valores(valor_servicos=100.0, iss_retido=2),
            item_lista_servico="1.01",
            discriminacao="Teste",
            codigo_municipio=1234567
        ),
        prestador=IdentificacaoPrestador(cnpj="12345678000199"),
        tomador=DadosTomador(razao_social="Tomador Teste")
    ))
    
    xml = carnaubal_provider.create_rps_nfse(
        rps_list=[rps],
        numero_lote=123,
        cnpj="12345678000199",
        inscricao_municipal="12345"
    )

    header_xml, params_xml = _parse_soap_request(xml, "RecepcionarLoteRps")

    assert "RecepcionarLoteRps" in xml
    assert '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"' in xml
    assert 'xmlns:nfse="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd"' in xml
    assert header_xml.tag == "{http://ws.speedgov.com.br/cabecalho_v1.xsd}cabecalho"
    assert params_xml.tag == "{http://ws.speedgov.com.br/enviar_lote_rps_envio_v1.xsd}EnviarLoteRpsEnvio"
    assert _text(params_xml, "NumeroLote") == "123"
    assert _text(params_xml, "Cnpj") == "12345678000199"
    assert _text(params_xml, "InscricaoMunicipal") == "12345"
    assert "<ds:Signature" not in xml
    assert "<ds:SignedInfo" not in xml

def test_create_rps_nfse_signed_xml_has_signature_without_ds_prefix(carnaubal_provider):
    signature = Signature(
        signed_info=SignedInfo(
            canonicalization_method=CanonicalizationMethod(algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"),
            signature_method=SignatureMethod(algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"),
            reference=[Reference(
                uri="#rps1",
                transforms=Transforms(transform=[Transform(algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature")]),
                digest_method=DigestMethod(algorithm="http://www.w3.org/2000/09/xmldsig#sha1"),
                digest_value="fake-digest"
            )]
        ),
        signature_value="fake-signature",
        key_info=KeyInfo(x509_data=X509Data(x509_certificate="fake-cert"))
    )

    rps = Rps(inf_rps=InfRps(
        id="rps1",
        identificacao_rps=IdentificacaoRps(numero=1, serie="A", tipo=1),
        data_emissao=datetime.now(),
        natureza_operacao=1,
        optante_simples_national=1,
        incentivador_cultural=2,
        status=1,
        servico=DadosServico(
            valores=Valores(valor_servicos=100.0, iss_retido=2),
            item_lista_servico="1.01",
            discriminacao="Teste assinado",
            codigo_municipio=1234567
        ),
        prestador=IdentificacaoPrestador(cnpj="12345678000199"),
        tomador=DadosTomador(razao_social="Tomador Teste")
    ), signature=signature)

    xml = carnaubal_provider.create_rps_nfse(
        rps_list=[rps],
        numero_lote=123,
        cnpj="12345678000199",
        inscricao_municipal="12345",
        signature=signature,
    )

    _, params_xml = _parse_soap_request(xml, "RecepcionarLoteRps")
    assert _text(params_xml, "SignatureValue") == "fake-signature"
    assert params_xml.xpath("boolean(.//*[local-name()='Signature' and namespace-uri()='http://www.w3.org/2000/09/xmldsig#'])")

def test_create_cancel_nfse_xml(carnaubal_provider):
    xml = carnaubal_provider.create_cancel_nfse(
        numero_nfse=2024001,
        cnpj="12345678000199",
        inscricao_municipal="12345",
        codigo_municipio=1234567,
        codigo_cancelamento="1"
    )

    _, params_xml = _parse_soap_request(xml, "CancelarNfse")
    assert "CancelarNfse" in xml
    assert _text(params_xml, "Numero") == "2024001"
    assert _text(params_xml, "CodigoCancelamento") == "1"

def test_create_consult_nfse_xml(carnaubal_provider):
    xml = carnaubal_provider.create_consult_nfse(
        cnpj="12345678000199",
        inscricao_municipal="12345",
        numero_nfse=10
    )

    _, params_xml = _parse_soap_request(xml, "ConsultarNfse")
    assert "ConsultarNfse" in xml
    assert _text(params_xml, "NumeroNfse") == "10"
    assert _text(params_xml, "Cnpj") == "12345678000199"

def test_create_consult_rps_xml(carnaubal_provider):
    xml = carnaubal_provider.create_consult_rps(
        numero=123,
        serie="A",
        tipo=1,
        cnpj="12345678000199",
        inscricao_municipal="12345"
    )

    _, params_xml = _parse_soap_request(xml, "ConsultarNfsePorRps")
    assert "ConsultarNfsePorRps" in xml
    assert _text(params_xml, "Numero") == "123"
    assert _text(params_xml, "Serie") == "A"
    assert _text(params_xml, "Tipo") == "1"

def test_create_consult_lote_rps_xml(carnaubal_provider):
    xml = carnaubal_provider.create_consult_lote_rps(
        protocolo="PROTOCOLO123",
        cnpj="12345678000199",
        inscricao_municipal="12345"
    )

    _, params_xml = _parse_soap_request(xml, "ConsultarLoteRps")
    assert "ConsultarLoteRps" in xml
    assert _text(params_xml, "Protocolo") == "PROTOCOLO123"

def test_create_consult_situacao_lote_rps_xml(carnaubal_provider):
    xml = carnaubal_provider.create_consult_situacao_lote_rps(
        protocolo="PROTOCOLO123",
        cnpj="12345678000199",
        inscricao_municipal="12345"
    )

    _, params_xml = _parse_soap_request(xml, "ConsultarSituacaoLoteRps")
    assert "ConsultarSituacaoLoteRps" in xml
    assert _text(params_xml, "Protocolo") == "PROTOCOLO123"

async def test_get_certificate_local(carnaubal_provider, tmp_path):
    """Testa o carregamento de certificado de arquivo local."""
    cert_file = tmp_path / "cert.pem"
    cert_content = b"fake-certificate-content"
    cert_file.write_bytes(cert_content)

    content = await carnaubal_provider.get_certificate(str(cert_file))
    assert content == cert_content
    assert str(cert_file) in carnaubal_provider._cert_cache

    content_cached = await carnaubal_provider.get_certificate(str(cert_file))
    assert content_cached == cert_content


async def test_get_certificate_url(carnaubal_provider):
    """Testa o download de certificado de uma URL."""
    url = "https://example.com/cert.pfx"
    cert_content = b"downloaded-cert-content"
    req = httpx.Request("GET", url)

    with patch.object(httpx.AsyncClient, "get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = httpx.Response(200, content=cert_content, request=req)

        content = await carnaubal_provider.get_certificate(url)
        assert content == cert_content
        mock_get.assert_called_once()
        assert mock_get.call_args[0][0] == url
        assert url in carnaubal_provider._cert_cache


async def test_get_xml_from_url_with_cache(carnaubal_provider):
    """Testa o download de XML de uma URL com cache."""
    url = "http://mock-url.com/nfse.xml"
    mock_content = b"<xml>conteudo</xml>"
    req = httpx.Request("GET", url)

    with patch.object(httpx.AsyncClient, "get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = httpx.Response(200, content=mock_content, request=req)

        content1 = await carnaubal_provider.get_xml_from_url(url)
        assert content1 == mock_content
        assert mock_get.call_count == 1

        content2 = await carnaubal_provider.get_xml_from_url(url)
        assert content2 == mock_content
        assert mock_get.call_count == 1
        assert url in carnaubal_provider._xml_cache
