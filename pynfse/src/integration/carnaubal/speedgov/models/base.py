"""
Tipos e estruturas base para SpeedGov (enviar_lote_rps.xml).
SpeedGovNode estende XMLNode com suporte a Enum, prefixos p:/p1: e blocos opcionais.
"""
from datetime import date, datetime
from enum import Enum
from typing import Any, ClassVar, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator

from lxml import etree

from pynfse.src.common.xml_node import XMLNode
from pynfse.src.integration.carnaubal.speedgov.constants import TIPOS_NS


def _has_any_value(obj: Any) -> bool:
    """Verifica recursivamente se o objeto tem ao menos um campo não-None."""
    if obj is None:
        return False
    if hasattr(obj, "model_fields"):
        for field_name in obj.model_fields:
            val = getattr(obj, field_name, None)
            if val is not None:
                if hasattr(val, "model_fields"):
                    if _has_any_value(val):
                        return True
                elif isinstance(val, list):
                    for item in val:
                        if _has_any_value(item):
                            return True
                else:
                    return True
        return False
    return True


def _field_xml_emit_if_any(field_info: Any) -> bool:
    """Retorna True se o campo tem xml_emit_if_any=True no json_schema_extra."""
    extra = field_info.json_schema_extra or {}
    return extra.get("xml_emit_if_any", False)


class SpeedGovNode(XMLNode):
    """
    Classe base para nós XML do SpeedGov.
    - Suporta Enum em _format_xml_value (str(v.value))
    - Suporta xml_emit_if_any para blocos opcionais (emitir só se houver valor)
    - Omite atributo Id quando vazio (para assinatura in-place)
    """

    xml_child_namespace: ClassVar[Optional[str]] = TIPOS_NS

    @staticmethod
    def _format_xml_value(value: Any) -> str:
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%dT%H:%M:%S")
        if isinstance(value, date):
            return value.isoformat()
        if isinstance(value, Enum):
            return str(value.value)
        return str(value)

    def to_element(
        self,
        tag_name: Optional[str] = None,
        namespace: Optional[str] = None,
        nsmap: Optional[Dict[str, str]] = None,
        child_namespace_override: Optional[str] = None,
    ) -> etree.Element:
        if tag_name is None:
            tag_name = self.__class__.__name__

        full_tag_name = f"{{{namespace}}}{tag_name}" if namespace else tag_name
        element = etree.Element(full_tag_name, nsmap=nsmap)

        child_namespace = child_namespace_override
        if child_namespace is None:
            child_namespace = (
                namespace if self.xml_inherit_namespace_for_children else self.xml_child_namespace
            )

        for field_name, field_info in self.__class__.model_fields.items():
            value = getattr(self, field_name)
            if value is None:
                continue

            xml_tag = field_info.alias or field_name

            if self.__class__._is_xml_attribute(xml_tag):
                if xml_tag.lower() == "id" and (value is None or value == ""):
                    continue
                element.set(xml_tag, self._format_xml_value(value))
                continue

            field_namespace = self._field_xml_namespace(field_info, child_namespace)
            field_child_namespace = self._field_xml_child_namespace(field_info)
            reset_default_namespace = self._field_xml_reset_default_namespace(field_info)
            emit_if_any = _field_xml_emit_if_any(field_info)

            if isinstance(value, XMLNode):
                if emit_if_any and not _has_any_value(value):
                    continue
                child_nsmap = (
                    {None: ""}
                    if namespace is not None
                    and field_namespace is None
                    and reset_default_namespace
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
                        if emit_if_any and not _has_any_value(item):
                            continue
                        child_nsmap = (
                            {None: ""}
                            if namespace is not None
                            and field_namespace is None
                            and reset_default_namespace
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
                        child_tag = (
                            f"{{{field_namespace}}}{xml_tag}" if field_namespace else xml_tag
                        )
                        child = etree.SubElement(
                            element,
                            child_tag,
                            nsmap=(
                                {None: ""}
                                if namespace is not None
                                and field_namespace is None
                                and reset_default_namespace
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
                        if namespace is not None
                        and field_namespace is None
                        and reset_default_namespace
                        else None
                    ),
                )
                child.text = self._format_xml_value(value)

        return element


# Tipos conforme XSD tipos_v1.xsd
class CpfCnpj(SpeedGovNode):
    """Cpf ou Cnpj - exatamente um."""
    model_config = ConfigDict(populate_by_name=True)

    cpf: Optional[str] = Field(None, alias="Cpf", min_length=11, max_length=11)
    cnpj: Optional[str] = Field(None, alias="Cnpj", min_length=14, max_length=14)

    @model_validator(mode="after")
    def validate_choice(self):
        if bool(self.cpf) == bool(self.cnpj):
            raise ValueError("CpfCnpj deve conter exatamente um entre Cpf ou Cnpj.")
        return self


class Endereco(SpeedGovNode):
    """Endereco do Tomador - sem Contato."""
    model_config = ConfigDict(populate_by_name=True)

    endereco: str = Field(..., alias="Endereco", max_length=125)
    numero: str = Field(..., alias="Numero", max_length=10)
    complemento: Optional[str] = Field(None, alias="Complemento", max_length=60)
    bairro: str = Field(..., alias="Bairro", max_length=60)
    codigo_municipio: int = Field(..., alias="CodigoMunicipio", ge=0, le=9999999)
    uf: str = Field(..., alias="Uf", min_length=2, max_length=2)
    cep: str = Field(..., alias="Cep", max_length=10)
