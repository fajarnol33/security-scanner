import os

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    
    # Security settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload
    WTF_CSRF_ENABLED = False  # Disable CSRF for API usage
    
    # Scanning configuration
    REQUEST_TIMEOUT = 15  # seconds
    MAX_REDIRECTS = 5
    MAX_PAYLOAD_TESTS = 3  # Limit payload tests to avoid being blocked
    RATE_LIMIT_DELAY = 0.5  # seconds between requests
    
    # Security headers to check
    SECURITY_HEADERS = {
        'X-Frame-Options': 'DENY or SAMEORIGIN',
        'X-Content-Type-Options': 'nosniff',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': 'Restrictive CSP policy',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Permissions-Policy': 'Restrictive permissions policy'
    }
    
    # File extensions that should not be publicly accessible
    SENSITIVE_EXTENSIONS = [
        '.env', '.git', '.config', '.backup', '.sql', '.db', '.log',
        '.old', '.bak', '.tmp', '.swp', '.DS_Store'
    ]

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
