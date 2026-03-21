"""
Constantes de namespace para SpeedGov (enviar_lote_rps.xml).
"""
DOMAIN = "speedgov.com.br"

ENVIO_NS = f"http://ws.{DOMAIN}/enviar_lote_rps_envio_v1.xsd"
TIPOS_NS = f"http://ws.{DOMAIN}/tipos_v1.xsd"
CABECALHO_NS = f"http://ws.{DOMAIN}/cabecalho_v1.xsd"
XMLDSIG_NS = "http://www.w3.org/2000/09/xmldsig#"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"


WEBSERVICE_PROD_URL = 'http://{DOMAIN}/wscar/Nfes?wsdl'
WEBSERVICE_DEV_URL = 'http://{DOMAIN}/wsmod/Nfes?wsdl'
URL_PDF_FALLBACK = 'https://{DOMAIN}/satcar/servlet//com.satweb.imprimenota?{inscricao_municipal}NF{number}'

CPF_LEN = 11
CNPJ_LEN = 14
