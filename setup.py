#!/usr/bin/env python3
"""
Setup script for MOC Report Streamlit App
This script helps you configure the initial setup for your secure Streamlit app.
"""

import os
import secrets
import shutil
from pathlib import Path


def generate_cookie_secret():
    """Generate a secure cookie secret"""
    return secrets.token_urlsafe(32)


def setup_secrets():
    """Setup the secrets.toml file"""
    print("🔧 Setting up secrets configuration...")

    # Create .streamlit directory if it doesn't exist
    streamlit_dir = Path(".streamlit")
    streamlit_dir.mkdir(exist_ok=True)

    secrets_file = streamlit_dir / "secrets.toml"
    example_file = streamlit_dir / "secrets.toml.example"

    if secrets_file.exists():
        print(f"⚠️  {secrets_file} already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return

    # Generate secure cookie secret
    cookie_secret = generate_cookie_secret()

    # Get user inputs
    print("\n📝 Please provide your Google OAuth configuration:")
    client_id = input("Google Client ID: ").strip()
    client_secret = input("Google Client Secret: ").strip()

    print("\n🌐 Environment Configuration:")
    print("1. Localhost development")
    print("2. Streamlit Cloud production")
    env_choice = input("Choose environment (1 or 2): ").strip()

    if env_choice == "1":
        redirect_uri = "http://localhost:8501/"
    elif env_choice == "2":
        app_name = input("Enter your Streamlit Cloud app name: ").strip()
        redirect_uri = f"https://{app_name}.streamlit.app/"
    else:
        redirect_uri = "http://localhost:8501/"
        print("⚠️  Invalid choice, defaulting to localhost")

    # Create secrets.toml content
    secrets_content = f'''# Google OIDC Configuration
# IMPORTANT: Do not commit this file to GitHub!
# Use Streamlit's Secrets Manager when deploying to Streamlit Cloud

[connections.gcs]
redirect_uri = "{redirect_uri}"
cookie_secret = "{cookie_secret}"
client_id = "{client_id}"
client_secret = "{client_secret}"
server_metadata_url = "https://accounts.google.com/.well-known/openid_configuration"
'''

    # Write secrets file
    with open(secrets_file, 'w') as f:
        f.write(secrets_content)

    print(f"✅ Created {secrets_file}")
    print(f"🔐 Generated secure cookie secret")
    print(f"🌐 Configured for: {redirect_uri}")


def setup_allowed_users():
    """Setup allowed users in the main app file"""
    print("\n👥 Setting up allowed users...")

    app_file = Path("streamlit_app.py")
    if not app_file.exists():
        print("❌ streamlit_app.py not found!")
        return

    print("Current allowed users will be replaced.")
    print("Enter email addresses (one per line, empty line to finish):")

    allowed_users = []
    while True:
        email = input("Email: ").strip()
        if not email:
            break
        allowed_users.append(email)

    if not allowed_users:
        print("⚠️  No users added, keeping default configuration")
        return

    # Read current file
    with open(app_file, 'r') as f:
        content = f.read()

    # Replace ALLOWED_USERS list
    new_users_list = "ALLOWED_USERS = [\n"
    for email in allowed_users:
        new_users_list += f'    "{email}",\n'
    new_users_list += "    # Add more authorized email addresses here\n]"

    # Find and replace the ALLOWED_USERS definition
    import re
    pattern = r'ALLOWED_USERS = \[.*?\]'
    content = re.sub(pattern, new_users_list, content, flags=re.DOTALL)

    # Write back to file
    with open(app_file, 'w') as f:
        f.write(content)

    print(f"✅ Updated allowed users list with {len(allowed_users)} users")


def main():
    """Main setup function"""
    print("🔒 MOC Report Streamlit App Setup")
    print("=" * 40)

    # Check if we're in the right directory
    if not Path("streamlit_app.py").exists():
        print("❌ Please run this script from the project root directory")
        return

    try:
        setup_secrets()
        setup_allowed_users()

        print("\n✅ Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Test locally: streamlit run streamlit_app.py")
        print("3. For production: Deploy to Streamlit Cloud and configure secrets")
        print("\n🔐 Security reminders:")
        print("- Never commit .streamlit/secrets.toml to git")
        print("- Use Streamlit's Secrets Manager for production")
        print("- Regularly review your allowed users list")

    except KeyboardInterrupt:
        print("\n❌ Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")


if __name__ == "__main__":
    main()
