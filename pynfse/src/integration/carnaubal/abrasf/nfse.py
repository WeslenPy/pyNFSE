from datetime import datetime
from typing import Optional, List, Union, Dict, Any
import base64
import requests
from pathlib import Path
from urllib.parse import urlparse

from lxml import etree
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from signxml import XMLSigner, methods
from loguru import logger

from pynfse.src.common.api import NFSeBase
from pynfse.src.common.xml import XMLBase
from pynfse.src.common.signature import (
    Signature,
    SignedInfo,
    CanonicalizationMethod,
    SignatureMethod,
    Reference,
    Transforms,
    Transform,
    DigestMethod,
    KeyInfo,
    X509Data
)
from pynfse.src.integration.carnaubal.abrasf.models.cancelamento import (
    CancelarNfseEnvio,
    InfPedidoCancelamento,
    PedidoCancelamento,
    IdentificacaoNfse
)
from pynfse.src.integration.carnaubal.abrasf.models.consulta import ConsultarNfseEnvio
from pynfse.src.integration.carnaubal.abrasf.models.consultar_rps import ConsultarNfseRpsEnvio
from pynfse.src.integration.carnaubal.abrasf.models.lote import (
    ListaRps,
    LoteRps as LoteRpsModel
)
from pynfse.src.integration.carnaubal.abrasf.models.rps import (
    CpfCnpj,
    Contato,
    DadosServico,
    DadosTomador,
    Endereco,
    IdentificacaoPrestador,
    IdentificacaoRps,
    IdentificacaoTomador,
    InfRps,
    Rps as RpsModel,
    Valores
)


class CarnaubalNFSe(NFSeBase):
    """
    Implementação do provedor Carnaubal seguindo o padrão ABRASF v1.
    Utiliza modelos Pydantic para geração de XML e envelope SOAP com CDATA.
    """

    def __init__(self, URL: str, **kwargs):
        super().__init__(URL, **kwargs)

        self._cert_cache: Dict[str, bytes] = {}

    def get_certificate(self, path_or_url: str, use_cache: bool = True) -> bytes:
        """
        Obtém o conteúdo do certificado de uma URL ou caminho local.
        Se for uma URL, faz o download. Se for um caminho, lê do disco.
        Mapeia em um dicionário de cache para evitar leituras/downloads repetidos.
        """
        if use_cache and path_or_url in self._cert_cache:
            logger.debug(f"Recuperando certificado do cache: {path_or_url}")
            return self._cert_cache[path_or_url]

        # Verifica se é uma URL
        parsed = urlparse(path_or_url)
        is_url = parsed.scheme in ('http', 'https')

        try:
            if is_url:
                logger.debug(f"Baixando certificado da URL: {path_or_url}")
                response = requests.get(path_or_url, verify=False, timeout=30)
                response.raise_for_status()
                content = response.content
            else:
                logger.debug(f"Lendo certificado do arquivo local: {path_or_url}")
                path = Path(path_or_url)
                if not path.is_file():
                    raise FileNotFoundError(f"Arquivo de certificado não encontrado: {path_or_url}")
                content = path.read_bytes()

            if use_cache:
                self._cert_cache[path_or_url] = content
            
            return content

        except Exception as e:
            logger.error(f"Erro ao obter certificado ({path_or_url}): {str(e)}")
            raise ValueError(f"Não foi possível obter o certificado: {str(e)}")

    def get_xml_base(self) -> XMLBase:
        """Retorna uma instância concreta de XMLBase."""
        class ConcreteXMLBase(XMLBase):
            def create_rps_nfse(self, lote): pass
            def create_cancel_nfse(self, nfse): pass
            def create_consult_nfse(self, nfse): pass
        return ConcreteXMLBase()

    def _get_default_header(self) -> str:
        """Retorna o cabeçalho XML padrão para as requisições ABRASF v1."""
        return (
            '<cabecalho xmlns="http://ws.speedgov.com.br/cabecalho_v1.xsd" versao="1">'
            '<versaoDados xmlns="">1</versaoDados>'
            '</cabecalho>'
        )

    def _load_certificate(self, certificate_data: bytes, password: Optional[str] = None):
        """
        Carrega o certificado PEM ou PFX e retorna a chave privada e o certificado público.
        """
        try:
            # Tenta carregar como PKCS12 (PFX)
            private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
                certificate_data,
                password.encode() if password else None
            )
            return private_key, certificate
        except Exception:
            # Tenta carregar como PEM
            try:
                private_key = serialization.load_pem_private_key(
                    certificate_data,
                    password=password.encode() if password else None
                )
                certificate = x509.load_pem_x509_certificate(certificate_data)
                return private_key, certificate
            except Exception as e:
                raise ValueError(f"Erro ao carregar certificado (PEM/PFX): {str(e)}")

    def generate_signature(self, xml_element: etree._Element, certificate_data: bytes, password: Optional[str] = None) -> Signature:
        """
        Gera a assinatura digital para um elemento XML usando um certificado PEM ou PFX.
        Retorna um objeto Signature (Pydantic).
        """
        private_key, certificate = self._load_certificate(certificate_data, password)
        
        # Prepara o assinador XML
        signer = XMLSigner(
            method=methods.enveloped,
            signature_algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256",
            digest_algorithm="sha256",
            c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"
        )
        
        # Assina o elemento
        signed_root = signer.sign(xml_element, key=private_key, cert=[certificate])
        
        # Extrai o nó Signature
        signature_node = signed_root.find(".//{http://www.w3.org/2000/09/xmldsig#}Signature")
        if signature_node is None:
            if signed_root.tag == "{http://www.w3.org/2000/09/xmldsig#}Signature":
                signature_node = signed_root
            else:
                raise ValueError("Não foi possível encontrar o nó Signature no XML assinado.")

        ns = {"ds": "http://www.w3.org/2000/09/xmldsig#"}
        
        signed_info_node = signature_node.find("ds:SignedInfo", ns)
        signature_value = signature_node.find("ds:SignatureValue", ns).text.strip()
        
        # SignedInfo details
        c14n_method = signed_info_node.find("ds:CanonicalizationMethod", ns).get("Algorithm")
        sig_method = signed_info_node.find("ds:SignatureMethod", ns).get("Algorithm")
        
        references = []
        for ref_node in signed_info_node.findall("ds:Reference", ns):
            uri = ref_node.get("URI")
            digest_method = ref_node.find("ds:DigestMethod", ns).get("Algorithm")
            digest_value = ref_node.find("ds:DigestValue", ns).text.strip()
            
            transforms_list = []
            transforms_node = ref_node.find("ds:Transforms", ns)
            if transforms_node is not None:
                for trans_node in transforms_node.findall("ds:Transform", ns):
                    transforms_list.append(Transform(algorithm=trans_node.get("Algorithm")))
            
            references.append(Reference(
                uri=uri,
                transforms=Transforms(transform=transforms_list) if transforms_list else None,
                digest_method=DigestMethod(algorithm=digest_method),
                digest_value=digest_value
            ))
            
        signed_info = SignedInfo(
            canonicalization_method=CanonicalizationMethod(algorithm=c14n_method),
            signature_method=SignatureMethod(algorithm=sig_method),
            reference=references
        )
        
        # KeyInfo
        cert_b64 = base64.b64encode(certificate.public_bytes(serialization.Encoding.DER)).decode("utf-8")
        key_info = KeyInfo(x509_data=X509Data(x509_certificate=cert_b64))
        
        return Signature(
            signed_info=signed_info,
            signature_value=signature_value,
            key_info=key_info
        )

    def create_rps_nfse(self, rps_list: List[RpsModel], numero_lote: int, cnpj: str, inscricao_municipal: str) -> str:
        """
        Cria XML de envio de Lote RPS.
        """
        lote_model = LoteRpsModel(
            id=f"lote_{numero_lote}",
            numero_lote=numero_lote,
            cnpj=cnpj,
            inscricao_municipal=inscricao_municipal,
            quantidade_rps=len(rps_list),
            lista_rps=ListaRps(rps=rps_list)
        )
        
        return self.get_xml_base().create_soap_envelope(
            body_content=lote_model.to_xml(),
            method_name="RecepcionarLoteRps",
            header_content=self._get_default_header()
        )
    
    def create_cancel_nfse(self, numero_nfse: int, cnpj: str, 
                           inscricao_municipal: str, 
                           codigo_municipio: int, 
                           codigo_cancelamento: str) -> str:
        
        """Cria XML para cancelamento de NFSE."""
        pedido = PedidoCancelamento(
            inf_pedido_cancelamento=InfPedidoCancelamento(
                identificacao_nfse=IdentificacaoNfse(
                    numero=numero_nfse,
                    cnpj=cnpj,
                    inscricao_municipal=inscricao_municipal,
                    codigo_municipio=codigo_municipio
                ),
                codigo_cancelamento=codigo_cancelamento
            )
        )
        
        return self.get_xml_base().create_soap_envelope(
            body_content=CancelarNfseEnvio(pedido=pedido).to_xml(),
            method_name="CancelarNfse",
            header_content=self._get_default_header()
        )
    
    def create_consult_nfse(self, cnpj: str, 
                            inscricao_municipal: str, 
                            numero_nfse: Optional[int] = None) -> str:
        """Cria XML para consulta de NFSE."""
        consulta = ConsultarNfseEnvio(
            prestador=IdentificacaoPrestador(
                cnpj=cnpj,
                inscricao_municipal=inscricao_municipal
            ),
            numero_nfse=numero_nfse
        )
        
        return self.get_xml_base().create_soap_envelope(
            body_content=consulta.to_xml(),
            method_name="ConsultarNfse",
            header_content=self._get_default_header()
        )

    def create_consult_rps(self, numero: int, serie: str, 
                           tipo: int, cnpj: str, 
                           inscricao_municipal: str = None) -> str:
        """Cria XML para consulta de NFSe por RPS."""
        consulta = ConsultarNfseRpsEnvio(
            identificacao_rps=IdentificacaoRps(
                numero=numero,
                serie=serie,
                tipo=tipo
            ),
            prestador=IdentificacaoPrestador(
                cnpj=cnpj,
                inscricao_municipal=inscricao_municipal
            )
        )
        
        return self.get_xml_base().create_soap_envelope(
            body_content=consulta.to_xml(),
            method_name="ConsultarNfsePorRps",
            header_content=self._get_default_header()
        )
