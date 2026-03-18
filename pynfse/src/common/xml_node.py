from datetime import date, datetime
from lxml import etree
from typing import Any, ClassVar, Dict, List, Optional, Set, Union
from pydantic import BaseModel, ConfigDict


class XMLNode(BaseModel):
    """
    Classe base para todos os nós XML do pyNFSE.
    Fornece funcionalidade para converter modelos Pydantic em elementos lxml.
    """
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    xml_attribute_aliases: ClassVar[Set[str]] = set()
    xml_inherit_namespace_for_children: ClassVar[bool] = False
    xml_child_namespace: ClassVar[Optional[str]] = None

    @classmethod
    def _is_xml_attribute(cls, xml_tag: str) -> bool:
        return (
            xml_tag in cls.xml_attribute_aliases
            or xml_tag.lower() == "id"
            or xml_tag.upper() == "URI"
        )

    @staticmethod
    def _format_xml_value(value: Any) -> str:
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%dT%H:%M:%S")
        if isinstance(value, date):
            return value.isoformat()
        return str(value)

    @staticmethod
    def _field_xml_namespace(field_info: Any, default_namespace: Optional[str]) -> Optional[str]:
        extra = field_info.json_schema_extra or {}
        if "xml_namespace" in extra:
            return extra["xml_namespace"]
        return default_namespace

    @staticmethod
    def _field_xml_child_namespace(field_info: Any) -> Optional[str]:
        extra = field_info.json_schema_extra or {}
        return extra.get("xml_child_namespace")

    @staticmethod
    def _field_xml_reset_default_namespace(field_info: Any) -> bool:
        extra = field_info.json_schema_extra or {}
        return extra.get("xml_reset_default_namespace", True)

    def to_element(
        self,
        tag_name: Optional[str] = None,
        namespace: Optional[str] = None,
        nsmap: Optional[Dict[str, str]] = None,
        child_namespace_override: Optional[str] = None,
    ) -> etree.Element:
        """
        Converte o modelo Pydantic em um elemento lxml.etree.Element.
        """
        if tag_name is None:
            tag_name = self.__class__.__name__

        # O elemento atual pode ter namespace
        full_tag_name = f"{{{namespace}}}{tag_name}" if namespace else tag_name
        element = etree.Element(full_tag_name, nsmap=nsmap)
        
        child_namespace = child_namespace_override
        if child_namespace is None:
            child_namespace = namespace if self.xml_inherit_namespace_for_children else self.xml_child_namespace

        for field_name, field_info in self.__class__.model_fields.items():
            value = getattr(self, field_name)
            if value is None:
                continue
                
            xml_tag = field_info.alias or field_name
            
            if self.__class__._is_xml_attribute(xml_tag):
                element.set(xml_tag, self._format_xml_value(value))
                continue

            field_namespace = self._field_xml_namespace(field_info, child_namespace)
            field_child_namespace = self._field_xml_child_namespace(field_info)
            reset_default_namespace = self._field_xml_reset_default_namespace(field_info)

            if isinstance(value, XMLNode):
                child_nsmap = (
                    {None: ""}
                    if namespace is not None and field_namespace is None and reset_default_namespace
                    else None
                )
                element.append(
                    value.to_element(
                        xml_tag,
                        namespace=field_namespace,
                        nsmap=child_nsmap,
                        child_namespace_override=field_child_namespace,
                    )
                )
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, XMLNode):
                        child_nsmap = (
                            {None: ""}
                            if namespace is not None and field_namespace is None and reset_default_namespace
                            else None
                        )
                        element.append(
                            item.to_element(
                                xml_tag,
                                namespace=field_namespace,
                                nsmap=child_nsmap,
                                child_namespace_override=field_child_namespace,
                            )
                        )
                    else:
                        child_tag = f"{{{field_namespace}}}{xml_tag}" if field_namespace else xml_tag
                        child = etree.SubElement(
                            element,
                            child_tag,
                            nsmap=(
                                {None: ""}
                                if namespace is not None and field_namespace is None and reset_default_namespace
                                else None
                            ),
                        )
                        child.text = self._format_xml_value(item)
            else:
                child_tag = f"{{{field_namespace}}}{xml_tag}" if field_namespace else xml_tag
                child = etree.SubElement(
                    element,
                    child_tag,
                    nsmap=(
                        {None: ""}
                        if namespace is not None and field_namespace is None and reset_default_namespace
                        else None
                    ),
                )
                child.text = self._format_xml_value(value)
                
        return element

    def to_xml(
        self,
        tag_name: Optional[str] = None,
        namespace: Optional[str] = None,
        encoding: str = "utf-8",
        pretty_print: bool = True,
        nsmap: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Converte o nó em uma string XML.
        """
        element = self.to_element(tag_name, namespace=namespace, nsmap=nsmap)
        return etree.tostring(element, encoding=encoding, pretty_print=pretty_print, xml_declaration=False).decode(encoding)
