#!/usr/bin/env python3
"""
Main launcher for the MOC Report Generator GUI application.
Run this file to start the Streamlit application.
"""

import subprocess
import sys
import os


def main():
    """Launch the Streamlit application."""
    
    # Get the path to the main GUI file
    gui_main_path = os.path.join(os.path.dirname(__file__), "GUI", "main.py")
    
    # Check if the file exists
    if not os.path.exists(gui_main_path):
        print(f"Error: GUI main file not found at {gui_main_path}")
        sys.exit(1)
    
    # Launch Streamlit
    print("🚀 Starting MOC Report Generator...")
    print(f"📁 GUI Path: {gui_main_path}")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", gui_main_path,
            "--server.port", "8501",
            "--server.address", "localhost",
            "--theme.base", "light"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching application: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
