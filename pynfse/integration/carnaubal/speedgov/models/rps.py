"""
Modelos RPS para SpeedGov - estrutura enviar_lote_rps.xml.
Inclui blocos opcionais NFS-e Nacional (DadosDPS, DadosObra, ComercioExterior, etc).
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Annotated, Optional, Union

from pydantic import Field, ConfigDict, model_validator

from pynfse.integration.carnaubal.speedgov.constants import XMLDSIG_NS
from pynfse.integration.carnaubal.speedgov.models.base import CpfCnpj, Endereco, SpeedGovNode
from pynfse.integration.carnaubal.speedgov.enums import (
    RegimeEspecialTributacao,
    TipoEmissaoDPS,
    TipoAmbiente,
    TributacaoIssqn,
    TipoRetencaoIssqn,
    OptanteSimplesNacionalDPS,
    RegimeApuracaoTributosSN,
)
from pynfse.common.coerced_decimal import CoercedDecimal
from pynfse.common.signature import Signature
from pynfse.integration.carnaubal.speedgov.helper.calc import (
    calc_base_calculo,
    calc_valor_iss,
    calc_pis_valor,
    calc_cofins_valor,
    calc_valor_liquido_nfse,
    calc_ibscbs,
    calc_valor_total_com_tributos,
)


# --- Blocos NFS-e Nacional encapsulados ---


class DadosDPS(SpeedGovNode):
    """
    Dados da Declaração de Prestação de Serviços - NFS-e Nacional.
    Campos de escolha usam enums: TipoEmissaoDPS, TipoAmbiente, TributacaoIssqn,
    TipoRetencaoIssqn, OptanteSimplesNacionalDPS, RegimeApuracaoTributosSN.
    """
    model_config = ConfigDict(populate_by_name=True)

    tp_emit: Optional[Union[TipoEmissaoDPS, int]] = Field(None, alias="TpEmit", description="TipoEmissaoDPS: 1=Prestador, 2=Tomador")
    tp_amb: Optional[Union[TipoAmbiente, int]] = Field(None, alias="TpAmb", description="TipoAmbiente: 1=Produção, 2=Homologação")
    dh_emi: Optional[datetime] = Field(None, alias="DhEmi")
    ver_aplic: Optional[str] = Field("ISS_V2_1.0.0", alias="VerAplic", max_length=20)
    cloc_emi: Optional[Union[int, str]] = Field(None, alias="CLocEmi")
    cloc_prestacao: Optional[Union[int, str]] = Field(None, alias="CLocPrestacao")
    ctrib_nac: Optional[str] = Field(None, alias="CTribNac", max_length=6)
    trib_issqn: Optional[Union[TributacaoIssqn, int]] = Field(None, alias="TribIssqn", description="TributacaoIssqn: 1=Normal, 2=Imune, 3=Isento, 4=Exportação")
    tp_ret_issqn: Optional[Union[TipoRetencaoIssqn, int]] = Field(None, alias="TpRetIssqn", description="TipoRetencaoIssqn: 1=Não retido, 2=Tomador, 3=Intermediário")
    op_simp_nac: Optional[Union[OptanteSimplesNacionalDPS, int]] = Field(None, alias="OpSimpNac", description="OptanteSimplesNacionalDPS: 1=Não optante, 2=ME/EPP, 3=MEI")
    reg_esp_trib: Optional[Union[RegimeEspecialTributacao, int]] = Field(None, alias="RegEspTrib", description="RegimeEspecialTributacao: 0=Nenhum, 1=Microempresa Municipal, 2=Estimativa, 3=Sociedade Profissionais, 4=Cooperativa, 5=MEI, 6=ME/EPP Simples Nacional")
    reg_ap_trib_sn: Optional[Union[RegimeApuracaoTributosSN, int]] = Field(None, alias="RegApTribSN", description="RegimeApuracaoTributosSN: 1=Fed+Mun SN, 2=Fed SN+ISSQN NFSe, 3=Fed+Mun NFSe")

    serie: Optional[int] = Field(None, alias="serie")
    numero_dps: Optional[int] = Field(None, alias="nDPS")
    data_competencia: Optional[datetime] = Field(None, alias="dCompet")


class EnderecoObra(SpeedGovNode):
    """Endereço da obra - NFS-e Nacional."""
    model_config = ConfigDict(populate_by_name=True)

    cep: Optional[str] = Field(None, alias="Cep", max_length=10)# cep da obra
    logradouro: Optional[str] = Field(None, alias="Logradouro", max_length=125)# logradouro da obra
    numero: Optional[str] = Field(None, alias="Numero", max_length=10)# número da obra
    complemento: Optional[str] = Field(None, alias="Complemento", max_length=60)# complemento da obra
    bairro: Optional[str] = Field(None, alias="Bairro", max_length=60)# bairro da obra


class DadosObra(SpeedGovNode):
    """Dados da obra - NFS-e Nacional."""
    model_config = ConfigDict(populate_by_name=True)

    codigo_obra: Optional[str] = Field(None, alias="CodigoObra", max_length=30)# código da obra
    insc_imob_fisc: Optional[str] = Field(None, alias="InscImobFisc", max_length=30)# inscrição imobiliária fiscal
    endereco_obra: Optional[EnderecoObra] = Field(None, alias="EnderecoObra")# endereço da obra


class ComercioExterior(SpeedGovNode):
    """Comércio exterior - NFS-e Nacional."""
    model_config = ConfigDict(populate_by_name=True)

    md_prestacao: Optional[int] = Field(None, alias="MdPrestacao", description="Use ModalidadePrestacao")
    vinc_prest: Optional[int] = Field(None, alias="VincPrest")# vinculação da prestação
    tp_moeda: Optional[int] = Field(None, alias="TpMoeda")# tipo de moeda
    v_serv_moeda: Optional[float] = Field(None, alias="VServMoeda")# valor do serviço em moeda
    mec_af_comex_p: Optional[str] = Field(None, alias="MecAFComexP", max_length=10)# mecanismo de ajuste de comércio exterior
    mec_af_comex_t: Optional[str] = Field(None, alias="MecAFComexT", max_length=10)# mecanismo de ajuste de comércio exterior
    mov_temp_bens: Optional[int] = Field(None, alias="MovTempBens")# movimentação temporária de bens
    ndi: Optional[str] = Field(None, alias="NDI", max_length=12)# número de declaração de importação
    nre: Optional[str] = Field(None, alias="NRE", max_length=12)# número de registro de exportação
    mdic: Optional[int] = Field(None, alias="MDIC")# município de destino
    c_pais_result: Optional[str] = Field(None, alias="CPaisResult", max_length=4)# código do país de resultado


class ExigibilidadeSuspensa(SpeedGovNode):
    """Exigibilidade suspensa - NFS-e Nacional. Use TipoExigibilidadeSuspensa para tp_susp."""
    model_config = ConfigDict(populate_by_name=True)

    tp_susp: Optional[int] = Field(None, alias="TpSusp", description="Use TipoExigibilidadeSuspensa")
    n_processo: Optional[str] = Field(None, alias="NProcesso", max_length=30)# número do processo


class BeneficioMunicipal(SpeedGovNode):
    """Benefício municipal - NFS-e Nacional."""
    model_config = ConfigDict(populate_by_name=True)

    tp_bm: Optional[int] = Field(None, alias="TpBM")
    nbm: Optional[str] = Field(None, alias="NBM", max_length=14)
    v_red_bcbm: Optional[float] = Field(None, alias="VRedBCBM")# valor de redução da base de cálculo do benefício municipal
    p_red_bcbm: Optional[float] = Field(None, alias="PRedBCBM")# percentual de redução da base de cálculo do benefício municipal


class ReembolsoRepasse(SpeedGovNode):
    """Reembolso/repasse - NFS-e Nacional."""
    model_config = ConfigDict(populate_by_name=True)

    tp_reemb_rep_res: Optional[int] = Field(None, alias="TpReembRepRes")# tipo de reembolso/repasse
    x_tp_reemb_rep_res: Optional[str] = Field(None, alias="XTpReembRepRes", max_length=2000)# descrição do tipo de reembolso/repasse
    v_reemb_rep_res: Optional[float] = Field(None, alias="VReembRepRes")# valor do reembolso/repasse


class Destinatario(SpeedGovNode):
    """Destinatário - NFS-e Nacional."""
    model_config = ConfigDict(populate_by_name=True)

    cnpj_cpf: Optional[str] = Field(None, alias="CnpjCpf", min_length=11, max_length=14)# CPF/CNPJ do destinatário
    nome: Optional[str] = Field(None, alias="Nome", max_length=115)# nome do destinatário
    logradouro: Optional[str] = Field(None, alias="Logradouro", max_length=125)# logradouro do destinatário
    numero: Optional[str] = Field(None, alias="Numero", max_length=10)# número do destinatário
    complemento: Optional[str] = Field(None, alias="Complemento", max_length=60)# complemento do destinatário
    bairro: Optional[str] = Field(None, alias="Bairro", max_length=60)# bairro do destinatário
    cidade: Optional[str] = Field(None, alias="Cidade", max_length=60)# cidade do destinatário
    uf: Optional[str] = Field(None, alias="UF", max_length=2)# uf do destinatário
    cep: Optional[str] = Field(None, alias="CEP", max_length=10)# cep do destinatário
    cod_municipio: Optional[int] = Field(None, alias="CodMunicipio")# código do municipio do destinatário
    cod_pais: Optional[str] = Field(None, alias="CodPais", max_length=4)# código do pais do destinatário
    cod_postal_ext: Optional[str] = Field(None, alias="CodPostalExt", max_length=10)# código postal extra do destinatário
    nif: Optional[str] = Field(None, alias="NIF", max_length=40)# número de identificação fiscal do destinatário
    email: Optional[str] = Field(None, alias="Email", max_length=120)# email do destinatário
    telefone: Optional[str] = Field(None, alias="Telefone", max_length=20)# telefone do destinatário


class ControleIBSCBS(SpeedGovNode):
    """Controle IBS/CBS - NFS-e Nacional. Use FinalidadeNFSe, IndicadorFinal, IndicadorDestino."""
    model_config = ConfigDict(populate_by_name=True)

    fin_nfse: Optional[int] = Field(None, alias="FinNFSe", description="Use FinalidadeNFSe")
    ind_final: Optional[int] = Field(None, alias="IndFinal", description="Use IndicadorFinal")
    tp_oper: Optional[int] = Field(None, alias="TpOper")# tipo de operação
    tp_ente_gov: Optional[int] = Field(None, alias="TpEnteGov")# tipo de ente governamental
    ind_dest: Optional[int] = Field(None, alias="IndDest", description="Use IndicadorDestino")
    c_ind_op: Optional[str] = Field(None, alias="CIndOp", max_length=6)# código do indicador de operação
    x_tp_ente_gov: Optional[str] = Field(None, alias="XTpEnteGov", max_length=2000)# descrição do tipo de ente governamental


class IBSCBS(SpeedGovNode):
    """IBS/CBS - NFS-e Nacional."""
    model_config = ConfigDict(populate_by_name=True)

    ibscbs_base_calculo: Optional[CoercedDecimal] = Field(None, alias="IBSCBSBaseCalculo")

    ibsu_f_aliquota: Optional[CoercedDecimal] = Field(None, alias="IBSUFAliquota")
    ib_mun_aliquota: Optional[CoercedDecimal] = Field(None, alias="IBSMunAliquota")
    cbs_aliquota: Optional[CoercedDecimal] = Field(None, alias="CBSAliquota")

    ibsu_f_valor: Optional[CoercedDecimal] = Field(None, alias="IBSUFValor")
    ibs_mun_valor: Optional[CoercedDecimal] = Field(None, alias="IBSMunValor")
    cbs_valor: Optional[CoercedDecimal] = Field(None, alias="CBSValor")

    ibsu_f_perc_reducao: Optional[CoercedDecimal] = Field(None, alias="IBSUFPercReducao")
    ibs_mun_perc_reducao: Optional[CoercedDecimal] = Field(None, alias="IBSMunPercReducao")
    cbs_perc_reducao: Optional[CoercedDecimal] = Field(None, alias="CBSPercReducao")

    ibsu_f_aliquota_efetiva: Optional[CoercedDecimal] = Field(None, alias="IBSUFAliquotaEfetiva")
    ibs_mun_aliquota_efetiva: Optional[CoercedDecimal] = Field(None, alias="IBSMunAliquotaEfetiva")
    cbs_aliquota_efetiva: Optional[CoercedDecimal] = Field(None, alias="CBSAliquotaEfetiva")

    ibsu_f_perc_diferimento: Optional[CoercedDecimal] = Field(None, alias="IBSUFPercDiferimento")
    ibs_mun_perc_diferimento: Optional[CoercedDecimal] = Field(None, alias="IBSMunPercDiferimento")
    cbs_perc_diferimento: Optional[CoercedDecimal] = Field(None, alias="CBSPercDiferimento")

    ibsu_f_valor_diferido: Optional[CoercedDecimal] = Field(None, alias="IBSUFValorDiferido")
    ibs_mun_valor_diferido: Optional[CoercedDecimal] = Field(None, alias="IBSMunValorDiferido")
    cbs_valor_diferido: Optional[CoercedDecimal] = Field(None, alias="CBSValorDiferido")

    ibs_credito_presumido_aliq: Optional[CoercedDecimal] = Field(None, alias="IBSCreditoPresumidoAliq")
    ibs_credito_presumido_valor: Optional[CoercedDecimal] = Field(None, alias="IBSCreditoPresumidoValor")
    cbs_credito_presumido_aliq: Optional[CoercedDecimal] = Field(None, alias="CBSCreditoPresumidoAliq")
    cbs_credito_presumido_valor: Optional[CoercedDecimal] = Field(None, alias="CBSCreditoPresumidoValor")

    ibs_valor_total: Optional[CoercedDecimal] = Field(None, alias="IBSValorTotal")
    valor_total_com_tributos: Optional[CoercedDecimal] = Field(None, alias="ValorTotalComTributos")

    ibs_valor_reembolso: Optional[CoercedDecimal] = Field(None, alias="IBSValorReembolso")

    localidade_incidencia_cod: Optional[str] = Field(None, alias="LocalidadeIncidenciaCod")
    localidade_incidencia_nome: Optional[Annotated[str, ...]] = Field(None, alias="LocalidadeIncidenciaNome")

    perc_redutor_compra_gov: Optional[CoercedDecimal] = Field(None, alias="PercRedutorCompraGov")

    @model_validator(mode="after")
    def _calcular_campos_ibscbs(self):
        """
        Calcula alíquotas efetivas, valores, diferidos, IBSValorTotal.
        ValorTotalComTributos é calculado em InfRps (usa valor_servicos do pai).
        """
        base = self.ibscbs_base_calculo or Decimal(0)
        if base == 0 and not (self.ibsu_f_aliquota or self.ib_mun_aliquota or self.cbs_aliquota):
            return self

        result = calc_ibscbs(
            base,
            self.ibsu_f_aliquota,
            self.ib_mun_aliquota,
            self.cbs_aliquota,
            self.ibsu_f_perc_reducao,
            self.ibs_mun_perc_reducao,
            self.cbs_perc_reducao,
            self.ibsu_f_perc_diferimento,
            self.ibs_mun_perc_diferimento,
            self.cbs_perc_diferimento,
        )

        for key, value in result.items():
            if value is not None and getattr(self, key, None) is None:
                object.__setattr__(self, key, value)

        return self


class IdentificacaoRps(SpeedGovNode):
    """
    Identificação do RPS.
    Para tipo, use o enum TipoRps (ex: TipoRps.RPS) ou int 1|2|3.
    """
    model_config = ConfigDict(populate_by_name=True)

    numero: int = Field(..., alias="Numero", ge=0, description="Número do RPS")
    serie: str = Field(..., alias="Serie", min_length=1, max_length=5, description="Série do RPS")
    tipo: int = Field(..., alias="Tipo", ge=1, le=3, description="Tipo: use TipoRps (RPS=1, NOTA_FISCAL_CONJUGADA_CUPOM=2, CUPOM=3)")


class IdentificacaoPrestador(SpeedGovNode):
    model_config = ConfigDict(populate_by_name=True)

    cnpj: str = Field(..., alias="Cnpj", min_length=14, max_length=14)# CNPJ do prestador
    inscricao_municipal: str = Field(..., alias="InscricaoMunicipal", min_length=1, max_length=15)# inscrição municipal do prestador


class IdentificacaoTomador(SpeedGovNode):
    model_config = ConfigDict(populate_by_name=True)

    cpf_cnpj: CpfCnpj = Field(..., alias="CpfCnpj")# CPF/CNPJ do tomador


class Valores(SpeedGovNode):
    """
    Valores do serviço - NFS-e.
    Campos derivados (base_calculo, valor_iss, valor_pis, valor_cofins, valor_liquido_nfse)
    podem ser omitidos e serão calculados automaticamente pelo model_validator.
    """
    model_config = ConfigDict(populate_by_name=True)

    valor_servicos: float = Field(..., alias="ValorServicos", ge=0)
    valor_deducoes: float = Field(0, alias="ValorDeducoes", ge=0)
    valor_pis: Optional[float] = Field(None, alias="ValorPis", ge=0)
    valor_cofins: Optional[float] = Field(None, alias="ValorCofins", ge=0)
    valor_inss: float = Field(0, alias="ValorInss", ge=0)
    valor_ir: float = Field(0, alias="ValorIr", ge=0)
    valor_csll: float = Field(0, alias="ValorCsll", ge=0)
    iss_retido: int = Field(2, alias="IssRetido", ge=1, le=2, description="Use IssRetido (SIM=1, NAO=2)")
    valor_iss: Optional[float] = Field(None, alias="ValorIss", ge=0)
    valor_iss_retido: float = Field(0, alias="ValorIssRetido", ge=0)
    outras_retencoes: float = Field(0, alias="OutrasRetencoes", ge=0)
    base_calculo: Optional[float] = Field(None, alias="BaseCalculo", ge=0)
    aliquota: float = Field(..., alias="Aliquota", ge=0, le=9.9999)
    valor_liquido_nfse: Optional[float] = Field(None, alias="ValorLiquidoNfse", ge=0)
    desconto_condicionado: float = Field(0, alias="DescontoCondicionado", ge=0)
    desconto_incondicionado: float = Field(0, alias="DescontoIncondicionado", ge=0)

    cstp_pis_cofins: float = Field(0, alias="CSTPisCofins", ge=0)
    base_calculo_pis_cofins: float = Field(0, alias="BaseCalculoPisCofins", ge=0)
    tipo_retencao_pis_cofins: float = Field(0, alias="TipoRetencaoPisCofins", ge=0)

    aliq_pis: float = Field(0, alias="AliqPis", ge=0)
    aliq_cofins: float = Field(0, alias="AliqCofins", ge=0)

    p_tot_trib_fed: float = Field(0, alias="pTotTribFed", ge=0)
    p_tot_trib_est: float = Field(0, alias="pTotTribEst", ge=0)
    p_tot_trib_mun: float = Field(0, alias="pTotTribMun", ge=0)

    @model_validator(mode="after")
    def _calcular_campos_derivados(self):
        """Preenche base_calculo, valor_iss, valor_pis, valor_cofins, valor_liquido_nfse se None."""
        # 1. Base de cálculo
        if self.base_calculo is None:
            bc = calc_base_calculo(self.valor_servicos, self.valor_deducoes)
            object.__setattr__(self, "base_calculo", float(bc))
        base = self.base_calculo

        # 2. Valor ISS
        if self.valor_iss is None:
            vi = calc_valor_iss(base, self.aliquota)
            object.__setattr__(self, "valor_iss", float(vi))

        # 3. PIS (se aliq_pis > 0)
        if self.valor_pis is None and self.aliq_pis and self.aliq_pis > 0:
            base_pc = self.base_calculo_pis_cofins or base
            vp = calc_pis_valor(base_pc, self.aliq_pis)
            if vp is not None:
                object.__setattr__(self, "valor_pis", float(vp))
            else:
                object.__setattr__(self, "valor_pis", 0.0)
        elif self.valor_pis is None:
            object.__setattr__(self, "valor_pis", 0.0)

        # 4. COFINS (se aliq_cofins > 0)
        if self.valor_cofins is None and self.aliq_cofins and self.aliq_cofins > 0:
            base_pc = self.base_calculo_pis_cofins or base
            vc = calc_cofins_valor(base_pc, self.aliq_cofins)
            if vc is not None:
                object.__setattr__(self, "valor_cofins", float(vc))
            else:
                object.__setattr__(self, "valor_cofins", 0.0)
        elif self.valor_cofins is None:
            object.__setattr__(self, "valor_cofins", 0.0)

        # 5. Valor líquido
        if self.valor_liquido_nfse is None:
            vl = calc_valor_liquido_nfse(
                base,
                self.valor_pis or 0,
                self.valor_cofins or 0,
                self.valor_inss,
                self.valor_ir,
                self.valor_csll,
                self.outras_retencoes,
                self.iss_retido,
                self.valor_iss or 0,
                self.valor_iss_retido,
            )
            object.__setattr__(self, "valor_liquido_nfse", float(vl))

        return self

class DadosServico(SpeedGovNode):
    model_config = ConfigDict(populate_by_name=True)

    valores: Valores = Field(..., alias="Valores")# valores do serviço
    item_lista_servico: str = Field(..., alias="ItemListaServico", min_length=1, max_length=5)# item lista serviço
    codigo_cnae: int = Field(..., alias="CodigoCnae", ge=0, le=9999999)# código CNAE
    codigo_tributacao_municipio: str = Field(..., alias="CodigoTributacaoMunicipio", min_length=1, max_length=20)# código tributação municipio
    discriminacao: str = Field(..., alias="Discriminacao", min_length=1, max_length=2000)# discriminação
    codigo_municipio: int = Field(..., alias="CodigoMunicipio", ge=0, le=9999999)# código municipio


class DadosTomador(SpeedGovNode):
    """Tomador - sem Contato."""
    model_config = ConfigDict(populate_by_name=True)

    identificacao_tomador: IdentificacaoTomador = Field(..., alias="IdentificacaoTomador")# identificacao do tomador
    razao_social: str = Field(..., alias="RazaoSocial", min_length=1, max_length=115)# razão social do tomador
    endereco: Endereco = Field(..., alias="Endereco")# endereço do tomador


class InfRps(SpeedGovNode):
    """
    InfRps - campos base + blocos opcionais NFS-e Nacional.
    Use os enums para campos de escolha: NaturezaOperacao, RegimeEspecialTributacao,
    SimNao, StatusRps.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[str] = Field("", alias="Id")
    identificacao_rps: IdentificacaoRps = Field(..., alias="IdentificacaoRps")
    data_emissao: datetime = Field(..., alias="DataEmissao")
    natureza_operacao: int = Field(1, alias="NaturezaOperacao", ge=1, le=6, description="Use NaturezaOperacao")
    regime_especial_tributacao: int = Field(..., alias="RegimeEspecialTributacao", ge=1, le=6, description="Use RegimeEspecialTributacao")
    optante_simples_nacional: int = Field(..., alias="OptanteSimplesNacional", ge=1, le=2, description="Use SimNao")
    incentivador_cultural: int = Field(2, alias="IncentivadorCultural", ge=1, le=2, description="Use SimNao")
    status: int = Field(1, alias="Status", ge=1, le=2, description="Use StatusRps")
    servico: DadosServico = Field(..., alias="Servico")
    prestador: IdentificacaoPrestador = Field(..., alias="Prestador")
    tomador: DadosTomador = Field(..., alias="Tomador")

    # Blocos NFS-e Nacional encapsulados (xml_emit_if_any: emitir só se houver valor)
    dados_dps: Optional[DadosDPS] = Field(None, alias="DadosDPS", json_schema_extra={"xml_emit_if_any": True})
    dados_obra: Optional[DadosObra] = Field(None, alias="DadosObra", json_schema_extra={"xml_emit_if_any": True})
    comercio_exterior: Optional[ComercioExterior] = Field(None, alias="ComercioExterior", json_schema_extra={"xml_emit_if_any": True})
    exigibilidade_suspensa: Optional[ExigibilidadeSuspensa] = Field(None, alias="ExigibilidadeSuspensa", json_schema_extra={"xml_emit_if_any": True})
    beneficio_municipal: Optional[BeneficioMunicipal] = Field(None, alias="BeneficioMunicipal", json_schema_extra={"xml_emit_if_any": True})
    reembolso_repasse: Optional[ReembolsoRepasse] = Field(None, alias="ReembolsoRepasse", json_schema_extra={"xml_emit_if_any": True})
    destinatario: Optional[Destinatario] = Field(None, alias="Destinatario", json_schema_extra={"xml_emit_if_any": True})
    controle_ibscbs: Optional[ControleIBSCBS] = Field(None, alias="ControleIBSCBS", json_schema_extra={"xml_emit_if_any": True})
    ibscbs: Optional[IBSCBS] = Field(None, alias="IBSCBS", json_schema_extra={"xml_emit_if_any": True})
    data_competencia: Optional[date] = Field(None, alias="DataCompetencia")

    @model_validator(mode="after")
    def _calcular_valor_total_com_tributos(self):
        """
        Preenche ibscbs.valor_total_com_tributos usando valor_servicos do pai.
        ValorTotalComTributos = ValorServicos + IBSValorTotal + CBSValor.
        """
        if self.ibscbs is None:
            return self
        if self.ibscbs.valor_total_com_tributos is not None:
            return self
        valor_servicos = self.servico.valores.valor_servicos
        ibs_total = self.ibscbs.ibs_valor_total or Decimal(0)
        cbs_valor = self.ibscbs.cbs_valor or Decimal(0)
        vtt = calc_valor_total_com_tributos(valor_servicos, ibs_total, cbs_valor)
        object.__setattr__(self.ibscbs, "valor_total_com_tributos", vtt)
        return self


class Rps(SpeedGovNode):
    """Rps = InfRps + Signature (conforme reference - Signature dentro de Rps)."""
    model_config = ConfigDict(populate_by_name=True)

    inf_rps: InfRps = Field(..., alias="InfRps")
    signature: Optional[Signature] = Field(
        None,
        alias="Signature",
        json_schema_extra={
            "xml_namespace": XMLDSIG_NS,
            "xml_child_namespace": None,
            "xml_reset_default_namespace": False,
        },
    )
