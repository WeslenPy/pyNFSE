"""
Header SOAP para SpeedGov (p:cabecalho).
"""
from lxml import etree

from pynfse.src.integration.carnaubal.speedgov.constants import (
    CABECALHO_NS,
    TIPOS_NS,
    XMLDSIG_NS,
    XSI_NS,
)


def get_header_speedgov() -> str:
    """Header p:cabecalho conforme reference."""
    nsmap = {
        "p": CABECALHO_NS,
        "p1": TIPOS_NS,
        "ds": XMLDSIG_NS,
        "xsi": XSI_NS,
    }
    root = etree.Element(f"{{{CABECALHO_NS}}}cabecalho", nsmap=nsmap)
    root.set("versao", "1")
    root.set(f"{{{XSI_NS}}}schemaLocation", CABECALHO_NS)
    v = etree.SubElement(root, "{}versaoDados")
    v.text = "1"
    return etree.tostring(
        root,
        encoding="UTF-8",
        xml_declaration=False,
        pretty_print=False,
    ).decode("utf-8")
