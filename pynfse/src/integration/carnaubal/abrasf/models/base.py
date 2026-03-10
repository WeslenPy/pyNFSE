from pynfse.src.common.xml_node import XMLNode
from typing import Optional, List, Annotated
from pydantic import Field, StringConstraints, conint, confloat

# Tipos Simples Baseados no XSD (tipos_v1.xsd)

# tsNumeroNfse, tsNumeroRps, tsNumeroLote (nonNegativeInteger, 15 digits)
tsNumero = Annotated[int, conint(ge=0, le=999999999999999)]
tsNumeroNfse = tsNumero
tsNumeroRps = tsNumero
tsNumeroLote = tsNumero

# tsCodigoVerificacao (string, 1-9 chars)
tsCodigoVerificacao = Annotated[str, StringConstraints(min_length=1, max_length=9)]

# tsStatusRps, tsStatusNfse, tsSimNao (byte, pattern 1|2)
tsStatus12 = Annotated[int, Field(ge=1, le=2)]
tsSimNao = tsStatus12

# tsNaturezaOperacao (byte, pattern 1|2|3|4|5|6)
tsNaturezaOperacao = Annotated[int, Field(ge=1, le=6)]

# tsRegimeEspecialTributacao (byte, pattern 1|2|3|4|5|6)
tsRegimeEspecialTributacao = Annotated[int, Field(ge=1, le=6)]

# tsSerieRps (string, 1-5 chars)
tsSerieRps = Annotated[str, StringConstraints(min_length=1, max_length=5)]

# tsTipoRps (byte, pattern 1|2|3)
tsTipoRps = Annotated[int, Field(ge=1, le=3)]

# tsValor (decimal, 15 total digits, 2 fraction digits)
tsValor = Annotated[float, confloat(ge=0, le=9999999999999.99)]

# tsItemListaServico (string, 1-5 chars)
tsItemListaServico = Annotated[str, StringConstraints(min_length=1, max_length=5)]

# tsCodigoCnae (int, 7 digits)
tsCodigoCnae = Annotated[int, conint(ge=0, le=9999999)]

# tsCodigoTributacao (string, 1-20 chars)
tsCodigoTributacao = Annotated[str, StringConstraints(min_length=1, max_length=20)]

# tsAliquota (decimal, 5 total, 4 fraction)
tsAliquota = Annotated[float, confloat(ge=0, le=9.9999)]

# tsDiscriminacao (string, 1-2000 chars)
tsDiscriminacao = Annotated[str, StringConstraints(min_length=1, max_length=2000)]

# tsCodigoMunicipioIbge (int, 7 digits)
tsCodigoMunicipioIbge = Annotated[int, conint(ge=0, le=9999999)]

# tsInscricaoMunicipal (string, 1-15 chars)
tsInscricaoMunicipal = Annotated[str, StringConstraints(min_length=1, max_length=15)]

# tsRazaoSocial (string, 1-115 chars)
tsRazaoSocial = Annotated[str, StringConstraints(min_length=1, max_length=115)]

# tsCnpj (string, 14 chars fixed)
tsCnpj = Annotated[str, StringConstraints(min_length=14, max_length=14, pattern=r"^\d{14}$")]

# tsCpf (string, 11 chars fixed)
tsCpf = Annotated[str, StringConstraints(min_length=11, max_length=11, pattern=r"^\d{11}$")]

# tsUf (string, 2 chars fixed)
tsUf = Annotated[str, StringConstraints(min_length=2, max_length=2)]

# tsCep (int, 8 digits)
tsCep = Annotated[int, conint(ge=0, le=99999999)]

# tsEmail (string, 1-80 chars)
tsEmail = Annotated[str, StringConstraints(min_length=1, max_length=80)]

# tsTelefone (string, 1-11 chars)
tsTelefone = Annotated[str, StringConstraints(min_length=1, max_length=11)]

# tsNumeroProtocolo (string, 1-50 chars)
tsNumeroProtocolo = Annotated[str, StringConstraints(min_length=1, max_length=50)]

# tsCodigoMensagemAlerta (string, 1-4 chars)
tsCodigoMensagemAlerta = Annotated[str, StringConstraints(min_length=1, max_length=4)]

# tsDescricaoMensagemAlerta (string, 1-200 chars)
tsDescricaoMensagemAlerta = Annotated[str, StringConstraints(min_length=1, max_length=200)]

# tsOutrasInformacoes (string, 1-255 chars)
tsOutrasInformacoes = Annotated[str, StringConstraints(min_length=1, max_length=255)]

# tsIdTag (string, 1-255 chars)
tsIdTag = Annotated[str, StringConstraints(min_length=1, max_length=255)]

class ABRASFNode(XMLNode):
    """Classe base para nós do padrão ABRASF."""
    pass

class MensagemRetorno(ABRASFNode):
    codigo: tsCodigoMensagemAlerta = Field(..., alias="Codigo")
    mensagem: tsDescricaoMensagemAlerta = Field(..., alias="Mensagem")
    correcao: Optional[tsDescricaoMensagemAlerta] = Field(None, alias="Correcao")

class ListaMensagemRetorno(ABRASFNode):
    mensagem_retorno: List[MensagemRetorno] = Field(..., alias="MensagemRetorno")

class CpfCnpj(ABRASFNode):
    cpf: Optional[tsCpf] = Field(None, alias="Cpf")
    cnpj: Optional[tsCnpj] = Field(None, alias="Cnpj")

class Endereco(ABRASFNode):
    endereco: Optional[Annotated[str, StringConstraints(max_length=125)]] = Field(None, alias="Endereco")
    numero: Optional[Annotated[str, StringConstraints(max_length=10)]] = Field(None, alias="Numero")
    complemento: Optional[Annotated[str, StringConstraints(max_length=60)]] = Field(None, alias="Complemento")
    bairro: Optional[Annotated[str, StringConstraints(max_length=60)]] = Field(None, alias="Bairro")
    codigo_municipio: Optional[tsCodigoMunicipioIbge] = Field(None, alias="CodigoMunicipio")
    uf: Optional[tsUf] = Field(None, alias="Uf")
    cep: Optional[tsCep] = Field(None, alias="Cep")

class Contato(ABRASFNode):
    telefone: Optional[tsTelefone] = Field(None, alias="Telefone")
    email: Optional[tsEmail] = Field(None, alias="Email")
