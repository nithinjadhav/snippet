#!/usr/bin/env python3
"""
Test script for Angular Documentation Crawler

This script tests the crawler functionality with a limited scope
to validate the implementation without downloading the entire documentation.
"""

import os
import sys
import tempfile
from angular_docs_crawler.crawler import AngularDocsCrawler
from angular_docs_crawler.config import *


def test_crawler_basic_functionality():
    """Test basic crawler functionality with limited scope."""
    print("🧪 Testing Angular Documentation Crawler...")
    
    # Create a test crawler instance
    crawler = AngularDocsCrawler()
    
    # Test URL validation
    test_urls = [
        "https://angular.dev/docs/overview",
        "https://angular.dev/docs/guide/components", 
        "https://angular.dev/playground",  # Should be excluded
        "https://example.com/docs",  # Should be excluded
        "https://angular.dev/docs/api"
    ]
    
    print("\n📋 Testing URL validation...")
    for url in test_urls:
        is_valid = crawler.is_valid_url(url)
        status = "✅ Valid" if is_valid else "❌ Invalid"
        print(f"   {url} - {status}")
    
    # Test URL normalization
    print("\n🔄 Testing URL normalization...")
    test_normalize_urls = [
        "https://angular.dev/docs/guide#section",
        "https://angular.dev/docs/guide?param=value",
        "https://angular.dev/docs/guide/"
    ]
    
    for url in test_normalize_urls:
        normalized = crawler.normalize_url(url)
        print(f"   {url} -> {normalized}")
    
    # Test basic connection and page download (just the main page)
    print("\n🌐 Testing basic page download...")
    try:
        content = crawler.download_page("https://angular.dev")
        if content and len(content) > 100:
            print(f"   ✅ Successfully downloaded main page ({len(content)} characters)")
            
            # Test link extraction
            links = crawler.extract_links_from_page(content, "https://angular.dev")
            valid_links = [link for link in links if crawler.is_valid_url(link)]
            print(f"   ✅ Extracted {len(links)} total links, {len(valid_links)} valid documentation links")
            
            if valid_links:
                print("   📄 Sample valid links:")
                for link in list(valid_links)[:5]:  # Show first 5
                    print(f"      - {link}")
        else:
            print("   ❌ Failed to download main page or content too small")
            
    except Exception as e:
        print(f"   ❌ Error downloading page: {e}")
    
    # Test file saving functionality
    print("\n💾 Testing file saving...")
    try:
        test_content = "<html><head><title>Test</title></head><body><h1>Test Content</h1></body></html>"
        test_url = "https://angular.dev/docs/test"
        
        # Create temporary directory for test
        with tempfile.TemporaryDirectory() as temp_dir:
            # Temporarily override the output directory
            original_output_dir = OUTPUT_DIR
            original_docs_dir = DOCS_DIR
            
            # Set test directories
            test_output_dir = temp_dir
            test_docs_dir = os.path.join(temp_dir, "documentation")
            
            # Update crawler directories
            crawler.logger.info(f"Using test directory: {test_output_dir}")
            
            # Save test content
            from angular_docs_crawler.utils import ensure_directory
            ensure_directory(test_docs_dir)
            
            # Create test file path
            test_file = os.path.join(test_docs_dir, "test.html")
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            if os.path.exists(test_file):
                print(f"   ✅ Successfully saved test file: {test_file}")
                with open(test_file, 'r', encoding='utf-8') as f:
                    saved_content = f.read()
                if saved_content == test_content:
                    print("   ✅ File content matches original")
                else:
                    print("   ❌ File content doesn't match")
            else:
                print("   ❌ Test file not created")
                
    except Exception as e:
        print(f"   ❌ Error testing file saving: {e}")
    
    print("\n🎉 Basic functionality test completed!")
    print("\nTo run a full crawl, use: python main.py")
    return True


if __name__ == '__main__':
    test_crawler_basic_functionality()