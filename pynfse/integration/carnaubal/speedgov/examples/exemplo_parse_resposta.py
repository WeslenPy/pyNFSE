"""
Exemplo: Parse de resposta XML -> modelo Pydantic.
Demonstra o fluxo inverso: xml -> pydantic.
"""
from loguru import logger

from pynfse.integration.carnaubal.speedgov import SpeedGovNFSe
from pynfse.integration.carnaubal.speedgov.models.respostas import (
    EnviarLoteRpsResposta,
    ConsultarSituacaoLoteRpsResposta,
    RespostasSpeedGov,
)

# XML de exemplo - resposta RecepcionarLoteRps (sucesso)
XML_ENVIAR_LOTE_SUCESSO = """<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <RecepcionarLoteRpsResponse>
      <RecepcionarLoteRpsResult>
        <EnviarLoteRpsResposta>
          <NumeroLote>1</NumeroLote>
          <DataRecebimento>2024-01-15T10:30:00</DataRecebimento>
          <Protocolo>20240000001</Protocolo>
        </EnviarLoteRpsResposta>
      </RecepcionarLoteRpsResult>
    </RecepcionarLoteRpsResponse>
  </soap:Body>
</soap:Envelope>"""

# XML de exemplo - resposta ConsultarSituacaoLoteRps (sucesso)
XML_SITUACAO_SUCESSO = """<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ConsultarSituacaoLoteRpsResponse>
      <ConsultarSituacaoLoteRpsResult>
        <ConsultarSituacaoLoteRpsResposta>
          <NumeroLote>1</NumeroLote>
          <Situacao>4</Situacao>
        </ConsultarSituacaoLoteRpsResposta>
      </ConsultarSituacaoLoteRpsResult>
    </ConsultarSituacaoLoteRpsResponse>
  </soap:Body>
</soap:Envelope>"""

# XML de exemplo - resposta com erro (ListaMensagemRetorno)
XML_ENVIAR_LOTE_ERRO = """<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <RecepcionarLoteRpsResponse>
      <RecepcionarLoteRpsResult>
        <EnviarLoteRpsResposta>
          <ListaMensagemRetorno>
            <MensagemRetorno>
              <Codigo>E001</Codigo>
              <Mensagem>Erro de validação</Mensagem>
            </MensagemRetorno>
          </ListaMensagemRetorno>
        </EnviarLoteRpsResposta>
      </RecepcionarLoteRpsResult>
    </RecepcionarLoteRpsResponse>
  </soap:Body>
</soap:Envelope>"""


def main():
    provider = SpeedGovNFSe()

    # Via método do provider
    logger.info("Parse EnviarLoteRpsResposta (sucesso)")
    resp1 = provider.parse_resposta_enviar_lote(XML_ENVIAR_LOTE_SUCESSO)
    print(f"  Protocolo: {resp1.protocolo}")
    print(f"  NumeroLote: {resp1.numero_lote}")
    print("-" * 60)

    # Via RespostasSpeedGov
    logger.info("Parse ConsultarSituacaoLoteRpsResposta")
    resp2 = RespostasSpeedGov.from_xml_consultar_situacao_lote(XML_SITUACAO_SUCESSO)
    print(f"  NumeroLote: {resp2.numero_lote}")
    print(f"  Situacao: {resp2.situacao} (1=NãoRecebido, 2=NãoProcessado, 3=Processado, 4=Erro)")
    print("-" * 60)

    # Resposta com erro
    logger.info("Parse EnviarLoteRpsResposta (erro)")
    resp3 = provider.parse_resposta(XML_ENVIAR_LOTE_ERRO, EnviarLoteRpsResposta)
    if resp3.lista_mensagem_retorno:
        for msg in resp3.lista_mensagem_retorno.mensagem_retorno:
            print(f"  [{msg.codigo}] {msg.mensagem}")


if __name__ == "__main__":
    main()
