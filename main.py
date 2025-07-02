"""
Apple Store - Main Entry Point
Modern e-commerce application with Apple-inspired design
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_dependencies():
    """Verify all required dependencies are available."""
    required_packages = ['nicegui', 'uvicorn', 'python_dotenv', 'sqlalchemy', 'pillow', 'passlib']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print(f"📦 Install with: pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All dependencies available")
    return True

if __name__ == "__main__":
    if check_dependencies():
        # Import and run the application
        from app.main import main
        main()
    else:
        exit(1)