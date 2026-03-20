"""
Exemplo: ConsultarLoteRps - consulta lote de RPS por protocolo.
"""
from loguru import logger

from pynfse.src.integration.carnaubal.speedgov import SpeedGovNFSe


def main():
    URL_HOMOLOGACAO = "http://speedgov.com.br:80/wsmod/Nfes?wsdl"
    cnpj = "40114832000153"
    inscricao_municipal = "1"
    protocolo = "42f469ea-ea73-4095-851d-ccee572ee05e"  # Protocolo retornado no RecepcionarLoteRps

    provider = SpeedGovNFSe(URL=URL_HOMOLOGACAO)

    xml = provider.create_consult_lote_rps(
        protocolo=protocolo,
        cnpj=cnpj,
        inscricao_municipal=inscricao_municipal,
    )
    logger.info(f"Consulta lote RPS protocolo {protocolo}")
    print(xml)

    # Envio opcional ao Web Service
    # result = provider.send(xml)
    # print("Resposta:", result.response.text)


if __name__ == "__main__":
    main()
