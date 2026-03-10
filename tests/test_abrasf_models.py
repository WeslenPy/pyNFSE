import pytest
from datetime import datetime
from pynfse.src.integration.carnaubal.abrasf.models.base import CpfCnpj, Endereco
from pynfse.src.integration.carnaubal.abrasf.models.rps import Rps, InfRps, IdentificacaoRps, IdentificacaoPrestador, DadosTomador, IdentificacaoTomador, DadosServico, Valores
from pynfse.src.integration.carnaubal.abrasf.models.lote import LoteRps, ListaRps, EnviarLoteRpsEnvio

def test_xml_node_to_xml():
    """Testa a conversão de um nó simples para XML."""
    identificacao = IdentificacaoRps(numero=123, serie="A", tipo=1)
    xml = identificacao.to_xml(pretty_print=False)
    assert "<IdentificacaoRps>" in xml
    assert "<Numero>123</Numero>" in xml
    assert "<Serie>A</Serie>" in xml
    assert "<Tipo>1</Tipo>" in xml

def test_nested_xml_node():
    """Testa a conversão de nós aninhados."""
    cpf_cnpj = CpfCnpj(cnpj="12345678000199")
    tomador = IdentificacaoTomador(cpf_cnpj=cpf_cnpj, inscricao_municipal="IM123")
    xml = tomador.to_xml(pretty_print=False)
    assert "<IdentificacaoTomador>" in xml
    assert "<CpfCnpj>" in xml
    assert "<Cnpj>12345678000199</Cnpj>" in xml
    assert "<InscricaoMunicipal>IM123</InscricaoMunicipal>" in xml

def test_full_lote_rps_xml():
    """Testa a geração de um XML completo de LoteRps."""
    # Setup
    identificacao = IdentificacaoRps(numero=1, serie="A", tipo=1)
    prestador = IdentificacaoPrestador(cnpj="12345678000199", inscricao_municipal="123")
    
    valores = Valores(valor_servicos=100.0, iss_retido=2)
    servico = DadosServico(
        valores=valores,
        item_lista_servico="1.01",
        discriminacao="Teste",
        codigo_municipio=1234567
    )
    
    tomador = DadosTomador(razao_social="Cliente Teste")
    
    inf_rps = InfRps(
        id="rps1",
        identificacao_rps=identificacao,
        data_emissao=datetime(2024, 3, 9, 12, 0, 0),
        natureza_operacao=1,
        optante_simples_national=1,
        incentivador_cultural=2,
        status=1,
        servico=servico,
        prestador=prestador,
        tomador=tomador
    )
    
    rps = Rps(inf_rps=inf_rps)
    lote = LoteRps(
        id="lote1",
        numero_lote=1,
        cnpj="12345678000199",
        inscricao_municipal="123",
        quantidade_rps=1,
        lista_rps=ListaRps(rps=[rps])
    )
    
    xml = lote.to_xml(pretty_print=True)
    
    # Assertions
    assert 'Id="lote1"' in xml
    assert "<NumeroLote>1</NumeroLote>" in xml
    assert "<ListaRps>" in xml
    assert "<Rps>" in xml
    assert "<InfRps" in xml
    assert 'Id="rps1"' in xml
    assert "<DataEmissao>2024-03-09T12:00:00</DataEmissao>" in xml
