"""
Main crawler module for downloading Angular documentation.
"""

import os
import time
import logging
import requests
from urllib.parse import urljoin, urlparse, urlunparse
from bs4 import BeautifulSoup
from typing import Set, List, Dict, Optional
import json
from pathlib import Path
import hashlib

from .config import *
from .utils import setup_logging, sanitize_filename, ensure_directory


class AngularDocsCrawler:
    """Main crawler class for Angular documentation."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        self.visited_urls: Set[str] = set()
        self.failed_urls: Set[str] = set()
        self.downloaded_files: Dict[str, str] = {}
        self.logger = setup_logging()
        
        # Ensure output directories exist
        ensure_directory(OUTPUT_DIR)
        ensure_directory(DOCS_DIR)
        ensure_directory(ASSETS_DIR)
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL should be crawled."""
        parsed = urlparse(url)
        
        # Must be from angular.dev domain
        if parsed.netloc and parsed.netloc not in ['angular.dev', 'www.angular.dev']:
            return False
        
        # Check exclude patterns
        for pattern in EXCLUDE_PATTERNS:
            if pattern in url:
                return False
        
        # Must be documentation related
        if '/docs' not in url and url != BASE_URL:
            return False
            
        return True
    
    def normalize_url(self, url: str) -> str:
        """Normalize URL for consistent handling."""
        parsed = urlparse(url)
        # Remove fragment
        normalized = urlunparse((parsed.scheme, parsed.netloc, parsed.path, 
                               parsed.params, parsed.query, ''))
        return normalized
    
    def discover_urls_from_sitemap(self) -> Set[str]:
        """Discover URLs from sitemap if available."""
        sitemap_urls = [
            urljoin(BASE_URL, '/sitemap.xml'),
            urljoin(BASE_URL, '/sitemap_index.xml'),
            urljoin(BASE_URL, '/docs/sitemap.xml')
        ]
        
        discovered_urls = set()
        
        for sitemap_url in sitemap_urls:
            try:
                response = self.session.get(sitemap_url, timeout=TIMEOUT)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'xml')
                    # Extract URLs from sitemap
                    for loc in soup.find_all('loc'):
                        url = loc.text.strip()
                        if self.is_valid_url(url):
                            discovered_urls.add(self.normalize_url(url))
                    
                    self.logger.info(f"Discovered {len(discovered_urls)} URLs from {sitemap_url}")
                    break
                    
            except Exception as e:
                self.logger.warning(f"Failed to fetch sitemap {sitemap_url}: {e}")
        
        return discovered_urls
    
    def extract_links_from_page(self, html_content: str, base_url: str) -> Set[str]:
        """Extract links from HTML content."""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = set()
        
        # Extract links from various elements
        for element in soup.find_all(['a', 'link'], href=True):
            href = element['href']
            full_url = urljoin(base_url, href)
            normalized_url = self.normalize_url(full_url)
            
            if self.is_valid_url(normalized_url):
                links.add(normalized_url)
        
        return links
    
    def download_page(self, url: str) -> Optional[str]:
        """Download a single page and return its content."""
        try:
            self.logger.info(f"Downloading: {url}")
            response = self.session.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            
            # Check content size
            if len(response.content) > MAX_FILE_SIZE:
                self.logger.warning(f"Skipping large file: {url} ({len(response.content)} bytes)")
                return None
            
            return response.text
            
        except Exception as e:
            self.logger.error(f"Failed to download {url}: {e}")
            self.failed_urls.add(url)
            return None
    
    def save_page(self, url: str, content: str) -> str:
        """Save page content to local file."""
        parsed = urlparse(url)
        
        # Create file path based on URL structure
        path_parts = [part for part in parsed.path.split('/') if part]
        
        if not path_parts or path_parts[-1] == 'docs':
            filename = 'index.html'
        else:
            filename = f"{path_parts[-1]}.html"
        
        # Create directory structure
        if len(path_parts) > 1:
            dir_path = os.path.join(DOCS_DIR, *path_parts[:-1])
        else:
            dir_path = DOCS_DIR
        
        ensure_directory(dir_path)
        
        # Sanitize filename
        filename = sanitize_filename(filename)
        file_path = os.path.join(dir_path, filename)
        
        # Handle duplicate filenames
        counter = 1
        original_path = file_path
        while os.path.exists(file_path):
            name, ext = os.path.splitext(original_path)
            file_path = f"{name}_{counter}{ext}"
            counter += 1
        
        # Save content
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.downloaded_files[url] = file_path
            self.logger.info(f"Saved: {file_path}")
            return file_path
            
        except Exception as e:
            self.logger.error(f"Failed to save {url} to {file_path}: {e}")
            return ""
    
    def crawl(self) -> Dict[str, any]:
        """Main crawling method."""
        self.logger.info("Starting Angular documentation crawl...")
        
        # Start with main documentation URLs
        initial_urls = {
            BASE_URL,
            DOCS_BASE_URL,
        }
        
        # Add priority sections
        for section in PRIORITY_SECTIONS:
            initial_urls.add(urljoin(BASE_URL, section))
        
        # Try to discover URLs from sitemap
        sitemap_urls = self.discover_urls_from_sitemap()
        if sitemap_urls:
            initial_urls.update(sitemap_urls)
        
        # URLs to process
        urls_to_process = list(initial_urls)
        processed_count = 0
        
        while urls_to_process:
            url = urls_to_process.pop(0)
            
            if url in self.visited_urls:
                continue
            
            self.visited_urls.add(url)
            
            # Download page
            content = self.download_page(url)
            if content:
                # Save page
                self.save_page(url, content)
                
                # Extract new links
                new_links = self.extract_links_from_page(content, url)
                for link in new_links:
                    if link not in self.visited_urls:
                        urls_to_process.append(link)
                
                processed_count += 1
                
                # Rate limiting
                time.sleep(REQUEST_DELAY)
                
                # Progress update
                if processed_count % 10 == 0:
                    self.logger.info(f"Processed {processed_count} pages, "
                                   f"{len(urls_to_process)} remaining")
        
        # Save crawl summary
        summary = {
            'total_pages': processed_count,
            'successful_downloads': len(self.downloaded_files),
            'failed_downloads': len(self.failed_urls),
            'downloaded_files': self.downloaded_files,
            'failed_urls': list(self.failed_urls)
        }
        
        summary_path = os.path.join(OUTPUT_DIR, 'crawl_summary.json')
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Crawl completed. Summary saved to {summary_path}")
        return summary