import unittest
from unittest.mock import patch, MagicMock
from oauthc import OAuthHandler

class TestOAuthHandler(unittest.TestCase):

    @patch('oauthc.OAuth2Session')
    def test_handle_home(self, MockOAuth2Session):
        mock_session = MockOAuth2Session.return_value
        mock_session.authorization_url.return_value = ('http://example.com', 'state')

        handler = OAuthHandler()
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()
        handler.wfile = MagicMock()

        handler.handle_home()

        handler.send_response.assert_called_with(200)
        handler.send_header.assert_called_with('Content-type', 'text/html')
        handler.end_headers.assert_called_once()
        handler.wfile.write.assert_called_once()

    @patch('oauthc.OAuth2Session')
    @patch('oauthc.requests')
    def test_handle_callback(self, MockRequests, MockOAuth2Session):
        mock_session = MockOAuth2Session.return_value
        mock_session.fetch_token.return_value = {
            'access_token': 'token',
            'token_type': 'Bearer',
            'id_token': 'header.payload.signature'
        }

        handler = OAuthHandler()
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()
        handler.wfile = MagicMock()

        query_params = {'code': 'auth_code', 'state': 'state'}
        handler.handle_callback(query_params)

        handler.send_response.assert_called_with(200)
        handler.send_header.assert_called_with('Content-type', 'text/html')
        handler.end_headers.assert_called_once()
        handler.wfile.write.assert_called_once()

    @patch('oauthc.requests')
    def test_handle_userinfo(self, MockRequests):
        mock_response = MockRequests.get.return_value
        mock_response.status_code = 200
        mock_response.text = '{"name": "John Doe"}'

        handler = OAuthHandler()
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()
        handler.wfile = MagicMock()

        query_params = {'token_type': 'Bearer', 'access_token': 'token'}
        handler.handle_userinfo(query_params)

        handler.send_response.assert_called_with(200)
        handler.send_header.assert_called_with('Content-type', 'text/html')
        handler.end_headers.assert_called_once()
        handler.wfile.write.assert_called_once()

if __name__ == '__main__':
    unittest.main()
