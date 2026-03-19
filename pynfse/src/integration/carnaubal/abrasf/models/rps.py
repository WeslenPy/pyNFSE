from datetime import date, datetime
from typing import Optional, List, Annotated
from pydantic import Field, StringConstraints
from pynfse.src.integration.carnaubal.abrasf.models.base import (
    ABRASFNode, ABRASFTypesNode, CpfCnpj, Endereco, Contato,
    tsNumero, tsSerieRps, tsTipoRps, tsInscricaoMunicipal,
    tsRazaoSocial, tsValor, tsItemListaServico, tsCodigoCnae,
    tsCodigoTributacao, tsDiscriminacao, tsCodigoMunicipioIbge,
    tsNaturezaOperacao, tsRegimeEspecialTributacao, tsStatus12,
    tsUf, tsEmail, tsAliquota
)
from pynfse.src.common.signature import Signature

class IdentificacaoRps(ABRASFTypesNode):
    numero: tsNumero = Field(..., alias="Numero")
    serie: tsSerieRps = Field(..., alias="Serie")
    tipo: tsTipoRps = Field(..., alias="Tipo")

class IdentificacaoPrestador(ABRASFTypesNode):
    cnpj: Annotated[str, StringConstraints(min_length=14, max_length=14)] = Field(..., alias="Cnpj")
    inscricao_municipal: Optional[tsInscricaoMunicipal] = Field(None, alias="InscricaoMunicipal")

class IdentificacaoTomador(ABRASFTypesNode):
    cpf_cnpj: Optional[CpfCnpj] = Field(None, alias="CpfCnpj")
    inscricao_municipal: Optional[tsInscricaoMunicipal] = Field(None, alias="InscricaoMunicipal")

class IdentificacaoIntermediarioServico(ABRASFTypesNode):
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

class DadosConstrucaoCivil(ABRASFTypesNode):
    codigo_obra: Annotated[str, StringConstraints(max_length=15)] = Field(..., alias="CodigoObra")
    art: Annotated[str, StringConstraints(max_length=15)] = Field(..., alias="Art")

class DadosTomador(ABRASFTypesNode):
    identificacao_tomador: Optional[IdentificacaoTomador] = Field(None, alias="IdentificacaoTomador")
    razao_social: Optional[tsRazaoSocial] = Field(None, alias="RazaoSocial")
    endereco: Optional[Endereco] = Field(None, alias="Endereco")
    contato: Optional[Contato] = Field(None, alias="Contato")

class DadosPrestador(ABRASFTypesNode):
    identificacao_prestador: IdentificacaoPrestador = Field(..., alias="IdentificacaoPrestador")
    razao_social: tsRazaoSocial = Field(..., alias="RazaoSocial")
    nome_fantasia: Optional[Annotated[str, StringConstraints(max_length=60)]] = Field(None, alias="NomeFantasia")
    endereco: Endereco = Field(..., alias="Endereco")
    contato: Optional[Contato] = Field(None, alias="Contato")

class IdentificacaoOrgaoGerador(ABRASFTypesNode):
    codigo_municipio: tsCodigoMunicipioIbge = Field(..., alias="CodigoMunicipio")
    uf: tsUf = Field(..., alias="Uf")

class Valores(ABRASFTypesNode):
    valor_servicos: tsValor = Field(..., alias="ValorServicos")
    valor_deducoes: Optional[tsValor] = Field(0, alias="ValorDeducoes")
    valor_pis: Optional[tsValor] = Field(0, alias="ValorPis")
    valor_cofins: Optional[tsValor] = Field(0, alias="ValorCofins")
    valor_inss: Optional[tsValor] = Field(0, alias="ValorInss")
    valor_ir: Optional[tsValor] = Field(0, alias="ValorIr")
    valor_csll: Optional[tsValor] = Field(0, alias="ValorCsll")
    iss_retido: tsStatus12 = Field(2, alias="IssRetido")
    valor_iss: Optional[tsValor] = Field(None, alias="ValorIss")
    valor_iss_retido: Optional[tsValor] = Field(0, alias="ValorIssRetido")
    outras_retencoes: Optional[tsValor] = Field(0, alias="OutrasRetencoes")
    base_calculo: Optional[tsValor] = Field(None, alias="BaseCalculo")
    aliquota: Optional[tsAliquota] = Field(None, alias="Aliquota")
    valor_liquido_nfse: Optional[tsValor] = Field(None, alias="ValorLiquidoNfse")
    desconto_condicionado: Optional[tsValor] = Field(0, alias="DescontoCondicionado")
    desconto_incondicionado: Optional[tsValor] = Field(0, alias="DescontoIncondicionado")
    cst_pis_cofins: Optional[Annotated[str, StringConstraints(max_length=10)]] = Field(None, alias="CSTPisCofins")
    base_calculo_pis_cofins: Optional[tsValor] = Field(None, alias="BaseCalculoPisCofins")
    tipo_retencao_pis_cofins: Optional[int] = Field(None, alias="TipoRetencaoPisCofins")

class DadosServico(ABRASFTypesNode):
    valores: Valores = Field(..., alias="Valores")
    item_lista_servico: tsItemListaServico = Field(..., alias="ItemListaServico")
    codigo_cnae: Optional[tsCodigoCnae] = Field(None, alias="CodigoCnae")
    codigo_tributacao_municipio: Optional[tsCodigoTributacao] = Field(None, alias="CodigoTributacaoMunicipio")
    discriminacao: tsDiscriminacao = Field(..., alias="Discriminacao")
    codigo_municipio: tsCodigoMunicipioIbge = Field(..., alias="CodigoMunicipio")

# Blocos NFS-e Nacional encapsulados
class DadosDPS(ABRASFTypesNode):
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

class EnderecoObra(ABRASFTypesNode):
    cep: Optional[Annotated[str, StringConstraints(max_length=10)]] = Field(None, alias="Cep")
    logradouro: Optional[Annotated[str, StringConstraints(max_length=125)]] = Field(None, alias="Logradouro")
    numero: Optional[Annotated[str, StringConstraints(max_length=10)]] = Field(None, alias="Numero")
    complemento: Optional[Annotated[str, StringConstraints(max_length=60)]] = Field(None, alias="Complemento")
    bairro: Optional[Annotated[str, StringConstraints(max_length=60)]] = Field(None, alias="Bairro")

class DadosObra(ABRASFTypesNode):
    codigo_obra: Optional[Annotated[str, StringConstraints(max_length=30)]] = Field(None, alias="CodigoObra")
    insc_imob_fisc: Optional[Annotated[str, StringConstraints(max_length=30)]] = Field(None, alias="InscImobFisc")
    endereco_obra: Optional[EnderecoObra] = Field(None, alias="EnderecoObra")

class ComercioExterior(ABRASFTypesNode):
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

class ExigibilidadeSuspensa(ABRASFTypesNode):
    tp_susp: Optional[int] = Field(None, alias="TpSusp")
    n_processo: Optional[Annotated[str, StringConstraints(max_length=30)]] = Field(None, alias="NProcesso")

class BeneficioMunicipal(ABRASFTypesNode):
    tp_bm: Optional[int] = Field(None, alias="TpBM")
    nbm: Optional[Annotated[str, StringConstraints(max_length=14)]] = Field(None, alias="NBM")
    v_red_bcbm: Optional[tsValor] = Field(None, alias="VRedBCBM")
    p_red_bcbm: Optional[tsValor] = Field(None, alias="PRedBCBM")

class ReembolsoRepasse(ABRASFTypesNode):
    tp_reemb_rep_res: Optional[int] = Field(None, alias="TpReembRepRes")
    x_tp_reemb_rep_res: Optional[Annotated[str, StringConstraints(max_length=2000)]] = Field(None, alias="XTpReembRepRes")
    v_reemb_rep_res: Optional[tsValor] = Field(None, alias="VReembRepRes")

class Destinatario(ABRASFTypesNode):
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

class ControleIBSCBS(ABRASFTypesNode):
    fin_nfse: Optional[int] = Field(None, alias="FinNFSe")
    ind_final: Optional[int] = Field(None, alias="IndFinal")
    tp_oper: Optional[int] = Field(None, alias="TpOper")
    tp_ente_gov: Optional[int] = Field(None, alias="TpEnteGov")
    ind_dest: Optional[int] = Field(None, alias="IndDest")
    c_ind_op: Optional[Annotated[str, StringConstraints(max_length=6)]] = Field(None, alias="CIndOp")
    x_tp_ente_gov: Optional[Annotated[str, StringConstraints(max_length=2000)]] = Field(None, alias="XTpEnteGov")

from typing import Optional, Annotated
from pydantic import Field, model_validator
from decimal import Decimal


class IBSCBS(ABRASFTypesNode):
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

    @model_validator(mode="after")
    def calcular_campos(self):
        base = self.ibscbs_base_calculo or Decimal(0)

        def calc_aliquota_efetiva(aliq, red):
            if aliq is None:
                return None
            red = red or Decimal(0)
            return aliq * (Decimal(1) - red)

        def calc_valor(base, aliq_efetiva):
            if base is None or aliq_efetiva is None:
                return None
            return base * aliq_efetiva

        def calc_diferido(valor, perc):
            if valor is None or perc is None:
                return None
            return valor * perc

        # ALÍQUOTAS EFETIVAS 
        if self.ibsu_f_aliquota_efetiva is None:
            self.ibsu_f_aliquota_efetiva = calc_aliquota_efetiva(
                self.ibsu_f_aliquota, self.ibsu_f_perc_reducao
            )

        if self.ibs_mun_aliquota_efetiva is None:
            self.ibs_mun_aliquota_efetiva = calc_aliquota_efetiva(
                self.ib_mun_aliquota, self.ibs_mun_perc_reducao
            )

        if self.cbs_aliquota_efetiva is None:
            self.cbs_aliquota_efetiva = calc_aliquota_efetiva(
                self.cbs_aliquota, self.cbs_perc_reducao
            )

        # VALORES 
        if self.ibsu_f_valor is None:
            self.ibsu_f_valor = calc_valor(base, self.ibsu_f_aliquota_efetiva)

        if self.ibs_mun_valor is None:
            self.ibs_mun_valor = calc_valor(base, self.ibs_mun_aliquota_efetiva)

        if self.cbs_valor is None:
            self.cbs_valor = calc_valor(base, self.cbs_aliquota_efetiva)

        #DIFERIDOS
        if self.ibsu_f_valor_diferido is None:
            self.ibsu_f_valor_diferido = calc_diferido(
                self.ibsu_f_valor, self.ibsu_f_perc_diferimento
            )

        if self.ibs_mun_valor_diferido is None:
            self.ibs_mun_valor_diferido = calc_diferido(
                self.ibs_mun_valor, self.ibs_mun_perc_diferimento
            )

        if self.cbs_valor_diferido is None:
            self.cbs_valor_diferido = calc_diferido(
                self.cbs_valor, self.cbs_perc_diferimento
            )

        #TOTAL IBS
        if self.ibs_valor_total is None:
            self.ibs_valor_total = (self.ibsu_f_valor or 0) + (self.ibs_mun_valor or 0)

        # TOTAL COM TRIBUTOS
        if self.valor_total_com_tributos is None:
            self.valor_total_com_tributos = (
                base
                + (self.ibs_valor_total or 0)
                + (self.cbs_valor or 0)
            )

        return self

class InfRps(ABRASFTypesNode):
    id: Optional[Annotated[str, StringConstraints(max_length=255)]] = Field(None, alias="Id")
    identificacao_rps: IdentificacaoRps = Field(..., alias="IdentificacaoRps")
    data_emissao: datetime = Field(..., alias="DataEmissao")
    natureza_operacao: tsNaturezaOperacao = Field(..., alias="NaturezaOperacao")
    regime_especial_tributacao: Optional[tsRegimeEspecialTributacao] = Field(None, alias="RegimeEspecialTributacao")
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
    data_competencia: Optional[date] = Field(None, alias="DataCompetencia")

class Rps(ABRASFTypesNode):
    inf_rps: InfRps = Field(..., alias="InfRps")
    signature: Optional[Signature] = Field(
        None,
        alias="Signature",
        json_schema_extra={
            "xml_namespace": None,
            "xml_child_namespace": None,
            "xml_reset_default_namespace": False,
        },
    )
