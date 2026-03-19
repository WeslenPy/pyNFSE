"""
Exemplo: CancelarNfse - cancelamento de NFSe.
"""
from loguru import logger

from pynfse.src.integration.carnaubal.speedgov import SpeedGovNFSe


def main():
    URL_HOMOLOGACAO = "http://speedgov.com.br:80/wsmod/Nfes?wsdl"
    cnpj = "57255426000103"
    inscricao_municipal = "1"
    codigo_municipio = 1  
    numero_nfse = 123
    codigo_cancelamento = "E12"  # Ex: E12 = Erro na emissão

    provider = SpeedGovNFSe(URL=URL_HOMOLOGACAO)

    xml = provider.create_cancel_nfse(
        numero_nfse=numero_nfse,
        cnpj=cnpj,
        inscricao_municipal=inscricao_municipal,
        codigo_municipio=codigo_municipio,
        codigo_cancelamento=codigo_cancelamento,
    )
    logger.info(f"XML CancelarNfse (NFSe {numero_nfse})")
    print(xml)

    # Envio opcional ao Web Service
    # result = provider.send(xml)
    # resp = provider.parse_resposta_cancelar(result.response.text)


if __name__ == "__main__":
    main()
