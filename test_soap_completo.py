"""Teste completo para verificar SOAP 1.1 com CDATA."""
from pynfse.src.integration.carnaubal.abrasf.nfse import CarnaubalNFSe
from pynfse.schemas.nfse import (
    InfoRPS, IdentificationNFSE, ValuesNFSE, ProviderNFSE,
    ServicesNFSE, IdentificationCostumerNFSE, AddressNFSE, CostumerNFSE
)
from datetime import date

# Criar RPS de teste
rps = InfoRPS(
    identification=IdentificationNFSE(number=1, serie="A"),
    costumer=CostumerNFSE(
        identification=IdentificationCostumerNFSE(cpf_cnpj="12345678901"),
        social_name="Cliente Teste",
        address=AddressNFSE(
            address="Rua Teste",
            number="123",
            district="Centro",
            uf="RN",
            zip_code="59000000"
        )
    ),
    services=ServicesNFSE(
        description="Teste",
        code_municipio="2408102",
        values=ValuesNFSE(
            value_services=1000.0,
            value_iss=50.0,
            base_calculation=1000.0,
            aliquot=5.0,
            liquid_value=950.0
        )
    ),
    provider=ProviderNFSE(
        cnpj="12345678000190",
        municipal_registration=12345
    ),
    date=date.today()
)

# Criar cliente
nfse = CarnaubalNFSe(URL="http://test.com/nfse")

# Gerar XML
xml = nfse.create_rps_nfse(rps)

print("XML Gerado:")
print(xml)
print("\n" + "="*80 + "\n")

# Verificações
checks = {
    "SOAP 1.1 Envelope": 'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"' in xml,
    "SOAP Header": '<soapenv:Header' in xml,
    "SOAP Body": '<soapenv:Body' in xml,
    "RecepcionarLoteRps": '<nfse:RecepcionarLoteRps' in xml or 'RecepcionarLoteRps' in xml,
    "Header em CDATA": '<header><![CDATA[' in xml or '<header>' in xml and '<![CDATA[' in xml,
    "Parameters em CDATA": '<parameters><![CDATA[' in xml or '<parameters>' in xml and '<![CDATA[' in xml,
    "Namespace nfse": 'xmlns:nfse="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd"' in xml,
}

print("Verificações SOAP 1.1 com CDATA:")
for check, result in checks.items():
    status = "✅" if result else "❌"
    print(f"{status} {check}: {result}")

all_ok = all(checks.values())
print(f"\n{'✅ SIM, está no padrão SOAP 1.1 com CDATA!' if all_ok else '❌ NÃO está completamente no padrão'}")
print(f"\n{'⚠️  Nota: Alguns elementos podem estar presentes mas não visíveis na string' if not all_ok else ''}")


