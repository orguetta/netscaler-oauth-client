#!/usr/bin/env python3

# Simple client for testing with NetScaler OAuth IDP
# Compatible with Python 3.13+ (no cgi module)
# Usage: python3 oauthc.py

import base64
import ssl
import logging
import os
import urllib.parse
import http.server
import socketserver
import json
from http import cookies

import requests
from requests_oauthlib import OAuth2Session

# Get configuration from environment variables or use defaults
client_id = os.environ.get('CLIENT_ID', 'oauthc')
client_secret = os.environ.get('CLIENT_SECRET', 'secret')
host_name = os.environ.get('HOST_NAME', 'localhost')
port = int(os.environ.get('PORT', 8000))
redirect_uri = os.environ.get('REDIRECT_URI', f'http://{host_name}:{port}/callback')
idp_login_url = os.environ.get('IDP_LOGIN_URL', 'https://AUTH_VSERVER/oauth/idp/login')
idp_token_url = os.environ.get('IDP_TOKEN_URL', 'https://AUTH_VSERVER/oauth/idp/token')
idp_info_url = os.environ.get('IDP_INFO_URL', 'https://AUTH_VSERVER/oauth/idp/userinfo')

# Disable SSL verification (use only for testing!)
requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context
logging.basicConfig(level=logging.INFO)

# Global variable to store OAuth state
oauth_state = None

class OAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global oauth_state
        
        # Parse the URL path and query parameters
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = dict(urllib.parse.parse_qsl(parsed_url.query))
        
        # Log the request
        logging.info(f"Request: {path} with params: {query_params}")
        
        # Handle each route
        if path == '/callback' and 'code' in query_params and 'state' in query_params:
            self.handle_callback(query_params)
        elif path == '/userinfo' and 'token_type' in query_params and 'access_token' in query_params:
            self.handle_userinfo(query_params)
        else:
            self.handle_home()
    
    def handle_home(self):
        """Display welcome page and redirect to authentication dialog"""
        global oauth_state
        
        oa2sess = OAuth2Session(
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=["openid"],
        )
        
        authorization_url, state = oa2sess.authorization_url(url=idp_login_url)
        oauth_state = state
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = f"""
        <html>
        <head>
        <title>oauthc - Start login</title>
        <meta http-equiv="Refresh" content="0; url={authorization_url}">
        </head>
        <body>
        <h1>Start login</h1>
        <p><a href="{authorization_url}">Start login</a></p>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode('utf-8'))
    
    def handle_callback(self, query_params):
        """Process the authorization code callback"""
        global oauth_state
        
        code = query_params.get('code')
        state = query_params.get('state')
        
        oa2sess = OAuth2Session(
            client_id=client_id,
            redirect_uri=redirect_uri,
            state=state,
        )
        
        try:
            token_dict = oa2sess.fetch_token(
                token_url=idp_token_url,
                client_secret=client_secret,
                code=code,
                verify=False,
            )
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <html>
            <head>
            <title>oauthc - Login result</title>
            </head>
            <body>
            <h1>Login result</h1>
            <table border="1">
            <tr><th>Key</th><th>Value</th></tr>
            """
            
            # Display all properties of the user token
            for k, v in token_dict.items():
                html += f"<tr><td>{k}</td><td>{v}</td></tr>\n"
            
            # Parse JWT if present
            if "id_token" in token_dict:
                jwt_parts = token_dict["id_token"].split(".")
                if len(jwt_parts) == 3:
                    # Handle padding for base64 decoding
                    padded = jwt_parts[1] + '=' * (4 - len(jwt_parts[1]) % 4)
                    try:
                        decoded = base64.b64decode(padded).decode('utf-8')
                        html += f"<tr><td>id_token (jwt message)</td><td>{decoded}</td></tr>\n"
                    except Exception as e:
                        html += f"<tr><td>id_token decode error</td><td>{str(e)}</td></tr>\n"
            
            html += "</table><br>\n"
            
            # Link for userinfo URL
            if "token_type" in token_dict and "access_token" in token_dict:
                token_type = urllib.parse.quote(token_dict["token_type"])
                access_token = urllib.parse.quote(token_dict["access_token"])
                html += f'<a href="/userinfo?token_type={token_type}&access_token={access_token}">Userinfo</a><br>\n'
            
            html += '<a href="/">Home</a></body></html>'
            
            self.wfile.write(html.encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = f"""
            <html>
            <head><title>OAuth Error</title></head>
            <body>
            <h1>Error fetching token</h1>
            <p>{str(e)}</p>
            <a href="/">Try again</a>
            </body>
            </html>
            """
            
            self.wfile.write(html.encode('utf-8'))
    
    def handle_userinfo(self, query_params):
        """Fetch and display user info"""
        token_type = query_params.get('token_type')
        access_token = query_params.get('access_token')
        
        headers = {
            "Authorization": f"{token_type} {access_token}"
        }
        
        try:
            response = requests.get(idp_info_url, headers=headers, verify=False)
            status_code = response.status_code
            response_text = response.text
            
            # Try to pretty print JSON if the response is JSON
            try:
                json_data = json.loads(response_text)
                response_text = json.dumps(json_data, indent=2)
            except:
                pass
            
        except Exception as e:
            status_code = "Error"
            response_text = str(e)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = f"""
        <html>
        <head>
        <title>oauthc - Userinfo</title>
        </head>
        <body>
        <h1>Userinfo</h1>
        <p>Status: {status_code}</p>
        <pre>{response_text}</pre>
        <a href="/">Home</a>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode('utf-8'))


def run_server():
    """Run the HTTP server"""
    with socketserver.TCPServer(("0.0.0.0", port), OAuthHandler) as httpd:
        print(f"Serving at http://{host_name}:{port}")
        print(f"OAuth Client configured with:")
        print(f"  Client ID: {client_id}")
        print(f"  Redirect URI: {redirect_uri}")
        print(f"  IDP Login URL: {idp_login_url}")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()