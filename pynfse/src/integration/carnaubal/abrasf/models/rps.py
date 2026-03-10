from datetime import datetime
from typing import Optional, List, Annotated
from pydantic import Field, StringConstraints
from pynfse.src.integration.carnaubal.abrasf.models.base import (
    ABRASFNode, CpfCnpj, Endereco, Contato,
    tsNumero, tsSerieRps, tsTipoRps, tsInscricaoMunicipal,
    tsRazaoSocial, tsValor, tsItemListaServico, tsCodigoCnae,
    tsCodigoTributacao, tsDiscriminacao, tsCodigoMunicipioIbge,
    tsNaturezaOperacao, tsRegimeEspecialTributacao, tsStatus12,
    tsUf, tsEmail
)
from pynfse.src.common.signature import Signature

class IdentificacaoRps(ABRASFNode):
    numero: tsNumero = Field(..., alias="Numero")
    serie: tsSerieRps = Field(..., alias="Serie")
    tipo: tsTipoRps = Field(..., alias="Tipo")

class IdentificacaoPrestador(ABRASFNode):
    cnpj: Annotated[str, StringConstraints(min_length=14, max_length=14)] = Field(..., alias="Cnpj")
    inscricao_municipal: Optional[tsInscricaoMunicipal] = Field(None, alias="InscricaoMunicipal")

class IdentificacaoTomador(ABRASFNode):
    cpf_cnpj: Optional[CpfCnpj] = Field(None, alias="CpfCnpj")
    inscricao_municipal: Optional[tsInscricaoMunicipal] = Field(None, alias="InscricaoMunicipal")

class IdentificacaoIntermediarioServico(ABRASFNode):
    razao_social: tsRazaoSocial = Field(..., alias="RazaoSocial")
    cpf_cnpj: CpfCnpj = Field(..., alias="CpfCnpj")
    inscricao_municipal: Optional[tsInscricaoMunicipal] = Field(None, alias="InscricaoMunicipal")
    tipo_logradouro: Optional[Annotated[str, StringConstraints(max_length=10)]] = Field(None, alias="TipoLogradouro")
    endereco: Optional[Annotated[str, StringConstraints(max_length=125)]] = Field(None, alias="Endereco")
    numero: Optional[Annotated[str, StringConstraints(max_length=10)]] = Field(None, alias="Numero")
    complemento: Optional[Annotated[str, StringConstraints(max_length=60)]] = Field(None, alias="Complemento")
    bairro: Optional[Annotated[str, StringConstraints(max_length=60)]] = Field(None, alias="Bairro")
    codigo_municipio: Optional[tsCodigoMunicipioIbge] = Field(None, alias="CodigoMunicipio")
    uf: Optional[tsUf] = Field(None, alias="UF")
    cep: Optional[Annotated[str, StringConstraints(max_length=10)]] = Field(None, alias="CEP")
    email: Optional[Annotated[str, StringConstraints(max_length=120)]] = Field(None, alias="Email")
    nif: Optional[Annotated[str, StringConstraints(max_length=40)]] = Field(None, alias="NIF")

class DadosConstrucaoCivil(ABRASFNode):
    codigo_obra: Annotated[str, StringConstraints(max_length=15)] = Field(..., alias="CodigoObra")
    art: Annotated[str, StringConstraints(max_length=15)] = Field(..., alias="Art")

class DadosTomador(ABRASFNode):
    identificacao_tomador: Optional[IdentificacaoTomador] = Field(None, alias="IdentificacaoTomador")
    razao_social: Optional[tsRazaoSocial] = Field(None, alias="RazaoSocial")
    endereco: Optional[Endereco] = Field(None, alias="Endereco")
    contato: Optional[Contato] = Field(None, alias="Contato")

class Valores(ABRASFNode):
    valor_servicos: tsValor = Field(..., alias="ValorServicos")
    valor_deducoes: Optional[tsValor] = Field(None, alias="ValorDeducoes")
    valor_pis: Optional[tsValor] = Field(None, alias="ValorPis")
    valor_cofins: Optional[tsValor] = Field(None, alias="ValorCofins")
    valor_inss: Optional[tsValor] = Field(None, alias="ValorInss")
    valor_ir: Optional[tsValor] = Field(None, alias="ValorIr")
    valor_csll: Optional[tsValor] = Field(None, alias="ValorCsll")
    iss_retido: tsStatus12 = Field(..., alias="IssRetido")
    valor_iss: Optional[tsValor] = Field(None, alias="ValorIss")
    valor_iss_retido: Optional[tsValor] = Field(None, alias="ValorIssRetido")
    outras_retencoes: Optional[tsValor] = Field(None, alias="OutrasRetencoes")
    base_calculo: Optional[tsValor] = Field(None, alias="BaseCalculo")
    aliquota: Optional[Annotated[float, Field(ge=0, le=1)]] = Field(None, alias="Aliquota")
    valor_liquido_nfse: Optional[tsValor] = Field(None, alias="ValorLiquidoNfse")
    desconto_condicionado: Optional[tsValor] = Field(None, alias="DescontoCondicionado")
    desconto_incondicionado: Optional[tsValor] = Field(None, alias="DescontoIncondicionado")
    cst_pis_cofins: Optional[Annotated[str, StringConstraints(max_length=10)]] = Field(None, alias="CSTPisCofins")
    base_calculo_pis_cofins: Optional[tsValor] = Field(None, alias="BaseCalculoPisCofins")
    tipo_retencao_pis_cofins: Optional[int] = Field(None, alias="TipoRetencaoPisCofins")

class DadosServico(ABRASFNode):
    valores: Valores = Field(..., alias="Valores")
    item_lista_servico: tsItemListaServico = Field(..., alias="ItemListaServico")
    codigo_cnae: Optional[tsCodigoCnae] = Field(None, alias="CodigoCnae")
    codigo_tributacao_municipio: Optional[tsCodigoTributacao] = Field(None, alias="CodigoTributacaoMunicipio")
    discriminacao: tsDiscriminacao = Field(..., alias="Discriminacao")
    codigo_municipio: tsCodigoMunicipioIbge = Field(..., alias="CodigoMunicipio")

# Blocos NFS-e Nacional encapsulados
class DadosDPS(ABRASFNode):
    tp_emit: Optional[Annotated[str, StringConstraints(max_length=1)]] = Field(None, alias="TpEmit")
    tp_amb: Optional[int] = Field(None, alias="TpAmb")
    dh_emi: Optional[datetime] = Field(None, alias="DhEmi")
    ver_aplic: Optional[Annotated[str, StringConstraints(max_length=20)]] = Field(None, alias="VerAplic")
    cloc_emi: Optional[int] = Field(None, alias="CLocEmi")
    cloc_prestacao: Optional[int] = Field(None, alias="CLocPrestacao")
    ctrib_nac: Optional[Annotated[str, StringConstraints(max_length=6)]] = Field(None, alias="CTribNac")
    trib_issqn: Optional[int] = Field(None, alias="TribIssqn")
    tp_ret_issqn: Optional[int] = Field(None, alias="TpRetIssqn")
    op_simp_nac: Optional[Annotated[str, StringConstraints(max_length=1)]] = Field(None, alias="OpSimpNac")
    reg_esp_trib: Optional[Annotated[str, StringConstraints(max_length=10)]] = Field(None, alias="RegEspTrib")
    reg_ap_trib_sn: Optional[Annotated[str, StringConstraints(max_length=1)]] = Field(None, alias="RegApTribSN")

class EnderecoObra(ABRASFNode):
    cep: Optional[Annotated[str, StringConstraints(max_length=10)]] = Field(None, alias="Cep")
    logradouro: Optional[Annotated[str, StringConstraints(max_length=125)]] = Field(None, alias="Logradouro")
    numero: Optional[Annotated[str, StringConstraints(max_length=10)]] = Field(None, alias="Numero")
    complemento: Optional[Annotated[str, StringConstraints(max_length=60)]] = Field(None, alias="Complemento")
    bairro: Optional[Annotated[str, StringConstraints(max_length=60)]] = Field(None, alias="Bairro")

class DadosObra(ABRASFNode):
    codigo_obra: Optional[Annotated[str, StringConstraints(max_length=30)]] = Field(None, alias="CodigoObra")
    insc_imob_fisc: Optional[Annotated[str, StringConstraints(max_length=30)]] = Field(None, alias="InscImobFisc")
    endereco_obra: Optional[EnderecoObra] = Field(None, alias="EnderecoObra")

class ComercioExterior(ABRASFNode):
    md_prestacao: Optional[int] = Field(None, alias="MdPrestacao")
    vinc_prest: Optional[int] = Field(None, alias="VincPrest")
    tp_moeda: Optional[int] = Field(None, alias="TpMoeda")
    v_serv_moeda: Optional[tsValor] = Field(None, alias="VServMoeda")
    mec_af_comex_p: Optional[Annotated[str, StringConstraints(max_length=10)]] = Field(None, alias="MecAFComexP")
    mec_af_comex_t: Optional[Annotated[str, StringConstraints(max_length=10)]] = Field(None, alias="MecAFComexT")
    mov_temp_bens: Optional[int] = Field(None, alias="MovTempBens")
    ndi: Optional[Annotated[str, StringConstraints(max_length=12)]] = Field(None, alias="NDI")
    nre: Optional[Annotated[str, StringConstraints(max_length=12)]] = Field(None, alias="NRE")
    mdic: Optional[int] = Field(None, alias="MDIC")
    c_pais_result: Optional[Annotated[str, StringConstraints(max_length=4)]] = Field(None, alias="CPaisResult")

class ExigibilidadeSuspensa(ABRASFNode):
    tp_susp: Optional[int] = Field(None, alias="TpSusp")
    n_processo: Optional[Annotated[str, StringConstraints(max_length=30)]] = Field(None, alias="NProcesso")

class BeneficioMunicipal(ABRASFNode):
    tp_bm: Optional[int] = Field(None, alias="TpBM")
    nbm: Optional[Annotated[str, StringConstraints(max_length=14)]] = Field(None, alias="NBM")
    v_red_bcbm: Optional[tsValor] = Field(None, alias="VRedBCBM")
    p_red_bcbm: Optional[tsValor] = Field(None, alias="PRedBCBM")

class ReembolsoRepasse(ABRASFNode):
    tp_reemb_rep_res: Optional[int] = Field(None, alias="TpReembRepRes")
    x_tp_reemb_rep_res: Optional[Annotated[str, StringConstraints(max_length=2000)]] = Field(None, alias="XTpReembRepRes")
    v_reemb_rep_res: Optional[tsValor] = Field(None, alias="VReembRepRes")

class Destinatario(ABRASFNode):
    cnpj_cpf: Optional[Annotated[str, StringConstraints(min_length=11, max_length=14)]] = Field(None, alias="CnpjCpf")
    nome: Optional[tsRazaoSocial] = Field(None, alias="Nome")
    logradouro: Optional[Annotated[str, StringConstraints(max_length=125)]] = Field(None, alias="Logradouro")
    numero: Optional[Annotated[str, StringConstraints(max_length=10)]] = Field(None, alias="Numero")
    complemento: Optional[Annotated[str, StringConstraints(max_length=60)]] = Field(None, alias="Complemento")
    bairro: Optional[Annotated[str, StringConstraints(max_length=60)]] = Field(None, alias="Bairro")
    cidade: Optional[Annotated[str, StringConstraints(max_length=60)]] = Field(None, alias="Cidade")
    uf: Optional[tsUf] = Field(None, alias="UF")
    cep: Optional[Annotated[str, StringConstraints(max_length=10)]] = Field(None, alias="CEP")
    cod_municipio: Optional[tsCodigoMunicipioIbge] = Field(None, alias="CodMunicipio")
    cod_pais: Optional[Annotated[str, StringConstraints(max_length=4)]] = Field(None, alias="CodPais")
    cod_postal_ext: Optional[Annotated[str, StringConstraints(max_length=10)]] = Field(None, alias="CodPostalExt")
    nif: Optional[Annotated[str, StringConstraints(max_length=40)]] = Field(None, alias="NIF")
    email: Optional[Annotated[str, StringConstraints(max_length=120)]] = Field(None, alias="Email")
    telefone: Optional[Annotated[str, StringConstraints(max_length=20)]] = Field(None, alias="Telefone")

class ControleIBSCBS(ABRASFNode):
    fin_nfse: Optional[int] = Field(None, alias="FinNFSe")
    ind_final: Optional[int] = Field(None, alias="IndFinal")
    tp_oper: Optional[int] = Field(None, alias="TpOper")
    tp_ente_gov: Optional[int] = Field(None, alias="TpEnteGov")
    ind_dest: Optional[int] = Field(None, alias="IndDest")
    c_ind_op: Optional[Annotated[str, StringConstraints(max_length=6)]] = Field(None, alias="CIndOp")
    x_tp_ente_gov: Optional[Annotated[str, StringConstraints(max_length=2000)]] = Field(None, alias="XTpEnteGov")

class IBSCBS(ABRASFNode):
    ibscbs_base_calculo: Optional[tsValor] = Field(None, alias="IBSCBSBaseCalculo")
    ibsu_f_aliquota: Optional[tsValor] = Field(None, alias="IBSUFAliquota")
    ib_mun_aliquota: Optional[tsValor] = Field(None, alias="IBSMunAliquota")
    cbs_aliquota: Optional[tsValor] = Field(None, alias="CBSAliquota")
    ibsu_f_valor: Optional[tsValor] = Field(None, alias="IBSUFValor")
    ibs_mun_valor: Optional[tsValor] = Field(None, alias="IBSMunValor")
    cbs_valor: Optional[tsValor] = Field(None, alias="CBSValor")
    ibsu_f_perc_reducao: Optional[tsValor] = Field(None, alias="IBSUFPercReducao")
    ibs_mun_perc_reducao: Optional[tsValor] = Field(None, alias="IBSMunPercReducao")
    cbs_perc_reducao: Optional[tsValor] = Field(None, alias="CBSPercReducao")
    ibsu_f_aliquota_efetiva: Optional[tsValor] = Field(None, alias="IBSUFAliquotaEfetiva")
    ibs_mun_aliquota_efetiva: Optional[tsValor] = Field(None, alias="IBSMunAliquotaEfetiva")
    cbs_aliquota_efetiva: Optional[tsValor] = Field(None, alias="CBSAliquotaEfetiva")
    ibsu_f_perc_diferimento: Optional[tsValor] = Field(None, alias="IBSUFPercDiferimento")
    ibs_mun_perc_diferimento: Optional[tsValor] = Field(None, alias="IBSMunPercDiferimento")
    cbs_perc_diferimento: Optional[tsValor] = Field(None, alias="CBSPercDiferimento")
    ibsu_f_valor_diferido: Optional[tsValor] = Field(None, alias="IBSUFValorDiferido")
    ibs_mun_valor_diferido: Optional[tsValor] = Field(None, alias="IBSMunValorDiferido")
    cbs_valor_diferido: Optional[tsValor] = Field(None, alias="CBSValorDiferido")
    ibs_credito_presumido_aliq: Optional[tsValor] = Field(None, alias="IBSCreditoPresumidoAliq")
    ibs_credito_presumido_valor: Optional[tsValor] = Field(None, alias="IBSCreditoPresumidoValor")
    cbs_credito_presumido_aliq: Optional[tsValor] = Field(None, alias="CBSCreditoPresumidoAliq")
    cbs_credito_presumido_valor: Optional[tsValor] = Field(None, alias="CBSCreditoPresumidoValor")
    ibs_valor_total: Optional[tsValor] = Field(None, alias="IBSValorTotal")
    valor_total_com_tributos: Optional[tsValor] = Field(None, alias="ValorTotalComTributos")
    ibs_valor_reembolso: Optional[tsValor] = Field(None, alias="IBSValorReembolso")
    localidade_incidencia_cod: Optional[tsCodigoMunicipioIbge] = Field(None, alias="LocalidadeIncidenciaCod")
    localidade_incidencia_nome: Optional[Annotated[str, StringConstraints(max_length=2000)]] = Field(None, alias="LocalidadeIncidenciaNome")
    perc_redutor_compra_gov: Optional[tsValor] = Field(None, alias="PercRedutorCompraGov")

class InfRps(ABRASFNode):
    id: Optional[Annotated[str, StringConstraints(max_length=255)]] = Field(None, alias="Id")
    identificacao_rps: IdentificacaoRps = Field(..., alias="IdentificacaoRps")
    data_emissao: datetime = Field(..., alias="DataEmissao")
    natureza_operacao: tsNaturezaOperacao = Field(..., alias="NaturezaOperacao")
    regime_special_tributation: Optional[tsRegimeEspecialTributacao] = Field(None, alias="RegimeEspecialTributacao")
    optante_simples_national: tsStatus12 = Field(..., alias="OptanteSimplesNacional")
    incentivador_cultural: tsStatus12 = Field(..., alias="IncentivadorCultural")
    status: tsStatus12 = Field(..., alias="Status")
    rps_substituido: Optional[IdentificacaoRps] = Field(None, alias="RpsSubstituido")
    servico: DadosServico = Field(..., alias="Servico")
    prestador: IdentificacaoPrestador = Field(..., alias="Prestador")
    tomador: DadosTomador = Field(..., alias="Tomador")
    intermediario_servico: Optional[IdentificacaoIntermediarioServico] = Field(None, alias="IntermediarioServico")
    construcao_civil: Optional[DadosConstrucaoCivil] = Field(None, alias="ConstrucaoCivil")

    # Blocos NFS-e Nacional encapsulados
    dados_dps: Optional[DadosDPS] = Field(None, alias="DadosDPS")
    dados_obra: Optional[DadosObra] = Field(None, alias="DadosObra")
    comercio_exterior: Optional[ComercioExterior] = Field(None, alias="ComercioExterior")
    exigibilidade_suspensa: Optional[ExigibilidadeSuspensa] = Field(None, alias="ExigibilidadeSuspensa")
    beneficio_municipal: Optional[BeneficioMunicipal] = Field(None, alias="BeneficioMunicipal")
    reembolso_repasse: Optional[ReembolsoRepasse] = Field(None, alias="ReembolsoRepasse")
    destinatario: Optional[Destinatario] = Field(None, alias="Destinatario")
    controle_ibscbs: Optional[ControleIBSCBS] = Field(None, alias="ControleIBSCBS")
    ibscbs: Optional[IBSCBS] = Field(None, alias="IBSCBS")
    data_competencia: Optional[datetime] = Field(None, alias="DataCompetencia")

class Rps(ABRASFNode):
    inf_rps: InfRps = Field(..., alias="InfRps")
    signature: Optional[Signature] = Field(None, alias="Signature")
