#!/usr/bin/env python3
"""
Security Scanner - Website Vulnerability Assessment Tool
========================================================

Usage:
    python run.py [--host HOST] [--port PORT] [--debug]

Options:
    --host HOST     Host to bind to (default: 127.0.0.1)
    --port PORT     Port to bind to (default: 5000)
    --debug         Enable debug mode

Example:
    python run.py --host 0.0.0.0 --port 8080
"""

import argparse
import os
import sys
from app.main import app

def main():
    parser = argparse.ArgumentParser(description='Security Scanner Web Application')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🛡️  Security Scanner - Website Vulnerability Assessment")
    print("=" * 60)
    print(f"🌐 Server starting on http://{args.host}:{args.port}")
    print("⚠️  WARNING: Use this tool responsibly and only on websites you own!")
    print("📚 This tool is for educational and defensive security purposes only.")
    print("=" * 60)
    
    try:
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
