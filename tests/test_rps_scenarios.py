import pytest
from datetime import datetime
from lxml import etree
from pynfse.integration.carnaubal.abrasf.models.base import CpfCnpj, Endereco, Contato
from pynfse.integration.carnaubal.abrasf.models.rps import (
    Rps, InfRps, IdentificacaoRps, IdentificacaoPrestador, 
    DadosTomador, IdentificacaoTomador, DadosServico, Valores,
    IdentificacaoIntermediarioServico, DadosConstrucaoCivil,
    DadosDPS, DadosObra, EnderecoObra, ComercioExterior,
    ExigibilidadeSuspensa, BeneficioMunicipal, ReembolsoRepasse,
    Destinatario, ControleIBSCBS, IBSCBS
)
from pynfse.integration.carnaubal.abrasf.models.lote import LoteRps, ListaRps


def _parse_xml(xml: str) -> etree._Element:
    return etree.fromstring(xml.encode("utf-8"))

def test_rps_simples():
    """Cenário 1: RPS Básico (apenas campos obrigatórios)"""
    identificacao = IdentificacaoRps(numero=10, serie="A", tipo=1)
    prestador = IdentificacaoPrestador(cnpj="12345678000199")
    
    valores = Valores(valor_servicos=500.0, iss_retido=2)
    servico = DadosServico(
        valores=valores,
        item_lista_servico="1.01",
        discriminacao="Serviço Simples",
        codigo_municipio=1234567
    )
    
    tomador = DadosTomador(razao_social="Tomador Teste")
    
    inf_rps = InfRps(
        id="rps10",
        identificacao_rps=identificacao,
        data_emissao=datetime(2024, 3, 9, 10, 0),
        natureza_operacao=1,
        optante_simples_national=1,
        incentivador_cultural=2,
        status=1,
        servico=servico,
        prestador=prestador,
        tomador=tomador
    )
    
    xml = Rps(inf_rps=inf_rps).to_xml(pretty_print=False)
    
    assert 'Id="rps10"' in xml
    assert "<Numero>10</Numero>" in xml
    assert "<ValorServicos>500.0</ValorServicos>" in xml
    assert "<RazaoSocial>Tomador Teste</RazaoSocial>" in xml

def test_rps_com_substituicao_e_intermediario():
    """Cenário 2: RPS com Substituição e Intermediário do Serviço"""
    identificacao = IdentificacaoRps(numero=11, serie="A", tipo=1)
    substituido = IdentificacaoRps(numero=9, serie="A", tipo=1)
    
    intermediario = IdentificacaoIntermediarioServico(
        razao_social="Intermediario S.A.",
        cpf_cnpj=CpfCnpj(cnpj="98765432000188"),
        uf="SP",
        email="contato@intermediario.com"
    )
    
    inf_rps = InfRps(
        identificacao_rps=identificacao,
        data_emissao=datetime.now(),
        natureza_operacao=1,
        optante_simples_national=1,
        incentivador_cultural=2,
        status=1,
        rps_substituido=substituido,
        servico=DadosServico(
            valores=Valores(valor_servicos=1000.0, iss_retido=1),
            item_lista_servico="1.01",
            discriminacao="Serviço com Intermediário",
            codigo_municipio=1234567
        ),
        prestador=IdentificacaoPrestador(cnpj="12345678000199"),
        tomador=DadosTomador(razao_social="Tomador"),
        intermediario_servico=intermediario
    )
    
    xml = Rps(inf_rps=inf_rps).to_xml(pretty_print=False)
    
    assert "<RpsSubstituido>" in xml
    assert "<Numero>9</Numero>" in xml
    assert "<IntermediarioServico>" in xml
    assert "<RazaoSocial>Intermediario S.A.</RazaoSocial>" in xml
    assert "<UF>SP</UF>" in xml

def test_rps_nfse_nacional_dps_e_obras():
    """Cenário 3: RPS com Blocos NFS-e Nacional (DPS e Obras)"""
    dps = DadosDPS(
        tp_emit="1",
        tp_amb=2,
        dh_emi=datetime(2024, 3, 9, 15, 30),
        ver_aplic="pyNFSE-v1",
        ctrib_nac="010101"
    )
    
    obra = DadosObra(
        codigo_obra="OBRA-2024-001",
        insc_imob_fisc="123456",
        endereco_obra=EnderecoObra(cep="12345678", logradouro="Rua da Obra", numero="100")
    )
    
    inf_rps = InfRps(
        identificacao_rps=IdentificacaoRps(numero=12, serie="A", tipo=1),
        data_emissao=datetime.now(),
        natureza_operacao=1,
        optante_simples_national=1,
        incentivador_cultural=2,
        status=1,
        servico=DadosServico(
            valores=Valores(valor_servicos=5000.0, iss_retido=2),
            item_lista_servico="7.02",
            discriminacao="Execução de Obra",
            codigo_municipio=1234567
        ),
        prestador=IdentificacaoPrestador(cnpj="12345678000199"),
        tomador=DadosTomador(razao_social="Construtora"),
        dados_dps=dps,
        dados_obra=obra
    )
    
    xml = Rps(inf_rps=inf_rps).to_xml(pretty_print=False)
    
    assert "<DadosDPS>" in xml
    assert "<VerAplic>pyNFSE-v1</VerAplic>" in xml
    assert "<DadosObra>" in xml
    assert "<CodigoObra>OBRA-2024-001</CodigoObra>" in xml
    assert "<EnderecoObra>" in xml

def test_rps_comercio_exterior_e_ibscbs():
    """Cenário 4: RPS Exportação (Comércio Exterior) e Tributos IBS/CBS"""
    comex = ComercioExterior(
        md_prestacao=1,
        tp_moeda=220, # USD
        v_serv_moeda=1000.0,
        ndi="DI-12345",
        c_pais_result="USA"
    )
    
    tributos = IBSCBS(
        ibscbs_base_calculo=5000.0,
        ibsu_f_aliquota=0.02,
        cbs_aliquota=0.03,
        ibs_valor_total=250.0
    )
    
    inf_rps = InfRps(
        identificacao_rps=IdentificacaoRps(numero=13, serie="A", tipo=1),
        data_emissao=datetime.now(),
        natureza_operacao=1,
        optante_simples_national=1,
        incentivador_cultural=2,
        status=1,
        servico=DadosServico(
            valores=Valores(valor_servicos=5000.0, iss_retido=2),
            item_lista_servico="1.01",
            discriminacao="Exportação de Software",
            codigo_municipio=1234567
        ),
        prestador=IdentificacaoPrestador(cnpj="12345678000199"),
        tomador=DadosTomador(razao_social="Global Corp"),
        comercio_exterior=comex,
        ibscbs=tributos
    )
    
    xml = Rps(inf_rps=inf_rps).to_xml(pretty_print=False)
    
    assert "<ComercioExterior>" in xml
    assert "<TpMoeda>220</TpMoeda>" in xml
    assert "<CPaisResult>USA</CPaisResult>" in xml
    assert "<IBSCBS>" in xml
    assert "<IBSUFAliquota>0.02</IBSUFAliquota>" in xml
    assert "<IBSValorTotal>250.00</IBSValorTotal>" in xml

from pynfse.common.signature import (
    Signature, SignedInfo, CanonicalizationMethod, SignatureMethod, 
    Reference, Transforms, Transform, DigestMethod, KeyInfo, X509Data
)

def test_rps_com_assinatura():
    """Cenário 6: RPS com estrutura de Assinatura Digital"""
    # Setup de assinatura fake seguindo o padrão XMLDSIG
    signature = Signature(
        signed_info=SignedInfo(
            canonicalization_method=CanonicalizationMethod(algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"),
            signature_method=SignatureMethod(algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"),
            reference=[Reference(
                uri="#rps1",
                transforms=Transforms(transform=[Transform(algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature")]),
                digest_method=DigestMethod(algorithm="http://www.w3.org/2000/09/xmldsig#sha1"),
                digest_value="fake-digest-value"
            )]
        ),
        signature_value="fake-signature-value",
        key_info=KeyInfo(x509_data=X509Data(x509_certificate="fake-cert"))
    )

    inf_rps = InfRps(
        id="rps1",
        identificacao_rps=IdentificacaoRps(numero=1, serie="A", tipo=1),
        data_emissao=datetime.now(), natureza_operacao=1, optante_simples_national=1, incentivador_cultural=2, status=1,
        servico=DadosServico(valores=Valores(valor_servicos=100.0, iss_retido=2), item_lista_servico="1.01", discriminacao="RPS Assinado", codigo_municipio=1234567),
        prestador=IdentificacaoPrestador(cnpj="12345678000199"), tomador=DadosTomador(razao_social="T1")
    )
    
    rps = Rps(inf_rps=inf_rps, signature=signature)
    xml = rps.to_xml(pretty_print=True)
    
    assert '<Signature xmlns="http://www.w3.org/2000/09/xmldsig#">' in xml
    assert "<SignedInfo>" in xml
    assert 'Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"' in xml
    assert 'Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"' in xml
    assert "<SignatureValue>fake-signature-value</SignatureValue>" in xml
    assert "<X509Certificate>fake-cert</X509Certificate>" in xml
    assert 'URI="#rps1"' in xml

def test_lote_com_assinatura():
    """Cenário 7: Lote com estrutura de Assinatura Digital"""
    signature = Signature(
        signed_info=SignedInfo(
            canonicalization_method=CanonicalizationMethod(algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"),
            signature_method=SignatureMethod(algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"),
            reference=[Reference(
                uri="#lote1",
                transforms=Transforms(transform=[Transform(algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature")]),
                digest_method=DigestMethod(algorithm="http://www.w3.org/2000/09/xmldsig#sha1"),
                digest_value="fake-digest-lote"
            )]
        ),
        signature_value="fake-signature-lote"
    )

    lote = LoteRps(
        id="lote1",
        numero_lote=1,
        cnpj="12345678000199",
        inscricao_municipal="123",
        quantidade_rps=0,
        lista_rps=ListaRps(rps=[]),
        signature=signature
    )
    
    xml = lote.to_xml(pretty_print=True)
    assert '<Signature xmlns="http://www.w3.org/2000/09/xmldsig#">' in xml
    assert 'URI="#lote1"' in xml
    assert "<SignatureValue>fake-signature-lote</SignatureValue>" in xml
    """Cenário 5: Lote com múltiplos RPS de diferentes tipos"""
    rps1 = Rps(inf_rps=InfRps(
        identificacao_rps=IdentificacaoRps(numero=101, serie="A", tipo=1),
        data_emissao=datetime.now(), natureza_operacao=1, optante_simples_national=1, incentivador_cultural=2, status=1,
        servico=DadosServico(valores=Valores(valor_servicos=100.0, iss_retido=2), item_lista_servico="1.01", discriminacao="RPS 1", codigo_municipio=1234567),
        prestador=IdentificacaoPrestador(cnpj="12345678000199"), tomador=DadosTomador(razao_social="T1")
    ))
    
    rps2 = Rps(inf_rps=InfRps(
        identificacao_rps=IdentificacaoRps(numero=102, serie="A", tipo=1),
        data_emissao=datetime.now(), natureza_operacao=1, optante_simples_national=1, incentivador_cultural=2, status=1,
        servico=DadosServico(valores=Valores(valor_servicos=200.0, iss_retido=2), item_lista_servico="1.01", discriminacao="RPS 2", codigo_municipio=1234567),
        prestador=IdentificacaoPrestador(cnpj="12345678000199"), tomador=DadosTomador(razao_social="T2")
    ))
    
    lote = LoteRps(
        id="L1",
        numero_lote=1,
        cnpj="12345678000199",
        inscricao_municipal="123",
        quantidade_rps=2,
        lista_rps=ListaRps(rps=[rps1, rps2])
    )
    
    xml = lote.to_xml(pretty_print=True)
    
    assert "<QuantidadeRps>2</QuantidadeRps>" in xml
    assert xml.count("<Rps>") == 2
    assert "<Discriminacao>RPS 1</Discriminacao>" in xml
    assert "<Discriminacao>RPS 2</Discriminacao>" in xml

def test_consultar_rps_xml():
    """Cenário 8: XML de Consulta de NFSe por RPS"""
    from pynfse.integration.carnaubal.abrasf.models.consultar_rps import ConsultarNfseRpsEnvio
    
    consulta = ConsultarNfseRpsEnvio(
        identificacao_rps=IdentificacaoRps(numero=123, serie="A", tipo=1),
        prestador=IdentificacaoPrestador(cnpj="12345678000199", inscricao_municipal="IM123")
    )
    
    xml = consulta.to_xml(pretty_print=True)

    root = _parse_xml(xml)
    assert root.tag == "ConsultarNfseRpsEnvio"
    assert root.xpath("string(.//*[local-name()='Numero'][1])") == "123"
    assert root.xpath("boolean(.//*[local-name()='IdentificacaoRps'])")
    assert root.xpath("boolean(.//*[local-name()='Prestador'])")
    assert root.xpath("string(.//*[local-name()='Cnpj'][1])") == "12345678000199"
