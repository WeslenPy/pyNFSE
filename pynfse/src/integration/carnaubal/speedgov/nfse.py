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
from pynfse.src.integration.carnaubal.speedgov.models.rps import Rps
from pynfse.src.integration.carnaubal.speedgov.models.lote import LoteRps, ListaRps
from pynfse.src.integration.carnaubal.speedgov.helper.build import (
    build_cancelar_nfse_xml,
    build_consult_lote_rps_xml,
    build_consult_nfse_xml,
    build_consult_rps_xml,
    build_consult_situacao_lote_rps_xml,
    build_lote_element,
    build_lote_xml,
    get_header_speedgov,
)
from pynfse.src.integration.carnaubal.speedgov.helper.build import TIPOS_NS
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
XMLDSIG_NS = "http://www.w3.org/2000/09/xmldsig#"


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

        if certificate_data is not None:
            root = build_lote_element(lote, signatures=None)
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
            sigs = [signature] * len(rps_list) if signature else None
            body_str = build_lote_xml(lote, sigs)

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
        body_str = build_consult_nfse_xml(
            cnpj=cnpj,
            inscricao_municipal=inscricao_municipal,
            numero_nfse=numero_nfse,
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
        body_str = build_consult_rps_xml(
            numero=numero,
            serie=serie,
            tipo=tipo,
            cnpj=cnpj,
            inscricao_municipal=inscricao_municipal,
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
        body_str = build_consult_lote_rps_xml(
            cnpj=cnpj,
            inscricao_municipal=inscricao_municipal,
            protocolo=protocolo,
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
        body_str = build_consult_situacao_lote_rps_xml(
            cnpj=cnpj,
            inscricao_municipal=inscricao_municipal,
            protocolo=protocolo,
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
        body_str = build_cancelar_nfse_xml(
            numero_nfse=numero_nfse,
            cnpj=cnpj,
            inscricao_municipal=inscricao_municipal,
            codigo_municipio=codigo_municipio,
            codigo_cancelamento=codigo_cancelamento,
            id_pedido=id_pedido,
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
