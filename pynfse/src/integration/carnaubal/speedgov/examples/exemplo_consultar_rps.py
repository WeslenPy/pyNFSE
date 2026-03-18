"""
Exemplo: ConsultarNfsePorRps - consulta NFSe por identificação do RPS.
"""
from loguru import logger

from pynfse.src.integration.carnaubal.speedgov import SpeedGovNFSe


def main():
    URL_HOMOLOGACAO = "http://speedgov.com.br:80/wsmod/Nfes?wsdl"
    cnpj = "40114832000153"
    inscricao_municipal = "10759"

    provider = SpeedGovNFSe(URL=URL_HOMOLOGACAO)

    # Consulta NFSe pelo RPS (número, série, tipo)
    xml = provider.create_consult_rps(
        numero=1,
        serie="A",
        tipo=1,
        cnpj=cnpj,
        inscricao_municipal=inscricao_municipal,
    )
    logger.info("Consulta NFSe por RPS (1/A/1)")
    print(xml)

    # Envio opcional ao Web Service
    # result = provider.send(xml)
    # print("Resposta:", result.response.text)


if __name__ == "__main__":
    main()
