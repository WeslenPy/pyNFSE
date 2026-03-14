from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
from loguru import logger
import re
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

    def create_soap_envelope(self, body_content: str, method_name: str, header_content: Optional[str] = None) -> str:
        """
        Cria um envelope SOAP 1.1 genérico com CDATA para o padrão ABRASF/SpeedGov.
        """
        soap_env = "http://schemas.xmlsoap.org/soap/envelope/"
        nfse_ns = "http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd"
        compact_body = self._compact_xml(body_content)
        compact_header = self._compact_xml(header_content) if header_content else None

        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<soapenv:Envelope xmlns:soapenv="{soap_env}"',
            f'      xmlns:nfse="{nfse_ns}">',
            '      <soapenv:Header />',
            '      <soapenv:Body>',
            f'            <nfse:{method_name}>',
        ]

        if compact_header:
            lines.append(f'                  <header><![CDATA[{compact_header}]]></header>')

        lines.extend([
            f'                  <parameters><![CDATA[{compact_body}]]></parameters>',
            f'            </nfse:{method_name}>',
            '      </soapenv:Body>',
            '</soapenv:Envelope>',
        ])

        return "\n".join(lines)

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
