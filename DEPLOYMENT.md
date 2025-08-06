# Streamlit Cloud Deployment Guide

## Prerequisites

- GitHub repository with your app code
- Google Cloud Console project with OAuth 2.0 configured
- Streamlit Cloud account (sign up at https://streamlit.io/cloud)

## Step 1: Prepare Your Repository

1. Ensure your repository contains:

   - `streamlit_app.py` (main app file)
   - `requirements.txt` (dependencies)
   - `README.md` (documentation)

2. **IMPORTANT**: Do NOT include `.streamlit/secrets.toml` in your repository!
   - This file should be in your `.gitignore`
   - Secrets will be configured in Streamlit Cloud

## Step 2: Configure Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project or create a new one
3. Enable the Google+ API:

   - Navigate to "APIs & Services" > "Library"
   - Search for "Google+ API" and enable it

4. Create OAuth 2.0 credentials:

   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Web application"
   - Add authorized redirect URIs:
     - `https://your-app-name.streamlit.app/` (replace with your actual app URL)

5. Note down your:
   - Client ID
   - Client Secret

## Step 3: Deploy to Streamlit Cloud

1. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with GitHub
3. Click "New app"
4. Connect your GitHub repository
5. Choose the repository and branch
6. Set the main file path to `streamlit_app.py`
7. Click "Deploy"

## Step 4: Configure Secrets in Streamlit Cloud

1. In your Streamlit Cloud app dashboard, click on "Settings"
2. Go to the "Secrets" tab
3. Add the following secrets:

```toml
[connections.gcs]
redirect_uri = "https://your-app-name.streamlit.app/"
cookie_secret = "your-secure-random-32-character-string"
client_id = "your-google-client-id.apps.googleusercontent.com"
client_secret = "your-google-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid_configuration"
```

**Important Notes:**

- Replace `your-app-name` with your actual Streamlit app name
- Generate a secure cookie_secret (32+ characters):
  Run in Python: `import secrets; print(secrets.token_urlsafe(32))`
- Use your actual Google OAuth credentials

## Step 5: Update Allowed Users

1. Edit the `ALLOWED_USERS` list in `streamlit_app.py`
2. Add the email addresses that should have access
3. Commit and push the changes to trigger a redeploy

## Step 6: Test Your Deployment

1. Visit your Streamlit Cloud app URL
2. Try logging in with an authorized Google account
3. Verify that unauthorized users are properly blocked

## Troubleshooting

### Common Issues:

1. **OAuth Error: redirect_uri_mismatch**

   - Ensure the redirect_uri in secrets matches your Streamlit app URL exactly
   - Check that the same URL is configured in Google Cloud Console

2. **Access Denied Error**

   - Verify the user's email is in the ALLOWED_USERS list
   - Check that the email case matches exactly

3. **Import Errors**

   - Ensure all required packages are in requirements.txt
   - Check Streamlit Cloud logs for specific error messages

4. **Authentication Not Working**
   - Verify all secrets are configured correctly
   - Check that Google OAuth credentials are valid
   - Ensure the Google+ API is enabled

### Security Best Practices:

- Never commit secrets to your repository
- Regularly rotate your cookie_secret
- Review allowed users list periodically
- Monitor app access logs
- Use HTTPS URLs only in production

### Support:

- Streamlit Community: https://discuss.streamlit.io/
- Streamlit Docs: https://docs.streamlit.io/
- Google OAuth Docs: https://developers.google.com/identity/protocols/oauth2
