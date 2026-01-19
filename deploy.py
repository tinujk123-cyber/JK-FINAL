#!/usr/bin/env python3
"""
Quick deployment helper script for JK TRINETRA application.

This script helps you deploy the application to Streamlit Cloud.
"""

import subprocess
import sys
import webbrowser
from pathlib import Path


def check_git_status():
    """Check if there are uncommitted changes."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def get_current_branch():
    """Get the current Git branch."""
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def push_to_github():
    """Push current branch to GitHub."""
    branch = get_current_branch()
    print(f"📤 Pushing {branch} branch to GitHub...")
    
    result = subprocess.run(
        ["git", "push", "origin", branch],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Successfully pushed to GitHub!")
        return True
    else:
        print(f"❌ Error pushing to GitHub: {result.stderr}")
        return False


def main():
    """Main deployment helper function."""
    print("🚀 JK TRINETRA Deployment Helper")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("streamlit_app.py").exists():
        print("❌ Error: streamlit_app.py not found!")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check Git status
    print("\n📋 Checking Git status...")
    uncommitted = check_git_status()
    
    if uncommitted:
        print("⚠️  Warning: You have uncommitted changes:")
        print(uncommitted)
        response = input("\nDo you want to commit these changes? (y/n): ")
        
        if response.lower() == 'y':
            message = input("Enter commit message: ")
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", message])
            print("✅ Changes committed!")
        else:
            print("⚠️  Proceeding with uncommitted changes...")
    else:
        print("✅ No uncommitted changes")
    
    # Get current branch
    branch = get_current_branch()
    print(f"\n📍 Current branch: {branch}")
    
    # Ask about pushing to GitHub
    print("\n" + "=" * 50)
    print("Deployment Options:")
    print("1. Push to GitHub and open Streamlit Cloud")
    print("2. Just push to GitHub")
    print("3. Open Streamlit Cloud (without pushing)")
    print("4. Cancel")
    
    choice = input("\nSelect option (1-4): ")
    
    if choice == "1":
        if push_to_github():
            print("\n🌐 Opening Streamlit Cloud in browser...")
            webbrowser.open("https://share.streamlit.io/")
            print("\n📝 Deployment Instructions:")
            print("1. Sign in with your GitHub account")
            print("2. Click 'New app'")
            print("3. Select your repository")
            print(f"4. Branch: {branch}")
            print("5. Main file: streamlit_app.py")
            print("6. Click 'Deploy!'")
    
    elif choice == "2":
        push_to_github()
    
    elif choice == "3":
        print("\n🌐 Opening Streamlit Cloud in browser...")
        webbrowser.open("https://share.streamlit.io/")
    
    else:
        print("❌ Deployment cancelled")
        return
    
    print("\n" + "=" * 50)
    print("✅ Deployment helper completed!")
    print("\nFor detailed deployment instructions, see DEPLOYMENT.md")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Deployment cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
