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

    def create_soap_envelope(self, body_content: str, method_name: str, header_content: Optional[str] = None) -> str:
        """
        Cria um envelope SOAP 1.1 genérico com CDATA para o padrão ABRASF/SpeedGov.
        """
        # Namespaces padrão
        soap_env = "http://schemas.xmlsoap.org/soap/envelope/"
        nfse_ns = "http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd"
        
        envelope = etree.Element(f"{{{soap_env}}}Envelope", nsmap={
            'soapenv': soap_env,
            'nfse': nfse_ns
        })
        
        etree.SubElement(envelope, f"{{{soap_env}}}Header")
        body = etree.SubElement(envelope, f"{{{soap_env}}}Body")
        
        method = etree.SubElement(body, f"{{{nfse_ns}}}{method_name}")
        
        if header_content:
            header_tag = etree.SubElement(method, "header")
            header_tag.text = etree.CDATA(header_content)
            
        parameters_tag = etree.SubElement(method, "parameters")
        parameters_tag.text = etree.CDATA(body_content)
        
        return etree.tostring(envelope, encoding="UTF-8", xml_declaration=True, pretty_print=True).decode("utf-8")

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
