from abc import abstractmethod
from pathlib import Path
from urllib.parse import urlparse
from typing import Any, Dict, Optional, Type, TypeVar
import requests
import xmltodict
from pydantic import BaseModel

from pynfse.src.common.response import ResponseNFSE
from pynfse.src.common.xml import XMLBase
from loguru import logger

from bs4 import BeautifulSoup

T = TypeVar("T", bound=BaseModel)

class NFSeBase:
    def __init__(self, URL: str, **kwargs):

        self.URL = URL

        self.headers = {'Content-Type': 'text/xml; charset=utf-8'}

        self.session = requests.Session()

        self.session.url = self.URL
        self.session.headers = self.headers
        self.session.verify = False

    def get_xml_base(self)->XMLBase:
        return XMLBase()
    
    def render(self,xml:str)->str:
        logger.info("Render do XML")
        return self.parse(xml.replace('\n',''))

    def parse(self,xml:str)->str:
        logger.info("Parse de XML")

        # soup = BeautifulSoup(xml, 'lxml-xml')
        # header = soup.header
        # content = header.decode_contents()
        # soup.header.clear()
        # soup.header.append(content)
        # parameters = soup.parameters
        # content_parameters = parameters.decode_contents()
        # soup.parameters.clear()
        # soup.parameters.append(content_parameters)
        xml = xml.replace(' &lt;','&lt;')
        return xml



    def send(self, xml: str)->ResponseNFSE:
        """Send the RPS to the NFSe"""
        
        # xml = self.render(xml)
        
        # xml = xml.replace("ds:", "")
        
        logger.debug(xml)
        
        response = self.session.post(url= self.URL,  data=xml)

        logger.debug(f"Status Code: {response.status_code}")
        logger.debug(f"Resposta do servidor: {response.text }")
        
        return ResponseNFSE(xml,response)

    def parse_response(self, response_text: str) -> Dict[str, Any]:
        """
        Converte o XML de resposta em um dicionário genérico.
        Remove envelopes SOAP e namespaces para facilitar o uso por camadas superiores.
        """
        # Converte XML para dicionário
        data_dict = xmltodict.parse(
            response_text, 
            attr_prefix='', 
            cdata_key='text',
            process_namespaces=False
        )

        # 1. Navega até o conteúdo útil (extraindo de dentro do Envelope SOAP se existir)
        content = data_dict
        for soap_key in ["soap:Envelope", "soapenv:Envelope", "Envelope"]:
            if soap_key in content:
                content = content[soap_key]
                for body_key in ["soap:Body", "soapenv:Body", "Body"]:
                    if body_key in content:
                        content = content[body_key]
                        break
                break
        
        # 2. Limpa os namespaces e atributos das chaves do dicionário
        def clean_dict(d):
            if not isinstance(d, dict):
                if isinstance(d, list):
                    return [clean_dict(item) for item in d]
                return d
            
            new_dict = {}
            for k, v in d.items():
                # Ignora atributos XML (como xmlns, xmlns:ns1, etc)
                if k.startswith("xmlns") or k == "xmlns":
                    continue
                
                # Remove namespace prefix (ex: ns1:Tag -> Tag)
                clean_k = k.split(':')[-1]
                new_dict[clean_k] = clean_dict(v)
            return new_dict

        final_content = clean_dict(content)
        
        # 3. Navega para dentro de tags de resposta se houver apenas uma chave
        # Repete o processo até encontrar um dicionário com múltiplas chaves ou conteúdo real
        while isinstance(final_content, dict) and len(final_content) == 1:
            key = list(final_content.keys())[0]
            val = final_content[key]
            if isinstance(val, dict):
                final_content = val
            else:
                break

        return final_content


    def send_nfse(self,lote):
        self.xml = self.get_xml_base()
        xml_data = self.xml.create_rps_nfse(lote=lote)
        return self.send(xml_data)


    def get_url_pdf(self, identification_number: str,nfse_id: int)->str:
        parse = urlparse(self.URL)
        domain = parse.netloc
        schema = parse.scheme

        return f"{schema}://{domain}/satcar/servlet//com.satweb.imprimenota?{identification_number}NF{nfse_id}"


    def get_pdf(self, identification_number: str,nfse_id: int)->bytes:
        url = self.get_url_pdf(identification_number,nfse_id)

        response = requests.get(url=url)
        if 'application/pdf' in response.headers.get("Content-Type",'not'):
            return response.content

        return False
