

from abc import abstractmethod
from pathlib import Path
from urllib.parse import urlparse
import requests

from pynfse.schemas.lote import LoteRps
from pynfse.schemas.nfse import InfoRPS
from pynfse.src.common.response import ResponseNFSE
from pynfse.src.common.xml import XMLBase
from loguru import logger


class NFSeBase:
    def __init__(self, URL: str, **kwargs):

        self.TEMPLATES:Path =self.get_templates()

        self.URL = URL

        self.headers = {'Content-Type': 'text/xml; charset=utf-8'}

        self.session = requests.Session()

        self.session.url = self.URL
        self.session.headers = self.headers
        self.session.verify = False

    def get_templates(self,file:Path=None)->Path:

        file=  file or __file__
        print(file)
        return Path(file).parent / 'templates'

    def get_xml_base(self)->XMLBase:
        return XMLBase(templates=self.TEMPLATES)


    def send(self, xml: str)->ResponseNFSE:
        """Send the RPS to the NFSe"""
        
        response = self.session.post(url= self.URL,  data=xml)

        logger.debug(f"Status Code: {response.status_code}")
        logger.debug(f"Resposta do servidor: {response.text }")
        
        return ResponseNFSE(xml,response)


    def send_nfse(self,lote:LoteRps):
        self.xml = self.get_xml_base()
        xml_data = self.xml.create_rps_nfse(lote=lote)
        return self.send(xml_data)



    def get_url_pdf(self, identification_number: str,nfse_id: int)->str:
        parse = urlparse(self.URL)
        domain = parse.netloc
        schema = parse.schema

        return f"{schema}://{domain}/satcar/servlet//com.satweb.imprimenota?{identification_number}NF{nfse_id}"


    def get_pdf(self, identification_number: str,nfse_id: int)->bytes:
        url = self.get_url_pdf(identification_number,nfse_id)

        response = requests.get(url=url)
        if 'application/pdf' in response.headers.get("Content-Type",'not'):
            return response.content

        return False
