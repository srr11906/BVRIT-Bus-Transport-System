#!/usr/bin/env python3
"""
Deployment helper script for BVRIT Transport Management System
"""

import os
import subprocess
import sys

def check_git():
    """Check if git is initialized and files are committed"""
    try:
        # Check if git is initialized
        subprocess.run(['git', 'status'], check=True, capture_output=True)
        print("✅ Git repository found")
        return True
    except subprocess.CalledProcessError:
        print("❌ Git repository not found. Initializing...")
        try:
            subprocess.run(['git', 'init'], check=True)
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit for deployment'], check=True)
            print("✅ Git repository initialized")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error initializing git: {e}")
            return False

def check_files():
    """Check if all required deployment files exist"""
    required_files = ['requirements.txt', 'Procfile', 'runtime.txt', 'app.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required deployment files found")
        return True

def main():
    print("🚀 BVRIT Transport Management System - Deployment Helper")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Please run this script from the project directory")
        sys.exit(1)
    
    # Check files
    if not check_files():
        print("❌ Please ensure all deployment files are created")
        sys.exit(1)
    
    # Check git
    if not check_git():
        print("❌ Git setup failed")
        sys.exit(1)
    
    print("\n🎉 Your app is ready for deployment!")
    print("\n📋 Next steps:")
    print("1. Push your code to GitHub")
    print("2. Choose a deployment platform:")
    print("   - Railway: https://railway.app (Recommended)")
    print("   - Render: https://render.com")
    print("   - Heroku: https://heroku.com")
    print("3. Connect your GitHub repository")
    print("4. Set environment variable: SESSION_SECRET=your-secret-key")
    print("5. Deploy!")
    
    print("\n🔑 Don't forget to change default passwords before going live!")

if __name__ == "__main__":
    main()
