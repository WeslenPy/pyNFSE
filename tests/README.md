# Testes do Projeto pyNFSE

Este diretório contém os testes automatizados do projeto pyNFSE usando pytest.

## Estrutura dos Testes

### Arquivos de Teste

- `test_schemas_nfse.py` - Testes para os modelos Pydantic de NFSE
- `test_schemas_rps.py` - Testes para os modelos Pydantic de RPS
- `test_response.py` - Testes para a classe ResponseNFSE
- `test_xml.py` - Testes para a classe XMLBase
- `test_api.py` - Testes para a classe NFSeBase
- `conftest.py` - Fixtures compartilhadas para todos os testes

## Cobertura de Testes

### Schemas (nfse.py)
- ✅ `IdentificationNFSE` - Criação com defaults, valores customizados, validação de campos obrigatórios
- ✅ `ValuesNFSE` - Criação com defaults, todos os campos, validação de campos obrigatórios
- ✅ `ProviderNFSE` - Criação e validação de campos obrigatórios
- ✅ `AddressNFSE` - Criação com defaults, todos os campos, validação de campos obrigatórios
- ✅ `IdentificationCostumerNFSE` - Criação e validação de campos obrigatórios
- ✅ `CostumerNFSE` - Criação e validação de campos obrigatórios
- ✅ `ServicesNFSE` - Criação com defaults, todos os campos, validação de campos obrigatórios
- ✅ `InfoRPS` - Criação com defaults, todos os campos, validação de campos obrigatórios

### Schemas (rps.py)
- ✅ `BaseNFSE` - Criação com defaults, todos os campos, validação de campos obrigatórios
- ✅ `CancelNFSE` - Criação com defaults, código customizado, validação de campos obrigatórios
- ✅ `ConsultNFSE` - Criação e validação de campos obrigatórios
- ✅ `ConsultLoteNFSE` - Criação e validação de campos obrigatórios
- ✅ `ConsultLoteRPS` - Criação e validação de campos obrigatórios

### ResponseNFSE (response.py)
- ✅ Inicialização
- ✅ `get_status_code()` - Diferentes códigos de status
- ✅ `get_json()` - Sucesso, exceções, diferentes tipos de erro

### XMLBase (xml.py)
- ✅ Inicialização com mocks do Jinja2
- ✅ `create_base()` - Renderização de XML base
- ✅ `create_rps_nfse()` - Método abstrato testado com implementação concreta
- ✅ `create_cancel_nfse()` - Método abstrato testado com implementação concreta
- ✅ `create_consult_nfse()` - Método abstrato testado com implementação concreta
- ✅ Propriedade `TEMPLATES`

### NFSeBase (api.py)
- ✅ Inicialização com e sem kwargs
- ✅ `send()` - Envio de XML, diferentes códigos de status
- ✅ `send_nfse()` - Envio de RPS
- ✅ `get_url_pdf()` - Geração de URL para PDF
- ✅ `get_pdf()` - Download de PDF (sucesso, não-PDF, sem Content-Type)
- ✅ Logging de debug

## Executando os Testes

### Executar todos os testes
```bash
poetry run pytest tests/ -v
```

### Executar um arquivo específico
```bash
poetry run pytest tests/test_schemas_nfse.py -v
```

### Executar uma classe de teste específica
```bash
poetry run pytest tests/test_schemas_nfse.py::TestIdentificationNFSE -v
```

### Executar um teste específico
```bash
poetry run pytest tests/test_schemas_nfse.py::TestIdentificationNFSE::test_create_identification_nfse_with_defaults -v
```

### Executar com output detalhado
```bash
poetry run pytest tests/ -v --tb=long
```

## Estatísticas

- **Total de testes**: 57
- **Taxa de sucesso**: 100%
- **Cobertura**: Todos os módulos principais do projeto estão cobertos

## Notas

- Os testes usam `unittest.mock` para mockar dependências externas (requests, jinja2)
- Fixtures compartilhadas estão em `conftest.py` para reutilização
- Todos os testes são independentes e podem ser executados em qualquer ordem

