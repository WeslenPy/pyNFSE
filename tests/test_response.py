"""Testes para ResponseNFSE."""
import httpx
from unittest.mock import Mock

from pynfse.common.response import ResponseNFSE


class TestResponseNFSE:
    """Testes para ResponseNFSE."""

    def test_init(self):
        xml = "<xml>test</xml>"
        mock_response = httpx.Response(200, content=b"<xml>response</xml>")
        response_nfse = ResponseNFSE(xml, mock_response)

        assert response_nfse.xml == xml
        assert response_nfse.response == mock_response

    def test_get_status_code(self):
        response_nfse = ResponseNFSE("<xml>test</xml>", httpx.Response(200))
        assert response_nfse.get_status_code() == 200

    def test_get_status_code_different_values(self):
        for status_code in [200, 201, 400, 404, 500]:
            response_nfse = ResponseNFSE("<xml>test</xml>", httpx.Response(status_code))
            assert response_nfse.get_status_code() == status_code

    def test_get_json_success(self):
        expected_json = {"status": "ok", "data": {"id": 123}}
        resp = httpx.Response(200, json=expected_json)
        response_nfse = ResponseNFSE("<xml>test</xml>", resp)
        result = response_nfse.get_json()

        assert result == expected_json

    def test_get_json_empty_dict_on_invalid_body(self):
        resp = httpx.Response(
            200,
            content=b"not json",
            headers={"Content-Type": "application/json"},
        )
        response_nfse = ResponseNFSE("<xml>test</xml>", resp)
        result = response_nfse.get_json()

        assert result == {}

    def test_get_json_with_mock_exception(self):
        mock_resp = Mock(spec=httpx.Response)
        mock_resp.json.side_effect = ValueError("Invalid JSON")

        response_nfse = ResponseNFSE("<xml>test</xml>", mock_resp)
        result = response_nfse.get_json()

        assert result == {}

    def test_get_json_with_different_exceptions(self):
        exceptions = [
            ValueError("Invalid JSON"),
            TypeError("Not JSON"),
            Exception("Generic error"),
        ]

        for exc in exceptions:
            mock_resp = Mock(spec=httpx.Response)
            mock_resp.json.side_effect = exc
            response_nfse = ResponseNFSE("<xml>test</xml>", mock_resp)
            result = response_nfse.get_json()
            assert result == {}

    def test_get_json_when_json_raises_attribute_error(self):
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.side_effect = AttributeError("'NoneType' object has no attribute 'json'")

        response_nfse = ResponseNFSE("<xml>test</xml>", mock_response)
        result = response_nfse.get_json()

        assert result == {}
