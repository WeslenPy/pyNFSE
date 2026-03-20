"""
Funções de construção de XML para SpeedGov (enviar_lote_rps.xml).
Gera estrutura com prefixos p:/p1:.
"""
from datetime import date, datetime
from typing import List, Optional

from lxml import etree

from pynfse.src.common.signature import Signature
from pynfse.src.integration.carnaubal.speedgov.models.rps import Rps
from pynfse.src.integration.carnaubal.speedgov.models.lote import LoteRps

ENVIO_NS = "http://ws.speedgov.com.br/enviar_lote_rps_envio_v1.xsd"
TIPOS_NS = "http://ws.speedgov.com.br/tipos_v1.xsd"
CABECALHO_NS = "http://ws.speedgov.com.br/cabecalho_v1.xsd"
XMLDSIG_NS = "http://www.w3.org/2000/09/xmldsig#"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"


def _format_value(v) -> str:
    from enum import Enum

    if isinstance(v, datetime):
        return v.strftime("%Y-%m-%dT%H:%M:%S")
    if isinstance(v, date):
        return v.isoformat()
    if isinstance(v, Enum):
        return str(v.value)
    return str(v)


def _elem(parent, tag: str, text=None, ns: str = TIPOS_NS, ns_prefix: str = "p1"):
    """Cria filho com namespace."""
    full_tag = f"{{{ns}}}{tag}" if ns else tag
    child = etree.SubElement(parent, full_tag)
    if text is not None:
        child.text = _format_value(text)
    return child


def _add_opt(parent, tag: str, value, ns: str = TIPOS_NS) -> None:
    """Adiciona elemento filho somente se value não for None."""
    if value is not None:
        _elem(parent, tag, value, ns=ns)


def _build_optional_block(parent, obj, block_tag: str, fields: list) -> None:
    """Monta bloco opcional: só adiciona se obj tiver ao menos um campo preenchido."""
    if obj is None:
        return
    has_any = any(getattr(obj, attr, None) is not None for attr, _ in fields)
    if not has_any:
        return
    block = etree.SubElement(parent, f"{{{TIPOS_NS}}}{block_tag}")
    for attr, xml_tag in fields:
        val = getattr(obj, attr, None)
        _add_opt(block, xml_tag, val)


def _build_endereco_obra(parent, endereco) -> None:
    """Monta p1:EnderecoObra."""
    if endereco is None:
        return
    has_any = any(
        getattr(endereco, a, None) is not None
        for a in ("cep", "logradouro", "numero", "complemento", "bairro")
    )
    if not has_any:
        return
    end_el = etree.SubElement(parent, f"{{{TIPOS_NS}}}EnderecoObra")
    _add_opt(end_el, "Cep", endereco.cep)
    _add_opt(end_el, "Logradouro", endereco.logradouro)
    _add_opt(end_el, "Numero", endereco.numero)
    _add_opt(end_el, "Complemento", endereco.complemento)
    _add_opt(end_el, "Bairro", endereco.bairro)


def _build_dados_obra(parent, dados) -> None:
    """Monta p1:DadosObra."""
    if dados is None:
        return
    has_any = (
        dados.codigo_obra is not None
        or dados.insc_imob_fisc is not None
        or dados.endereco_obra is not None
    )
    if not has_any:
        return
    obra = etree.SubElement(parent, f"{{{TIPOS_NS}}}DadosObra")
    _add_opt(obra, "CodigoObra", dados.codigo_obra)
    _add_opt(obra, "InscImobFisc", dados.insc_imob_fisc)
    if dados.endereco_obra is not None:
        _build_endereco_obra(obra, dados.endereco_obra)


def _build_nfe_blocks(inf, inf_rps) -> None:
    """Monta blocos opcionais NFS-e Nacional em InfRps."""

    # DadosDPS
    dd = inf_rps.dados_dps
    if dd is not None:
        _build_optional_block(
            inf,
            dd,
            "DadosDPS",
            [
                ("tp_emit", "TpEmit"),
                ("tp_amb", "TpAmb"),
                ("dh_emi", "DhEmi"),
                ("ver_aplic", "VerAplic"),
                ("cloc_emi", "CLocEmi"),
                ("cloc_prestacao", "CLocPrestacao"),
                ("ctrib_nac", "CTribNac"),
                ("trib_issqn", "TribIssqn"),
                ("tp_ret_issqn", "TpRetIssqn"),
                ("op_simp_nac", "OpSimpNac"),
                ("reg_esp_trib", "RegEspTrib"),
                ("reg_ap_trib_sn", "RegApTribSN"),
            ],
        )

    # DadosObra (com EnderecoObra aninhado)
    _build_dados_obra(inf, inf_rps.dados_obra)

    # ComercioExterior
    _build_optional_block(
        inf,
        inf_rps.comercio_exterior,
        "ComercioExterior",
        [
            ("md_prestacao", "MdPrestacao"),
            ("vinc_prest", "VincPrest"),
            ("tp_moeda", "TpMoeda"),
            ("v_serv_moeda", "VServMoeda"),
            ("mec_af_comex_p", "MecAFComexP"),
            ("mec_af_comex_t", "MecAFComexT"),
            ("mov_temp_bens", "MovTempBens"),
            ("ndi", "NDI"),
            ("nre", "NRE"),
            ("mdic", "MDIC"),
            ("c_pais_result", "CPaisResult"),
        ],
    )

    # ExigibilidadeSuspensa
    _build_optional_block(
        inf,
        inf_rps.exigibilidade_suspensa,
        "ExigibilidadeSuspensa",
        [("tp_susp", "TpSusp"), ("n_processo", "NProcesso")],
    )

    # BeneficioMunicipal
    _build_optional_block(
        inf,
        inf_rps.beneficio_municipal,
        "BeneficioMunicipal",
        [
            ("tp_bm", "TpBM"),
            ("nbm", "NBM"),
            ("v_red_bcbm", "VRedBCBM"),
            ("p_red_bcbm", "PRedBCBM"),
        ],
    )

    # ReembolsoRepasse
    _build_optional_block(
        inf,
        inf_rps.reembolso_repasse,
        "ReembolsoRepasse",
        [
            ("tp_reemb_rep_res", "TpReembRepRes"),
            ("x_tp_reemb_rep_res", "XTpReembRepRes"),
            ("v_reemb_rep_res", "VReembRepRes"),
        ],
    )

    # Destinatario
    _build_optional_block(
        inf,
        inf_rps.destinatario,
        "Destinatario",
        [
            ("cnpj_cpf", "CnpjCpf"),
            ("nome", "Nome"),
            ("logradouro", "Logradouro"),
            ("numero", "Numero"),
            ("complemento", "Complemento"),
            ("bairro", "Bairro"),
            ("cidade", "Cidade"),
            ("uf", "UF"),
            ("cep", "CEP"),
            ("cod_municipio", "CodMunicipio"),
            ("cod_pais", "CodPais"),
            ("cod_postal_ext", "CodPostalExt"),
            ("nif", "NIF"),
            ("email", "Email"),
            ("telefone", "Telefone"),
        ],
    )

    # ControleIBSCBS
    _build_optional_block(
        inf,
        inf_rps.controle_ibscbs,
        "ControleIBSCBS",
        [
            ("fin_nfse", "FinNFSe"),
            ("ind_final", "IndFinal"),
            ("tp_oper", "TpOper"),
            ("tp_ente_gov", "TpEnteGov"),
            ("ind_dest", "IndDest"),
            ("c_ind_op", "CIndOp"),
            ("x_tp_ente_gov", "XTpEnteGov"),
        ],
    )

    # IBSCBS (campos principais)
    ibs = inf_rps.ibscbs
    if ibs is not None:
        _build_optional_block(
            inf,
            ibs,
            "IBSCBS",
            [
                ("ibscbs_base_calculo", "IBSCBSBaseCalculo"),
                ("ibsu_f_aliquota", "IBSUFAliquota"),
                ("ib_mun_aliquota", "IBSMunAliquota"),
                ("cbs_aliquota", "CBSAliquota"),
                ("ibsu_f_valor", "IBSUFValor"),
                ("ibs_mun_valor", "IBSMunValor"),
                ("cbs_valor", "CBSValor"),
                ("ibsu_f_perc_reducao", "IBSUFPercReducao"),
                ("ibs_mun_perc_reducao", "IBSMunPercReducao"),
                ("cbs_perc_reducao", "CBSPercReducao"),
                ("ibsu_f_aliquota_efetiva", "IBSUFAliquotaEfetiva"),
                ("ibs_mun_aliquota_efetiva", "IBSMunAliquotaEfetiva"),
                ("cbs_aliquota_efetiva", "CBSAliquotaEfetiva"),
                ("ibsu_f_perc_diferimento", "IBSUFPercDiferimento"),
                ("ibs_mun_perc_diferimento", "IBSMunPercDiferimento"),
                ("cbs_perc_diferimento", "CBSPercDiferimento"),
                ("ibsu_f_valor_diferido", "IBSUFValorDiferido"),
                ("ibs_mun_valor_diferido", "IBSMunValorDiferido"),
                ("cbs_valor_diferido", "CBSValorDiferido"),
                ("ibs_credito_presumido_aliq", "IBSCreditoPresumidoAliq"),
                ("ibs_credito_presumido_valor", "IBSCreditoPresumidoValor"),
                ("cbs_credito_presumido_aliq", "CBSCreditoPresumidoAliq"),
                ("cbs_credito_presumido_valor", "CBSCreditoPresumidoValor"),
                ("ibs_valor_total", "IBSValorTotal"),
                ("valor_total_com_tributos", "ValorTotalComTributos"),
                ("ibs_valor_reembolso", "IBSValorReembolso"),
                ("localidade_incidencia_cod", "LocalidadeIncidenciaCod"),
                ("localidade_incidencia_nome", "LocalidadeIncidenciaNome"),
                ("perc_redutor_compra_gov", "PercRedutorCompraGov"),
            ],
        )

    # DataCompetencia (elemento simples)
    _add_opt(inf, "DataCompetencia", inf_rps.data_competencia)


def _build_infrps(parent, inf_rps) -> None:
    """Monta p1:InfRps com filhos p1:."""
    inf = etree.SubElement(parent, f"{{{TIPOS_NS}}}InfRps")
    if inf_rps.id is not None:
        inf.set("Id", str(inf_rps.id))

    ir = inf_rps.identificacao_rps
    idrps = etree.SubElement(inf, f"{{{TIPOS_NS}}}IdentificacaoRps")
    _elem(idrps, "Numero", ir.numero)
    _elem(idrps, "Serie", ir.serie)
    _elem(idrps, "Tipo", ir.tipo)

    _elem(inf, "DataEmissao", inf_rps.data_emissao)
    _elem(inf, "NaturezaOperacao", inf_rps.natureza_operacao)
    _elem(inf, "RegimeEspecialTributacao", inf_rps.regime_especial_tributacao)
    _elem(inf, "OptanteSimplesNacional", inf_rps.optante_simples_nacional)
    _elem(inf, "IncentivadorCultural", inf_rps.incentivador_cultural)
    _elem(inf, "Status", inf_rps.status)

    srv = inf_rps.servico
    serv = etree.SubElement(inf, f"{{{TIPOS_NS}}}Servico")
    val = etree.SubElement(serv, f"{{{TIPOS_NS}}}Valores")
    v = srv.valores
    _elem(val, "ValorServicos", v.valor_servicos)
    _elem(val, "ValorDeducoes", v.valor_deducoes)
    _elem(val, "ValorPis", v.valor_pis or 0)
    _elem(val, "ValorCofins", v.valor_cofins or 0)
    _elem(val, "ValorInss", v.valor_inss)
    _elem(val, "ValorIr", v.valor_ir)
    _elem(val, "ValorCsll", v.valor_csll)
    _elem(val, "IssRetido", v.iss_retido)
    _elem(val, "ValorIss", v.valor_iss or 0)
    _elem(val, "ValorIssRetido", v.valor_iss_retido)
    _elem(val, "OutrasRetencoes", v.outras_retencoes)
    _elem(val, "BaseCalculo", v.base_calculo or (v.valor_servicos - v.valor_deducoes))
    _elem(val, "Aliquota", v.aliquota)
    _elem(val, "ValorLiquidoNfse", v.valor_liquido_nfse or 0)
    _elem(val, "DescontoCondicionado", v.desconto_condicionado)
    _elem(val, "DescontoIncondicionado", v.desconto_incondicionado)

    _elem(serv, "ItemListaServico", srv.item_lista_servico)
    _elem(serv, "CodigoCnae", srv.codigo_cnae)
    _elem(serv, "CodigoTributacaoMunicipio", srv.codigo_tributacao_municipio)
    _elem(serv, "Discriminacao", srv.discriminacao)
    _elem(serv, "CodigoMunicipio", srv.codigo_municipio)

    prest = inf_rps.prestador
    pre = etree.SubElement(inf, f"{{{TIPOS_NS}}}Prestador")
    _elem(pre, "Cnpj", prest.cnpj)
    _elem(pre, "InscricaoMunicipal", prest.inscricao_municipal)

    tom = inf_rps.tomador
    tom_el = etree.SubElement(inf, f"{{{TIPOS_NS}}}Tomador")
    id_tom = etree.SubElement(tom_el, f"{{{TIPOS_NS}}}IdentificacaoTomador")
    cpc = etree.SubElement(id_tom, f"{{{TIPOS_NS}}}CpfCnpj")
    if tom.identificacao_tomador.cpf_cnpj.cpf:
        _elem(cpc, "Cpf", tom.identificacao_tomador.cpf_cnpj.cpf)
    else:
        _elem(cpc, "Cnpj", tom.identificacao_tomador.cpf_cnpj.cnpj)
    _elem(tom_el, "RazaoSocial", tom.razao_social)
    end = tom.endereco
    ende = etree.SubElement(tom_el, f"{{{TIPOS_NS}}}Endereco")
    _elem(ende, "Endereco", end.endereco)
    _elem(ende, "Numero", end.numero)
    if end.complemento:
        _elem(ende, "Complemento", end.complemento)
    _elem(ende, "Bairro", end.bairro)
    _elem(ende, "CodigoMunicipio", end.codigo_municipio)
    _elem(ende, "Uf", end.uf)
    _elem(ende, "Cep", end.cep)

    # Blocos NFS-e Nacional
    _build_nfe_blocks(inf, inf_rps)


def _build_rps(parent, rps: Rps, signature: Optional[Signature] = None) -> None:
    """Monta p1:Rps = p1:InfRps + Signature."""
    rps_el = etree.SubElement(parent, f"{{{TIPOS_NS}}}Rps")
    _build_infrps(rps_el, rps.inf_rps)
    if signature:
        sig_el = signature.to_element("Signature", namespace=XMLDSIG_NS, nsmap={None: XMLDSIG_NS})
        rps_el.append(sig_el)


def build_lote_element(
    lote: LoteRps,
    signatures: Optional[List[Optional[Signature]]] = None,
):
    """Retorna elemento raiz EnviarLoteRpsEnvio (para assinatura in-place)."""
    nsmap = {
        "p": ENVIO_NS,
        "p1": TIPOS_NS,
        "ds": XMLDSIG_NS,
        "xsi": XSI_NS,
    }
    root = etree.Element(
        f"{{{ENVIO_NS}}}EnviarLoteRpsEnvio",
        nsmap=nsmap,
    )
    root.set(f"{{{XSI_NS}}}schemaLocation", ENVIO_NS)

    lote_el = etree.SubElement(root, f"{{{ENVIO_NS}}}LoteRps")
    lote_el.set("Id", lote.id or "")

    _elem(lote_el, "NumeroLote", lote.numero_lote)
    _elem(lote_el, "Cnpj", lote.cnpj)
    _elem(lote_el, "InscricaoMunicipal", lote.inscricao_municipal)
    _elem(lote_el, "QuantidadeRps", lote.quantidade_rps)

    lista = etree.SubElement(lote_el, f"{{{TIPOS_NS}}}ListaRps")
    sigs = signatures or []
    for i, rps in enumerate(lote.lista_rps.rps):
        sig = sigs[i] if i < len(sigs) else (rps.signature if hasattr(rps, "signature") else None)
        _build_rps(lista, rps, sig)

    return root


def build_lote_xml(
    lote: LoteRps,
    signatures: Optional[List[Optional[Signature]]] = None,
) -> str:
    """Gera XML EnviarLoteRpsEnvio com estrutura p:/p1:."""
    root = build_lote_element(lote, signatures)
    return etree.tostring(
        root,
        encoding="UTF-8",
        xml_declaration=False,
        pretty_print=False,
    ).decode("utf-8")


def get_header_speedgov() -> str:
    """Header p:cabecalho conforme reference."""
    nsmap = {
        "p": CABECALHO_NS,
        "p1": TIPOS_NS,
        "ds": XMLDSIG_NS,
        "xsi": XSI_NS,
    }
    root = etree.Element(f"{{{CABECALHO_NS}}}cabecalho", nsmap=nsmap)
    root.set("versao", "1")
    root.set(f"{{{XSI_NS}}}schemaLocation", CABECALHO_NS)
    v = etree.SubElement(root, "{}versaoDados")
    v.text = "1"
    return etree.tostring(
        root,
        encoding="UTF-8",
        xml_declaration=False,
        pretty_print=False,
    ).decode("utf-8")


# --- Cancelamento ---
CANCELAR_NFSE_NS = "http://ws.speedgov.com.br/cancelar_nfse_envio_v1.xsd"

# --- Consultas ---
CONSULTAR_NFSE_NS = "http://ws.speedgov.com.br/consultar_nfse_envio_v1.xsd"
CONSULTAR_NFSE_RPS_NS = "http://ws.speedgov.com.br/consultar_nfse_rps_envio_v1.xsd"
CONSULTAR_LOTE_RPS_NS = "http://ws.speedgov.com.br/consultar_lote_rps_envio_v1.xsd"
CONSULTAR_SITUACAO_LOTE_RPS_NS = "http://ws.speedgov.com.br/consultar_situacao_lote_rps_envio_v1.xsd"


def build_cancelar_nfse_xml(
    numero_nfse: int,
    cnpj: str,
    inscricao_municipal: str,
    codigo_municipio: int,
    codigo_cancelamento: str,
    id_pedido: str = "",
) -> str:
    """Gera XML CancelarNfseEnvio (p:/p1:)."""
    nsmap = {
        "p": CANCELAR_NFSE_NS,
        "p1": TIPOS_NS,
        "ds": XMLDSIG_NS,
        "xsi": XSI_NS,
    }
    root = etree.Element(
        f"{{{CANCELAR_NFSE_NS}}}CancelarNfseEnvio",
        nsmap=nsmap,
    )
    root.set(f"{{{XSI_NS}}}schemaLocation", CANCELAR_NFSE_NS)

    pedido = etree.SubElement(root, f"{{{CANCELAR_NFSE_NS}}}Pedido")
    inf = etree.SubElement(pedido, f"{{{TIPOS_NS}}}InfPedidoCancelamento")
    inf.set("Id", id_pedido)

    id_nfse = etree.SubElement(inf, f"{{{TIPOS_NS}}}IdentificacaoNfse")
    _elem(id_nfse, "Numero", numero_nfse)
    _elem(id_nfse, "Cnpj", cnpj)
    _elem(id_nfse, "InscricaoMunicipal", inscricao_municipal)
    _elem(id_nfse, "CodigoMunicipio", codigo_municipio)

    _elem(inf, "CodigoCancelamento", codigo_cancelamento)

    return etree.tostring(
        root,
        encoding="UTF-8",
        xml_declaration=False,
        pretty_print=False,
    ).decode("utf-8")


def _build_prestador(parent, cnpj: str, inscricao_municipal: str, envio_ns: str) -> None:
    """Adiciona p:Prestador com p1:Cnpj e p1:InscricaoMunicipal."""
    prest = etree.SubElement(parent, f"{{{envio_ns}}}Prestador")
    _elem(prest, "Cnpj", cnpj)
    _elem(prest, "InscricaoMunicipal", inscricao_municipal)


def build_consult_nfse_xml(
    cnpj: str,
    inscricao_municipal: str,
    numero_nfse: Optional[int] = None,
) -> str:
    """Gera XML ConsultarNfseEnvio (p:/p1:)."""
    nsmap = {
        "p": CONSULTAR_NFSE_NS,
        "p1": TIPOS_NS,
        "ds": XMLDSIG_NS,
        "xsi": XSI_NS,
    }
    root = etree.Element(
        f"{{{CONSULTAR_NFSE_NS}}}ConsultarNfseEnvio",
        nsmap=nsmap,
    )
    root.set(f"{{{XSI_NS}}}schemaLocation", CONSULTAR_NFSE_NS)
    _build_prestador(root, cnpj, inscricao_municipal, CONSULTAR_NFSE_NS)
    if numero_nfse is not None:
        num_el = etree.SubElement(root, f"{{{CONSULTAR_NFSE_NS}}}NumeroNfse")
        num_el.text = str(numero_nfse)
    return etree.tostring(
        root,
        encoding="UTF-8",
        xml_declaration=False,
        pretty_print=False,
    ).decode("utf-8")


def build_consult_rps_xml(
    numero: int,
    serie: str,
    tipo: int,
    cnpj: str,
    inscricao_municipal: str,
) -> str:
    """Gera XML ConsultarNfseRpsEnvio (p:/p1:)."""
    nsmap = {
        "p": CONSULTAR_NFSE_RPS_NS,
        "p1": TIPOS_NS,
        "ds": XMLDSIG_NS,
        "xsi": XSI_NS,
    }
    root = etree.Element(
        f"{{{CONSULTAR_NFSE_RPS_NS}}}ConsultarNfseRpsEnvio",
        nsmap=nsmap,
    )
    root.set(f"{{{XSI_NS}}}schemaLocation", CONSULTAR_NFSE_RPS_NS)
    idrps = etree.SubElement(root, f"{{{CONSULTAR_NFSE_RPS_NS}}}IdentificacaoRps")
    _elem(idrps, "Numero", numero)
    _elem(idrps, "Serie", serie)
    _elem(idrps, "Tipo", tipo)
    _build_prestador(root, cnpj, inscricao_municipal, CONSULTAR_NFSE_RPS_NS)
    return etree.tostring(
        root,
        encoding="UTF-8",
        xml_declaration=False,
        pretty_print=False,
    ).decode("utf-8")


def build_consult_lote_rps_xml(
    cnpj: str,
    inscricao_municipal: str,
    protocolo: str,
) -> str:
    """Gera XML ConsultarLoteRpsEnvio (p:/p1:)."""
    nsmap = {
        "p": CONSULTAR_LOTE_RPS_NS,
        "p1": TIPOS_NS,
        "ds": XMLDSIG_NS,
        "xsi": XSI_NS,
    }
    root = etree.Element(
        f"{{{CONSULTAR_LOTE_RPS_NS}}}ConsultarLoteRpsEnvio",
        nsmap=nsmap,
    )
    root.set("Id", "")
    root.set(f"{{{XSI_NS}}}schemaLocation", CONSULTAR_LOTE_RPS_NS)
    _build_prestador(root, cnpj, inscricao_municipal, CONSULTAR_LOTE_RPS_NS)
    prot = etree.SubElement(root, f"{{{CONSULTAR_LOTE_RPS_NS}}}Protocolo")
    prot.text = str(protocolo)
    return etree.tostring(
        root,
        encoding="UTF-8",
        xml_declaration=False,
        pretty_print=False,
    ).decode("utf-8")


def build_consult_situacao_lote_rps_xml(
    cnpj: str,
    inscricao_municipal: str,
    protocolo: str,
) -> str:
    """Gera XML ConsultarSituacaoLoteRpsEnvio (p:/p1:)."""
    nsmap = {
        "p": CONSULTAR_SITUACAO_LOTE_RPS_NS,
        "p1": TIPOS_NS,
        "ds": XMLDSIG_NS,
        "xsi": XSI_NS,
    }
    root = etree.Element(
        f"{{{CONSULTAR_SITUACAO_LOTE_RPS_NS}}}ConsultarSituacaoLoteRpsEnvio",
        nsmap=nsmap,
    )
    root.set("Id", "")
    root.set(f"{{{XSI_NS}}}schemaLocation", CONSULTAR_SITUACAO_LOTE_RPS_NS)
    _build_prestador(root, cnpj, inscricao_municipal, CONSULTAR_SITUACAO_LOTE_RPS_NS)
    prot = etree.SubElement(root, f"{{{CONSULTAR_SITUACAO_LOTE_RPS_NS}}}Protocolo")
    prot.text = str(protocolo)
    return etree.tostring(
        root,
        encoding="UTF-8",
        xml_declaration=False,
        pretty_print=False,
    ).decode("utf-8")
