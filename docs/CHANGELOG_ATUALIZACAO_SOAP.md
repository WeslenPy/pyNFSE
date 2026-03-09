# Changelog - Atualização para Schema SOAP NFS-e Nacional

## Resumo das Mudanças

A biblioteca foi atualizada para funcionar com o novo schema SOAP conforme documentação NFS-e Nacional (versão 2.0, Dezembro 2025).

## Mudanças Implementadas

### 1. Novo Schema: LoteRps ✅

**Arquivo**: `pynfse/schemas/lote.py`

Criado schema `LoteRps` para agrupar múltiplos RPS conforme especificação:

```python
class LoteRps(BaseModel):
    numero_lote: int
    cnpj: str
    inscricao_municipal: str
    quantidade_rps: int
    lista_rps: List[InfoRPS]
    id: str = ""  # Para assinatura digital
```

### 2. Template info_rps.xml ✅

**Arquivo**: `pynfse/src/integration/carnaubal/abrasf/templates/info_rps.xml`

Criado novo template que será incluído no `reception_rps.xml`:
- Extraído do `rps.xml` original
- Suporta múltiplos RPS em loop
- DataEmissao agora usa formato DateTime: `YYYY-MM-DDTHH:MM:SS`

### 3. Template reception_rps.xml Atualizado ✅

**Arquivo**: `pynfse/src/integration/carnaubal/abrasf/templates/reception_rps.xml`

Atualizado conforme documentação:
- Removidas declarações XML desnecessárias dentro de header/parameters
- Estrutura `<LoteRps xmlns="">` conforme especificação
- Loop para múltiplos RPS usando `{% for rps in lote.lista_rps %}`
- Campos do lote usando variáveis do schema: `lote.numero_lote`, `lote.cnpj`, etc.

### 4. parse_xml_nfse Atualizado ✅

**Arquivo**: `pynfse/src/common/xml.py`

Método atualizado para colocar conteúdo de `header` e `parameters` em CDATA:
- Usa `BeautifulSoup.CData` para encapsular conteúdo
- Verifica existência dos elementos antes de processar
- Mantém compatibilidade com XMLs que não têm header/parameters

### 5. create_rps_nfse Atualizado ✅

**Arquivo**: `pynfse/src/common/xml.py`

Método agora aceita parâmetro opcional `lote: Optional[LoteRps]`:
- Se `lote` fornecido: usa estrutura `reception_rps.xml` com LoteRps
- Se `lote` não fornecido: mantém compatibilidade com código antigo usando `rps.xml`

### 6. CarnaubalNFSe Atualizado ✅

**Arquivo**: `pynfse/src/integration/carnaubal/abrasf/nfse.py`

Classe implementada completamente:
- `create_rps_nfse`: Cria lote automático se não fornecido
- `create_cancel_nfse`: Implementado
- `create_consult_nfse`: Implementado

## Estrutura SOAP Final

Conforme documentação, o XML gerado segue esta estrutura:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope 
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
    xmlns:nfse="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd">
    <soapenv:Header/>
    <soapenv:Body>
        <nfse:RecepcionarLoteRps>
            <header><![CDATA[
                <p:cabecalho versao="1" ...>
                    <versaoDados xmlns="">1</versaoDados>
                </p:cabecalho>
            ]]></header>
            <parameters><![CDATA[
                <p:EnviarLoteRpsEnvio ...>
                    <LoteRps xmlns="" Id="lote_001">
                        <NumeroLote>1</NumeroLote>
                        <Cnpj>...</Cnpj>
                        <InscricaoMunicipal>...</InscricaoMunicipal>
                        <QuantidadeRps>1</QuantidadeRps>
                        <ListaRps>
                            <Rps>...</Rps>
                        </ListaRps>
                    </LoteRps>
                </p:EnviarLoteRpsEnvio>
            ]]></parameters>
        </nfse:RecepcionarLoteRps>
    </soapenv:Body>
</soapenv:Envelope>
```

## Compatibilidade

### Mantida Compatibilidade Retroativa ✅

- Código antigo que usa `create_rps_nfse(rps)` continua funcionando
- Se não fornecer `lote`, cria XML simples sem estrutura LoteRps
- Templates antigos (`rps.xml`) ainda funcionam

### Nova Funcionalidade

- Suporte a múltiplos RPS em um único lote
- Estrutura SOAP conforme NFS-e Nacional
- Header e parameters em CDATA conforme especificação

## Exemplo de Uso

### Uso Simples (compatível com código antigo)
```python
from pynfse.src.integration.carnaubal.abrasf.nfse import CarnaubalNFSe
from pynfse.schemas.nfse import InfoRPS, ...

nfse_client = CarnaubalNFSe(URL="https://api.exemplo.com/nfse")
rps = InfoRPS(...)
xml = nfse_client.create_rps_nfse(rps)  # Cria lote automático
```

### Uso com Lote Customizado
```python
from pynfse.schemas.lote import LoteRps

lote = LoteRps(
    numero_lote=1,
    cnpj="12345678000190",
    inscricao_municipal="12345",
    quantidade_rps=2,
    lista_rps=[rps1, rps2],
    id="lote_001"
)
xml = nfse_client.create_rps_nfse(rps1, lote=lote)
```

## Próximos Passos

1. ✅ Estrutura SOAP básica implementada
2. ⏳ Adicionar campos faltantes do ABRASF 2.04 (Contato, Intermediário, etc.)
3. ⏳ Implementar novos campos NFS-e Nacional conforme necessidade
4. ⏳ Atualizar testes para nova estrutura

## Notas

- Todos os campos novos da NFS-e Nacional são opcionais
- A implementação atual cobre a estrutura básica necessária
- Campos adicionais podem ser implementados incrementalmente


