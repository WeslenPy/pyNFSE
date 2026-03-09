"""Testes para ResponseNFSE."""
import pytest
from unittest.mock import Mock
from requests import Response

from pynfse.src.common.response import ResponseNFSE


class TestResponseNFSE:
    """Testes para ResponseNFSE."""

    def test_init(self, mock_response):
        """Testa inicialização de ResponseNFSE."""
        xml = "<xml>test</xml>"
        response_nfse = ResponseNFSE(xml, mock_response)
        
        assert response_nfse.xml == xml
        assert response_nfse.response == mock_response

    def test_get_status_code(self, mock_response):
        """Testa get_status_code."""
        mock_response.status_code = 200
        response_nfse = ResponseNFSE("<xml>test</xml>", mock_response)
        
        assert response_nfse.get_status_code() == 200

    def test_get_status_code_different_values(self, mock_response):
        """Testa get_status_code com diferentes códigos."""
        for status_code in [200, 201, 400, 404, 500]:
            mock_response.status_code = status_code
            response_nfse = ResponseNFSE("<xml>test</xml>", mock_response)
            assert response_nfse.get_status_code() == status_code

    def test_get_json_success(self, mock_response):
        """Testa get_json com resposta JSON válida."""
        expected_json = {"status": "ok", "data": {"id": 123}}
        mock_response.json.return_value = expected_json
        
        response_nfse = ResponseNFSE("<xml>test</xml>", mock_response)
        result = response_nfse.get_json()
        
        assert result == expected_json
        mock_response.json.assert_called_once()

    def test_get_json_empty_dict_on_exception(self, mock_response):
        """Testa get_json retorna {} quando há exceção."""
        mock_response.json.side_effect = ValueError("Invalid JSON")
        
        response_nfse = ResponseNFSE("<xml>test</xml>", mock_response)
        result = response_nfse.get_json()
        
        assert result == {}

    def test_get_json_with_different_exceptions(self, mock_response):
        """Testa get_json com diferentes tipos de exceção."""
        exceptions = [
            ValueError("Invalid JSON"),
            TypeError("Not JSON"),
            Exception("Generic error")
        ]
        
        for exc in exceptions:
            mock_response.json.side_effect = exc
            response_nfse = ResponseNFSE("<xml>test</xml>", mock_response)
            result = response_nfse.get_json()
            assert result == {}

    def test_get_json_with_none_response(self):
        """Testa get_json quando response é None."""
        mock_response = Mock(spec=Response)
        mock_response.json.side_effect = AttributeError("'NoneType' object has no attribute 'json'")
        
        response_nfse = ResponseNFSE("<xml>test</xml>", mock_response)
        result = response_nfse.get_json()
        
        assert result == {}

