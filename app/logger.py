import logging
import os
from datetime import datetime

def setup_logging():
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure logging
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # File handler
    file_handler = logging.FileHandler(f'logs/security_scanner_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(logging.Formatter(log_format))
    
    # Setup logger
    logger = logging.getLogger('security_scanner')
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def log_scan_attempt(url, user_ip, user_agent):
    """Log scanning attempt"""
    logger = logging.getLogger('security_scanner')
    logger.info(f"Scan attempt - URL: {url}, IP: {user_ip}, User-Agent: {user_agent}")

def log_vulnerability_found(url, vuln_type, severity):
    """Log vulnerability discovery"""
    logger = logging.getLogger('security_scanner')
    logger.warning(f"Vulnerability found - URL: {url}, Type: {vuln_type}, Severity: {severity}")

def log_error(error_msg, url=None):
    """Log error"""
    logger = logging.getLogger('security_scanner')
    logger.error(f"Error: {error_msg}" + (f" - URL: {url}" if url else "")

def log_scan_summary(url, total_vulns, duration):
    """Log scan summary"""
    logger = logging.getLogger('security_scanner')
    logger.info(f"Scan completed - URL: {url}, Vulnerabilities: {total_vulns}, Duration: {duration:.2f}s")
