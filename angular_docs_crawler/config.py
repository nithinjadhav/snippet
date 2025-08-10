"""
Configuration settings for the Angular documentation crawler.
"""

import os
from urllib.parse import urljoin

# Base configuration
BASE_URL = "https://angular.dev"
DOCS_BASE_URL = urljoin(BASE_URL, "/docs")

# Output directories
OUTPUT_DIR = os.path.join(os.getcwd(), "angular_docs")
DOCS_DIR = os.path.join(OUTPUT_DIR, "documentation")
ASSETS_DIR = os.path.join(OUTPUT_DIR, "assets")

# Crawler settings
MAX_CONCURRENT_REQUESTS = 10
REQUEST_DELAY = 1.0  # seconds between requests
TIMEOUT = 30
USER_AGENT = "Angular-Docs-Crawler/1.0 (+https://github.com/nithinjadhav/snippet)"

# File settings
ALLOWED_EXTENSIONS = {'.html', '.md', '.txt', '.json', '.xml'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# URLs to exclude from crawling
EXCLUDE_PATTERNS = [
    '/api/',
    '/playground/',
    '/tutorial/playground',
    '.pdf',
    '.zip',
    '.tar.gz',
    'mailto:',
    'javascript:',
    '#'
]

# Important documentation sections to prioritize
PRIORITY_SECTIONS = [
    '/docs/overview',
    '/docs/tutorials',
    '/docs/guide',
    '/docs/api',
    '/docs/cli',
    '/docs/reference'
]