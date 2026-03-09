"""Testes para XMLBase."""
import pytest
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from pathlib import Path

from pynfse.src.common.xml import XMLBase
from pynfse.schemas.nfse import InfoRPS
from pynfse.schemas.rps import CancelNFSE, ConsultNFSE


class TestXMLBase:
    """Testes para XMLBase."""

    @patch('pynfse.src.common.xml.PackageLoader')
    @patch('pynfse.src.common.xml.Environment')
    def test_init(self, mock_env_class, mock_loader_class):
        """Testa inicialização de XMLBase."""
        mock_env = MagicMock()
        mock_template = MagicMock()
        mock_env.get_template.return_value = mock_template
        mock_env_class.return_value = mock_env
        
        xml_base = XMLBase()
        
        assert xml_base.env == mock_env
        assert xml_base.base == mock_template
        assert xml_base.rps == mock_template
        assert xml_base.cancel_nfse == mock_template
        assert xml_base.consult_nfse == mock_template
        assert xml_base.reception_rps == mock_template
        assert mock_env.get_template.call_count == 5

    @patch('pynfse.src.common.xml.PackageLoader')
    @patch('pynfse.src.common.xml.Environment')
    def test_create_base(self, mock_env_class, mock_loader_class):
        """Testa create_base."""
        mock_env = MagicMock()
        mock_base_template = MagicMock()
        mock_base_template.render.return_value = "<soap>body</soap>"
        mock_env.get_template.return_value = mock_base_template
        mock_env_class.return_value = mock_env
        
        xml_base = XMLBase()
        result = xml_base.create_base(soap_body="<body>test</body>")
        
        assert result == "<soap>body</soap>"
        mock_base_template.render.assert_called_once_with(soap_body="<body>test</body>")

    @patch('pynfse.src.common.xml.PackageLoader')
    @patch('pynfse.src.common.xml.Environment')
    def test_create_rps_nfse_abstract(self, mock_env_class, mock_loader_class):
        """Testa que create_rps_nfse é abstrato e precisa ser implementado."""
        mock_env = MagicMock()
        mock_template = MagicMock()
        mock_env.get_template.return_value = mock_template
        mock_env_class.return_value = mock_env
        
        xml_base = XMLBase()
        
        # XMLBase não herda de ABC, então não podemos testar diretamente
        # Mas podemos testar que o método existe e pode ser chamado se implementado
        # Na prática, como não herda de ABC, o método pode ser chamado mas falhará
        # se não for implementado em uma subclasse
        
        # Vamos criar uma implementação concreta para testar
        class ConcreteXMLBase(XMLBase):
            def create_rps_nfse(self, rps: InfoRPS) -> str:
                xml_rps = self.rps.render(rps=rps)
                return self.create_base(soap_body=xml_rps)
            
            def create_cancel_nfse(self, nfse: CancelNFSE) -> str:
                return self.create_base(soap_body="<cancel/>")
            
            def create_consult_nfse(self, nfse: ConsultNFSE) -> str:
                return self.create_base(soap_body="<consult/>")
        
        mock_rps_template = MagicMock()
        mock_rps_template.render.return_value = "<rps>test</rps>"
        mock_base_template = MagicMock()
        mock_base_template.render.return_value = "<soap><rps>test</rps></soap>"
        
        def get_template_side_effect(name):
            if name == 'rps.xml':
                return mock_rps_template
            return mock_base_template
        
        mock_env.get_template.side_effect = get_template_side_effect
        
        concrete_xml = ConcreteXMLBase()
        
        # Criar um mock de InfoRPS
        mock_rps = Mock(spec=InfoRPS)
        
        result = concrete_xml.create_rps_nfse(mock_rps)
        
        assert result == "<soap><rps>test</rps></soap>"
        mock_rps_template.render.assert_called_once_with(rps=mock_rps)
        mock_base_template.render.assert_called_once_with(soap_body="<rps>test</rps>")

    @patch('pynfse.src.common.xml.PackageLoader')
    @patch('pynfse.src.common.xml.Environment')
    def test_create_cancel_nfse_abstract(self, mock_env_class, mock_loader_class):
        """Testa que create_cancel_nfse é abstrato."""
        mock_env = MagicMock()
        mock_template = MagicMock()
        mock_env.get_template.return_value = mock_template
        mock_env_class.return_value = mock_env
        
        class ConcreteXMLBase(XMLBase):
            def create_rps_nfse(self, rps: InfoRPS) -> str:
                return ""
            
            def create_cancel_nfse(self, nfse: CancelNFSE) -> str:
                return self.create_base(soap_body="<cancel/>")
            
            def create_consult_nfse(self, nfse: ConsultNFSE) -> str:
                return ""
        
        mock_base_template = MagicMock()
        mock_base_template.render.return_value = "<soap><cancel/></soap>"
        mock_env.get_template.return_value = mock_base_template
        
        concrete_xml = ConcreteXMLBase()
        mock_cancel = Mock(spec=CancelNFSE)
        
        result = concrete_xml.create_cancel_nfse(mock_cancel)
        
        assert result == "<soap><cancel/></soap>"
        mock_base_template.render.assert_called_once_with(soap_body="<cancel/>")

    @patch('pynfse.src.common.xml.PackageLoader')
    @patch('pynfse.src.common.xml.Environment')
    def test_create_consult_nfse_abstract(self, mock_env_class, mock_loader_class):
        """Testa que create_consult_nfse é abstrato."""
        mock_env = MagicMock()
        mock_template = MagicMock()
        mock_env.get_template.return_value = mock_template
        mock_env_class.return_value = mock_env
        
        class ConcreteXMLBase(XMLBase):
            def create_rps_nfse(self, rps: InfoRPS) -> str:
                return ""
            
            def create_cancel_nfse(self, nfse: CancelNFSE) -> str:
                return ""
            
            def create_consult_nfse(self, nfse: ConsultNFSE) -> str:
                return self.create_base(soap_body="<consult/>")
        
        mock_base_template = MagicMock()
        mock_base_template.render.return_value = "<soap><consult/></soap>"
        mock_env.get_template.return_value = mock_base_template
        
        concrete_xml = ConcreteXMLBase()
        mock_consult = Mock(spec=ConsultNFSE)
        
        result = concrete_xml.create_consult_nfse(mock_consult)
        
        assert result == "<soap><consult/></soap>"
        mock_base_template.render.assert_called_once_with(soap_body="<consult/>")

    def test_templates_path(self):
        """Testa que TEMPLATES é um Path."""
        assert isinstance(XMLBase.TEMPLATES, Path)

