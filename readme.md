# pyNFSE - Integração com NFSe (Nota Fiscal de Serviço Eletrônica)

Biblioteca Python para geração, assinatura e comunicação com Web Services de Nota Fiscal de Serviço Eletrônica (NFSe), com foco inicial no padrão ABRASF v1 (Provedor Carnaubal/SpeedGov).

## 🚀 Características

- **Modelagem com Pydantic**: Estruturas XML definidas como classes Python fortemente tipadas, garantindo validação de dados antes mesmo da geração do XML.
- **Assinatura Digital Integrada**: Suporte a certificados PEM e PFX (PKCS#12) com assinatura XMLDSIG (SHA256) automática.
- **Envelope SOAP Genérico**: Geração dinâmica de envelopes SOAP 1.1 com suporte a seções CDATA, conforme exigido por muitos órgãos governamentais.
- **Parser Inteligente**: Conversão automática de respostas XML/SOAP para dicionários Python ou modelos Pydantic, removendo namespaces e envelopes desnecessários.
- **Cache de Recursos**: Sistema de cache em memória para certificados e arquivos XML remotos.

## 🛠️ Tecnologias Utilizadas

- [Python 3.11+](https://www.python.org/)
- [Pydantic v2](https://docs.pydantic.dev/) para modelagem e validação.
- [lxml](https://lxml.de/) para manipulação performática de XML.
- [signxml](https://github.com/XML-Security/signxml) para assinaturas digitais.
- [cryptography](https://cryptography.io/) para tratamento de certificados.
- [xmltodict](https://github.com/martinblech/xmltodict) para conversão XML -> Dict.

## 📂 Estrutura do Projeto

```text
pynfse/
├── src/
│   ├── common/                # Componentes genéricos (API base, XML, Assinatura)
│   │   ├── api.py             # Classe base para provedores e parser de resposta
│   │   ├── xml_node.py        # Base para serialização Pydantic -> XML
│   │   └── signature.py       # Modelos para XML Digital Signature
│   └── integration/
│       └── carnaubal/         # Implementação específica (Provedor Carnaubal)
│           └── abrasf/
│               ├── models/    # Modelos Pydantic (RPS, Lote, Respostas)
│               └── nfse.py    # Classe principal do provedor
└── tests/                     # Suíte de testes unitários e de integração
```

## 💻 Como Usar

### 1. Configuração do Provedor

```python
from pynfse.src.integration.carnaubal.abrasf.nfse import CarnaubalNFSe

# Inicializa o provedor com a URL do Web Service
provider = CarnaubalNFSe(URL="https://homologacao.speedgov.com.br/carnaubal/ws")
```

### 2. Geração e Assinatura de Lote RPS

```python
from pynfse.src.integration.carnaubal.abrasf.models.rps import Rps, InfRps
# ... importe outros modelos necessários (IdentificacaoRps, DadosServico, etc)

# 1. Carrega o certificado (URL ou Local)
cert_data = provider.get_certificate("caminho/para/certificado.pfx")

# 2. Cria os modelos de dados
rps = Rps(inf_rps=InfRps(...))

# 3. Gera a assinatura para o elemento
lote_xml_element = lote_model.to_element()
signature = provider.generate_signature(lote_xml_element, cert_data, password="senha")

# 4. Atribui a assinatura e gera o XML final
lote_model.signature = signature
xml_final = lote_model.to_xml()
```

### 3. Processamento de Resposta

```python
from pynfse.src.integration.carnaubal.abrasf.models.respostas import EnviarLoteRpsResposta

# Envia o XML e obtém a resposta bruta
response_nfse = provider.send(xml_final)

# Converte a resposta (limpando SOAP/Namespaces) para o modelo Pydantic
resposta = provider.parse_response(response_nfse.text)
# Agora você tem um dicionário limpo ou pode instanciar o modelo:
resultado = EnviarLoteRpsResposta(**resposta)

print(f"Protocolo recebido: {resultado.protocolo}")
```

## 🧪 Testes

Para rodar a suíte de testes completa:

```bash
poetry run pytest -vv
```

