# 🔒 Secure MOC Report Streamlit App

A secure Streamlit application with Google OIDC authentication and user authorization.

## Features

- ✅ Google OpenID Connect (OIDC) authentication
- ✅ User email whitelist authorization
- ✅ Secure secrets management
- ✅ Works on localhost and Streamlit Cloud
- ✅ Protected content access

## Setup Instructions

### 1. Google OAuth Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Go to "Credentials" and create an OAuth 2.0 Client ID
5. Set the authorized redirect URIs:
   - For localhost: `http://localhost:8501/`
   - For Streamlit Cloud: `https://your-app-name.streamlit.app/`

### 2. Local Development Setup

1. Clone this repository
2. Install the requirements:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure your secrets in `.streamlit/secrets.toml`:

   ```toml
   [connections.gcs]
   redirect_uri = "http://localhost:8501/"
   cookie_secret = "your-secure-random-string"  # Generate a random 32+ character string
   client_id = "your-google-client-id.apps.googleusercontent.com"
   client_secret = "your-google-client-secret"
   server_metadata_url = "https://accounts.google.com/.well-known/openid_configuration"
   ```

4. Update the `ALLOWED_USERS` list in `streamlit_app.py` with authorized email addresses

5. Run the app:
   ```bash
   streamlit run streamlit_app.py
   ```

### 3. Streamlit Cloud Deployment

1. Deploy your app to Streamlit Cloud (without the `.streamlit/secrets.toml` file)

2. In your Streamlit Cloud app settings, add secrets via the Secrets Manager:

   ```toml
   [connections.gcs]
   redirect_uri = "https://your-app-name.streamlit.app/"
   cookie_secret = "your-secure-random-string"
   client_id = "your-google-client-id.apps.googleusercontent.com"
   client_secret = "your-google-client-secret"
   server_metadata_url = "https://accounts.google.com/.well-known/openid_configuration"
   ```

3. Update your Google OAuth redirect URI to match your Streamlit Cloud URL

## Security Features

- **Authentication**: Uses Google OIDC for secure user authentication
- **Authorization**: Only whitelisted email addresses can access the app
- **Secrets Management**: Sensitive credentials stored securely (not in repo)
- **Access Control**: Immediate access denial for unauthorized users

## Configuration

### Adding/Removing Users

Edit the `ALLOWED_USERS` list in `streamlit_app.py`:

```python
ALLOWED_USERS = [
    "user1@example.com",
    "user2@company.com",
    "admin@yourcompany.com",
    # Add more authorized emails here
]
```

### Environment-Specific Settings

- **Local Development**: Use `http://localhost:8501/` as redirect_uri
- **Production/Cloud**: Use your full Streamlit Cloud URL as redirect_uri

## Important Security Notes

1. **Never commit secrets**: The `.streamlit/secrets.toml` file is gitignored
2. **Use strong cookie secret**: Generate a random 32+ character string
3. **Regular access review**: Periodically review the ALLOWED_USERS list
4. **HTTPS in production**: Always use HTTPS URLs for production redirect URIs

## Troubleshooting

- **Authentication errors**: Check your Google OAuth configuration
- **Access denied**: Ensure your email is in the ALLOWED_USERS list
- **Redirect URI mismatch**: Verify the redirect_uri matches your Google OAuth settings
