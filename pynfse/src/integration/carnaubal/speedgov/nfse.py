"""
Integração SpeedGov para NFS-e.
Segue a estrutura exata do enviar_lote_rps.xml: prefixos p:/p1:, RPS simplificado.
"""
from pathlib import Path
from typing import Dict, List, Optional, Type, TypeVar
from urllib.parse import urlparse

import requests
from lxml import etree
from pydantic import BaseModel

from pynfse.src.common.api import NFSeBase
from pynfse.src.common.response_parser import parse_resposta_xml
from pynfse.src.common.xml import XMLBase
from pynfse.src.common.signature import Signature
from pynfse.src.integration.carnaubal.abrasf.models.cancelamento import (
    CancelarNfseEnvio,
    InfPedidoCancelamento,
    PedidoCancelamento,
    IdentificacaoNfse,
)
from pynfse.src.integration.carnaubal.abrasf.models.consulta import ConsultarNfseEnvio
from pynfse.src.integration.carnaubal.abrasf.models.consultar_lote import (
    ConsultarLoteRpsEnvio,
    ConsultarSituacaoLoteRpsEnvio,
)
from pynfse.src.integration.carnaubal.abrasf.models.consultar_rps import ConsultarNfseRpsEnvio
from pynfse.src.integration.carnaubal.abrasf.models.rps import (
    IdentificacaoPrestador as AbrasfIdentificacaoPrestador,
    IdentificacaoRps as AbrasfIdentificacaoRps,
)
from pynfse.src.integration.carnaubal.speedgov.constants import (
    ENVIO_NS,
    TIPOS_NS,
    XMLDSIG_NS,
    XSI_NS,
)
from pynfse.src.integration.carnaubal.speedgov.models.rps import Rps
from pynfse.src.integration.carnaubal.speedgov.models.lote import EnviarLoteRpsEnvio, LoteRps, ListaRps
from pynfse.src.integration.carnaubal.speedgov.helper.header import get_header_speedgov
from pynfse.src.integration.carnaubal.speedgov.helper.sign import sign_rps_element
from pynfse.src.integration.carnaubal.speedgov.models.respostas import (
    CancelarNfseResposta,
    ConsultarLoteRpsResposta,
    ConsultarNfseResposta,
    ConsultarNfseRpsResposta,
    ConsultarSituacaoLoteRpsResposta,
    EnviarLoteRpsResposta,
)

T = TypeVar("T", bound=BaseModel)

DEFAULT_SPEEDGOV_URL = "http://speedgov.com.br:80/wsmod/Nfes?wsdl"

CONSULTAR_NFSE_ENVIO_NS = "http://ws.speedgov.com.br/consultar_nfse_envio_v1.xsd"
CONSULTAR_NFSE_RPS_ENVIO_NS = "http://ws.speedgov.com.br/consultar_nfse_rps_envio_v1.xsd"
CONSULTAR_LOTE_RPS_ENVIO_NS = "http://ws.speedgov.com.br/consultar_lote_rps_envio_v1.xsd"
CONSULTAR_SITUACAO_LOTE_RPS_ENVIO_NS = "http://ws.speedgov.com.br/consultar_situacao_lote_rps_envio_v1.xsd"
CANCELAR_NFSE_ENVIO_NS = "http://ws.speedgov.com.br/cancelar_nfse_envio_v1.xsd"


def _serialize_request_model(model, root_tag: str, schema_location: str) -> str:
    """Serializa modelo ABRASF para XML string."""
    element = model.to_element(
        tag_name=root_tag,
        namespace=schema_location,
        nsmap={None: schema_location},
    )
    return etree.tostring(
        element,
        encoding="UTF-8",
        xml_declaration=False,
        pretty_print=False,
    ).decode("utf-8")


def _remove_ds_prefix(xml_str: str) -> str:
    """Remove prefixo ds: da assinatura - usa xmlns default como referência."""
    xml_str = xml_str.replace(' xmlns:ds="' + XMLDSIG_NS + '"', "")
    # Ordem: nomes mais longos primeiro para não corromper SignatureMethod/SignatureValue
    xml_str = xml_str.replace("<ds:SignatureMethod", "<SignatureMethod")
    xml_str = xml_str.replace("</ds:SignatureMethod>", "</SignatureMethod>")
    xml_str = xml_str.replace("<ds:SignatureValue", "<SignatureValue")
    xml_str = xml_str.replace("</ds:SignatureValue>", "</SignatureValue>")
    xml_str = xml_str.replace("<ds:Signature", f'<Signature xmlns="{XMLDSIG_NS}"')
    xml_str = xml_str.replace("</ds:Signature>", "</Signature>")
    xml_str = xml_str.replace("<ds:", "<")
    xml_str = xml_str.replace("</ds:", "</")
    return xml_str


class SpeedGovNFSe(NFSeBase):
    """
    Integração SpeedGov - estrutura enviar_lote_rps.xml.
    Prefixos p:/p1:, RPS simplificado (sem blocos opcionais ABRASF).
    """

    def __init__(self, URL: str = DEFAULT_SPEEDGOV_URL, **kwargs):
        super().__init__(URL=URL, **kwargs)
        self._cert_cache: Dict[str, bytes] = {}

    def get_certificate(self, path_or_url: str, use_cache: bool = True) -> bytes:
        """Obtém o conteúdo do certificado de uma URL ou caminho local."""
        if use_cache and path_or_url in self._cert_cache:
            return self._cert_cache[path_or_url]
        parsed = urlparse(path_or_url)
        is_url = parsed.scheme in ("http", "https")
        try:
            if is_url:
                response = requests.get(path_or_url, verify=False, timeout=30)
                response.raise_for_status()
                content = response.content
            else:
                path = Path(path_or_url)
                if not path.is_file():
                    raise FileNotFoundError(f"Certificado não encontrado: {path_or_url}")
                content = path.read_bytes()
            if use_cache:
                self._cert_cache[path_or_url] = content
            return content
        except Exception as e:
            raise ValueError(f"Não foi possível obter o certificado: {e}") from e

    def get_xml_base(self) -> XMLBase:
        class _XMLBase(XMLBase):
            def create_rps_nfse(self, lote): raise NotImplementedError
            def create_cancel_nfse(self, nfse): raise NotImplementedError
            def create_consult_nfse(self, nfse): raise NotImplementedError
        return _XMLBase()

    def create_rps_nfse(
        self,
        rps_list: List[Rps],
        numero_lote: int,
        cnpj: str,
        inscricao_municipal: str,
        signature: Optional[Signature] = None,
        certificate_data: Optional[bytes] = None,
        certificate_password: Optional[str] = None,
        lote_id: Optional[str] = None,
    ) -> str:
        """Cria XML conforme enviar_lote_rps.xml (p:/p1:, estrutura SpeedGov)."""
        lote = LoteRps(
            id=lote_id or "",
            numero_lote=numero_lote,
            cnpj=cnpj,
            inscricao_municipal=inscricao_municipal,
            quantidade_rps=len(rps_list),
            lista_rps=ListaRps(rps=rps_list),
        )
        if signature and certificate_data is None:
            for rps in lote.lista_rps.rps:
                rps.signature = signature
        envio = EnviarLoteRpsEnvio(lote_rps=lote)

        nsmap = {
            "p": ENVIO_NS,
            "p1": TIPOS_NS,
            "ds": XMLDSIG_NS,
            "xsi": XSI_NS,
        }
        root = envio.to_element(
            "EnviarLoteRpsEnvio",
            namespace=ENVIO_NS,
            nsmap=nsmap,
        )
        root.set(f"{{{XSI_NS}}}schemaLocation", ENVIO_NS)

        if certificate_data is not None:
            lista = root.find(f".//{{{TIPOS_NS}}}ListaRps")
            if lista is not None:
                rps_elements = list(lista.findall(f"{{{TIPOS_NS}}}Rps"))
                for i, rps_el in enumerate(rps_elements):
                    inf = rps_el.find(f"{{{TIPOS_NS}}}InfRps")
                    if inf is not None and not inf.get("Id"):
                        inf.set("Id", f"rps_{i}")
                    ref_uri = f"#rps_{i}"
                    signed = sign_rps_element(
                        rps_el,
                        certificate_data,
                        password=certificate_password,
                        reference_uri=ref_uri,
                    )
                    lista.remove(rps_el)
                    lista.append(signed)
            body_str = etree.tostring(
                root, encoding="UTF-8", xml_declaration=False, pretty_print=False
            ).decode("utf-8")
            body_str = _remove_ds_prefix(body_str)
        else:
            body_str = etree.tostring(
                root, encoding="UTF-8", xml_declaration=False, pretty_print=False
            ).decode("utf-8")

        header = get_header_speedgov()
        xml_base = self.get_xml_base()
        return xml_base.create_soap_envelope(
            body_content=body_str,
            method_name="RecepcionarLoteRps",
            header_content=header,
            use_cdata=False,  # Referência enviar_lote_rps.xml não usa CDATA
        )

    def create_consult_nfse(
        self,
        cnpj: str,
        inscricao_municipal: str,
        numero_nfse: Optional[int] = None,
    ) -> str:
        """Cria XML para consulta de NFSE (ConsultarNfse)."""
        consulta = ConsultarNfseEnvio(
            prestador=AbrasfIdentificacaoPrestador(
                cnpj=cnpj,
                inscricao_municipal=inscricao_municipal,
            ),
            numero_nfse=numero_nfse,
        )
        body_str = _serialize_request_model(
            consulta,
            "ConsultarNfseEnvio",
            CONSULTAR_NFSE_ENVIO_NS,
        )
        header = get_header_speedgov()
        return self.get_xml_base().create_soap_envelope(
            body_content=body_str,
            method_name="ConsultarNfse",
            header_content=header,
            use_cdata=False,
        )

    def create_consult_rps(
        self,
        numero: int,
        serie: str,
        tipo: int,
        cnpj: str,
        inscricao_municipal: str,
    ) -> str:
        """Cria XML para consulta de NFSE por RPS (ConsultarNfsePorRps)."""
        consulta = ConsultarNfseRpsEnvio(
            identificacao_rps=AbrasfIdentificacaoRps(numero=numero, serie=serie, tipo=tipo),
            prestador=AbrasfIdentificacaoPrestador(
                cnpj=cnpj,
                inscricao_municipal=inscricao_municipal,
            ),
        )
        body_str = _serialize_request_model(
            consulta,
            "ConsultarNfseRpsEnvio",
            CONSULTAR_NFSE_RPS_ENVIO_NS,
        )
        header = get_header_speedgov()
        return self.get_xml_base().create_soap_envelope(
            body_content=body_str,
            method_name="ConsultarNfsePorRps",
            header_content=header,
            use_cdata=False,
        )

    def create_consult_lote_rps(
        self,
        protocolo: str,
        cnpj: str,
        inscricao_municipal: str,
    ) -> str:
        """Cria XML para consulta de lote de RPS por protocolo (ConsultarLoteRps)."""
        consulta = ConsultarLoteRpsEnvio(
            id="",
            prestador=AbrasfIdentificacaoPrestador(
                cnpj=cnpj,
                inscricao_municipal=inscricao_municipal,
            ),
            protocolo=protocolo,
        )
        body_str = _serialize_request_model(
            consulta,
            "ConsultarLoteRpsEnvio",
            CONSULTAR_LOTE_RPS_ENVIO_NS,
        )
        header = get_header_speedgov()
        return self.get_xml_base().create_soap_envelope(
            body_content=body_str,
            method_name="ConsultarLoteRps",
            header_content=header,
            use_cdata=False,
        )

    def create_consult_situacao_lote_rps(
        self,
        protocolo: str,
        cnpj: str,
        inscricao_municipal: str,
    ) -> str:
        """Cria XML para consulta de situação de lote de RPS (ConsultarSituacaoLoteRps)."""
        consulta = ConsultarSituacaoLoteRpsEnvio(
            id="",
            prestador=AbrasfIdentificacaoPrestador(
                cnpj=cnpj,
                inscricao_municipal=inscricao_municipal,
            ),
            protocolo=protocolo,
        )
        body_str = _serialize_request_model(
            consulta,
            "ConsultarSituacaoLoteRpsEnvio",
            CONSULTAR_SITUACAO_LOTE_RPS_ENVIO_NS,
        )
        header = get_header_speedgov()
        return self.get_xml_base().create_soap_envelope(
            body_content=body_str,
            method_name="ConsultarSituacaoLoteRps",
            header_content=header,
            use_cdata=False,
        )

    def create_cancel_nfse(
        self,
        numero_nfse: int,
        cnpj: str,
        inscricao_municipal: str,
        codigo_municipio: int,
        codigo_cancelamento: str,
        id_pedido: str = "",
    ) -> str:
        """Cria XML para cancelamento de NFSE (CancelarNfse)."""
        pedido = PedidoCancelamento(
            inf_pedido_cancelamento=InfPedidoCancelamento(
                id=id_pedido or None,
                identificacao_nfse=IdentificacaoNfse(
                    numero=numero_nfse,
                    cnpj=cnpj,
                    inscricao_municipal=inscricao_municipal,
                    codigo_municipio=codigo_municipio,
                ),
                codigo_cancelamento=codigo_cancelamento,
            ),
        )
        body_str = _serialize_request_model(
            CancelarNfseEnvio(pedido=pedido),
            "CancelarNfseEnvio",
            CANCELAR_NFSE_ENVIO_NS,
        )
        header = get_header_speedgov()
        return self.get_xml_base().create_soap_envelope(
            body_content=body_str,
            method_name="CancelarNfse",
            header_content=header,
            use_cdata=False,
        )

    def parse_resposta(self, response_xml: str, model_class: Type[T]) -> T:
        """
        Converte XML de resposta em modelo Pydantic (xml -> pydantic).

        Args:
            response_xml: XML da resposta SOAP (ex: result.response.text).
            model_class: Classe do modelo (EnviarLoteRpsResposta, ConsultarNfseResposta, etc.).

        Returns:
            Instância do modelo populada.
        """
        return parse_resposta_xml(response_xml, model_class)

    def parse_resposta_enviar_lote(self, response_xml: str) -> EnviarLoteRpsResposta:
        """Parse de resposta RecepcionarLoteRps."""
        return self.parse_resposta(response_xml, EnviarLoteRpsResposta)

    def parse_resposta_consultar_nfse(self, response_xml: str) -> ConsultarNfseResposta:
        """Parse de resposta ConsultarNfse."""
        return self.parse_resposta(response_xml, ConsultarNfseResposta)

    def parse_resposta_consultar_rps(self, response_xml: str) -> ConsultarNfseRpsResposta:
        """Parse de resposta ConsultarNfsePorRps."""
        return self.parse_resposta(response_xml, ConsultarNfseRpsResposta)

    def parse_resposta_consultar_lote_rps(self, response_xml: str) -> ConsultarLoteRpsResposta:
        """Parse de resposta ConsultarLoteRps."""
        return self.parse_resposta(response_xml, ConsultarLoteRpsResposta)

    def parse_resposta_consultar_situacao_lote(
        self, response_xml: str
    ) -> ConsultarSituacaoLoteRpsResposta:
        """Parse de resposta ConsultarSituacaoLoteRps."""
        return self.parse_resposta(response_xml, ConsultarSituacaoLoteRpsResposta)

    def parse_resposta_cancelar(self, response_xml: str) -> CancelarNfseResposta:
        """Parse de resposta CancelarNfse."""
        return self.parse_resposta(response_xml, CancelarNfseResposta)
