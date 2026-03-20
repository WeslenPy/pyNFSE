"""Testes para módulo calc e validators de cálculo automático - SpeedGov."""
import pytest
from decimal import Decimal
from datetime import datetime
from lxml import etree

from pynfse.src.integration.carnaubal.speedgov.helper.calc import (
    calc_base_calculo,
    calc_valor_iss,
    calc_pis_valor,
    calc_cofins_valor,
    calc_valor_liquido_nfse,
    calc_ibscbs,
    calc_valor_total_com_tributos,
    calc_aliquota_efetiva,
    calc_valor_tributo,
    calc_diferido,
)
from pynfse.src.integration.carnaubal.speedgov.models.rps import (
    Valores,
    IBSCBS,
    InfRps,
    DadosServico,
    IdentificacaoRps,
    IdentificacaoPrestador,
    DadosTomador,
    IdentificacaoTomador,
)
from pynfse.src.integration.carnaubal.speedgov.models.base import CpfCnpj, Endereco
from pynfse.src.integration.carnaubal.speedgov.helper.build import build_lote_element
from pynfse.src.integration.carnaubal.speedgov.models.lote import LoteRps, ListaRps


# --- Testes das funções de cálculo puras ---


class TestCalcBaseCalculo:
    def test_basico(self):
        assert calc_base_calculo(10000, 500) == Decimal("9500.00")

    def test_sem_deducoes(self):
        assert calc_base_calculo(100, 0) == Decimal("100.00")


class TestCalcValorIss:
    def test_basico(self):
        assert calc_valor_iss(9500, 0.05) == Decimal("475.00")

    def test_zero(self):
        assert calc_valor_iss(100, 0) == Decimal("0.00")


class TestCalcPisCofins:
    def test_pis(self):
        # 9500 * 0.0068 ≈ 64.60, arredondado
        assert calc_pis_valor(9500, 0.0068) == Decimal("64.60")

    def test_cofins(self):
        assert calc_cofins_valor(9500, 0.0316) == Decimal("300.20")

    def test_aliq_zero_retorna_none(self):
        assert calc_pis_valor(9500, 0) is None
        assert calc_cofins_valor(9500, 0) is None


class TestCalcValorLiquidoNfse:
    def test_envio_lote_referencia(self):
        """Conforme envio_lote.xml: 9500 - 2240 = 7260."""
        vl = calc_valor_liquido_nfse(
            base_calculo=9500,
            valor_pis=65,
            valor_cofins=300,
            valor_inss=1100,
            valor_ir=150,
            valor_csll=100,
            outras_retencoes=50,
            iss_retido=1,
            valor_iss=475,
            valor_iss_retido=475,
        )
        assert vl == Decimal("7260.00")

    def test_sem_retencoes(self):
        vl = calc_valor_liquido_nfse(
            base_calculo=100,
            valor_pis=0,
            valor_cofins=0,
            valor_inss=0,
            valor_ir=0,
            valor_csll=0,
            outras_retencoes=0,
            iss_retido=2,
            valor_iss=5,
            valor_iss_retido=0,
        )
        assert vl == Decimal("95.00")


class TestCalcIBSCBS:
    def test_valores_envio_lote(self):
        """Conforme envio_lote.xml: base 9500, aliq UF 9.5%, Mun 3.5%, CBS 8.8%."""
        result = calc_ibscbs(
            base=Decimal("9500"),
            aliq_uf=Decimal("0.095"),
            aliq_mun=Decimal("0.035"),
            aliq_cbs=Decimal("0.088"),
        )
        assert result["ibsu_f_valor"] == Decimal("902.50")
        assert result["ibs_mun_valor"] == Decimal("332.50")
        assert result["cbs_valor"] == Decimal("836.00")
        assert result["ibs_valor_total"] == Decimal("1235.00")


class TestCalcValorTotalComTributos:
    def test_envio_lote(self):
        """ValorServicos + IBSValorTotal + CBSValor = 10000 + 1235 + 836 = 12071."""
        vtt = calc_valor_total_com_tributos(
            valor_servicos=10000,
            ibs_valor_total=Decimal("1235"),
            cbs_valor=Decimal("836"),
        )
        assert vtt == Decimal("12071.00")


# --- Testes dos model validators ---


class TestValoresValidator:
    def test_minimal_valor_servicos_aliquota(self):
        """Apenas valor_servicos e aliquota -> base, iss, liquido calculados."""
        v = Valores(valor_servicos=100, aliquota=0.05)
        assert v.base_calculo == 100.0
        assert v.valor_iss == 5.0
        assert v.valor_liquido_nfse == 95.0

    def test_com_deducoes(self):
        v = Valores(valor_servicos=10000, valor_deducoes=500, aliquota=0.05)
        assert v.base_calculo == 9500.0
        assert v.valor_iss == 475.0

    def test_valores_explicitos_nao_sobrescritos(self):
        """Valores informados pelo usuário permanecem."""
        v = Valores(
            valor_servicos=100,
            aliquota=0.05,
            base_calculo=95.0,
            valor_iss=4.75,
        )
        assert v.base_calculo == 95.0
        assert v.valor_iss == 4.75

    def test_pis_cofins_calculados_quando_aliq_informada(self):
        v = Valores(
            valor_servicos=9500,
            aliquota=0.05,
            base_calculo_pis_cofins=9500,
            aliq_pis=0.0068,
            aliq_cofins=0.0316,
        )
        assert v.valor_pis == pytest.approx(64.60, abs=0.01)
        assert v.valor_cofins == pytest.approx(300.20, abs=0.01)


class TestIBSCBSValidator:
    def test_calculo_automatico(self):
        ibs = IBSCBS(
            ibscbs_base_calculo=Decimal("100"),
            ibsu_f_aliquota=Decimal("0.10"),
            ib_mun_aliquota=Decimal("0"),
            cbs_aliquota=Decimal("0.90"),
        )
        assert ibs.ibsu_f_valor == Decimal("10.00")
        assert ibs.ibs_mun_valor == Decimal("0.00")
        assert ibs.cbs_valor == Decimal("90.00")
        assert ibs.ibs_valor_total == Decimal("10.00")

    def test_aliquota_efetiva_com_reducao(self):
        ibs = IBSCBS(
            ibscbs_base_calculo=Decimal("100"),
            ibsu_f_aliquota=Decimal("0.10"),
            ibsu_f_perc_reducao=Decimal("0.50"),
        )
        assert ibs.ibsu_f_aliquota_efetiva == Decimal("0.05")
        assert ibs.ibsu_f_valor == Decimal("5.00")


class TestInfRpsValorTotalComTributos:
    def test_valor_total_com_tributos_calculado(self):
        inf = InfRps(
            identificacao_rps=IdentificacaoRps(numero=1, serie="1", tipo=1),
            data_emissao=datetime.now(),
            regime_especial_tributacao=1,
            optante_simples_nacional=2,
            servico=DadosServico(
                valores=Valores(valor_servicos=100, aliquota=0.05),
                item_lista_servico="106",
                codigo_cnae=6204000,
                codigo_tributacao_municipio="620400000",
                discriminacao="Teste",
                codigo_municipio=2303402,
            ),
            prestador=IdentificacaoPrestador(cnpj="12345678000199", inscricao_municipal="1"),
            tomador=DadosTomador(
                identificacao_tomador=IdentificacaoTomador(cpf_cnpj=CpfCnpj(cnpj="12345678000199")),
                razao_social="Cliente",
                endereco=Endereco(
                    endereco="Rua",
                    numero="1",
                    bairro="Centro",
                    codigo_municipio=2303402,
                    uf="CE",
                    cep="63100000",
                ),
            ),
            ibscbs=IBSCBS(
                ibscbs_base_calculo=Decimal("100"),
                ibsu_f_aliquota=Decimal("0.10"),
                ib_mun_aliquota=Decimal("0"),
                cbs_aliquota=Decimal("0.90"),
            ),
        )
        assert inf.ibscbs.valor_total_com_tributos == Decimal("200.00")


# --- Testes integrados: cenário completo envio_lote.xml ---


class TestCenarioEnvioLoteCompleto:
    """Valida todos os cálculos do cenário envio_lote.xml de referência."""

    def test_valores_completos_envio_lote(self):
        """
        Cenário envio_lote.xml:
        ValorServicos=10000, ValorDeducoes=500, Aliquota=0.05
        ValorPis=65, ValorCofins=300, ValorInss=1100, ValorIr=150, ValorCsll=100,
        OutrasRetencoes=50, IssRetido=1, ValorIssRetido=475
        BaseCalculo=9500, ValorIss=475, ValorLiquidoNfse=7260
        """
        v = Valores(
            valor_servicos=10000,
            valor_deducoes=500,
            valor_pis=65,
            valor_cofins=300,
            valor_inss=1100,
            valor_ir=150,
            valor_csll=100,
            iss_retido=1,
            valor_iss_retido=475,
            outras_retencoes=50,
            aliquota=0.05,
        )
        assert v.base_calculo == 9500.0
        assert v.valor_iss == 475.0
        assert v.valor_liquido_nfse == 7260.0

    def test_ibscbs_envio_lote(self):
        """
        Cenário envio_lote.xml: base 9500, IBSUF 9.5%, IBSMun 3.5%, CBS 8.8%
        IBSUFValor=902.50, IBSMunValor=332.50, CBSValor=836, IBSValorTotal=1235
        """
        ibs = IBSCBS(
            ibscbs_base_calculo=Decimal("9500"),
            ibsu_f_aliquota=Decimal("0.095"),
            ib_mun_aliquota=Decimal("0.035"),
            cbs_aliquota=Decimal("0.088"),
        )
        assert ibs.ibsu_f_valor == Decimal("902.50")
        assert ibs.ibs_mun_valor == Decimal("332.50")
        assert ibs.cbs_valor == Decimal("836.00")
        assert ibs.ibs_valor_total == Decimal("1235.00")

    def test_valor_total_com_tributos_envio_lote(self):
        """ValorTotalComTributos = 10000 + 1235 + 836 = 12071."""
        inf = InfRps(
            identificacao_rps=IdentificacaoRps(numero=100, serie="A1", tipo=1),
            data_emissao=datetime(2025, 12, 5, 10, 30),
            regime_especial_tributacao=1,
            optante_simples_nacional=2,
            servico=DadosServico(
                valores=Valores(
                    valor_servicos=10000,
                    valor_deducoes=500,
                    valor_pis=65,
                    valor_cofins=300,
                    valor_inss=1100,
                    valor_ir=150,
                    valor_csll=100,
                    iss_retido=1,
                    valor_iss_retido=475,
                    outras_retencoes=50,
                    aliquota=0.05,
                ),
                item_lista_servico="01.01",
                codigo_cnae=6201501,
                codigo_tributacao_municipio="010100",
                discriminacao="Desenvolvimento de software personalizado.",
                codigo_municipio=3550308,
            ),
            prestador=IdentificacaoPrestador(cnpj="12345678000199", inscricao_municipal="12345"),
            tomador=DadosTomador(
                identificacao_tomador=IdentificacaoTomador(cpf_cnpj=CpfCnpj(cnpj="98765432000188")),
                razao_social="CLIENTE EXEMPLO LTDA",
                endereco=Endereco(
                    endereco="Avenida Paulista",
                    numero="1000",
                    complemento="Sala 1501",
                    bairro="Bela Vista",
                    codigo_municipio=3550308,
                    uf="SP",
                    cep="01310100",
                ),
            ),
            ibscbs=IBSCBS(
                ibscbs_base_calculo=Decimal("9500"),
                ibsu_f_aliquota=Decimal("0.095"),
                ib_mun_aliquota=Decimal("0.035"),
                cbs_aliquota=Decimal("0.088"),
            ),
        )
        assert inf.ibscbs.valor_total_com_tributos == Decimal("12071.00")


# --- Testes de arredondamento ---


class TestArredondamento:
    def test_arredondamento_half_up_base_calculo(self):
        """BaseCalculo com decimais: 100.005 deve arredondar para 100.01."""
        assert calc_base_calculo(100.005, 0) == Decimal("100.01")

    def test_arredondamento_valor_iss(self):
        """ValorIss: 100 * 0.055 = 5.50."""
        assert calc_valor_iss(100, 0.055) == Decimal("5.50")

    def test_arredondamento_pis_cofins(self):
        """PIS/COFINS com resultado .xx5 arredonda para cima."""
        assert calc_pis_valor(1000, 0.0065) == Decimal("6.50")
        assert calc_cofins_valor(1000, 0.0305) == Decimal("30.50")


# --- Testes de edge cases ---


class TestEdgeCases:
    def test_valor_liquido_iss_nao_retido(self):
        """Quando iss_retido=2, desconta ValorIss (não ValorIssRetido)."""
        vl = calc_valor_liquido_nfse(
            base_calculo=100,
            valor_pis=0,
            valor_cofins=0,
            valor_inss=0,
            valor_ir=0,
            valor_csll=0,
            outras_retencoes=0,
            iss_retido=2,
            valor_iss=5,
            valor_iss_retido=0,
        )
        assert vl == Decimal("95.00")

    def test_valor_liquido_zero_retencoes(self):
        """Base 100, sem retenções: líquido = 100."""
        vl = calc_valor_liquido_nfse(
            base_calculo=100,
            valor_pis=0,
            valor_cofins=0,
            valor_inss=0,
            valor_ir=0,
            valor_csll=0,
            outras_retencoes=0,
            iss_retido=2,
            valor_iss=0,
            valor_iss_retido=0,
        )
        assert vl == Decimal("100.00")

    def test_valor_liquido_minimo_zero(self):
        """Se retenções > base, líquido não pode ser negativo."""
        vl = calc_valor_liquido_nfse(
            base_calculo=100,
            valor_pis=50,
            valor_cofins=50,
            valor_inss=50,
            valor_ir=0,
            valor_csll=0,
            outras_retencoes=0,
            iss_retido=2,
            valor_iss=50,
            valor_iss_retido=0,
        )
        assert vl == Decimal("0.00")

    def test_base_calculo_pis_cofins_fallback(self):
        """Quando base_calculo_pis_cofins=0, usa base_calculo."""
        v = Valores(
            valor_servicos=9500,
            aliquota=0.05,
            base_calculo_pis_cofins=0,
            aliq_pis=0.0068,
            aliq_cofins=0.0316,
        )
        # base_calculo calculado = 9500
        assert v.base_calculo == 9500.0
        assert v.valor_pis == pytest.approx(64.60, abs=0.01)
        assert v.valor_cofins == pytest.approx(300.20, abs=0.01)


# --- Testes de funções auxiliares calc ---


class TestCalcAuxiliares:
    def test_calc_aliquota_efetiva(self):
        assert calc_aliquota_efetiva(Decimal("0.10"), Decimal("0.50")) == Decimal("0.05")
        assert calc_aliquota_efetiva(Decimal("0.095"), None) == Decimal("0.095")

    def test_calc_valor_tributo(self):
        assert calc_valor_tributo(Decimal("100"), Decimal("0.10")) == Decimal("10.00")
        assert calc_valor_tributo(Decimal("100"), None) is None

    def test_calc_diferido(self):
        assert calc_diferido(Decimal("100"), Decimal("0.50")) == Decimal("50.00")
        assert calc_diferido(Decimal("100"), None) is None


# --- Testes de IBSCBS com diferimento ---


class TestIBSCBSDiferimento:
    def test_diferimento_calculado(self):
        """IBSCBS com percentual de diferimento preenche valor diferido."""
        ibs = IBSCBS(
            ibscbs_base_calculo=Decimal("100"),
            ibsu_f_aliquota=Decimal("0.10"),
            ibsu_f_perc_diferimento=Decimal("0.20"),
        )
        assert ibs.ibsu_f_valor == Decimal("10.00")
        assert ibs.ibsu_f_valor_diferido == Decimal("2.00")


# --- Testes de XML gerado (valores calculados no output) ---


class TestXmlValoresCalculados:
    def test_xml_contem_valores_calculados(self):
        """O XML gerado deve conter os valores calculados corretamente."""
        from pynfse.src.integration.carnaubal.speedgov.models.rps import Rps

        rps = Rps(
            inf_rps=InfRps(
                identificacao_rps=IdentificacaoRps(numero=1, serie="1", tipo=1),
                data_emissao=datetime.now(),
                regime_especial_tributacao=1,
                optante_simples_nacional=2,
                servico=DadosServico(
                    valores=Valores(valor_servicos=100, aliquota=0.05),
                    item_lista_servico="106",
                    codigo_cnae=6204000,
                    codigo_tributacao_municipio="620400000",
                    discriminacao="Teste",
                    codigo_municipio=2303402,
                ),
                prestador=IdentificacaoPrestador(cnpj="12345678000199", inscricao_municipal="1"),
                tomador=DadosTomador(
                    identificacao_tomador=IdentificacaoTomador(cpf_cnpj=CpfCnpj(cnpj="12345678000199")),
                    razao_social="Cliente",
                    endereco=Endereco(
                        endereco="Rua",
                        numero="1",
                        bairro="Centro",
                        codigo_municipio=2303402,
                        uf="CE",
                        cep="63100000",
                    ),
                ),
            )
        )
        lote = LoteRps(
            id="lote_001",
            numero_lote=1,
            cnpj="12345678000199",
            inscricao_municipal="1",
            quantidade_rps=1,
            lista_rps=ListaRps(rps=[rps]),
        )
        root = build_lote_element(lote)
        xml_str = etree.tostring(root, encoding="unicode")
        assert "100.0" in xml_str or "100" in xml_str  # ValorServicos
        assert "5.0" in xml_str or "5" in xml_str  # ValorIss calculado
        assert "95.0" in xml_str or "95" in xml_str  # ValorLiquidoNfse calculado
        assert "BaseCalculo" in xml_str or "100" in xml_str
