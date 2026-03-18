"""
Parser de respostas XML para modelos Pydantic.
Converte XML de resposta SOAP em dict normalizado e popula classes Pydantic (xml -> pydantic).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Type, TypeVar, get_origin, get_args

import xmltodict
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def _clean_dict(d: Any) -> Any:
    """
    Remove namespaces das chaves e limpa atributos XML.
    """
    if not isinstance(d, dict):
        if isinstance(d, list):
            return [_clean_dict(item) for item in d]
        return d

    new_dict: Dict[str, Any] = {}
    for k, v in d.items():
        if k.startswith("xmlns") or k == "xmlns" or k.startswith("@"):
            continue
        clean_k = k.split(":")[-1]
        new_dict[clean_k] = _clean_dict(v)
    return new_dict


RESPOSTA_ROOTS = frozenset([
    "EnviarLoteRpsResposta", "ConsultarNfseResposta", "ConsultarNfseRpsResposta",
    "ConsultarLoteRpsResposta", "ConsultarSituacaoLoteRpsResposta", "CancelarNfseResposta",
])


def _find_resposta_root(content: Any, target_tag: Optional[str] = None) -> Dict[str, Any]:
    """
    Localiza o dict da resposta (por tag conhecida) navegando no envelope SOAP.
    """
    if not isinstance(content, dict):
        return {}

    # Sair do envelope SOAP
    for soap_key in ["soap:Envelope", "soapenv:Envelope", "Envelope"]:
        if soap_key in content:
            content = content[soap_key]
            break

    for body_key in ["soap:Body", "soapenv:Body", "Body"]:
        if isinstance(content, dict) and body_key in content:
            content = content[body_key]
            break

    # Desembrulha *Response e *Result até encontrar a tag de resposta
    while isinstance(content, dict) and len(content) == 1:
        key = list(content.keys())[0]
        val = content[key]
        if key in RESPOSTA_ROOTS or (target_tag and key == target_tag):
            # Retorna o conteúdo interno da tag de resposta
            return val if isinstance(val, dict) else content
        if isinstance(val, dict):
            content = val
        else:
            break

    return content if isinstance(content, dict) else {}


def _is_list_field(field_type: Any) -> bool:
    """Verifica se o tipo do campo é List[...]."""
    origin = get_origin(field_type)
    return origin is list


def _normalize_for_model(d: Any, model_class: Type[BaseModel], field_name: Optional[str] = None) -> Any:
    """
    Normaliza o dict para compatibilidade com Pydantic.
    - Converte valor único em lista quando o campo espera List
    - Remove chaves com valor None ou vazio
    """
    if d is None:
        return None

    if isinstance(d, list):
        return [_normalize_for_model(item, model_class, field_name) for item in d]

    if not isinstance(d, dict):
        return d

    # Obter campos do modelo para saber quais esperam lista
    model_fields = getattr(model_class, "model_fields", {})
    result: Dict[str, Any] = {}

    for k, v in d.items():
        if v is None or (isinstance(v, str) and v.strip() == ""):
            continue

        # Encontrar o field info pelo alias ou nome
        field_info = None
        for fname, finfo in model_fields.items():
            alias = getattr(finfo, "alias", None) or fname
            if alias == k or fname == k:
                field_info = finfo
                break

        if field_info is not None:
            field_type = field_info.annotation
            if _is_list_field(field_type) and isinstance(v, dict):
                v = [v]
            # Recursão para modelos aninhados
            args = get_args(field_type)
            if args and isinstance(v, dict):
                inner_model = args[0]
                if isinstance(inner_model, type) and issubclass(inner_model, BaseModel):
                    if isinstance(v, list):
                        v = [_normalize_for_model(x, inner_model, None) for x in v]
                    else:
                        v = _normalize_for_model(v, inner_model, None)
            elif args and isinstance(v, list):
                inner_model = args[0]
                if isinstance(inner_model, type) and issubclass(inner_model, BaseModel):
                    v = [_normalize_for_model(x, inner_model, None) for x in v]
        elif isinstance(v, dict):
            v = _clean_dict(v)

        result[k] = v

    return result


def parse_soap_to_dict(xml_text: str) -> Dict[str, Any]:
    """
    Converte XML de resposta SOAP em dicionário limpo (sem namespaces).
    """
    data = xmltodict.parse(
        xml_text,
        attr_prefix="",
        cdata_key="text",
        process_namespaces=False,
    )
    return _clean_dict(data)


def _extract_resposta_dict(xml_text: str, root_tag: Optional[str] = None) -> Dict[str, Any]:
    """Extrai o dict da tag de resposta do XML SOAP."""
    data = xmltodict.parse(
        xml_text,
        attr_prefix="",
        cdata_key="text",
        process_namespaces=False,
    )
    data = _clean_dict(data)
    content = _find_resposta_root(data, root_tag)
    return content if isinstance(content, dict) else {}


def parse_resposta_xml(xml_text: str, model_class: Type[T], root_tag: Optional[str] = None) -> T:
    """
    Converte XML de resposta em instância do modelo Pydantic.

    Args:
        xml_text: XML completo da resposta (envelope SOAP).
        model_class: Classe do modelo Pydantic (ex: EnviarLoteRpsResposta).
        root_tag: Tag raiz esperada (ex: "EnviarLoteRpsResposta").
                  Se None, infere a partir de model_class.__name__.

    Returns:
        Instância do modelo populada com os dados do XML.
    """
    tag = root_tag or model_class.__name__
    data = _extract_resposta_dict(xml_text, root_tag=tag)
    normalized = _normalize_for_model(data, model_class, None)
    return model_class.model_validate(normalized)
