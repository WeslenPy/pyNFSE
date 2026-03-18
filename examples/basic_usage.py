"""
Exemplos básicos de uso da biblioteca pyNFSE.

Este arquivo demonstra como usar a biblioteca para criar e gerenciar NFSE.
"""

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
from pynfse.schemas.rps import (
    CancelNFSE,
    ConsultNFSE,
    ConsultLoteNFSE,
    ConsultLoteRPS,
)


# ============================================================================
# EXEMPLO 1: Criar uma NFSE básica (InfoRPS)
# ============================================================================

def exemplo_criar_nfse_basica():
    """Exemplo de como criar uma NFSE básica."""
    
    # 1. Criar identificação do RPS
    identificacao = IdentificationNFSE(
        number=123,
        serie="A",
        typer=1  # 1 = RPS, 2 = NFSe Conjugada, etc.
    )
    
    # 2. Criar valores da NFSE
    valores = ValuesNFSE(
        value_services=1000.00,  # Valor dos serviços
        value_iss=50.00,  # Valor do ISS
        base_calculation=1000.00,  # Base de cálculo
        aliquot=5.0,  # Alíquota (%)
        liquid_value=950.00  # Valor líquido
        # Os demais campos têm valores padrão (0.0)
    )
    
    # 3. Criar dados do prestador
    prestador = ProviderNFSE(
        cnpj="12345678000190",
        municipal_registration=12345
    )
    
    # 4. Criar dados do serviço
    servico = ServicesNFSE(
        description="Desenvolvimento de software",
        code_municipio="2408102",  # Código IBGE do município
        values=valores
        # item_list_service, code_cnae, etc. têm valores padrão
    )
    
    # 5. Criar endereço do tomador
    endereco = AddressNFSE(
        address="Rua Exemplo",
        number="123",
        complement="Sala 101",
        district="Centro",
        ibge_code="2408102",
        uf="RN",
        zip_code="59000000"
    )
    
    # 6. Criar identificação do tomador
    identificacao_tomador = IdentificationCostumerNFSE(
        cpf_cnpj="12345678901"  # CPF ou CNPJ
    )
    
    # 7. Criar dados do tomador
    tomador = CostumerNFSE(
        identification=identificacao_tomador,
        social_name="Cliente Exemplo LTDA",
        address=endereco
    )
    
    # 8. Criar InfoRPS completo
    info_rps = InfoRPS(
        identification=identificacao,
        costumer=tomador,
        services=servico,
        provider=prestador,
        date=date.today()
        # nature_of_operation, regime_especial_tributacao, etc. têm valores padrão
    )
    
    print("NFSE criada com sucesso!")
    print(f"Número: {info_rps.identification.number}")
    print(f"Série: {info_rps.identification.serie}")
    print(f"Valor dos serviços: R$ {info_rps.services.values.value_services:.2f}")
    print(f"Valor do ISS: R$ {info_rps.services.values.value_iss:.2f}")
    
    return info_rps


# ============================================================================
# EXEMPLO 2: Criar NFSE com todos os campos preenchidos
# ============================================================================

def exemplo_criar_nfse_completa():
    """Exemplo de como criar uma NFSE com todos os campos preenchidos."""
    
    identificacao = IdentificationNFSE(
        number=456,
        serie="B",
        typer=1
    )
    
    # Valores completos com todas as retenções
    valores = ValuesNFSE(
        value_services=2000.00,
        value_deductions=100.00,
        value_pis=10.00,
        value_cofins=20.00,
        value_inss=30.00,
        value_ir=40.00,
        value_csll=50.00,
        iss_retido=1,  # 1 = Sim, 2 = Não
        value_iss=100.00,
        value_iss_retido=50.00,
        others_retentions=25.00,
        base_calculation=1900.00,
        aliquot=5.0,
        liquid_value=1800.00,
        discount_conditioned=50.00,
        discount_unconditioned=50.00
    )
    
    prestador = ProviderNFSE(
        cnpj="98765432000100",
        municipal_registration=54321
    )
    
    servico = ServicesNFSE(
        item_list_service=105,  # Item da lista de serviços
        code_cnae="6203000",  # Código CNAE
        code_tributation_municipio="620300000",  # Código de tributação
        description="Consultoria em TI e desenvolvimento de sistemas",
        code_municipio="2408102",
        values=valores
    )
    
    endereco = AddressNFSE(
        address="Avenida Principal",
        number="1000",
        complement="Edifício Comercial, 5º andar",
        district="Zona Norte",
        ibge_code="2408102",
        uf="RN",
        zip_code="59015000"
    )
    
    identificacao_tomador = IdentificationCostumerNFSE(
        cpf_cnpj="98765432000100"  # CNPJ
    )
    
    tomador = CostumerNFSE(
        identification=identificacao_tomador,
        social_name="Empresa Cliente S.A.",
        address=endereco
    )
    
    info_rps = InfoRPS(
        identification=identificacao,
        costumer=tomador,
        services=servico,
        provider=prestador,
        date=date(2024, 1, 15),
        nature_of_operation=1,  # 1 = Tributação no município
        regime_especial_tributacao=6,  # 6 = Regime especial
        optant_simple_national=1,  # 1 = Sim, 2 = Não
        incentivator_cultural=2,  # 2 = Não
        status=1  # 1 = Normal
    )
    
    print("\nNFSE completa criada!")
    print(f"Tomador: {info_rps.costumer.social_name}")
    print(f"Descrição: {info_rps.services.description}")
    print(f"Valor líquido: R$ {info_rps.services.values.liquid_value:.2f}")
    
    return info_rps


# ============================================================================
# EXEMPLO 3: Criar dados para cancelamento de NFSE
# ============================================================================

def exemplo_cancelar_nfse():
    """Exemplo de como criar dados para cancelamento de NFSE."""
    
    cancel_nfse = CancelNFSE(
        cnpj="12345678000190",
        municipal_registration=12345,
        municipality_code="2408102",
        number=123,
        cancellation_code="E12"  # Código padrão, pode ser customizado
    )
    
    print("\nDados para cancelamento criados!")
    print(f"Número da NFSE: {cancel_nfse.number}")
    print(f"Código de cancelamento: {cancel_nfse.cancellation_code}")
    
    return cancel_nfse


# ============================================================================
# EXEMPLO 4: Consultar NFSE por RPS
# ============================================================================

def exemplo_consultar_nfse():
    """Exemplo de como criar dados para consulta de NFSE."""
    
    consult_nfse = ConsultNFSE(
        cnpj="12345678000190",
        municipal_registration=12345,
        number=123,
        serie="A"
    )
    
    print("\nDados para consulta criados!")
    print(f"Número: {consult_nfse.number}")
    print(f"Série: {consult_nfse.serie}")
    
    return consult_nfse


# ============================================================================
# EXEMPLO 5: Consultar lote de NFSE
# ============================================================================

def exemplo_consultar_lote_nfse():
    """Exemplo de como consultar um lote de NFSE."""
    
    consult_lote = ConsultLoteNFSE(
        cnpj="12345678000190",
        municipal_registration=12345,
        protocol="12345678901234567890"
    )
    
    print("\nDados para consulta de lote criados!")
    print(f"Protocolo: {consult_lote.protocol}")
    
    return consult_lote


# ============================================================================
# EXEMPLO 6: Consultar lote de RPS
# ============================================================================

def exemplo_consultar_lote_rps():
    """Exemplo de como consultar um lote de RPS."""
    
    consult_lote_rps = ConsultLoteRPS(
        cnpj="12345678000190",
        municipal_registration=12345,
        protocol="98765432109876543210"
    )
    
    print("\nDados para consulta de lote RPS criados!")
    print(f"Protocolo: {consult_lote_rps.protocol}")
    
    return consult_lote_rps


# ============================================================================
# EXEMPLO 7: Uso com classe de integração (exemplo conceitual)
# ============================================================================

def exemplo_uso_com_api():
    """
    Exemplo conceitual de como usar com a classe NFSeBase.
    
    NOTA: Este é um exemplo conceitual. A implementação real depende
    da classe concreta que herda de NFSeBase e implementa os métodos abstratos.
    """
    
    # Criar a NFSE
    info_rps = exemplo_criar_nfse_basica()
    
    # Exemplo de como seria o uso (comentado porque requer implementação concreta)
    """
    from pynfse.src.common.api import NFSeBase
    
    # Inicializar cliente NFSE
    nfse_client = NFSeBase(
        URL="https://api.exemplo.com.br/nfse"
    )
    
    # Enviar NFSE
    response = nfse_client.send_nfse(info_rps)
    
    # Verificar resposta
    if response.get_status_code() == 200:
        print("NFSE enviada com sucesso!")
        json_response = response.get_json()
        print(f"Resposta: {json_response}")
    else:
        print(f"Erro ao enviar NFSE. Status: {response.get_status_code()}")
    
    # Obter URL do PDF
    url_pdf = nfse_client.get_url_pdf(
        identification_number="123456",
        nfse_id=789
    )
    print(f"URL do PDF: {url_pdf}")
    
    # Baixar PDF
    pdf_content = nfse_client.get_pdf(
        identification_number="123456",
        nfse_id=789
    )
    if pdf_content:
        with open("nfse.pdf", "wb") as f:
            f.write(pdf_content)
        print("PDF salvo com sucesso!")
    """
    
    print("\nExemplo conceitual de uso com API mostrado nos comentários.")


# ============================================================================
# EXECUTAR EXEMPLOS
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXEMPLOS DE USO DA BIBLIOTECA pyNFSE")
    print("=" * 60)
    
    # Executar exemplos
    exemplo_criar_nfse_basica()
    exemplo_criar_nfse_completa()
    exemplo_cancelar_nfse()
    exemplo_consultar_nfse()
    exemplo_consultar_lote_nfse()
    exemplo_consultar_lote_rps()
    exemplo_uso_com_api()
    
    print("\n" + "=" * 60)
    print("Todos os exemplos executados com sucesso!")
    print("=" * 60)

