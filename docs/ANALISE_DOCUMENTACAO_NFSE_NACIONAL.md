# Análise da Documentação NFS-e Nacional vs Schema Atual

## Resumo Executivo

A documentação do WebService NFS-e Nacional (versão 2.0, Dezembro 2025) apresenta **103 novos campos opcionais** além do padrão ABRASF 2.04. O schema atual do projeto cobre apenas os campos básicos do ABRASF 2.04 e **não inclui os novos campos da NFS-e Nacional**.

## Comparação: Campos Atuais vs Documentação

### ✅ Campos Já Implementados (ABRASF 2.04 Básico)

#### Identificação RPS
- ✅ `Numero` → `identification.number`
- ✅ `Serie` → `identification.serie`
- ✅ `Tipo` → `identification.typer`

#### Dados Básicos
- ✅ `DataEmissao` → `date` (mas falta formato DateTime com hora)
- ✅ `NaturezaOperacao` → `nature_of_operation`
- ✅ `RegimeEspecialTributacao` → `regime_special_tributation`
- ✅ `OptanteSimplesNacional` → `optant_simple_national`
- ✅ `IncentivadorCultural` → `incentivator_cultural`
- ✅ `Status` → `status`

#### Valores (ABRASF Básico)
- ✅ `ValorServicos` → `value_services`
- ✅ `ValorDeducoes` → `value_deductions`
- ✅ `ValorPis` → `value_pis`
- ✅ `ValorCofins` → `value_cofins`
- ✅ `ValorInss` → `value_inss`
- ✅ `ValorIr` → `value_ir`
- ✅ `ValorCsll` → `value_csll`
- ✅ `IssRetido` → `iss_retido`
- ✅ `ValorIss` → `value_iss`
- ✅ `ValorIssRetido` → `value_iss_retido`
- ✅ `OutrasRetencoes` → `others_retentions`
- ✅ `BaseCalculo` → `base_calculation`
- ✅ `Aliquota` → `aliquot`
- ✅ `ValorLiquidoNfse` → `liquid_value`
- ✅ `DescontoCondicionado` → `discount_conditioned`
- ✅ `DescontoIncondicionado` → `discount_unconditioned`

#### Serviço
- ✅ `ItemListaServico` → `item_list_service`
- ✅ `CodigoCnae` → `code_cnae`
- ✅ `CodigoTributacaoMunicipio` → `code_tributation_municipio`
- ✅ `Discriminacao` → `description`
- ✅ `CodigoMunicipio` → `code_municipio`

#### Prestador
- ✅ `Cnpj` → `provider.cnpj`
- ✅ `InscricaoMunicipal` → `provider.municipal_registration`

#### Tomador
- ✅ `CpfCnpj/Cpf` → `costumer.identification.cpf_cnpj`
- ✅ `CpfCnpj/Cnpj` → `costumer.identification.cpf_cnpj`
- ✅ `RazaoSocial` → `costumer.social_name`
- ✅ `Endereco` → `costumer.address.address`
- ✅ `Numero` → `costumer.address.number`
- ✅ `Complemento` → `costumer.address.complement`
- ✅ `Bairro` → `costumer.address.district`
- ✅ `CodigoMunicipio` → `costumer.address.ibge_code`
- ✅ `Uf` → `costumer.address.uf`
- ✅ `Cep` → `costumer.address.zip_code`

### ❌ Campos Faltantes do ABRASF 2.04

#### Tomador - Contato
- ❌ `Telefone` (Texto, 11)
- ❌ `Email` (Texto, 80)
- ❌ `InscricaoMunicipal` (no IdentificacaoTomador)

#### Intermediário do Serviço (ABRASF Básico)
- ❌ `IntermediarioServico` (bloco completo)
  - `RazaoSocial` (Texto, 115)
  - `CpfCnpj` (CPF ou CNPJ)
  - `InscricaoMunicipal` (Texto, 15)

#### Construção Civil
- ❌ `ConstrucaoCivil` (bloco completo)
  - `CodigoObra` (Texto, 15)
  - `Art` (Texto, 15)

### 🆕 Novos Campos NFS-e Nacional (103 campos) - TODOS FALTANTES

#### 1. Valores - Campos PIS/COFINS (5 campos)
- ❌ `CSTPisCofins` (Texto, 10) - Código de Situação Tributária
- ❌ `BaseCalculoPisCofins` (Decimal 15,2) - Base de cálculo
- ❌ `TipoRetencaoPisCofins` (Numérico) - 1=Retido, 2=Não retido
- ❌ `AliqPis` (Decimal 5,4) - Alíquota do PIS
- ❌ `AliqCofins` (Decimal 5,4) - Alíquota do COFINS

#### 2. Intermediário Expandido (10 campos)
- ❌ `TipoLogradouro` (Texto, 10)
- ❌ `Endereco` (Texto, 125)
- ❌ `Numero` (Texto, 10)
- ❌ `Complemento` (Texto, 60)
- ❌ `Bairro` (Texto, 60)
- ❌ `CodigoMunicipio` (Numérico, 7)
- ❌ `UF` (Texto, 2)
- ❌ `CEP` (Texto, 10)
- ❌ `Email` (Texto, 120)
- ❌ `NIF` (Texto, 40) - Número de Identificação Fiscal (estrangeiro)

#### 3. DadosDPS (12 campos)
- ❌ `TpEmit` (Texto) - Tipo do Emitente: 1=Prestador, 2=Tomador
- ❌ `TpAmb` (Inteiro) - Tipo de Ambiente: 1=Produção, 2=Homologação
- ❌ `DhEmi` (DateTime) - Data/Hora Emissão
- ❌ `VerAplic` (Texto, 20) - Versão da Aplicação
- ❌ `CLocEmi` (Inteiro) - Cód. Município Emissão
- ❌ `CLocPrestacao` (Inteiro) - Cód. Município Prestação
- ❌ `CTribNac` (Texto, 6) - Cód. Tributação Nacional
- ❌ `TribIssqn` (Inteiro) - Tributação ISSQN: 1=Normal, 2=Imune, 3=Isento, 4=Exportação
- ❌ `TpRetIssqn` (Inteiro) - Tipo Retenção ISSQN: 1=Não retido, 2=Retido tomador, 3=Retido intermediário
- ❌ `OpSimpNac` (Texto) - Optante Simples Nacional: 1=Não optante, 2=ME/EPP, 3=MEI
- ❌ `RegEspTrib` (Inteiro) - Regime Especial Tributação
- ❌ `RegApTribSN` (Texto) - Regime Apuração Tributos SN

#### 4. DadosObra (7 campos)
- ❌ `CodigoObra` (Texto, 30) - Código CNO da obra
- ❌ `InscImobFisc` (Texto, 30) - Inscrição Imobiliária Fiscal
- ❌ `EnderecoObra` (bloco com):
  - `Cep` (Texto, 10)
  - `Logradouro` (Texto, 125)
  - `Numero` (Texto, 10)
  - `Complemento` (Texto, 60)
  - `Bairro` (Texto, 60)

#### 5. ComercioExterior (11 campos)
- ❌ `MdPrestacao` (Short) - Modo de Prestação
- ❌ `VincPrest` (Short) - Vínculo Prestador/Tomador
- ❌ `TpMoeda` (Short) - Código Moeda BACEN
- ❌ `VServMoeda` (Decimal 15,2) - Valor em Moeda Estrangeira
- ❌ `MecAFComexP` (Texto, 10) - Mecanismo Apoio - Prestador
- ❌ `MecAFComexT` (Texto, 10) - Mecanismo Apoio - Tomador
- ❌ `MovTempBens` (Short) - Mov. Temporária de Bens
- ❌ `NDI` (Texto, 12) - Nº Declaração Importação
- ❌ `NRE` (Texto, 12) - Nº Registro Exportação
- ❌ `MDIC` (Short) - Enviar ao MDIC
- ❌ `CPaisResult` (Texto, 4) - Código País Resultado

#### 6. ExigibilidadeSuspensa (2 campos)
- ❌ `TpSusp` (Short) - Tipo de Suspensão: 1=Decisão Judicial, 2=Proc. Administrativo
- ❌ `NProcesso` (Texto, 30) - Número do Processo

#### 7. BeneficioMunicipal (4 campos)
- ❌ `TpBM` (Short) - Tipo do Benefício: 1=Isenção, 2=Redução BC %, 3=Redução BC R$, 4=Alíq. Diferenciada
- ❌ `NBM` (Texto, 14) - Número do Benefício Municipal
- ❌ `VRedBCBM` (Decimal 15,2) - Valor Redução da BC
- ❌ `PRedBCBM` (Decimal 15,2) - Percentual Redução da BC

#### 8. ReembolsoRepasse (3 campos)
- ❌ `TpReembRepRes` (Short) - Tipo: 1=Reembolso, 2=Repasse, 3=Ressarcimento, 9=Outros
- ❌ `XTpReembRepRes` (Texto, 2000) - Descrição (quando Tipo=9)
- ❌ `VReembRepRes` (Decimal 15,2) - Valor

#### 9. Destinatario (15 campos)
- ❌ `CnpjCpf` (Texto, 14)
- ❌ `Nome` (Texto, 115)
- ❌ `Logradouro` (Texto, 125)
- ❌ `Numero` (Texto, 10)
- ❌ `Complemento` (Texto, 60)
- ❌ `Bairro` (Texto, 60)
- ❌ `Cidade` (Texto, 60)
- ❌ `UF` (Texto, 2)
- ❌ `CEP` (Texto, 10)
- ❌ `CodMunicipio` (Numérico, 7)
- ❌ `CodPais` (Texto, 4)
- ❌ `CodPostalExt` (Texto, 10)
- ❌ `NIF` (Texto, 40)
- ❌ `Email` (Texto, 120)
- ❌ `Telefone` (Texto, 20)

#### 10. ControleIBSCBS (7 campos)
- ❌ `FinNFSe` (Short) - Finalidade da NFS-e: 0=Regular, 1=Crédito, 2=Débito
- ❌ `IndFinal` (Short) - Indicador Consumidor Final: 0=Não, 1=Sim
- ❌ `TpOper` (Short) - Tipo de Operação: 1-5 (específicos)
- ❌ `TpEnteGov` (Short) - Tipo Ente Governamental: 0=Não é, 1=União, 2=Estado, 3=DF, 4=Município, 9=Outro
- ❌ `IndDest` (Short) - Indicador de Destinatário: 0-4 (específicos)
- ❌ `CIndOp` (Texto, 6) - Código Indicador Operação
- ❌ `XTpEnteGov` (Texto, 2000) - Descrição (quando TpEnteGov=9)

#### 11. IBSCBS (28 campos)
**Base e Alíquotas:**
- ❌ `IBSCBSBaseCalculo` (Decimal 15,2)
- ❌ `IBSUFAliquota` (Decimal 15,2)
- ❌ `IBSMunAliquota` (Decimal 15,2)
- ❌ `CBSAliquota` (Decimal 15,2)

**Valores Calculados:**
- ❌ `IBSUFValor` (Decimal 15,2)
- ❌ `IBSMunValor` (Decimal 15,2)
- ❌ `CBSValor` (Decimal 15,2)

**Reduções:**
- ❌ `IBSUFPercReducao` (Decimal 15,2)
- ❌ `IBSMunPercReducao` (Decimal 15,2)
- ❌ `CBSPercReducao` (Decimal 15,2)

**Alíquotas Efetivas:**
- ❌ `IBSUFAliquotaEfetiva` (Decimal 15,2)
- ❌ `IBSMunAliquotaEfetiva` (Decimal 15,2)
- ❌ `CBSAliquotaEfetiva` (Decimal 15,2)

**Diferimento:**
- ❌ `IBSUFPercDiferimento` (Decimal 15,2)
- ❌ `IBSMunPercDiferimento` (Decimal 15,2)
- ❌ `CBSPercDiferimento` (Decimal 15,2)
- ❌ `IBSUFValorDiferido` (Decimal 15,2)
- ❌ `IBSMunValorDiferido` (Decimal 15,2)
- ❌ `CBSValorDiferido` (Decimal 15,2)

**Crédito Presumido:**
- ❌ `IBSCreditoPresumidoAliq` (Decimal 15,2)
- ❌ `IBSCreditoPresumidoValor` (Decimal 15,2)
- ❌ `CBSCreditoPresumidoAliq` (Decimal 15,2)
- ❌ `CBSCreditoPresumidoValor` (Decimal 15,2)

**Totalizadores:**
- ❌ `IBSValorTotal` (Decimal 15,2)
- ❌ `ValorTotalComTributos` (Decimal 15,2)
- ❌ `IBSValorReembolso` (Decimal 15,2)
- ❌ `LocalidadeIncidenciaCod` (Numérico, 7)
- ❌ `LocalidadeIncidenciaNome` (Texto, 2000)
- ❌ `PercRedutorCompraGov` (Decimal 15,2)

#### 12. DataCompetencia (1 campo)
- ❌ `DataCompetencia` (Date) - Data de competência (formato: AAAA-MM-DD)

## Problemas Identificados no Código Atual

### 1. Template rps.xml - Erros de Nomenclatura
- **Linha 48**: `rps.costumer.identification.cpf_cnpf` → deveria ser `cpf_cnpj` (typo)
- **Linha 55**: `rps.costumer.full_name` → deveria ser `social_name`
- **Linha 42**: `services.provider.cnpj` → deveria ser `rps.provider.cnpj`

### 2. DataEmissao
- Atualmente usa apenas `date` (sem hora)
- Documentação exige formato DateTime: `AAAA-MM-DDTHH:MM:SS`

### 3. Estrutura SOAP
- Documentação exige envelope SOAP com elementos `header` e `parameters` em CDATA
- Template atual não segue essa estrutura

### 4. LoteRps
- Schema atual não tem suporte para `LoteRps` (container que agrupa múltiplos RPS)
- Campos necessários:
  - `NumeroLote` (Numérico, 15)
  - `Cnpj` (Texto, 14)
  - `InscricaoMunicipal` (Texto, 15)
  - `QuantidadeRps` (Numérico, 4)
  - `Id` (Atributo, 255) - para assinatura digital

## Recomendações

### Prioridade Alta
1. **Corrigir erros no template** (`rps.xml`)
2. **Adicionar suporte a DateTime** para `DataEmissao`
3. **Implementar LoteRps** para envio de múltiplos RPS
4. **Adicionar Contato do Tomador** (Telefone, Email)
5. **Adicionar Intermediário** (bloco básico ABRASF)

### Prioridade Média
6. **Adicionar Construção Civil** (quando aplicável)
7. **Implementar campos PIS/COFINS** em Valores
8. **Expandir Intermediário** com endereço completo
9. **Implementar DadosDPS** (12 campos)

### Prioridade Baixa (Conforme Necessidade)
10. **Implementar blocos opcionais**:
    - DadosObra
    - ComercioExterior
    - ExigibilidadeSuspensa
    - BeneficioMunicipal
    - ReembolsoRepasse
    - Destinatario
    - ControleIBSCBS
    - IBSCBS (28 campos)
    - DataCompetencia

### Estrutura SOAP
- Implementar estrutura SOAP completa conforme documentação
- Usar CDATA para `header` e `parameters`
- Incluir namespace correto: `xmlns:nfse="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd"`

## Resumo Quantitativo

| Categoria | Campos Atuais | Campos Documentação | Faltantes |
|-----------|--------------|---------------------|-----------|
| ABRASF 2.04 Básico | ~40 | ~45 | ~5 |
| NFS-e Nacional | 0 | 103 | 103 |
| **TOTAL** | **~40** | **~148** | **~108** |

## Conclusão

O schema atual cobre aproximadamente **27%** dos campos necessários para integração completa com NFS-e Nacional. Para uma implementação completa, é necessário:

1. Corrigir bugs existentes
2. Adicionar campos faltantes do ABRASF 2.04 básico
3. Implementar os 103 novos campos da NFS-e Nacional (opcionais, conforme necessidade)
4. Ajustar estrutura SOAP conforme especificação

**Nota**: Todos os novos campos da NFS-e Nacional são **opcionais**, então a implementação pode ser feita incrementalmente conforme a necessidade de cada integração.

