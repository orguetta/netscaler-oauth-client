# NetScaler OAuth IDP Client

This is a simple OAuth 2.0 client for testing with NetScaler OAuth IDP.

## Setup

1. Update the `.env` file with your specific OAuth configuration:
   - `CLIENT_ID`: Your OAuth client ID
   - `CLIENT_SECRET`: Your OAuth client secret
   - `REDIRECT_URI`: The redirect URI (default: http://localhost:8000/cgi-bin/oauthc.py)
   - `IDP_LOGIN_URL`: Your NetScaler OAuth IDP login URL
   - `IDP_TOKEN_URL`: Your NetScaler OAuth IDP token URL
   - `IDP_INFO_URL`: Your NetScaler OAuth IDP userinfo URL
   - `HOST_NAME`: Your hostname (default: localhost)

2. Create a `cgi-bin` directory to hold the script:
   ```
   mkdir -p cgi-bin
   ```

3. Start the application using Docker Compose:
   ```
   docker-compose up -d
   ```

4. Access the OAuth client in your web browser:
   ```
   http://localhost:8000/cgi-bin/oauthc.py
   ```

## Notes

- This client disables SSL verification for testing purposes. In production, you should enable proper SSL verification.
- You may need to modify the redirect URI in your OAuth provider's configuration to match the one used in this application.
- Make sure your NetScaler OAuth IDP is properly configured to accept requests from this client.

## Files

- `docker-compose.yml`: Docker Compose configuration
- `Dockerfile`: Docker image definition
- `.env`: Environment variable configuration
- `entrypoint.sh`: Script to initialize the application
- `cgi-bin/oauthc.py`: Generated OAuth client script
