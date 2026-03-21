import pytest
from datetime import datetime, date
from pynfse.integration.carnaubal.abrasf.models.respostas import (
    EnviarLoteRpsResposta, ConsultarNfseRpsResposta, ConsultarNfseResposta,
    CancelarNfseResposta, ConsultarLoteRpsResposta, ConsultarSituacaoLoteRpsResposta,
    CompNfse, Nfse, InfNfse
)
from pynfse.integration.carnaubal.abrasf.models.base import ListaMensagemRetorno, MensagemRetorno
from pynfse.integration.carnaubal.abrasf.nfse import CarnaubalNFSe

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
                    "PrestadorServico": {
                        "IdentificacaoPrestador": {"Cnpj": "12345678000199"},
                        "RazaoSocial": "Prestador",
                        "Endereco": {"Endereco": "Rua A", "Numero": "1"}
                    },
                    "TomadorServico": {"RazaoSocial": "Tomador"},
                    "OrgaoGerador": {"CodigoMunicipio": 1234567, "Uf": "CE"}
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
                "Pedido": {
                    "InfPedidoCancelamento": {
                        "IdentificacaoNfse": {
                            "Numero": 1,
                            "Cnpj": "12345678000199",
                            "CodigoMunicipio": 1234567
                        },
                        "CodigoCancelamento": "1"
                    }
                },
                "InfConfirmacaoCancelamento": {
                    "Sucesso": True,
                    "DataHora": "2024-03-09T11:00:00"
                }
            }
        }
    }
    resp = CancelarNfseResposta(**data)
    assert resp.cancelamento.confirmacao.inf_confirmacao_cancelamento.data_hora == datetime(2024, 3, 9, 11, 0)

def test_consultar_lote_rps_resposta():
    data = {
        "ListaNfse": {
            "CompNfse": []
        }
    }
    resp = ConsultarLoteRpsResposta(**data)
    assert resp.lista_nfse is not None

def test_consultar_situacao_lote_rps_resposta():
    data = {
        "NumeroLote": 10,
        "Situacao": 2
    }
    resp = ConsultarSituacaoLoteRpsResposta(**data)
    assert resp.numero_lote == 10
    assert resp.situacao == 2


def test_parse_consultar_situacao_lote_sucesso_nested():
    """Parse de ConsultarSituacaoLoteRps com tag aninhada vazia (formato real da API)."""
    soap_xml = """<?xml version='1.0' encoding='UTF-8'?><S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"><S:Body><ns2:ConsultarSituacaoLoteRpsResponse xmlns:ns2="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd"><return>&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;
&lt;ConsultarSituacaoLoteRpsResposta&gt;&lt;ConsultarSituacaoLoteRpsResposta/&gt;&lt;NumeroLote&gt;13&lt;/NumeroLote&gt;&lt;Situacao&gt;4&lt;/Situacao&gt;&lt;/ConsultarSituacaoLoteRpsResposta&gt;</return></ns2:ConsultarSituacaoLoteRpsResponse></S:Body></S:Envelope>"""
    from pynfse.common.response_parser import parse_resposta_xml
    resp = parse_resposta_xml(soap_xml, ConsultarSituacaoLoteRpsResposta)
    assert resp.numero_lote == 13
    assert resp.situacao == 4


def test_parse_consultar_situacao_lote_erro_escapado():
    """Parse de ConsultarSituacaoLoteRps com return escapado em caso de erro (Sucesso/DataHora)."""
    soap_xml = """<?xml version='1.0' encoding='UTF-8'?><S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"><S:Body><ns2:ConsultarSituacaoLoteRpsResponse xmlns:ns2="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd"><return>&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;
&lt;ConsultarSituacaoLoteRpsResposta&gt;&lt;Sucesso&gt;false&lt;/Sucesso&gt;&lt;DataHora&gt;2026-03-21T12:22:51&lt;/DataHora&gt;&lt;MensagemRetorno&gt;&lt;Codigo&gt;E10&lt;/Codigo&gt;&lt;Mensagem&gt;RPS já informado.&lt;/Mensagem&gt;&lt;Correcao&gt;Para essa Inscrição Municipal/CNPJ já existe um RPS informado com o mesmo número, série e tipo.&lt;/Correcao&gt;&lt;/MensagemRetorno&gt;&lt;/ConsultarSituacaoLoteRpsResposta&gt;</return></ns2:ConsultarSituacaoLoteRpsResponse></S:Body></S:Envelope>"""
    from pynfse.common.response_parser import parse_resposta_xml
    resp = parse_resposta_xml(soap_xml, ConsultarSituacaoLoteRpsResposta)
    assert resp.sucesso is False
    assert resp.data_hora == datetime(2026, 3, 21, 12, 22, 51)
    assert resp.numero_lote is None
    assert resp.situacao is None
    assert resp.lista_mensagem_retorno is not None
    assert len(resp.lista_mensagem_retorno.mensagem_retorno) == 1
    assert resp.lista_mensagem_retorno.mensagem_retorno[0].codigo == "E10"

def test_parse_consultar_lote_rps_sucesso_xml_real():
    """Parse de ConsultarLoteRps com XML real da API (ListaNfse com InfNfse completo)."""
    soap_xml = r"""<?xml version='1.0' encoding='UTF-8'?><S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"><S:Body><ns2:ConsultarLoteRpsResponse xmlns:ns2="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd"><return>&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;
&lt;ConsultarLoteRpsResposta&gt;&lt;ListaNfse&gt;&lt;CompNfse&gt;&lt;Nfse&gt;&lt;InfNfse id=&quot;id&quot;&gt;&lt;Numero&gt;634583&lt;/Numero&gt;&lt;CodigoVerificacao&gt;0121W1530&lt;/CodigoVerificacao&gt;&lt;DataEmissao&gt;2026-03-21&lt;/DataEmissao&gt;&lt;IdentificacaoRps&gt;&lt;Numero&gt;6&lt;/Numero&gt;&lt;Serie&gt;1&lt;/Serie&gt;&lt;Tipo&gt;1&lt;/Tipo&gt;&lt;/IdentificacaoRps&gt;&lt;DataEmissaoRps&gt;2026-03-21&lt;/DataEmissaoRps&gt;&lt;NaturezaOperacao&gt;1&lt;/NaturezaOperacao&gt;&lt;OptanteSimplesNacional&gt;1&lt;/OptanteSimplesNacional&gt;&lt;Competencia&gt;2026-03-01&lt;/Competencia&gt;&lt;Servico&gt;&lt;Valores&gt;&lt;ValorServicos&gt;1.0&lt;/ValorServicos&gt;&lt;IssRetido&gt;2&lt;/IssRetido&gt;&lt;ValorIss&gt;0.03&lt;/ValorIss&gt;&lt;BaseCalculo&gt;1.0&lt;/BaseCalculo&gt;&lt;Aliquota&gt;3.0&lt;/Aliquota&gt;&lt;ValorLiquidoNfse&gt;0.97&lt;/ValorLiquidoNfse&gt;&lt;/Valores&gt;&lt;ItemListaServico&gt;106&lt;/ItemListaServico&gt;&lt;Discriminacao&gt;Recarga painel&lt;/Discriminacao&gt;&lt;CodigoMunicipio&gt;2303402&lt;/CodigoMunicipio&gt;&lt;/Servico&gt;&lt;PrestadorServico&gt;&lt;IdentificacaoPrestador&gt;&lt;Cnpj&gt;40114832000153&lt;/Cnpj&gt;&lt;InscricaoMunicipal&gt;10759&lt;/InscricaoMunicipal&gt;&lt;/IdentificacaoPrestador&gt;&lt;RazaoSocial&gt;F K HIGINO BRITO&lt;/RazaoSocial&gt;&lt;Endereco&gt;&lt;Endereco&gt;RUA MANOEL ESTORGIO&lt;/Endereco&gt;&lt;Numero&gt;279&lt;/Numero&gt;&lt;Bairro&gt;VARZEA&lt;/Bairro&gt;&lt;CodigoMunicipio&gt;2303402&lt;/CodigoMunicipio&gt;&lt;Uf&gt;CE&lt;/Uf&gt;&lt;Cep&gt;62375000&lt;/Cep&gt;&lt;/Endereco&gt;&lt;/PrestadorServico&gt;&lt;TomadorServico&gt;&lt;RazaoSocial&gt;CLIENTE EXEMPLO LTDA&lt;/RazaoSocial&gt;&lt;Endereco&gt;&lt;Endereco&gt;Rua Exemplo&lt;/Endereco&gt;&lt;Numero&gt;100&lt;/Numero&gt;&lt;Bairro&gt;Centro&lt;/Bairro&gt;&lt;CodigoMunicipio&gt;2303402&lt;/CodigoMunicipio&gt;&lt;Uf&gt;CE&lt;/Uf&gt;&lt;Cep&gt;63100000&lt;/Cep&gt;&lt;/Endereco&gt;&lt;/TomadorServico&gt;&lt;OrgaoGerador&gt;&lt;CodigoMunicipio&gt;2303402&lt;/CodigoMunicipio&gt;&lt;Uf&gt;CE&lt;/Uf&gt;&lt;/OrgaoGerador&gt;&lt;ConstrucaoCivil&gt;&lt;CodigoObra&gt;&lt;/CodigoObra&gt;&lt;Art&gt;&lt;/Art&gt;&lt;/ConstrucaoCivil&gt;&lt;/InfNfse&gt;&lt;/Nfse&gt;&lt;/CompNfse&gt;&lt;/ListaNfse&gt;&lt;/ConsultarLoteRpsResposta&gt;</return></ns2:ConsultarLoteRpsResponse></S:Body></S:Envelope>"""
    from pynfse.common.response_parser import parse_resposta_xml
    resp = parse_resposta_xml(soap_xml, ConsultarLoteRpsResposta)
    assert resp.lista_nfse is not None
    assert len(resp.lista_nfse.comp_nfse) == 1
    inf = resp.lista_nfse.comp_nfse[0].nfse.inf_nfse
    assert inf.numero == 634583
    assert inf.codigo_verificacao == "0121W1530"
    assert inf.servico.discriminacao == "Recarga painel"
    assert inf.prestador_servico.razao_social == "F K HIGINO BRITO"
    assert inf.tomador_servico.razao_social == "CLIENTE EXEMPLO LTDA"


def test_parse_consultar_lote_rps_sucesso_escapado():
    """Parse de ConsultarLoteRps com return escapado em caso de sucesso."""
    soap_xml = """<?xml version='1.0' encoding='UTF-8'?><S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"><S:Body><ns2:ConsultarLoteRpsResponse xmlns:ns2="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd"><return>&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;
&lt;ConsultarLoteRpsResposta&gt;&lt;Sucesso&gt;true&lt;/Sucesso&gt;&lt;DataHora&gt;2026-03-21T12:30:00&lt;/DataHora&gt;&lt;ListaNfse&gt;&lt;CompNfse&gt;&lt;Nfse&gt;&lt;InfNfse&gt;&lt;Numero&gt;1&lt;/Numero&gt;&lt;CodigoVerificacao&gt;ABC123&lt;/CodigoVerificacao&gt;&lt;DataEmissao&gt;2026-03-21T12:30:00&lt;/DataEmissao&gt;&lt;NaturezaOperacao&gt;1&lt;/NaturezaOperacao&gt;&lt;OptanteSimplesNacional&gt;1&lt;/OptanteSimplesNacional&gt;&lt;IncentivadorCultural&gt;2&lt;/IncentivadorCultural&gt;&lt;Competencia&gt;2026-03-01&lt;/Competencia&gt;&lt;Servico&gt;&lt;Valores&gt;&lt;ValorServicos&gt;100.0&lt;/ValorServicos&gt;&lt;IssRetido&gt;2&lt;/IssRetido&gt;&lt;/Valores&gt;&lt;ItemListaServico&gt;1.01&lt;/ItemListaServico&gt;&lt;Discriminacao&gt;Teste&lt;/Discriminacao&gt;&lt;CodigoMunicipio&gt;2304400&lt;/CodigoMunicipio&gt;&lt;/Servico&gt;&lt;PrestadorServico&gt;&lt;IdentificacaoPrestador&gt;&lt;Cnpj&gt;12345678000199&lt;/Cnpj&gt;&lt;/IdentificacaoPrestador&gt;&lt;RazaoSocial&gt;Prestador&lt;/RazaoSocial&gt;&lt;Endereco&gt;&lt;Endereco&gt;Rua A&lt;/Endereco&gt;&lt;Numero&gt;1&lt;/Numero&gt;&lt;/Endereco&gt;&lt;/PrestadorServico&gt;&lt;TomadorServico&gt;&lt;RazaoSocial&gt;Tomador&lt;/RazaoSocial&gt;&lt;/TomadorServico&gt;&lt;OrgaoGerador&gt;&lt;CodigoMunicipio&gt;2304400&lt;/CodigoMunicipio&gt;&lt;Uf&gt;CE&lt;/Uf&gt;&lt;/OrgaoGerador&gt;&lt;/InfNfse&gt;&lt;/Nfse&gt;&lt;/CompNfse&gt;&lt;/ListaNfse&gt;&lt;/ConsultarLoteRpsResposta&gt;</return></ns2:ConsultarLoteRpsResponse></S:Body></S:Envelope>"""
    from pynfse.common.response_parser import parse_resposta_xml
    resp = parse_resposta_xml(soap_xml, ConsultarLoteRpsResposta)
    assert resp.sucesso is True
    assert resp.data_hora == datetime(2026, 3, 21, 12, 30, 0)
    assert resp.lista_nfse is not None
    assert len(resp.lista_nfse.comp_nfse) == 1
    assert resp.lista_nfse.comp_nfse[0].nfse.inf_nfse.numero == 1
    assert resp.lista_nfse.comp_nfse[0].nfse.inf_nfse.codigo_verificacao == "ABC123"

def test_parse_consultar_lote_rps_erro_escapado():
    """Parse de ConsultarLoteRps com return escapado (formato real da API)."""
    soap_xml = """<?xml version='1.0' encoding='UTF-8'?><S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"><S:Body><ns2:ConsultarLoteRpsResponse xmlns:ns2="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd"><return>&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;
&lt;ConsultarLoteRpsResposta&gt;&lt;Sucesso&gt;false&lt;/Sucesso&gt;&lt;DataHora&gt;2026-03-21T12:22:51&lt;/DataHora&gt;&lt;MensagemRetorno&gt;&lt;Codigo&gt;E390&lt;/Codigo&gt;&lt;Mensagem&gt;Se Simples Nacional (opSimpNac=2 ou 3) com apuração pelo Simples (regApTribSN=1), então regEspTrib DEVE ser 0 (Nenhum)&lt;/Mensagem&gt;&lt;Correcao&gt;Se Simples Nacional (opSimpNac=2 ou 3) com apuração pelo Simples (regApTribSN=1), então regEspTrib DEVE ser 0 (Nenhum)&lt;/Correcao&gt;&lt;/MensagemRetorno&gt;&lt;MensagemRetorno&gt;&lt;Codigo&gt;E391&lt;/Codigo&gt;&lt;Mensagem&gt;Campo CTribNac - Código de Tributação Nacional inválido ou não informado&lt;/Mensagem&gt;&lt;Correcao&gt;Campo CTribNac - Código de Tributação Nacional inválido ou não informado&lt;/Correcao&gt;&lt;/MensagemRetorno&gt;&lt;/ConsultarLoteRpsResposta&gt;</return></ns2:ConsultarLoteRpsResponse></S:Body></S:Envelope>"""
    from pynfse.common.response_parser import parse_resposta_xml
    resp = parse_resposta_xml(soap_xml, ConsultarLoteRpsResposta)
    assert resp.sucesso is False
    assert resp.data_hora == datetime(2026, 3, 21, 12, 22, 51)
    assert resp.lista_mensagem_retorno is not None
    assert len(resp.lista_mensagem_retorno.mensagem_retorno) == 2
    assert resp.lista_mensagem_retorno.mensagem_retorno[0].codigo == "E390"
    assert resp.lista_mensagem_retorno.mensagem_retorno[1].codigo == "E391"
    assert "opSimpNac" in resp.lista_mensagem_retorno.mensagem_retorno[0].mensagem

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
