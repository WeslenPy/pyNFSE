# Exemplos de Uso da Biblioteca pyNFSE

Este diretório contém exemplos práticos de como usar a biblioteca pyNFSE.

## Arquivos

- `basic_usage.py` - Exemplos básicos de uso da biblioteca

## Como Executar os Exemplos

### Pré-requisitos

Certifique-se de que todas as dependências estão instaladas:

```bash
poetry install
```

### Executar os Exemplos

```bash
# Executar exemplo básico
poetry run python examples/basic_usage.py
```

## Exemplos Disponíveis

### 1. Criar NFSE Básica

Demonstra como criar uma NFSE simples com os campos mínimos necessários:

```python
from pynfse.schemas.nfse import InfoRPS, IdentificationNFSE, ValuesNFSE, ...

# Criar identificação
identificacao = IdentificationNFSE(number=123, serie="A")

# Criar valores
valores = ValuesNFSE(
    value_services=1000.00,
    value_iss=50.00,
    base_calculation=1000.00,
    aliquot=5.0,
    liquid_value=950.00
)

# ... criar outros componentes e montar InfoRPS
```

### 2. Criar NFSE Completa

Demonstra como criar uma NFSE com todos os campos preenchidos, incluindo retenções e descontos.

### 3. Cancelar NFSE

Demonstra como criar os dados necessários para cancelar uma NFSE:

```python
from pynfse.schemas.rps import CancelNFSE

cancel_nfse = CancelNFSE(
    cnpj="12345678000190",
    municipal_registration=12345,
    municipality_code="2408102",
    number=123
)
```

### 4. Consultar NFSE

Demonstra como criar os dados para consultar uma NFSE por RPS:

```python
from pynfse.schemas.rps import ConsultNFSE

consult_nfse = ConsultNFSE(
    cnpj="12345678000190",
    municipal_registration=12345,
    number=123,
    serie="A"
)
```

### 5. Consultar Lote de NFSE

Demonstra como consultar um lote de NFSE usando o protocolo:

```python
from pynfse.schemas.rps import ConsultLoteNFSE

consult_lote = ConsultLoteNFSE(
    cnpj="12345678000190",
    municipal_registration=12345,
    protocol="12345678901234567890"
)
```

### 6. Consultar Lote de RPS

Demonstra como consultar um lote de RPS usando o protocolo.

### 7. Uso com API

Exemplo conceitual de como usar a classe `NFSeBase` para enviar NFSE e obter PDFs.

## Estrutura de Dados

### InfoRPS

A estrutura principal para criar uma NFSE é o `InfoRPS`, que contém:

- **identification**: Identificação do RPS (número, série, tipo)
- **costumer**: Dados do tomador (identificação, razão social, endereço)
- **services**: Dados do serviço (descrição, valores, códigos)
- **provider**: Dados do prestador (CNPJ, inscrição municipal)
- **date**: Data de emissão

### Valores Padrão

Muitos campos têm valores padrão que podem ser omitidos:

- `typer`: 1 (RPS)
- `nature_of_operation`: 1 (Tributação no município)
- `regime_special_tributation`: 6 (Regime especial)
- `optant_simple_national`: 1 (Sim)
- `incentivator_cultural`: 2 (Não)
- `status`: 1 (Normal)
- `item_list_service`: 106
- `code_cnae`: "6204000"
- `iss_retido`: 2 (Não)

## Validação

Todos os modelos usam Pydantic para validação automática. Campos obrigatórios são validados automaticamente:

```python
# Isso gerará um erro de validação
try:
    identificacao = IdentificationNFSE(serie="A")  # Falta 'number'
except ValidationError as e:
    print(f"Erro: {e}")
```

## Próximos Passos

1. Implementar uma classe concreta que herde de `NFSeBase`
2. Implementar os métodos abstratos de `XMLBase`
3. Configurar a URL do serviço de NFSE
4. Enviar a NFSE usando `send_nfse()`
5. Processar a resposta e obter o PDF

## Notas

- Os exemplos mostram apenas a criação dos dados. O envio real requer uma implementação concreta da classe `NFSeBase`.
- Todos os valores nos exemplos são fictícios e devem ser substituídos por dados reais.
- Certifique-se de validar os códigos IBGE, CNAE e outros códigos específicos do município.

