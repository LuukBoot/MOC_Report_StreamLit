# Streamlit Cloud Deployment Guide

## Step 1: Update Google OAuth Configuration

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "APIs & Services" > "Credentials"
3. Find your OAuth 2.0 Client ID
4. Edit the "Authorized redirect URIs" to include:
   - `http://localhost:8501` (for local development)
   - `https://your-app-name.streamlit.app` (for Streamlit Cloud)

**Note**: Replace `your-app-name` with your actual Streamlit Cloud app name.

## Step 2: Deploy to Streamlit Cloud

1. **Push to GitHub**: Make sure your code is pushed to GitHub

   ```powershell
   git add .
   git commit -m "Ready for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Go to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io)

3. **Connect GitHub**: Sign in with GitHub and authorize Streamlit

4. **Deploy App**:
   - Click "New app"
   - Select your repository: `LuukBoot/MOC_Report_StreamLit`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
   - App URL: Choose a unique name (e.g., `moc-report-secure`)

## Step 3: Configure Secrets in Streamlit Cloud

1. After deploying, go to your app's settings
2. Click on "Secrets" in the left sidebar
3. Add the following secrets:

```toml
[connections.gcs]
redirect_uri = "https://your-app-name.streamlit.app"
cookie_secret = "your-secure-random-string"
client_id = "your-google-client-id"
client_secret = "your-google-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid_configuration"
```

4. Replace the values with your actual credentials
5. **Important**: Use your Streamlit Cloud URL for `redirect_uri`

## Step 4: Update Google OAuth Redirect URI

1. Go back to Google Cloud Console
2. Update your OAuth redirect URI to: `https://your-app-name.streamlit.app`
3. Save the changes

## Step 5: Test Your Deployment

1. Visit your Streamlit Cloud app URL
2. Test the Google OAuth login
3. Verify that only whitelisted users can access the app

## Troubleshooting

### Common Issues:

1. **OAuth Error**: Make sure redirect URI in Google Console matches your Streamlit Cloud URL exactly
2. **Secrets Error**: Double-check that all secrets are properly configured in Streamlit Cloud
3. **Module Not Found**: Ensure all dependencies are listed in `requirements.txt`

### Security Notes:

- Never commit `.streamlit/secrets.toml` to GitHub
- Use strong, unique values for `cookie_secret`
- Regularly rotate your OAuth credentials
- Monitor access logs in Google Cloud Console

## App URL Structure

Your app will be available at:
`https://your-chosen-name.streamlit.app`

Example: `https://moc-report-secure.streamlit.app`
