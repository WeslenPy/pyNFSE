import pytest
from datetime import datetime, date
from pynfse.src.integration.carnaubal.abrasf.models.respostas import (
    EnviarLoteRpsResposta, ConsultarNfseRpsResposta, ConsultarNfseResposta,
    CancelarNfseResposta, CompNfse, Nfse, InfNfse
)
from pynfse.src.integration.carnaubal.abrasf.models.base import ListaMensagemRetorno, MensagemRetorno
from pynfse.src.integration.carnaubal.abrasf.nfse import CarnaubalNFSe

@pytest.fixture
def carnaubal_provider():
    return CarnaubalNFSe(URL="http://test.com")

def test_enviar_lote_rps_resposta_sucesso():
    """Testa resposta de sucesso no envio de lote."""
    data = {
        "NumeroLote": 123,
        "DataRecebimento": "2024-03-09T10:00:00",
        "Protocolo": "PROT123456"
    }
    resp = EnviarLoteRpsResposta(**data)
    assert resp.numero_lote == 123
    assert resp.protocolo == "PROT123456"
    assert resp.data_recebimento == datetime(2024, 3, 9, 10, 0)

def test_enviar_lote_rps_resposta_erro():
    """Testa resposta de erro no envio de lote."""
    data = {
        "ListaMensagemRetorno": {
            "MensagemRetorno": [
                {"Codigo": "E001", "Mensagem": "Erro de teste", "Correcao": "Corrija o teste"}
            ]
        }
    }
    resp = EnviarLoteRpsResposta(**data)
    assert resp.lista_mensagem_retorno is not None
    assert resp.lista_mensagem_retorno.mensagem_retorno[0].codigo == "E001"

def test_consultar_nfse_rps_resposta_completa():
    """Testa resposta completa de consulta por RPS."""
    # Simulação simplificada de um CompNfse
    data = {
        "CompNfse": {
            "Nfse": {
                "InfNfse": {
                    "Numero": 1001,
                    "CodigoVerificacao": "XYZ123",
                    "DataEmissao": "2024-03-09T10:00:00",
                    "NaturezaOperacao": 1,
                    "OptanteSimplesNacional": 1,
                    "IncentivadorCultural": 2,
                    "Competencia": "2024-03-01",
                    "Servico": {
                        "Valores": {"ValorServicos": 100.0, "IssRetido": 2},
                        "ItemListaServico": "1.01",
                        "Discriminacao": "Teste",
                        "CodigoMunicipio": 1234567
                    },
                    "PrestadorServico": {"Cnpj": "12345678000199"},
                    "TomadorServico": {"RazaoSocial": "Tomador"}
                }
            }
        }
    }
    resp = ConsultarNfseRpsResposta(**data)
    assert resp.comp_nfse.nfse.inf_nfse.numero == 1001
    assert resp.comp_nfse.nfse.inf_nfse.codigo_verificacao == "XYZ123"
    assert resp.comp_nfse.nfse.inf_nfse.competencia == date(2024, 3, 1)

def test_cancelar_nfse_resposta_sucesso():
    """Testa resposta de sucesso no cancelamento."""
    data = {
        "Cancelamento": {
            "Confirmacao": {
                "DataHora": "2024-03-09T11:00:00"
            }
        }
    }
    resp = CancelarNfseResposta(**data)
    assert resp.cancelamento.confirmacao.data_hora == datetime(2024, 3, 9, 11, 0)

def test_parse_response_soap_generic(carnaubal_provider):
    """Testa o método parse_response genérico com um envelope SOAP real."""
    soap_xml = """
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
      <soapenv:Body>
        <ns1:RecepcionarLoteRpsResponse xmlns:ns1="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd">
          <EnviarLoteRpsResposta xmlns="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd">
            <NumeroLote>123</NumeroLote>
            <DataRecebimento>2024-03-09T10:00:00</DataRecebimento>
            <Protocolo>PROT123456</Protocolo>
          </EnviarLoteRpsResposta>
        </ns1:RecepcionarLoteRpsResponse>
      </soapenv:Body>
    </soapenv:Envelope>
    """
    
    resp_dict = carnaubal_provider.parse_response(soap_xml)
    # Adiciona log para depuração se falhar
    print(f"DEBUG: {resp_dict}")
    assert "NumeroLote" in resp_dict
    assert resp_dict["NumeroLote"] == "123"
    assert resp_dict["Protocolo"] == "PROT123456"
    assert resp_dict["DataRecebimento"] == "2024-03-09T10:00:00"
