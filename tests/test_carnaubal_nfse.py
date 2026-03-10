import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from lxml import etree
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

from pynfse.src.integration.carnaubal.abrasf.nfse import CarnaubalNFSe
from pynfse.src.integration.carnaubal.abrasf.models.rps import Rps, InfRps, IdentificacaoRps, DadosServico, Valores, IdentificacaoPrestador, DadosTomador
from pynfse.src.common.signature import Signature

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
    return CarnaubalNFSe(URL="http://test.com")

def test_get_default_header(carnaubal_provider):
    header = carnaubal_provider._get_default_header()
    assert 'xmlns="http://ws.speedgov.com.br/cabecalho_v1.xsd"' in header
    assert '<versaoDados xmlns="">1</versaoDados>' in header

def test_generate_signature(carnaubal_provider, mock_certificate):
    # Criar um elemento XML simples para assinar
    root = etree.Element("Teste", Id="root1")
    etree.SubElement(root, "Dados").text = "Conteudo para assinar"
    
    signature = carnaubal_provider.generate_signature(root, mock_certificate)
    
    assert isinstance(signature, Signature)
    assert signature.signature_value is not None
    assert signature.signed_info.signature_method.algorithm == "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"
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
    
    assert "RecepcionarLoteRps" in xml
    assert "<NumeroLote>123</NumeroLote>" in xml
    assert "<Cnpj>12345678000199</Cnpj>" in xml
    assert "<InscricaoMunicipal>12345</InscricaoMunicipal>" in xml
    assert "<![CDATA[" in xml

def test_create_cancel_nfse_xml(carnaubal_provider):
    xml = carnaubal_provider.create_cancel_nfse(
        numero_nfse=2024001,
        cnpj="12345678000199",
        inscricao_municipal="12345",
        codigo_municipio=1234567,
        codigo_cancelamento="1"
    )
    
    assert "CancelarNfse" in xml
    assert "<Numero>2024001</Numero>" in xml
    assert "<CodigoCancelamento>1</CodigoCancelamento>" in xml
    assert "<![CDATA[" in xml

def test_create_consult_nfse_xml(carnaubal_provider):
    xml = carnaubal_provider.create_consult_nfse(
        cnpj="12345678000199",
        inscricao_municipal="12345",
        numero_nfse=10
    )
    
    assert "ConsultarNfse" in xml
    assert "<NumeroNfse>10</NumeroNfse>" in xml
    assert "<Cnpj>12345678000199</Cnpj>" in xml

def test_create_consult_rps_xml(carnaubal_provider):
    xml = carnaubal_provider.create_consult_rps(
        numero=123,
        serie="A",
        tipo=1,
        cnpj="12345678000199",
        inscricao_municipal="12345"
    )
    
    assert "ConsultarNfsePorRps" in xml
    assert "<Numero>123</Numero>" in xml
    assert "<Serie>A</Serie>" in xml
    assert "<Tipo>1</Tipo>" in xml

def test_get_certificate_local(carnaubal_provider, tmp_path):
    """Testa o carregamento de certificado de arquivo local."""
    cert_file = tmp_path / "cert.pem"
    cert_content = b"fake-certificate-content"
    cert_file.write_bytes(cert_content)
    
    # Primeira leitura (disco)
    content = carnaubal_provider.get_certificate(str(cert_file))
    assert content == cert_content
    assert str(cert_file) in carnaubal_provider._cert_cache
    
    # Segunda leitura (cache)
    content_cached = carnaubal_provider.get_certificate(str(cert_file))
    assert content_cached == cert_content

def test_get_certificate_url(carnaubal_provider):
    """Testa o download de certificado de uma URL."""
    url = "https://example.com/cert.pfx"
    cert_content = b"downloaded-cert-content"
    
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.content = cert_content
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Download
        content = carnaubal_provider.get_certificate(url)
        assert content == cert_content
        mock_get.assert_called_once_with(url, verify=False, timeout=30)
        assert url in carnaubal_provider._cert_cache

def test_get_xml_from_url_with_cache(carnaubal_provider):
    """Testa o download de XML de uma URL com cache."""
    url = "http://mock-url.com/nfse.xml"
    mock_content = b"<xml>conteudo</xml>"
    
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.content = mock_content
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Primeira chamada (deve baixar)
        content1 = carnaubal_provider.get_xml_from_url(url)
        assert content1 == mock_content
        assert mock_get.call_count == 1
        
        # Segunda chamada (deve vir do cache)
        content2 = carnaubal_provider.get_xml_from_url(url)
        assert content2 == mock_content
        assert mock_get.call_count == 1
        assert url in carnaubal_provider._xml_cache
