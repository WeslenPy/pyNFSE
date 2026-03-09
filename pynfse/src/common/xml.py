from abc import abstractmethod
from jinja2 import Environment, PackageLoader
from pathlib import Path

from typing import Optional
from pynfse.schemas.nfse import InfoRPS
from pynfse.schemas.rps import CancelNFSE, ConsultNFSE
from pynfse.schemas.lote import LoteRps
from bs4 import BeautifulSoup
from loguru import logger
import re

from functools import wraps


class XMLParser:

    def parse(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            result=  func(*args,**kwargs)

            if isinstance(result,str):
                return XMLParser.parse_xml_nfse(result)  # type: ignore

            return result

        return wrapper

    @staticmethod
    def parse_xml_nfse(xml_nfse: str)->str:
        """
        Parse and clean XML NFSE, preserving CDATA sections.
        
        The template already includes CDATA sections, so we need to preserve
        them when processing the XML. This method ensures CDATA content is
        not escaped when the XML is processed.
        """
        logger.debug("Parse de XML NFSE")
        
        # Check if XML already has proper CDATA sections
        # If so, we can skip processing to avoid escaping issues
        has_cdata = '<![CDATA[' in xml_nfse
        
        if has_cdata:
            # XML already has CDATA, just clean up whitespace and return
            # Remove extra newlines but preserve structure
            xml_nfse = xml_nfse.replace("\n", '')
            # Fix any spacing issues around CDATA
            xml_nfse = re.sub(r'\s*<!\[CDATA\[', '<![CDATA[', xml_nfse)
            xml_nfse = re.sub(r'\]\]>\s*', ']]>', xml_nfse)
            print(xml_nfse)
            return xml_nfse
        
        # If no CDATA, process normally (for backward compatibility)
        xml_nfse = xml_nfse.replace("\n", '')
        soup = BeautifulSoup(xml_nfse, 'lxml-xml')
        xml = str(soup)
        print(xml)
        return xml


class XMLBase:

    def __init__(self,templates:Path):
        self.templates = templates 

        print(self.templates.as_posix())

        self.env = Environment(loader=PackageLoader(package_name=__name__,
                                    package_path=self.templates ),
                                    autoescape=False)


        self.base = self.env.get_template('base.xml')

        self.rps = self.env.get_template('rps.xml')
        self.cancel_nfse = self.env.get_template('cancel.xml')
        self.consult_nfse = self.env.get_template('consult.xml')
        self.lote_rps = self.env.get_template('lote_rps.xml')

 
    def create_base(self,soap_body: str)->str:
        """Create the Base XML"""
        return self.base.render(soap_body=soap_body)

    @abstractmethod
    # @XMLParser.parse
    def create_rps_nfse(self, lote: LoteRps) -> str:
        """
        Create the RPS XML.
        
        Se lote for fornecido, cria XML com estrutura LoteRps conforme NFS-e Nacional.
        Caso contrário, cria XML simples com apenas o RPS.
        """
        # Usa estrutura com LoteRps conforme documentação NFS-e Nacional
        xml_body = self.lote_rps.render(lote=lote)
        xml_created = self.create_base(soap_body=xml_body)
        
        print(xml_created)
        return xml_created

    @abstractmethod
    def create_cancel_nfse(self,nfse: CancelNFSE)->str:
        """Create the Cancel NFSE XML"""

    @abstractmethod
    def create_consult_nfse(self,nfse: ConsultNFSE)->str:
        """Create the Consult NFSE XML"""