#!/usr/bin/env python3
"""
Security Scanner Launcher
Automatically detects and starts the security scanner with proper configuration
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

def find_python():
    """Find the best Python executable"""
    python_commands = ['python', 'python3', 'py', sys.executable]
    
    for cmd in python_commands:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Found Python: {cmd} - {result.stdout.strip()}")
                return cmd
        except:
            continue
    
    print("❌ No Python executable found!")
    return None

def install_dependencies(python_cmd):
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run([python_cmd, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def start_server(python_cmd):
    """Start the Flask server"""
    print("\n🚀 Starting Security Scanner server...")
    
    try:
        # Start the server in background
        process = subprocess.Popen([python_cmd, 'app/main.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Server started successfully!")
            print("🌐 Opening browser...")
            
            # Open browser
            try:
                webbrowser.open('http://localhost:5000')
            except:
                print("⚠️  Could not open browser automatically")
                print("   Please open: http://localhost:5000")
            
            print("\n" + "="*60)
            print("🛡️  Security Scanner is now running!")
            print("📍 URL: http://localhost:5000")
            print("⚠️  Use responsibly - only scan websites you own!")
            print("🔴 Press Ctrl+C to stop the server")
            print("="*60)
            
            try:
                # Keep the script running
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Shutting down server...")
                process.terminate()
                process.wait()
                print("✅ Server stopped")
                
        else:
            print("❌ Server failed to start")
            stdout, stderr = process.communicate()
            if stderr:
                print(f"Error: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("=" * 60)
    print("🛡️  Security Scanner Launcher")
    print("   Website Vulnerability Assessment Tool")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('app/main.py'):
        print("❌ Error: Not in the correct directory!")
        print("   Please run this script from the cekweb directory")
        sys.exit(1)
    
    # Find Python
    python_cmd = find_python()
    if not python_cmd:
        print("❌ Please install Python first!")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies(python_cmd):
        print("❌ Failed to install dependencies. Please check your internet connection.")
        sys.exit(1)
    
    # Start server
    if not start_server(python_cmd):
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Exiting launcher...")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
