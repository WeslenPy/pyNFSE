"""
Exemplo: ConsultarSituacaoLoteRps - consulta situação do lote (processado, em processamento, etc.).
"""
from loguru import logger

from pynfse.integration.carnaubal.speedgov import SpeedGovNFSe


def main():
    URL_HOMOLOGACAO = "http://speedgov.com.br:80/wsmod/Nfes?wsdl"
    cnpj = "57255426000103"
    inscricao_municipal = "1"
    protocolo = "e810429f-e89d-4c4d-a9aa-d55847c16cd9"  # Protocolo retornado no RecepcionarLoteRps

    provider = SpeedGovNFSe(URL=URL_HOMOLOGACAO)

    xml = provider.create_consult_situacao_lote_rps(
        protocolo=protocolo,
        cnpj=cnpj,
        inscricao_municipal=inscricao_municipal,
    )
    logger.info(f"Consulta situação lote RPS protocolo {protocolo}")
    print(xml)

    # Envio opcional ao Web Service
    result = provider.send(xml)
    print("Resposta:", result.response.text)


if __name__ == "__main__":
    main()
