# Angular Documentation Crawler

A comprehensive web crawler for downloading Angular.dev documentation, designed to enhance VS Code Copilot integration and provide offline access to Angular documentation.

## 🚀 Features

- **Complete Documentation Download**: Crawls and downloads all Angular.dev documentation pages
- **Intelligent URL Discovery**: Uses sitemaps and recursive link following for comprehensive coverage
- **Organized Storage**: Saves documentation in a structured, browsable format
- **VS Code Copilot Integration**: Generates detailed instructions for using downloaded docs with Copilot
- **Rate Limiting**: Respectful crawling with configurable delays
- **Error Handling**: Robust error handling with detailed logging and retry mechanisms
- **Progress Tracking**: Real-time progress updates and detailed crawl summaries

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd snippet
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Usage

### Basic Usage

```bash
python main.py
```

### Advanced Options

```bash
# Enable verbose logging
python main.py --verbose

# Specify custom output directory
python main.py --output-dir /path/to/custom/directory

# Help
python main.py --help
```

## 📁 Output Structure

After running the crawler, you'll get:

```
angular_docs/
├── documentation/          # Downloaded documentation pages
│   ├── docs/              # Main documentation sections
│   │   ├── overview/      # Angular overview and getting started
│   │   ├── tutorials/     # Step-by-step tutorials  
│   │   ├── guide/         # Development guides
│   │   ├── api/           # API reference
│   │   ├── cli/           # Angular CLI docs
│   │   └── reference/     # Additional references
│   └── assets/            # Images, styles, and other assets
├── crawl_summary.json     # Detailed crawl statistics
└── angular_docs_crawler.log  # Crawler execution log
```

Plus:
- `instructions.md` - Comprehensive guide for using the docs with VS Code Copilot

## 🤖 VS Code Copilot Integration

The crawler generates a detailed `instructions.md` file that provides:

- **Setup instructions** for optimal Copilot integration
- **Commenting techniques** to provide Copilot with documentation context
- **Workflow examples** for documentation-guided development
- **Specific use cases** for components, services, routing, and forms
- **Pro tips** for maximum productivity
- **Troubleshooting guide** for common issues

### Quick Start with Copilot

1. Run the crawler to download Angular documentation
2. Open the `instructions.md` file for detailed guidance
3. Open Angular documentation files in VS Code alongside your code
4. Use documentation references in comments to guide Copilot suggestions

Example:
```typescript
// Based on Angular docs: Component Lifecycle (docs/guide/lifecycle-hooks)
// Implement proper component cleanup with OnDestroy
export class MyComponent implements OnInit, OnDestroy {
  // Copilot will suggest proper lifecycle implementations
}
```

## ⚙️ Configuration

The crawler can be configured by modifying `angular_docs_crawler/config.py`:

```python
# Crawler behavior
REQUEST_DELAY = 1.0  # Seconds between requests
TIMEOUT = 30         # Request timeout
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB file size limit

# URLs to exclude
EXCLUDE_PATTERNS = ['/api/', '/playground/', '.pdf']

# Priority sections (crawled first)
PRIORITY_SECTIONS = ['/docs/overview', '/docs/tutorials', '/docs/guide']
```

## 🔧 Technical Details

### Architecture

- **Modular Design**: Separate modules for crawling, parsing, and storage
- **Robust Error Handling**: Comprehensive error handling with detailed logging
- **Rate Limiting**: Configurable delays to respect server resources
- **URL Normalization**: Consistent URL handling to avoid duplicates
- **Content Validation**: Checks for valid content and file sizes

### Dependencies

- `requests`: HTTP client for downloading pages
- `beautifulsoup4`: HTML parsing and link extraction
- `lxml`: Fast XML/HTML parser
- `pathlib`: Modern path handling

### Supported Python Versions

- Python 3.7+
- Cross-platform compatibility (Windows, macOS, Linux)

## 📊 Features in Detail

### Smart URL Discovery

1. **Sitemap Analysis**: Automatically discovers URLs from XML sitemaps
2. **Recursive Link Following**: Follows internal links to find all documentation
3. **URL Validation**: Filters URLs to ensure only relevant documentation is downloaded
4. **Duplicate Prevention**: Avoids downloading the same content multiple times

### Content Organization

1. **Hierarchical Structure**: Preserves Angular.dev's documentation organization
2. **Clean Filenames**: Sanitizes filenames for cross-platform compatibility
3. **Metadata Preservation**: Maintains content structure and relationships
4. **Asset Management**: Downloads and organizes images and other assets

### Progress and Monitoring

1. **Real-time Progress**: Live updates during crawling process
2. **Detailed Logging**: Comprehensive logs for debugging and monitoring
3. **Crawl Summary**: JSON summary with statistics and failed URLs
4. **Error Tracking**: Detailed error reporting and failed URL tracking

## 🛠️ Development

### Project Structure

```
angular_docs_crawler/
├── __init__.py           # Package initialization
├── config.py             # Configuration settings
├── crawler.py            # Main crawler implementation
└── utils.py              # Utility functions

main.py                   # CLI entry point
requirements.txt          # Python dependencies
README.md                 # This file
```

### Adding Features

1. **New Crawling Strategies**: Extend the `AngularDocsCrawler` class
2. **Content Processing**: Add new methods to `utils.py`
3. **Configuration Options**: Update `config.py` for new settings
4. **CLI Options**: Extend argument parser in `main.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Disclaimer

This crawler is designed to respectfully download Angular documentation for educational and development purposes. Please ensure you comply with Angular.dev's terms of service and robots.txt when using this tool.

## 🔗 Links

- [Angular Official Documentation](https://angular.dev)
- [VS Code Copilot Documentation](https://docs.github.com/en/copilot)
- [Python Requests Library](https://requests.readthedocs.io/)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

**Happy coding with Angular and VS Code Copilot!** 🚀
