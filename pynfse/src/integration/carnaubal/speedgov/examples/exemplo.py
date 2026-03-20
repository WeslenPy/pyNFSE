"""
Exemplo completo da integração SpeedGov com assinatura digital.
Baseado em speedgov.py: carrega certificado, gera XML assinado, valida e envia.
"""
from decimal import Decimal
import os
from datetime import datetime
from lxml import etree

from loguru import logger

from pynfse.src.integration.carnaubal.speedgov.models.rps import IBSCBS, DadosDPS
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
    TipoRps,
    NaturezaOperacao,
    RegimeEspecialTributacao,
    SimNao,
    StatusRps,
    IssRetido,
    TipoEmissaoDPS,
    TipoAmbiente,
    TributacaoIssqn,
    TipoRetencaoIssqn,
    OptanteSimplesNacionalDPS,
    RegimeApuracaoTributosSN,
)

def criar_rps_exemplo(cnpj_lote: str, inscricao_municipal: str) -> Rps:
    """RPS conforme modelo enviar_lote_rps.xml (referência SpeedGov)."""
    valor_produto = 1

    return Rps(
        inf_rps=InfRps(
            id="",
            identificacao_rps=IdentificacaoRps(numero=1, serie="1", tipo=TipoRps.RPS),
            data_emissao=datetime.now(),
            natureza_operacao=NaturezaOperacao.TRIBUTACAO_NO_MUNICIPIO,
            regime_especial_tributacao=RegimeEspecialTributacao.ME_EPP_SIMPLES_NACIONAL,
            optante_simples_nacional=SimNao.SIM,
            incentivador_cultural=SimNao.NAO,
            status=StatusRps.NORMAL,
            servico=DadosServico(
                valores=Valores(
                    valor_servicos=valor_produto,
                    valor_deducoes=0.00,
                    valor_inss=0.00,
                    valor_ir=0.00,
                    valor_csll=0.00,
                    iss_retido=IssRetido.NAO,
                    # valor_iss=5.00,
                    valor_iss_retido=0.00,
                    outras_retencoes=0.00,
                    base_calculo=valor_produto,
                    aliquota=0.03,
                    # valor_liquido_nfse=95.00,
                    cstp_pis_cofins=0.00,
                    # base_calculo_pis_cofins=0.00,
                    # tipo_retencao_pis_cofins=,
                    aliq_pis=0.00,
                    aliq_cofins=0.00,
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
            data_competencia=datetime.now().date(),
            
            dados_dps=DadosDPS(
                tp_emit=TipoEmissaoDPS.PRESTADOR,
                tp_amb=TipoAmbiente.PRODUCAO,
                dh_emi=datetime.now(),
                ver_aplic="1.0.0",
                cloc_emi=2303402,
                cloc_prestacao=2303402,
                # ctrib_nac="",
                trib_issqn=TributacaoIssqn.NORMAL,
                tp_ret_issqn=TipoRetencaoIssqn.NAO_RETIDO,
                op_simp_nac=OptanteSimplesNacionalDPS.OPTANTE_ME_EPP,
                reg_esp_trib=RegimeEspecialTributacao.NENHUM,
                reg_ap_trib_sn=RegimeApuracaoTributosSN.FED_MUN_PELO_SN,
                numero_dps=0,
            ),
            ibscbs=IBSCBS(
                ibscbs_base_calculo=Decimal("0"),
                ibsu_f_aliquota=Decimal("0"),
                ib_mun_aliquota=Decimal("0"),
                cbs_aliquota=Decimal("0"),
                localidade_incidencia_cod="2303402",
                localidade_incidencia_nome="CARNAUBAL/CE",
            )
        )
    )


def main():
    """Fluxo completo: certificado → XML assinado → validação → envio."""
    URL_HOMOLOGACAO = "http://speedgov.com.br:80/wsmod/Nfes?wsdl"
    CERT_PATH = "teste.pfx"
    CERT_PASSWORD = "123456"

    cnpj_lote = "57255426000103"
    inscricao_municipal = "1"

    provider = SpeedGovNFSe(URL=URL_HOMOLOGACAO)
    rps = criar_rps_exemplo(cnpj_lote,inscricao_municipal)
    
    print(rps)

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
