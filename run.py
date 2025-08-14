#!/usr/bin/env python3
"""
Startup script for the URL Shortener application
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import flask_sqlalchemy
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ['static/css', 'static/js', 'templates']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def main():
    """Main startup function"""
    print("🚀 Starting URL Shortener Application")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Set environment variables
    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('FLASK_DEBUG', '1')
    
    print("📁 Project structure verified")
    print("🔧 Environment configured")
    print("🌐 Starting Flask development server...")
    print("=" * 40)
    print("📱 Application will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 40)
    
    try:
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
