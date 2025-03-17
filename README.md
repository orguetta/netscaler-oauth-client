# NetScaler OAuth IDP Client

This is a simple OAuth 2.0 client for testing with NetScaler OAuth IDP.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/orguetta/netscaler_oauth-client.git
   cd netscaler_oauth-client
   ```

2. Update the `.env` file with your specific OAuth configuration:
   - `CLIENT_ID`: Your OAuth client ID
   - `CLIENT_SECRET`: Your OAuth client secret
   - `REDIRECT_URI`: The redirect URI (default: http://localhost:8000/callback)
   - `IDP_LOGIN_URL`: Your NetScaler OAuth IDP login URL
   - `IDP_TOKEN_URL`: Your NetScaler OAuth IDP token URL
   - `IDP_INFO_URL`: Your NetScaler OAuth IDP userinfo URL
   - `HOST_NAME`: Your hostname (default: localhost)

3. Create a `cgi-bin` directory to hold the script:
   ```
   mkdir -p cgi-bin
   ```

4. Start the application using Docker Compose:
   ```
   docker-compose up -d
   ```

5. Access the OAuth client in your web browser:
   ```
   http://localhost:8000
   ```

## Running the Application

To run the application locally without Docker, follow these steps:

1. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python oauthc.py
   ```

4. Access the OAuth client in your web browser:
   ```
   http://localhost:8000
   ```

## Contributing

We welcome contributions to this project! If you would like to contribute, please follow these guidelines:

1. Fork the repository and create a new branch for your feature or bugfix.
2. Make your changes and ensure that the code passes all tests.
3. Submit a pull request with a clear description of your changes.

For more detailed information, please refer to the `CONTRIBUTING.md` file.

## Notes

- This client disables SSL verification for testing purposes. In production, you should enable proper SSL verification.
- You may need to modify the redirect URI in your OAuth provider's configuration to match the one used in this application.
- Make sure your NetScaler OAuth IDP is properly configured to accept requests from this client.

## Files

- `docker-compose.yml`: Docker Compose configuration
- `Dockerfile`: Docker image definition
- `.env`: Environment variable configuration
- `oauthc.py`: OAuth client script
