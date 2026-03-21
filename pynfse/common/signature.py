from typing import List, Optional, Union, Dict
from pydantic import Field
from pynfse.common.xml_node import XMLNode
from lxml import etree

class SignatureNode(XMLNode):
    """Classe base para nós da Assinatura Digital (XMLDSIG)."""
    xml_attribute_aliases = {"Algorithm", "URI"}
    xml_inherit_namespace_for_children = True

    def to_element(
        self,
        tag_name: Optional[str] = None,
        namespace: Optional[str] = "http://www.w3.org/2000/09/xmldsig#",
        nsmap: Optional[Dict[str, str]] = None,
        child_namespace_override: Optional[str] = None,
    ) -> etree.Element:
        # if namespace is None:
        #     namespace =  "http://www.w3.org/2000/09/xmldsig#"
        # # Garante que o elemento Signature sempre declare xmlns="http://www.w3.org/2000/09/xmldsig#"
        # if tag_name == "Signature":
        #     nsmap = {None: namespace}
        return super().to_element(
            tag_name,
            namespace=namespace,
            nsmap=nsmap,
            child_namespace_override=child_namespace_override,
        )

class CanonicalizationMethod(SignatureNode):
    algorithm: str = Field(..., alias="Algorithm")

class SignatureMethod(SignatureNode):
    algorithm: str = Field(..., alias="Algorithm")

class Transform(SignatureNode):
    algorithm: str = Field(..., alias="Algorithm")

class Transforms(SignatureNode):
    transform: List[Transform] = Field(..., alias="Transform")

class DigestMethod(SignatureNode):
    algorithm: str = Field(..., alias="Algorithm")

class Reference(SignatureNode):
    uri: str = Field(..., alias="URI")
    transforms: Optional[Transforms] = Field(None, alias="Transforms")
    digest_method: DigestMethod = Field(..., alias="DigestMethod")
    digest_value: str = Field(..., alias="DigestValue")

class SignedInfo(SignatureNode):
    canonicalization_method: CanonicalizationMethod = Field(..., alias="CanonicalizationMethod")
    signature_method: SignatureMethod = Field(..., alias="SignatureMethod")
    reference: List[Reference] = Field(..., alias="Reference")

class X509Data(SignatureNode):
    x509_certificate: str = Field(..., alias="X509Certificate")

class KeyInfo(SignatureNode):
    x509_data: Optional[X509Data] = Field(None, alias="X509Data")

class Signature(SignatureNode):
    signed_info: SignedInfo = Field(..., alias="SignedInfo")
    signature_value: str = Field(..., alias="SignatureValue")
    key_info: Optional[KeyInfo] = Field(None, alias="KeyInfo")
