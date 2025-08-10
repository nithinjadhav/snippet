"""
Utility functions for the Angular documentation crawler.
"""

import os
import re
import logging
from pathlib import Path
from .config import LOG_LEVEL, LOG_FORMAT


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('angular_docs_crawler.log')
        ]
    )
    return logging.getLogger(__name__)


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for cross-platform compatibility."""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove control characters
    filename = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', filename)
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    return filename or 'index.html'


def ensure_directory(path: str) -> None:
    """Ensure directory exists, create if it doesn't."""
    Path(path).mkdir(parents=True, exist_ok=True)


def get_file_extension(url: str) -> str:
    """Get file extension from URL."""
    path = url.split('?')[0].split('#')[0]  # Remove query and fragment
    return os.path.splitext(path)[1].lower()


def is_documentation_url(url: str) -> bool:
    """Check if URL is likely documentation content."""
    doc_indicators = [
        '/docs/',
        '/guide/',
        '/tutorial/',
        '/api/',
        '/reference/',
        '/cli/',
        '/overview/'
    ]
    return any(indicator in url.lower() for indicator in doc_indicators)


def format_bytes(bytes_value: int) -> str:
    """Format bytes into human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} TB"