# pyNFSE

Biblioteca Python para geração e gerenciamento de Nota Fiscal de Serviços Eletrônica (NFSE).

## Características

- ✅ Modelos Pydantic para validação de dados
- ✅ Suporte para criação de NFSE, cancelamento e consultas
- ✅ Estrutura extensível para diferentes municípios
- ✅ Testes completos com pytest
- ✅ Documentação e exemplos práticos

## Instalação

```bash
# Usando Poetry (recomendado)
poetry install

# Ou usando pip
pip install -e .
```

## Uso Rápido

```python
from datetime import date
from pynfse.schemas.nfse import (
    InfoRPS,
    IdentificationNFSE,
    ValuesNFSE,
    ProviderNFSE,
    ServicesNFSE,
    IdentificationCostumerNFSE,
    AddressNFSE,
    CostumerNFSE,
)

# Criar valores
valores = ValuesNFSE(
    value_services=1000.00,
    value_iss=50.00,
    base_calculation=1000.00,
    aliquot=5.0,
    liquid_value=950.00
)

# Criar NFSE
nfse = InfoRPS(
    identification=IdentificationNFSE(number=1, serie="A"),
    costumer=CostumerNFSE(
        identification=IdentificationCostumerNFSE(cpf_cnpj="12345678901"),
        social_name="Cliente Exemplo",
        address=AddressNFSE(
            address="Rua Exemplo",
            number="123",
            district="Centro",
            uf="RN",
            zip_code="59000000"
        )
    ),
    services=ServicesNFSE(
        description="Desenvolvimento de software",
        code_municipio="2408102",
        values=valores
    ),
    provider=ProviderNFSE(
        cnpj="12345678000190",
        municipal_registration=12345
    ),
    date=date.today()
)
```

## Exemplos

Consulte a pasta `examples/` para exemplos completos:

- **Quick Start**: `examples/quick_start.py` - Exemplo mínimo para começar
- **Uso Básico**: `examples/basic_usage.py` - Exemplos completos de uso
- **Documentação**: `examples/README.md` - Guia detalhado dos exemplos

### Executar Exemplos

```bash
# Quick Start
poetry run python examples/quick_start.py

# Exemplos completos
poetry run python examples/basic_usage.py
```

## Estrutura do Projeto

```
pynfse/
├── schemas/          # Modelos Pydantic (NFSE, RPS)
├── src/
│   ├── common/      # Classes base (API, XML, Response)
│   └── integration/ # Implementações específicas por município
└── tests/           # Testes automatizados
```

## Funcionalidades

### Schemas Disponíveis

#### NFSE
- `IdentificationNFSE` - Identificação do RPS
- `ValuesNFSE` - Valores e impostos
- `ProviderNFSE` - Dados do prestador
- `ServicesNFSE` - Dados do serviço
- `CostumerNFSE` - Dados do tomador
- `InfoRPS` - Estrutura completa da NFSE

#### RPS (Requisições)
- `BaseNFSE` - Classe base para requisições
- `CancelNFSE` - Cancelamento de NFSE
- `ConsultNFSE` - Consulta de NFSE
- `ConsultLoteNFSE` - Consulta de lote de NFSE
- `ConsultLoteRPS` - Consulta de lote de RPS

### Classes Principais

- `NFSeBase` - Classe base para integração com serviços de NFSE
- `XMLBase` - Classe base para geração de XML
- `ResponseNFSE` - Wrapper para respostas da API

## Testes

Execute os testes com:

```bash
poetry run pytest tests/ -v
```

Todos os 57 testes devem passar com sucesso.

## Documentação

- **Testes**: Veja `tests/README.md` para documentação dos testes
- **Exemplos**: Veja `examples/README.md` para guia de exemplos

## Desenvolvimento

### Pré-requisitos

- Python 3.11+
- Poetry

### Instalação do Ambiente de Desenvolvimento

```bash
# Instalar dependências
poetry install --with dev

# Executar testes
poetry run pytest tests/ -v
```

## Licença

Este projeto está sob licença MIT.

## Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Autor

weslenpy - weslenjhony@gmail.com

