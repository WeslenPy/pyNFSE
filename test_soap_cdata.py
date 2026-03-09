"""Teste para verificar se o XML está no padrão SOAP 1.1 com CDATA."""
from pynfse.src.common.xml import XMLParser

# XML de teste conforme estrutura esperada
xml_test = """<nfse:RecepcionarLoteRps xmlns:nfse="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd">
    <header>
        <p:cabecalho versao="1">
            <versaoDados xmlns="">1</versaoDados>
        </p:cabecalho>
    </header>
    <parameters>
        <p:EnviarLoteRpsEnvio>
            <LoteRps xmlns="" Id="lote_001">
                <NumeroLote>1</NumeroLote>
            </LoteRps>
        </p:EnviarLoteRpsEnvio>
    </parameters>
</nfse:RecepcionarLoteRps>"""

print("XML Original:")
print(xml_test)
print("\n" + "="*60 + "\n")

result = XMLParser.parse_xml_nfse(xml_test)

print("XML Processado:")
print(result)
print("\n" + "="*60 + "\n")

# Verificações
has_cdata_header = '<![CDATA[' in result and 'header' in result
has_cdata_parameters = '<![CDATA[' in result and 'parameters' in result
has_soap_envelope = 'soapenv:Envelope' in result or 'xmlns:soapenv' in result

print("Verificações:")
print(f"✅ Header em CDATA: {has_cdata_header}")
print(f"✅ Parameters em CDATA: {has_cdata_parameters}")
print(f"✅ SOAP 1.1 Envelope: {has_soap_envelope}")

if has_cdata_header and has_cdata_parameters:
    print("\n✅ XML está no padrão SOAP 1.1 com CDATA!")
else:
    print("\n❌ XML NÃO está no padrão correto!")


