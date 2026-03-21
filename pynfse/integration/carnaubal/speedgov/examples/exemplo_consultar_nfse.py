"""
Exemplo: ConsultarNfse - consulta NFSe(s) do prestador.
"""
from loguru import logger

from pynfse.integration.carnaubal.speedgov import SpeedGovNFSe


def main():
    URL_HOMOLOGACAO = "http://speedgov.com.br:80/wsmod/Nfes?wsdl"
    cnpj = "57255426000103"
    inscricao_municipal = "1"

    provider = SpeedGovNFSe(URL=URL_HOMOLOGACAO)

    # Consulta todas as NFSe do prestador
    xml_todas = provider.create_consult_nfse(
        cnpj=cnpj,
        inscricao_municipal=inscricao_municipal,
    )
    logger.info("Consulta todas NFSe")
    print(xml_todas)
    print("-" * 60)

    # Consulta NFSe específica por número
    xml_numero = provider.create_consult_nfse(
        cnpj=cnpj,
        inscricao_municipal=inscricao_municipal,
        numero_nfse=123,
    )
    logger.info("Consulta NFSe número 123")
    print(xml_numero)

    # Envio opcional ao Web Service
    # result = provider.send(xml_todas)
    # print("Resposta:", result.response.text)


if __name__ == "__main__":
    main()
