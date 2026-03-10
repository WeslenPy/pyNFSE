from typing import List, Optional, Union
from pydantic import Field
from pynfse.src.integration.carnaubal.abrasf.models.base import ABRASFNode

class CanonicalizationMethod(ABRASFNode):
    algorithm: str = Field(..., alias="Algorithm")

class SignatureMethod(ABRASFNode):
    algorithm: str = Field(..., alias="Algorithm")

class Transform(ABRASFNode):
    algorithm: str = Field(..., alias="Algorithm")

class Transforms(ABRASFNode):
    transform: List[Transform] = Field(..., alias="Transform")

class DigestMethod(ABRASFNode):
    algorithm: str = Field(..., alias="Algorithm")

class Reference(ABRASFNode):
    uri: str = Field(..., alias="URI")
    transforms: Optional[Transforms] = Field(None, alias="Transforms")
    digest_method: DigestMethod = Field(..., alias="DigestMethod")
    digest_value: str = Field(..., alias="DigestValue")

class SignedInfo(ABRASFNode):
    canonicalization_method: CanonicalizationMethod = Field(..., alias="CanonicalizationMethod")
    signature_method: SignatureMethod = Field(..., alias="SignatureMethod")
    reference: List[Reference] = Field(..., alias="Reference")

class X509Data(ABRASFNode):
    x509_certificate: str = Field(..., alias="X509Certificate")

class KeyInfo(ABRASFNode):
    x509_data: Optional[X509Data] = Field(None, alias="X509Data")

class Signature(ABRASFNode):
    signed_info: SignedInfo = Field(..., alias="SignedInfo")
    signature_value: str = Field(..., alias="SignatureValue")
    key_info: Optional[KeyInfo] = Field(None, alias="KeyInfo")
