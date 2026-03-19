"""
Modelos RPS para SpeedGov - estrutura enviar_lote_rps.xml.
Inclui blocos opcionais NFS-e Nacional (DadosDPS, DadosObra, ComercioExterior, etc).
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Annotated, Optional, Union

from pydantic import BaseModel, Field, ConfigDict

from pynfse.src.integration.carnaubal.abrasf.models.rps import IdentificacaoOrgaoGerador
from pynfse.src.integration.carnaubal.speedgov.models.base import CpfCnpj, Endereco
from pynfse.src.integration.carnaubal.speedgov.enums import (
    TipoEmissaoDPS,
    TipoAmbiente,
    TributacaoIssqn,
    TipoRetencaoIssqn,
    OptanteSimplesNacionalDPS,
    RegimeApuracaoTributosSN,
)
from pynfse.src.common.signature import Signature


# --- Blocos NFS-e Nacional encapsulados ---


class DadosDPS(BaseModel):
    """
    Dados da Declaração de Prestação de Serviços - NFS-e Nacional.
    Campos de escolha usam enums: TipoEmissaoDPS, TipoAmbiente, TributacaoIssqn,
    TipoRetencaoIssqn, OptanteSimplesNacionalDPS, RegimeApuracaoTributosSN.
    """
    model_config = ConfigDict(populate_by_name=True)

    tp_emit: Optional[Union[TipoEmissaoDPS, int]] = Field(None, alias="TpEmit", description="TipoEmissaoDPS: 1=Prestador, 2=Tomador")
    tp_amb: Optional[Union[TipoAmbiente, int]] = Field(None, alias="TpAmb", description="TipoAmbiente: 1=Produção, 2=Homologação")
    dh_emi: Optional[datetime] = Field(None, alias="DhEmi")
    ver_aplic: Optional[str] = Field(None, alias="VerAplic", max_length=20)
    cloc_emi: Optional[Union[int, str]] = Field(None, alias="CLocEmi")
    cloc_prestacao: Optional[Union[int, str]] = Field(None, alias="CLocPrestacao")
    ctrib_nac: Optional[str] = Field(None, alias="CTribNac", max_length=6)
    trib_issqn: Optional[Union[TributacaoIssqn, int]] = Field(None, alias="TribIssqn", description="TributacaoIssqn: 1=Normal, 2=Imune, 3=Isento, 4=Exportação")
    tp_ret_issqn: Optional[Union[TipoRetencaoIssqn, int]] = Field(None, alias="TpRetIssqn", description="TipoRetencaoIssqn: 1=Não retido, 2=Tomador, 3=Intermediário")
    op_simp_nac: Optional[Union[OptanteSimplesNacionalDPS, int]] = Field(None, alias="OpSimpNac", description="OptanteSimplesNacionalDPS: 1=Não optante, 2=ME/EPP, 3=MEI")
    reg_esp_trib: Optional[str] = Field(None, alias="RegEspTrib", max_length=10)
    reg_ap_trib_sn: Optional[Union[RegimeApuracaoTributosSN, int]] = Field(None, alias="RegApTribSN", description="RegimeApuracaoTributosSN: 1=Fed+Mun SN, 2=Fed SN+ISSQN NFSe, 3=Fed+Mun NFSe")

    serie: Optional[int] = Field(None, alias="serie")
    numero_dps: Optional[int] = Field(None, alias="nDPS")
    data_competencia: Optional[datetime] = Field(None, alias="dCompet")


class EnderecoObra(BaseModel):
    """Endereço da obra - NFS-e Nacional."""
    model_config = ConfigDict(populate_by_name=True)

    cep: Optional[str] = Field(None, alias="Cep", max_length=10)# cep da obra
    logradouro: Optional[str] = Field(None, alias="Logradouro", max_length=125)# logradouro da obra
    numero: Optional[str] = Field(None, alias="Numero", max_length=10)# número da obra
    complemento: Optional[str] = Field(None, alias="Complemento", max_length=60)# complemento da obra
    bairro: Optional[str] = Field(None, alias="Bairro", max_length=60)# bairro da obra


class DadosObra(BaseModel):
    """Dados da obra - NFS-e Nacional."""
    model_config = ConfigDict(populate_by_name=True)

    codigo_obra: Optional[str] = Field(None, alias="CodigoObra", max_length=30)# código da obra
    insc_imob_fisc: Optional[str] = Field(None, alias="InscImobFisc", max_length=30)# inscrição imobiliária fiscal
    endereco_obra: Optional[EnderecoObra] = Field(None, alias="EnderecoObra")# endereço da obra


class ComercioExterior(BaseModel):
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


class ExigibilidadeSuspensa(BaseModel):
    """Exigibilidade suspensa - NFS-e Nacional. Use TipoExigibilidadeSuspensa para tp_susp."""
    model_config = ConfigDict(populate_by_name=True)

    tp_susp: Optional[int] = Field(None, alias="TpSusp", description="Use TipoExigibilidadeSuspensa")
    n_processo: Optional[str] = Field(None, alias="NProcesso", max_length=30)# número do processo


class BeneficioMunicipal(BaseModel):
    """Benefício municipal - NFS-e Nacional."""
    model_config = ConfigDict(populate_by_name=True)

    tp_bm: Optional[int] = Field(None, alias="TpBM")
    nbm: Optional[str] = Field(None, alias="NBM", max_length=14)
    v_red_bcbm: Optional[float] = Field(None, alias="VRedBCBM")# valor de redução da base de cálculo do benefício municipal
    p_red_bcbm: Optional[float] = Field(None, alias="PRedBCBM")# percentual de redução da base de cálculo do benefício municipal


class ReembolsoRepasse(BaseModel):
    """Reembolso/repasse - NFS-e Nacional."""
    model_config = ConfigDict(populate_by_name=True)

    tp_reemb_rep_res: Optional[int] = Field(None, alias="TpReembRepRes")# tipo de reembolso/repasse
    x_tp_reemb_rep_res: Optional[str] = Field(None, alias="XTpReembRepRes", max_length=2000)# descrição do tipo de reembolso/repasse
    v_reemb_rep_res: Optional[float] = Field(None, alias="VReembRepRes")# valor do reembolso/repasse


class Destinatario(BaseModel):
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


class ControleIBSCBS(BaseModel):
    """Controle IBS/CBS - NFS-e Nacional. Use FinalidadeNFSe, IndicadorFinal, IndicadorDestino."""
    model_config = ConfigDict(populate_by_name=True)

    fin_nfse: Optional[int] = Field(None, alias="FinNFSe", description="Use FinalidadeNFSe")
    ind_final: Optional[int] = Field(None, alias="IndFinal", description="Use IndicadorFinal")
    tp_oper: Optional[int] = Field(None, alias="TpOper")# tipo de operação
    tp_ente_gov: Optional[int] = Field(None, alias="TpEnteGov")# tipo de ente governamental
    ind_dest: Optional[int] = Field(None, alias="IndDest", description="Use IndicadorDestino")
    c_ind_op: Optional[str] = Field(None, alias="CIndOp", max_length=6)# código do indicador de operação
    x_tp_ente_gov: Optional[str] = Field(None, alias="XTpEnteGov", max_length=2000)# descrição do tipo de ente governamental


class IBSCBS(BaseModel):
    """IBS/CBS - NFS-e Nacional."""
    model_config = ConfigDict(populate_by_name=True)

    ibscbs_base_calculo: Optional[Decimal] = Field(None, alias="IBSCBSBaseCalculo")

    ibsu_f_aliquota: Optional[Decimal] = Field(None, alias="IBSUFAliquota")
    ib_mun_aliquota: Optional[Decimal] = Field(None, alias="IBSMunAliquota")
    cbs_aliquota: Optional[Decimal] = Field(None, alias="CBSAliquota")

    ibsu_f_valor: Optional[Decimal] = Field(None, alias="IBSUFValor")
    ibs_mun_valor: Optional[Decimal] = Field(None, alias="IBSMunValor")
    cbs_valor: Optional[Decimal] = Field(None, alias="CBSValor")

    ibsu_f_perc_reducao: Optional[Decimal] = Field(None, alias="IBSUFPercReducao")
    ibs_mun_perc_reducao: Optional[Decimal] = Field(None, alias="IBSMunPercReducao")
    cbs_perc_reducao: Optional[Decimal] = Field(None, alias="CBSPercReducao")

    ibsu_f_aliquota_efetiva: Optional[Decimal] = Field(None, alias="IBSUFAliquotaEfetiva")
    ibs_mun_aliquota_efetiva: Optional[Decimal] = Field(None, alias="IBSMunAliquotaEfetiva")
    cbs_aliquota_efetiva: Optional[Decimal] = Field(None, alias="CBSAliquotaEfetiva")

    ibsu_f_perc_diferimento: Optional[Decimal] = Field(None, alias="IBSUFPercDiferimento")
    ibs_mun_perc_diferimento: Optional[Decimal] = Field(None, alias="IBSMunPercDiferimento")
    cbs_perc_diferimento: Optional[Decimal] = Field(None, alias="CBSPercDiferimento")

    ibsu_f_valor_diferido: Optional[Decimal] = Field(None, alias="IBSUFValorDiferido")
    ibs_mun_valor_diferido: Optional[Decimal] = Field(None, alias="IBSMunValorDiferido")
    cbs_valor_diferido: Optional[Decimal] = Field(None, alias="CBSValorDiferido")

    ibs_credito_presumido_aliq: Optional[Decimal] = Field(None, alias="IBSCreditoPresumidoAliq")
    ibs_credito_presumido_valor: Optional[Decimal] = Field(None, alias="IBSCreditoPresumidoValor")
    cbs_credito_presumido_aliq: Optional[Decimal] = Field(None, alias="CBSCreditoPresumidoAliq")
    cbs_credito_presumido_valor: Optional[Decimal] = Field(None, alias="CBSCreditoPresumidoValor")

    ibs_valor_total: Optional[Decimal] = Field(None, alias="IBSValorTotal")
    valor_total_com_tributos: Optional[Decimal] = Field(None, alias="ValorTotalComTributos")

    ibs_valor_reembolso: Optional[Decimal] = Field(None, alias="IBSValorReembolso")

    localidade_incidencia_cod: Optional[str] = Field(None, alias="LocalidadeIncidenciaCod")
    localidade_incidencia_nome: Optional[Annotated[str, ...]] = Field(None, alias="LocalidadeIncidenciaNome")

    perc_redutor_compra_gov: Optional[Decimal] = Field(None, alias="PercRedutorCompraGov")



    # @model_validator(mode="after")
    # def calcular_campos(self):
    #     base = self.ibscbs_base_calculo or Decimal(0)

    #     def calc_aliquota_efetiva(aliq, red):
    #         if aliq is None:
    #             return None
    #         red = red or Decimal(0)
    #         return aliq * (Decimal(1) - red)

    #     def calc_valor(base, aliq_efetiva):
    #         if base is None or aliq_efetiva is None:
    #             return None
    #         return base * aliq_efetiva

    #     def calc_diferido(valor, perc):
    #         if valor is None or perc is None:
    #             return None
    #         return valor * perc

    #     # ALÍQUOTAS EFETIVAS 
    #     if self.ibsu_f_aliquota_efetiva is None:
    #         self.ibsu_f_aliquota_efetiva = calc_aliquota_efetiva(
    #             self.ibsu_f_aliquota, self.ibsu_f_perc_reducao
    #         )

    #     if self.ibs_mun_aliquota_efetiva is None:
    #         self.ibs_mun_aliquota_efetiva = calc_aliquota_efetiva(
    #             self.ib_mun_aliquota, self.ibs_mun_perc_reducao
    #         )

    #     if self.cbs_aliquota_efetiva is None:
    #         self.cbs_aliquota_efetiva = calc_aliquota_efetiva(
    #             self.cbs_aliquota, self.cbs_perc_reducao
    #         )

    #     # VALORES 
    #     if self.ibsu_f_valor is None:
    #         self.ibsu_f_valor = calc_valor(base, self.ibsu_f_aliquota_efetiva)

    #     if self.ibs_mun_valor is None:
    #         self.ibs_mun_valor = calc_valor(base, self.ibs_mun_aliquota_efetiva)

    #     if self.cbs_valor is None:
    #         self.cbs_valor = calc_valor(base, self.cbs_aliquota_efetiva)

    #     #DIFERIDOS
    #     if self.ibsu_f_valor_diferido is None:
    #         self.ibsu_f_valor_diferido = calc_diferido(
    #             self.ibsu_f_valor, self.ibsu_f_perc_diferimento
    #         )

    #     if self.ibs_mun_valor_diferido is None:
    #         self.ibs_mun_valor_diferido = calc_diferido(
    #             self.ibs_mun_valor, self.ibs_mun_perc_diferimento
    #         )

    #     if self.cbs_valor_diferido is None:
    #         self.cbs_valor_diferido = calc_diferido(
    #             self.cbs_valor, self.cbs_perc_diferimento
    #         )

    #     #TOTAL IBS
    #     if self.ibs_valor_total is None:
    #         self.ibs_valor_total = (self.ibsu_f_valor or 0) + (self.ibs_mun_valor or 0)

    #     # TOTAL COM TRIBUTOS
    #     if self.valor_total_com_tributos is None:
    #         self.valor_total_com_tributos = (
    #             base
    #             + (self.ibs_valor_total or 0)
    #             + (self.cbs_valor or 0)
    #         )

    #     return self
    
    
class IdentificacaoRps(BaseModel):
    """
    Identificação do RPS.
    Para tipo, use o enum TipoRps (ex: TipoRps.RPS) ou int 1|2|3.
    """
    model_config = ConfigDict(populate_by_name=True)

    numero: int = Field(..., alias="Numero", ge=0, description="Número do RPS")
    serie: str = Field(..., alias="Serie", min_length=1, max_length=5, description="Série do RPS")
    tipo: int = Field(..., alias="Tipo", ge=1, le=3, description="Tipo: use TipoRps (RPS=1, NOTA_FISCAL_CONJUGADA_CUPOM=2, CUPOM=3)")


class IdentificacaoPrestador(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    cnpj: str = Field(..., alias="Cnpj", min_length=14, max_length=14)# CNPJ do prestador
    inscricao_municipal: str = Field(..., alias="InscricaoMunicipal", min_length=1, max_length=15)# inscrição municipal do prestador


class IdentificacaoTomador(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    cpf_cnpj: CpfCnpj = Field(..., alias="CpfCnpj")# CPF/CNPJ do tomador


class Valores(BaseModel):
    """Valores básicos - sem CSTPisCofins, BaseCalculoPisCofins, TipoRetencaoPisCofins."""
    model_config = ConfigDict(populate_by_name=True)

    valor_servicos: float = Field(..., alias="ValorServicos", ge=0)# valor dos serviços 
    valor_deducoes: float = Field(0, alias="ValorDeducoes", ge=0)
    valor_pis: float = Field(0, alias="ValorPis", ge=0)# valor do PIS
    valor_cofins: float = Field(0, alias="ValorCofins", ge=0)# valor do COFINS
    valor_inss: float = Field(0, alias="ValorInss", ge=0)# valor do INSS
    valor_ir: float = Field(0, alias="ValorIr", ge=0)# valor do IR
    valor_csll: float = Field(0, alias="ValorCsll", ge=0)# valor do CSLL
    iss_retido: int = Field(2, alias="IssRetido", ge=1, le=2, description="Use IssRetido (SIM=1, NAO=2)")
    valor_iss: float = Field(..., alias="ValorIss", ge=0)# valor do ISS
    valor_iss_retido: float = Field(0, alias="ValorIssRetido", ge=0)# valor do ISS retido
    outras_retencoes: float = Field(0, alias="OutrasRetencoes", ge=0)# outras retenções
    base_calculo: float = Field(..., alias="BaseCalculo", ge=0)# base de cálculo
    aliquota: float = Field(..., alias="Aliquota", ge=0, le=9.9999)# aliquota
    valor_liquido_nfse: float = Field(..., alias="ValorLiquidoNfse", ge=0)# valor líquido da NFSE
    desconto_condicionado: float = Field(0, alias="DescontoCondicionado", ge=0)
    desconto_incondicionado: float = Field(0, alias="DescontoIncondicionado", ge=0)# desconto incondicionado
    
    cstp_pis_cofins: float = Field(0, alias="CSTPisCofins", ge=0)# desconto incondicionado
    base_calculo_pis_cofins: float = Field(0, alias="BaseCalculoPisCofins", ge=0)# desconto incondicionado
    tipo_retencao_pis_cofins: float = Field(0, alias="TipoRetencaoPisCofins", ge=0)# desconto incondicionado
    
    aliq_pis: float = Field(0, alias="AliqPis", ge=0)
    aliq_cofins: float = Field(0, alias="AliqCofins", ge=0)
    
    p_tot_trib_fed: float = Field(0, alias="pTotTribFed", ge=0)
    p_tot_trib_est: float = Field(0, alias="pTotTribEst", ge=0)
    p_tot_trib_mun: float = Field(0, alias="pTotTribMun", ge=0)

class DadosServico(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    valores: Valores = Field(..., alias="Valores")# valores do serviço
    item_lista_servico: str = Field(..., alias="ItemListaServico", min_length=1, max_length=5)# item lista serviço
    codigo_cnae: int = Field(..., alias="CodigoCnae", ge=0, le=9999999)# código CNAE
    codigo_tributacao_municipio: str = Field(..., alias="CodigoTributacaoMunicipio", min_length=1, max_length=20)# código tributação municipio
    discriminacao: str = Field(..., alias="Discriminacao", min_length=1, max_length=2000)# discriminação
    codigo_municipio: int = Field(..., alias="CodigoMunicipio", ge=0, le=9999999)# código municipio


class DadosTomador(BaseModel):
    """Tomador - sem Contato."""
    model_config = ConfigDict(populate_by_name=True)

    identificacao_tomador: IdentificacaoTomador = Field(..., alias="IdentificacaoTomador")# identificacao do tomador
    razao_social: str = Field(..., alias="RazaoSocial", min_length=1, max_length=115)# razão social do tomador
    endereco: Endereco = Field(..., alias="Endereco")# endereço do tomador


class InfRps(BaseModel):
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
    servico: DadosServico = Field(..., alias="Servico")# dados do serviço
    prestador: IdentificacaoPrestador = Field(..., alias="Prestador")# identificacao do prestador
    tomador: DadosTomador = Field(..., alias="Tomador")# dados do tomador
    
    # Blocos NFS-e Nacional encapsulados
    dados_dps: Optional[DadosDPS] = Field(None, alias="DadosDPS") # prestação de serviços
    dados_obra: Optional[DadosObra] = Field(None, alias="DadosObra") # obra
    comercio_exterior: Optional[ComercioExterior] = Field(None, alias="ComercioExterior") # comércio exterior
    exigibilidade_suspensa: Optional[ExigibilidadeSuspensa] = Field(None, alias="ExigibilidadeSuspensa") # exigibilidade suspensa
    beneficio_municipal: Optional[BeneficioMunicipal] = Field(None, alias="BeneficioMunicipal") # benefício municipal
    reembolso_repasse: Optional[ReembolsoRepasse] = Field(None, alias="ReembolsoRepasse") # reembolso/repasse
    destinatario: Optional[Destinatario] = Field(None, alias="Destinatario") # destinatário
    controle_ibscbs: Optional[ControleIBSCBS] = Field(None, alias="ControleIBSCBS") # controle IBS/CBS
    ibscbs: Optional[IBSCBS] = Field(None, alias="IBSCBS") # IBS/CBS
    data_competencia: Optional[date] = Field(None, alias="DataCompetencia") # data de competência do RPS


class Rps(BaseModel):
    """Rps = InfRps + Signature (conforme reference - Signature dentro de Rps)."""
    model_config = ConfigDict(populate_by_name=True)

    inf_rps: InfRps = Field(..., alias="InfRps")# informações do RPS
    signature: Optional[Signature] = Field(None, alias="Signature")# assinatura do RPS
