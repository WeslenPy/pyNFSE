"""
Assinatura digital para SpeedGov (RPS por RPS).
"""
from typing import Optional

from lxml import etree
from signxml import XMLSigner, methods

from cryptography.hazmat.primitives.serialization import pkcs12


class LegacyXMLSigner(XMLSigner):
    """Permite algoritmos legados exigidos pelo provedor."""

    def check_deprecated_methods(self):
        return None


def _load_certificate(certificate_data: bytes, password: Optional[str] = None):
    """Carrega PFX e retorna (private_key, certificate)."""
    try:
        return pkcs12.load_key_and_certificates(
            certificate_data,
            password.encode() if password else None,
        )[:2]
    except Exception:
        from cryptography.hazmat.primitives import serialization
        from cryptography import x509
        private_key = serialization.load_pem_private_key(
            certificate_data,
            password=password.encode() if password else None,
        )
        certificate = x509.load_pem_x509_certificate(certificate_data)
        return private_key, certificate


def sign_rps_element(
    rps_element: etree._Element,
    certificate_data: bytes,
    password: Optional[str] = None,
    reference_uri: Optional[str] = None,
) -> etree._Element:
    """
    Assina o elemento Rps (enveloped).
    Retorna o elemento assinado - substitua o original pelo retorno.
    """
    private_key, certificate = _load_certificate(certificate_data, password)
    signer = LegacyXMLSigner(
        method=methods.enveloped,
        signature_algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1",
        digest_algorithm="sha1",
        c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315",
    )
    kwargs = {"key": private_key, "cert": [certificate]}
    if reference_uri:
        kwargs["reference_uri"] = reference_uri
    return signer.sign(rps_element, **kwargs)
