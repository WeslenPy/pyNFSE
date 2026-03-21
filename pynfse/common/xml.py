from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
from loguru import logger
import re
from xml.sax.saxutils import escape
from bs4 import BeautifulSoup
from functools import wraps
from lxml import etree


class XMLParser:
    """Helper para processamento e limpeza de XML."""

    def parse(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, str):
                return XMLParser.parse_xml_nfse(result)
            return result
        return wrapper

    @staticmethod
    def parse_xml_nfse(xml_nfse: str) -> str:
        """
        Limpa o XML preservando seções CDATA.
        """
        logger.debug("Processando XML NFSE")
        
        has_cdata = '<![CDATA[' in xml_nfse
        
        if has_cdata:
            # Remove quebras de linha extras mas preserva estrutura
            xml_nfse = xml_nfse.replace("\n", '')
            # Ajusta espaços ao redor de CDATA
            xml_nfse = re.sub(r'\s*<!\[CDATA\[', '<![CDATA[', xml_nfse)
            xml_nfse = re.sub(r'\]\]>\s*', ']]>', xml_nfse)
            return xml_nfse
        
        # Se não tiver CDATA, usa BeautifulSoup para formatar
        xml_nfse = xml_nfse.replace("\n", '')
        soup = BeautifulSoup(xml_nfse, 'lxml-xml')
        return str(soup)


class XMLBase(ABC):
    """
    Classe base para geração de XML.
    Refatorada para não usar Jinja2, priorizando modelos Pydantic.
    """

    def __init__(self, templates: Optional[Path] = None):
        self.templates = templates

    @staticmethod
    def _compact_xml(xml_content: str) -> str:
        xml_content = xml_content.strip()
        return re.sub(r">\s+<", "><", xml_content)

    @staticmethod
    def _escape_embedded_xml(xml_content: str) -> str:
        return escape(
            xml_content,
            {
                '"': "&quot;",
                "'": "&quot;",
            },
        )

    def create_soap_envelope(self, body_content: str, method_name: str, header_content: Optional[str] = None, use_cdata: bool = True) -> str:
        """
        Cria um envelope SOAP 1.1 com o XML interno em header e parameters.

        Args:
            use_cdata: Se True (padrão), usa CDATA para header/parameters (novo padrão SpeedGov).
                       Se False, usa escape XML (legado).
        """
        soap_env = "http://schemas.xmlsoap.org/soap/envelope/"
        nfse_ns = "http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd"
        compact_body = self._compact_xml(body_content)
        compact_header = self._compact_xml(header_content) if header_content else None

        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<soapenv:Envelope xmlns:soapenv="{soap_env}" xmlns:nfse="{nfse_ns}">',
            "  <soapenv:Header/>",
            "  <soapenv:Body>",
            f"    <nfse:{method_name}>",
        ]

        if compact_header:
            if use_cdata:
                h = compact_header.replace("<?xml version=\"1.0\" encoding=\"UTF-8\"?>", "").strip()
                lines.append(f"      <header><![CDATA[{h}]]></header>")
            else:
                escaped_header = self._escape_embedded_xml(compact_header)
                lines.append(f"      <header>{escaped_header}</header>")

        if use_cdata:
            b = compact_body.replace("<?xml version=\"1.0\" encoding=\"UTF-8\"?>", "").strip()
            lines.append(f"      <parameters><![CDATA[{b}]]></parameters>")
        else:
            escaped_body = self._escape_embedded_xml(compact_body)
            lines.append(f"      <parameters>{escaped_body}</parameters>")

        lines.extend(
            [
                f"    </nfse:{method_name}>",
                "  </soapenv:Body>",
                "</soapenv:Envelope>",
            ]
        )

        return "\n".join(lines) + "\n"

    @abstractmethod
    def create_rps_nfse(self, lote) -> str:
        """Deve ser implementado pelo provedor específico."""
        pass

    @abstractmethod
    def create_cancel_nfse(self, nfse) -> str:
        """Deve ser implementado pelo provedor específico."""
        pass

    @abstractmethod
    def create_consult_nfse(self, nfse) -> str:
        """Deve ser implementado pelo provedor específico."""
        pass
