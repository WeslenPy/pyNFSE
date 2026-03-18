"""
Modelos RPS para SpeedGov - estrutura enviar_lote_rps.xml.
Inclui blocos opcionais NFS-e Nacional (DadosDPS, DadosObra, ComercioExterior, etc).
"""
from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from pynfse.src.integration.carnaubal.speedgov.models.base import CpfCnpj, Endereco
from pynfse.src.common.signature import Signature


# --- Blocos NFS-e Nacional encapsulados ---


class DadosDPS(BaseModel):
    """Dados da Declaração de Prestação de Serviços - NFS-e Nacional."""
    model_config = ConfigDict(populate_by_name=True)

    tp_emit: Optional[str] = Field(None, alias="TpEmit", max_length=1)# tipo de emissão
    tp_amb: Optional[int] = Field(None, alias="TpAmb")# tipo de ambiente
    dh_emi: Optional[datetime] = Field(None, alias="DhEmi")# data e hora de emissão
    ver_aplic: Optional[str] = Field(None, alias="VerAplic", max_length=20)# versão do aplicativo
    cloc_emi: Optional[int] = Field(None, alias="CLocEmi")# código do local de emissão
    cloc_prestacao: Optional[int] = Field(None, alias="CLocPrestacao")# código do local de prestação
    ctrib_nac: Optional[str] = Field(None, alias="CTribNac", max_length=6)# código tributação nacional
    trib_issqn: Optional[int] = Field(None, alias="TribIssqn")# tributação ISSQN
    tp_ret_issqn: Optional[int] = Field(None, alias="TpRetIssqn")# tipo de retenção ISSQN
    op_simp_nac: Optional[str] = Field(None, alias="OpSimpNac", max_length=1)# operação simples nacional
    reg_esp_trib: Optional[str] = Field(None, alias="RegEspTrib", max_length=10)# regime especial de tributação
    reg_ap_trib_sn: Optional[str] = Field(None, alias="RegApTribSN", max_length=1)# regime apuracional de tributação SN


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

    md_prestacao: Optional[int] = Field(None, alias="MdPrestacao")# modalidade de prestação
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
    """Exigibilidade suspensa - NFS-e Nacional."""
    model_config = ConfigDict(populate_by_name=True)

    tp_susp: Optional[int] = Field(None, alias="TpSusp")# tipo de suspensão
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
    """Controle IBS/CBS - NFS-e Nacional."""
    model_config = ConfigDict(populate_by_name=True)

    fin_nfse: Optional[int] = Field(None, alias="FinNFSe")# finalidade da NFSE
    ind_final: Optional[int] = Field(None, alias="IndFinal")# indicador final
    tp_oper: Optional[int] = Field(None, alias="TpOper")# tipo de operação
    tp_ente_gov: Optional[int] = Field(None, alias="TpEnteGov")# tipo de ente governamental
    ind_dest: Optional[int] = Field(None, alias="IndDest")# indicador de destino
    c_ind_op: Optional[str] = Field(None, alias="CIndOp", max_length=6)# código do indicador de operação
    x_tp_ente_gov: Optional[str] = Field(None, alias="XTpEnteGov", max_length=2000)# descrição do tipo de ente governamental


class IBSCBS(BaseModel):
    """IBS/CBS - NFS-e Nacional."""
    model_config = ConfigDict(populate_by_name=True)

    ibscbs_base_calculo: Optional[float] = Field(None, alias="IBSCBSBaseCalculo")# base de cálculo do IBS/CBS
    ibsu_f_aliquota: Optional[float] = Field(None, alias="IBSUFAliquota")# aliquota do IBS/CBS
    ib_mun_aliquota: Optional[float] = Field(None, alias="IBSMunAliquota")# aliquota do IBS/CBS
    cbs_aliquota: Optional[float] = Field(None, alias="CBSAliquota")# aliquota do CBS
    ibsu_f_valor: Optional[float] = Field(None, alias="IBSUFValor")# valor do IBS/CBS
    ibs_mun_valor: Optional[float] = Field(None, alias="IBSMunValor")# valor do IBS/CBS
    cbs_valor: Optional[float] = Field(None, alias="CBSValor")# valor do CBS
    ibsu_f_perc_reducao: Optional[float] = Field(None, alias="IBSUFPercReducao")# percentual de redução do IBS/CBS
    ibs_mun_perc_reducao: Optional[float] = Field(None, alias="IBSMunPercReducao")# percentual de redução do IBS/CBS
    cbs_perc_reducao: Optional[float] = Field(None, alias="CBSPercReducao")# percentual de redução do CBS
    ibsu_f_aliquota_efetiva: Optional[float] = Field(None, alias="IBSUFAliquotaEfetiva")# aliquota efetiva do IBS/CBS
    ibs_mun_aliquota_efetiva: Optional[float] = Field(None, alias="IBSMunAliquotaEfetiva")# aliquota efetiva do IBS/CBS
    cbs_aliquota_efetiva: Optional[float] = Field(None, alias="CBSAliquotaEfetiva")# aliquota efetiva do CBS
    ibsu_f_perc_diferimento: Optional[float] = Field(None, alias="IBSUFPercDiferimento")# percentual de diferimento do IBS/CBS
    ibs_mun_perc_diferimento: Optional[float] = Field(None, alias="IBSMunPercDiferimento")# percentual de diferimento do IBS/CBS
    cbs_perc_diferimento: Optional[float] = Field(None, alias="CBSPercDiferimento")# percentual de diferimento do CBS
    ibsu_f_valor_diferido: Optional[float] = Field(None, alias="IBSUFValorDiferido")# valor diferido do IBS/CBS
    ibs_mun_valor_diferido: Optional[float] = Field(None, alias="IBSMunValorDiferido")# valor diferido do IBS/CBS
    cbs_valor_diferido: Optional[float] = Field(None, alias="CBSValorDiferido")# valor diferido do CBS
    ibs_credito_presumido_aliq: Optional[float] = Field(None, alias="IBSCreditoPresumidoAliq")# crédito presumido do IBS/CBS
    ibs_credito_presumido_valor: Optional[float] = Field(None, alias="IBSCreditoPresumidoValor")# crédito presumido do IBS/CBS
    cbs_credito_presumido_aliq: Optional[float] = Field(None, alias="CBSCreditoPresumidoAliq")# crédito presumido do CBS
    cbs_credito_presumido_valor: Optional[float] = Field(None, alias="CBSCreditoPresumidoValor")# crédito presumido do CBS
    ibs_valor_total: Optional[float] = Field(None, alias="IBSValorTotal")# valor total do IBS/CBS
    valor_total_com_tributos: Optional[float] = Field(None, alias="ValorTotalComTributos")# valor total com tributos do IBS/CBS
    ibs_valor_reembolso: Optional[float] = Field(None, alias="IBSValorReembolso")# valor do reembolso do IBS/CBS
    localidade_incidencia_cod: Optional[int] = Field(None, alias="LocalidadeIncidenciaCod")# código da localidade de incidência do IBS/CBS
    localidade_incidencia_nome: Optional[str] = Field(None, alias="LocalidadeIncidenciaNome", max_length=2000)# nome da localidade de incidência do IBS/CBS
    perc_redutor_compra_gov: Optional[float] = Field(None, alias="PercRedutorCompraGov")# percentual de redutor de compra governamental do IBS/CBS


class IdentificacaoRps(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    numero: int = Field(..., alias="Numero", ge=0)# número do RPS
    serie: str = Field(..., alias="Serie", min_length=1, max_length=5)# série do RPS
    tipo: int = Field(..., alias="Tipo", ge=1, le=3)# tipo do RPS


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
    iss_retido: int = Field(2, alias="IssRetido", ge=1, le=2)# ISS retido
    valor_iss: float = Field(..., alias="ValorIss", ge=0)# valor do ISS
    valor_iss_retido: float = Field(0, alias="ValorIssRetido", ge=0)# valor do ISS retido
    outras_retencoes: float = Field(0, alias="OutrasRetencoes", ge=0)# outras retenções
    base_calculo: float = Field(..., alias="BaseCalculo", ge=0)# base de cálculo
    aliquota: float = Field(..., alias="Aliquota", ge=0, le=9.9999)# aliquota
    valor_liquido_nfse: float = Field(..., alias="ValorLiquidoNfse", ge=0)# valor líquido da NFSE
    desconto_condicionado: float = Field(0, alias="DescontoCondicionado", ge=0)
    desconto_incondicionado: float = Field(0, alias="DescontoIncondicionado", ge=0)# desconto incondicionado


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
    """InfRps - campos base + blocos opcionais NFS-e Nacional."""
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[str] = Field("", alias="Id")# id do RPS
    identificacao_rps: IdentificacaoRps = Field(..., alias="IdentificacaoRps")# identificacao do RPS
    data_emissao: datetime = Field(..., alias="DataEmissao")# data de emissão do RPS
    natureza_operacao: int = Field(1, alias="NaturezaOperacao", ge=1, le=6)# natureza da operação
    regime_especial_tributacao: int = Field(..., alias="RegimeEspecialTributacao", ge=1, le=6)# regime especial de tributação
    optante_simples_nacional: int = Field(..., alias="OptanteSimplesNacional", ge=1, le=2)# optante simples nacional
    incentivador_cultural: int = Field(2, alias="IncentivadorCultural", ge=1, le=2)# incentivador cultural
    status: int = Field(1, alias="Status", ge=1, le=2)# status do RPS
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
