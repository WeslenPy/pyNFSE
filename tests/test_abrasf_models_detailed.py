import pytest
from datetime import datetime, date
from pydantic import ValidationError
from pynfse.src.integration.carnaubal.abrasf.models.rps import (
    Rps, InfRps, IdentificacaoRps, IdentificacaoPrestador, 
    DadosTomador, IdentificacaoTomador, DadosServico, Valores
)
from pynfse.src.integration.carnaubal.abrasf.models.lote import LoteRps, ListaRps, EnviarLoteRpsEnvio
from pynfse.src.integration.carnaubal.abrasf.models.cancelamento import (
    CancelarNfseEnvio, PedidoCancelamento, InfPedidoCancelamento, IdentificacaoNfse
)
from pynfse.src.integration.carnaubal.abrasf.models.consulta import ConsultarNfseEnvio, PeriodoEmissao
from pynfse.src.integration.carnaubal.abrasf.models.consultar_lote import ConsultarLoteRpsEnvio, ConsultarSituacaoLoteRpsEnvio
from pynfse.src.integration.carnaubal.abrasf.models.consultar_rps import ConsultarNfseRpsEnvio
from pynfse.src.integration.carnaubal.abrasf.models.base import CpfCnpj

def test_model_rps_validation():
    """Testa validações básicas do modelo RPS."""
    # Dados válidos
    inf_rps = InfRps(
        id="rps1",
        identificacao_rps=IdentificacaoRps(numero=1, serie="A", tipo=1),
        data_emissao=datetime.now(),
        natureza_operacao=1,
        optante_simples_national=1,
        incentivador_cultural=2,
        status=1,
        servico=DadosServico(
            valores=Valores(valor_servicos=100.0, iss_retido=2),
            item_lista_servico="1.01",
            discriminacao="Teste",
            codigo_municipio=1234567
        ),
        prestador=IdentificacaoPrestador(cnpj="12345678000199"),
        tomador=DadosTomador(razao_social="Tomador")
    )
    rps = Rps(inf_rps=inf_rps)
    assert rps.inf_rps.identificacao_rps.numero == 1

    # CNPJ inválido (menos de 14 dígitos)
    with pytest.raises(ValidationError):
        IdentificacaoPrestador(cnpj="123")

def test_model_lote_rps_xml():
    """Testa a geração de XML para LoteRps."""
    rps = Rps(inf_rps=InfRps(
        identificacao_rps=IdentificacaoRps(numero=1, serie="A", tipo=1),
        data_emissao=datetime(2024, 3, 9, 10, 0),
        natureza_operacao=1,
        optante_simples_national=1,
        incentivador_cultural=2,
        status=1,
        servico=DadosServico(
            valores=Valores(valor_servicos=100.0, iss_retido=2),
            item_lista_servico="1.01",
            discriminacao="Teste",
            codigo_municipio=1234567
        ),
        prestador=IdentificacaoPrestador(cnpj="12345678000199"),
        tomador=DadosTomador(razao_social="Tomador")
    ))
    
    lote = LoteRps(
        id="L1",
        numero_lote=123,
        cnpj="12345678000199",
        inscricao_municipal="12345",
        quantidade_rps=1,
        lista_rps=ListaRps(rps=[rps])
    )
    
    xml = lote.to_xml()
    assert "<NumeroLote>123</NumeroLote>" in xml
    assert "<Cnpj>12345678000199</Cnpj>" in xml
    assert "<QuantidadeRps>1</QuantidadeRps>" in xml

def test_model_cancelamento_xml():
    """Testa a geração de XML para Cancelamento."""
    pedido = PedidoCancelamento(
        inf_pedido_cancelamento=InfPedidoCancelamento(
            id="C1",
            identificacao_nfse=IdentificacaoNfse(
                numero=20241,
                cnpj="12345678000199",
                inscricao_municipal="12345",
                codigo_municipio=1234567
            ),
            codigo_cancelamento="1"
        )
    )
    envio = CancelarNfseEnvio(pedido=pedido)
    xml = envio.to_xml()
    
    assert "<CancelarNfseEnvio" in xml
    assert "<Numero>20241</Numero>" in xml
    assert "<CodigoCancelamento>1</CodigoCancelamento>" in xml

def test_model_consulta_xml():
    """Testa a geração de XML para Consulta de NFSe."""
    consulta = ConsultarNfseEnvio(
        prestador=IdentificacaoPrestador(cnpj="12345678000199", inscricao_municipal="12345"),
        numero_nfse=10,
        periodo_emissao=PeriodoEmissao(
            data_inicial=date(2024, 1, 1),
            data_final=date(2024, 1, 31)
        )
    )
    xml = consulta.to_xml()
    
    assert "<ConsultarNfseEnvio" in xml
    assert "<NumeroNfse>10</NumeroNfse>" in xml
    assert "<DataInicial>2024-01-01</DataInicial>" in xml

def test_model_consultar_rps_xml():
    """Testa a geração de XML para Consulta por RPS."""
    consulta = ConsultarNfseRpsEnvio(
        identificacao_rps=IdentificacaoRps(numero=123, serie="A", tipo=1),
        prestador=IdentificacaoPrestador(cnpj="12345678000199", inscricao_municipal="12345")
    )
    xml = consulta.to_xml()
    
    assert "<ConsultarNfseRpsEnvio" in xml
    assert "<Numero>123</Numero>" in xml
    assert "<Cnpj>12345678000199</Cnpj>" in xml

def test_model_consultar_lote_xml():
    consulta = ConsultarLoteRpsEnvio(
        prestador=IdentificacaoPrestador(cnpj="12345678000199", inscricao_municipal="12345"),
        protocolo="PROTOCOLO123"
    )
    xml = consulta.to_xml()

    assert "<ConsultarLoteRpsEnvio" in xml
    assert "<Protocolo>PROTOCOLO123</Protocolo>" in xml

def test_model_consultar_situacao_lote_xml():
    consulta = ConsultarSituacaoLoteRpsEnvio(
        prestador=IdentificacaoPrestador(cnpj="12345678000199", inscricao_municipal="12345"),
        protocolo="PROTOCOLO123"
    )
    xml = consulta.to_xml()

    assert "<ConsultarSituacaoLoteRpsEnvio" in xml
    assert "<Protocolo>PROTOCOLO123</Protocolo>" in xml

def test_cpf_cnpj_validation():
    """Testa o modelo auxiliar CpfCnpj."""
    # CPF válido
    c = CpfCnpj(cpf="12345678901")
    assert c.cpf == "12345678901"
    assert "<Cpf>12345678901</Cpf>" in c.to_xml()
    
    # CNPJ válido
    c = CpfCnpj(cnpj="12345678000199")
    assert c.cnpj == "12345678000199"
    assert "<Cnpj>12345678000199</Cnpj>" in c.to_xml()
    
    # Ambos preenchidos devem falhar pela regra de choice do XSD
    with pytest.raises(ValidationError):
        CpfCnpj(cpf="12345678901", cnpj="12345678000199")
