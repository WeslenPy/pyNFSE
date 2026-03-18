"""
Exemplo completo da integração SpeedGov com assinatura digital.
Baseado em speedgov.py: carrega certificado, gera XML assinado, valida e envia.
"""
import os
from datetime import datetime
from lxml import etree

from loguru import logger

from pynfse.src.integration.carnaubal.speedgov import (
    SpeedGovNFSe,
    Rps,
    InfRps,
    IdentificacaoRps,
    IdentificacaoPrestador,
    DadosTomador,
    IdentificacaoTomador,
    DadosServico,
    Valores,
    CpfCnpj,
    Endereco,
)


def criar_rps_exemplo(cnpj_lote:str,inscricao_municipal:str) -> Rps:
    """RPS conforme modelo enviar_lote_rps.xml (referência SpeedGov)."""
    return Rps(
        inf_rps=InfRps(
            id="",
            identificacao_rps=IdentificacaoRps(numero=1, serie="1", tipo=1),
            data_emissao=datetime.now(),
            natureza_operacao=1,
            regime_especial_tributacao=6,
            optante_simples_nacional=1,
            incentivador_cultural=2,
            status=1,
            servico=DadosServico(
                valores=Valores(
                    valor_servicos=100.00,
                    valor_deducoes=0.0,
                    valor_pis=0.0,
                    valor_cofins=0.0,
                    valor_inss=0.0,
                    valor_ir=0.0,
                    valor_csll=0.0,
                    iss_retido=2,
                    valor_iss=5.00,
                    valor_iss_retido=0.0,
                    outras_retencoes=0.0,
                    base_calculo=100.00,
                    aliquota=0.05,
                    valor_liquido_nfse=95.00,
                    desconto_condicionado=0.0,
                    desconto_incondicionado=0.0,
                ),
                item_lista_servico="106",
                codigo_cnae=6204000,
                codigo_tributacao_municipio="620400000",
                discriminacao="Recarga painel",
                codigo_municipio=2303402,
            ),
            prestador=IdentificacaoPrestador(
                cnpj=cnpj_lote,
                inscricao_municipal=inscricao_municipal,
            ),
            tomador=DadosTomador(
                identificacao_tomador=IdentificacaoTomador(
                    cpf_cnpj=CpfCnpj(cnpj="12345678000199"),
                ),
                razao_social="CLIENTE EXEMPLO LTDA",
                endereco=Endereco(
                    endereco="Rua Exemplo",
                    numero="100",
                    complemento="casa",
                    bairro="Centro",
                    codigo_municipio=2303402,
                    uf="CE",
                    cep="63100000",
                ),
            ),
            data_competencia=datetime.now(),
        )
    )


def main():
    """Fluxo completo: certificado → XML assinado → validação → envio."""
    URL_HOMOLOGACAO = "http://speedgov.com.br:80/wsmod/Nfes?wsdl"
    CERT_PATH = "F K HIGINO BRITO_40114832000153.pfx"
    CERT_PASSWORD = "123456"

    cnpj_lote = "57255426000103"
    inscricao_municipal = "1"

    provider = SpeedGovNFSe(URL=URL_HOMOLOGACAO)
    rps = criar_rps_exemplo(cnpj_lote,inscricao_municipal)

    # Carrega certificado (se existir) para assinatura
    cert_data = None
    if os.path.exists(CERT_PATH):
        try:
            cert_data = provider.get_certificate(CERT_PATH)
            logger.info("Certificado carregado")
        except Exception as e:
            logger.warning(f"Erro ao carregar certificado: {e}")

    # Gera XML (com ou sem assinatura)
    xml_lote = provider.create_rps_nfse(
        rps_list=[rps],
        numero_lote=1,
        cnpj=cnpj_lote,
        inscricao_municipal=inscricao_municipal,
        lote_id="lote_001",
        certificate_data=cert_data,
        certificate_password=CERT_PASSWORD if cert_data else None,
    )

    logger.success("XML gerado com sucesso")
    print("-" * 60)
    print(xml_lote)
    print("-" * 60)


    # Envio ao Web Service
    if cert_data:
        logger.info("Enviando para o Web Service...")
        result = provider.send(xml_lote)
        logger.info(f"Status: {result.response.status_code}")
        print("RESPOSTA:", (result.response.text[:500] if result.response.text else "-"))
    else:
        logger.info("Certificado não encontrado - XML gerado localmente (sem envio)")


if __name__ == "__main__":
    main()
