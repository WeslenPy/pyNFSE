from datetime import datetime
from lxml import etree
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, ConfigDict


class XMLNode(BaseModel):
    """
    Classe base para todos os nós XML do pyNFSE.
    Fornece funcionalidade para converter modelos Pydantic em elementos lxml.
    """
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    def to_element(self, tag_name: Optional[str] = None) -> etree.Element:
        """
        Converte o modelo Pydantic em um elemento lxml.etree.Element.
        """
        if tag_name is None:
            # Usa o nome da classe como nome da tag se não for fornecido
            tag_name = self.__class__.__name__

        element = etree.Element(tag_name)
        
        # Itera pelos campos do modelo
        for field_name, field_info in self.__class__.model_fields.items():
            value = getattr(self, field_name)
            
            if value is None:
                continue
                
            # Usa o alias do campo se disponível (importante para nomes de tags XML com iniciais maiúsculas)
            xml_tag = field_info.alias or field_name
            
            # Se o campo for 'id' ou 'Id', e for um atributo XML (comum em ABRASF)
            if xml_tag.lower() == "id" and isinstance(value, str):
                element.set("Id", value)
                continue

            # Se o campo for 'uri' ou 'URI', e for um atributo XML (comum em XMLDSIG)
            if xml_tag.upper() == "URI" and isinstance(value, str):
                element.set("URI", value)
                continue

            if isinstance(value, XMLNode):
                # Recursão para nós filhos
                element.append(value.to_element(xml_tag))
            elif isinstance(value, list):
                # Trata listas de itens
                for item in value:
                    if isinstance(item, XMLNode):
                        element.append(item.to_element(xml_tag))
                    else:
                        child = etree.SubElement(element, xml_tag)
                        child.text = str(item)
            else:
                # Trata valores simples
                child = etree.SubElement(element, xml_tag)
                if isinstance(value, datetime):
                    child.text = value.isoformat()
                else:
                    child.text = str(value)
                
        return element

    def to_xml(self, tag_name: Optional[str] = None, encoding: str = "utf-8", pretty_print: bool = True) -> str:
        """
        Converte o nó em uma string XML.
        """
        element = self.to_element(tag_name)
        return etree.tostring(element, encoding=encoding, pretty_print=pretty_print, xml_declaration=False).decode(encoding)
