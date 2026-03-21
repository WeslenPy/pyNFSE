"""
Enums auxiliares para campos de escolha da integração SpeedGov.
Facilitam o uso com nomes descritivos em vez de códigos numéricos.
"""
from enum import IntEnum


# --- InfRps / IdentificacaoRps ---


class TipoRps(IntEnum):
    """Tipo do RPS (IdentificacaoRps.Tipo)."""

    RPS = 1
    NOTA_FISCAL_CONJUGADA_CUPOM = 2
    CUPOM = 3


class NaturezaOperacao(IntEnum):
    """Natureza da operação (InfRps.NaturezaOperacao)."""

    TRIBUTACAO_NO_MUNICIPIO = 1
    TRIBUTACAO_FORA_DO_MUNICIPIO = 2
    ISENCAO = 3
    IMUNE = 4
    EXIGIBILIDADE_SUSPENSA = 5
    NAO_TRIBUTAVEL = 6


class RegimeEspecialTributacao(IntEnum):
    """Regime especial de tributação (InfRps.RegimeEspecialTributacao)."""

    NENHUM = 0
    MICROEMPRESA_MUNICIPAL = 1
    ESTIMATIVA = 2
    SOCIEDADE_DE_PROFISSIONAIS = 3
    COOPERATIVA = 4
    MEI = 5
    ME_EPP_SIMPLES_NACIONAL = 6


class SimNao(IntEnum):
    """Indicador Sim/Não (1=Sim, 2=Não). Usado em OptanteSimplesNacional, IncentivadorCultural, IssRetido."""

    SIM = 1
    NAO = 2


class StatusRps(IntEnum):
    """Status do RPS (InfRps.Status)."""

    NORMAL = 1
    CANCELADO = 2


# --- Valores.iss_retido ---


class IssRetido(IntEnum):
    """Indica se ISS foi retido pelo tomador (Valores.IssRetido)."""

    SIM = 1
    NAO = 2


# --- Situação do Lote (resposta ConsultarSituacaoLoteRps) ---


class SituacaoLoteRps(IntEnum):
    """Situação do lote de RPS (resposta ConsultarSituacaoLoteRps)."""

    NAO_RECEBIDO = 1
    NAO_PROCESSADO = 2
    PROCESSADO_COM_ERRO = 3
    PROCESSADO_COM_SUCESSO = 4


# --- DadosDPS (NFS-e Nacional) ---


class TipoEmissaoDPS(IntEnum):
    """Tipo de emitente (DadosDPS.tp_emit): 1=Prestador, 2=Tomador."""

    PRESTADOR = 1
    TOMADOR = 2


class TipoAmbiente(IntEnum):
    """Tipo de ambiente (DadosDPS.tp_amb): 1=Produção, 2=Homologação."""

    PRODUCAO = 1
    HOMOLOGACAO = 2


class TributacaoIssqn(IntEnum):
    """Tributação ISSQN (DadosDPS.trib_issqn): 1=Normal, 2=Imune, 3=Isento, 4=Exportação."""

    NORMAL = 1
    IMUNE = 2
    ISENTO = 3
    EXPORTACAO = 4


class TipoRetencaoIssqn(IntEnum):
    """Tipo de retenção ISSQN (DadosDPS.tp_ret_issqn): 1=Não retido, 2=Retido pelo tomador, 3=Retido pelo intermediário."""

    NAO_RETIDO = 1
    RETIDO_PELO_TOMADOR = 2
    RETIDO_PELO_INTERMEDIARIO = 3


class OptanteSimplesNacionalDPS(IntEnum):
    """Optante Simples Nacional (DadosDPS.op_simp_nac): 1=Não optante, 2=Optante ME/EPP, 3=MEI."""
    
    NAO_OPTANTE = 1
    OPTANTE_ME_EPP = 3
    MEI = 2


class RegimeApuracaoTributosSN(IntEnum):
    """Regime de apuração de tributos no SN (DadosDPS.reg_ap_trib_sn): 1=Fed+Mun pelo SN, 2=Fed SN e ISSQN NFS-e, 3=Fed+Mun pela NFS-e."""

    FED_MUN_PELO_SN = 1
    FED_SN_ISSQN_NFSE = 2
    FED_MUN_PELA_NFSE = 3


# --- ComercioExterior ---


class ModalidadePrestacao(IntEnum):
    """Modalidade de prestação do serviço (ComercioExterior.md_prestacao)."""

    EXECUCAO_NO_BRASIL = 1
    EXECUCAO_NO_EXTERIOR = 2
    EXECUCAO_NO_BRASIL_E_EXTERIOR = 3


# --- ExigibilidadeSuspensa ---


class TipoExigibilidadeSuspensa(IntEnum):
    """Tipo de suspensão da exigibilidade (ExigibilidadeSuspensa.tp_susp)."""

    DECISAO_JUDICIAL = 1
    PROCESSO_ADMINISTRATIVO = 2


# --- ControleIBSCBS ---


class FinalidadeNFSe(IntEnum):
    """Finalidade da NFSe (ControleIBSCBS.fin_nfse)."""

    NFSE_NORMAL = 1
    NFSE_COMPLEMENTAR = 2
    NFSE_DE_AJUSTE = 3
    NFSE_SUBSTITUIDA = 4


class IndicadorFinal(IntEnum):
    """Indicador de operação para consumidor final (ControleIBSCBS.ind_final)."""

    CONSUMIDOR_FINAL = 1
    NAO_CONSUMIDOR_FINAL = 2


class IndicadorDestino(IntEnum):
    """Indicador de destino da operação (ControleIBSCBS.ind_dest)."""

    INTERNA = 1
    INTERESTADUAL = 2
    EXTERIOR = 3
