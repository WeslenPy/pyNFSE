from datetime import datetime, date
from typing import Optional, List
from pydantic import Field
from pynfse.src.integration.carnaubal.abrasf.models.base import (
    ABRASFNode, tsNumeroLote, tsNumeroProtocolo, tsIdTag, tsNumeroNfse,
    tsCodigoVerificacao, tsNaturezaOperacao, tsRegimeEspecialTributacao,
    tsStatus12, tsSimNao, tsOutrasInformacoes, tsValor, ListaMensagemRetorno
)
from pynfse.src.integration.carnaubal.abrasf.models.rps import (
    IdentificacaoRps, IdentificacaoPrestador, DadosTomador, DadosServico,
    DadosConstrucaoCivil, DadosDPS, DadosObra, ComercioExterior,
    ExigibilidadeSuspensa, BeneficioMunicipal, ReembolsoRepasse,
    Destinatario, ControleIBSCBS, IBSCBS
)
from pynfse.src.common.signature import Signature

class InfNfse(ABRASFNode):
    id: Optional[tsIdTag] = Field(None, alias="Id")
    numero: tsNumeroNfse = Field(..., alias="Numero")
    codigo_verificacao: tsCodigoVerificacao = Field(..., alias="CodigoVerificacao")
    data_emissao: datetime = Field(..., alias="DataEmissao")
    identificacao_rps: Optional[IdentificacaoRps] = Field(None, alias="IdentificacaoRps")
    data_emissao_rps: Optional[date] = Field(None, alias="DataEmissaoRps")
    natureza_operacao: tsNaturezaOperacao = Field(..., alias="NaturezaOperacao")
    regime_especial_tributacao: Optional[tsRegimeEspecialTributacao] = Field(None, alias="RegimeEspecialTributacao")
    optante_simples_nacional: tsSimNao = Field(..., alias="OptanteSimplesNacional")
    incentivador_cultural: tsSimNao = Field(..., alias="IncentivadorCultural")
    competencia: date = Field(..., alias="Competencia")
    nfse_substituida: Optional[tsNumeroNfse] = Field(None, alias="NfseSubstituida")
    outras_informacoes: Optional[tsOutrasInformacoes] = Field(None, alias="OutrasInformacoes")
    servico: DadosServico = Field(..., alias="Servico")
    valor_credito: Optional[tsValor] = Field(None, alias="ValorCredito")
    prestador_servico: IdentificacaoPrestador = Field(..., alias="PrestadorServico")
    tomador_servico: DadosTomador = Field(..., alias="TomadorServico")
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

class Nfse(ABRASFNode):
    inf_nfse: InfNfse = Field(..., alias="InfNfse")
    signature: Optional[List[Signature]] = Field(None, alias="Signature")

class ConfirmacaoCancelamento(ABRASFNode):
    id: Optional[tsIdTag] = Field(None, alias="Id")
    data_hora: datetime = Field(..., alias="DataHora")

class CancelamentoNfse(ABRASFNode):
    confirmacao: ConfirmacaoCancelamento = Field(..., alias="Confirmacao")
    signature: Optional[Signature] = Field(None, alias="Signature")

class CompNfse(ABRASFNode):
    nfse: Nfse = Field(..., alias="Nfse")
    nfse_cancelamento: Optional[CancelamentoNfse] = Field(None, alias="NfseCancelamento")

class EnviarLoteRpsResposta(ABRASFNode):
    numero_lote: Optional[tsNumeroLote] = Field(None, alias="NumeroLote")
    data_recebimento: Optional[datetime] = Field(None, alias="DataRecebimento")
    protocolo: Optional[tsNumeroProtocolo] = Field(None, alias="Protocolo")
    lista_mensagem_retorno: Optional[ListaMensagemRetorno] = Field(None, alias="ListaMensagemRetorno")

class ConsultarNfseRpsResposta(ABRASFNode):
    comp_nfse: Optional[CompNfse] = Field(None, alias="CompNfse")
    lista_mensagem_retorno: Optional[ListaMensagemRetorno] = Field(None, alias="ListaMensagemRetorno")

class ListaNfse(ABRASFNode):
    comp_nfse: List[CompNfse] = Field(default_factory=list, alias="CompNfse")

class ConsultarNfseResposta(ABRASFNode):
    lista_nfse: Optional[ListaNfse] = Field(None, alias="ListaNfse")
    lista_mensagem_retorno: Optional[ListaMensagemRetorno] = Field(None, alias="ListaMensagemRetorno")

class CancelarNfseResposta(ABRASFNode):
    cancelamento: Optional[CancelamentoNfse] = Field(None, alias="Cancelamento")
    lista_mensagem_retorno: Optional[ListaMensagemRetorno] = Field(None, alias="ListaMensagemRetorno")
