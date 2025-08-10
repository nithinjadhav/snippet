# Angular Documentation Crawler

A Node.js-based web crawler designed to download the entire Angular documentation from https://angular.dev and generate comprehensive instructions for using the documentation with VS Code Copilot.

## 🚀 Features

- **Comprehensive Crawling**: Downloads all accessible documentation pages from angular.dev
- **Intelligent Content Extraction**: Extracts clean, readable content from each page
- **Organized Storage**: Saves documentation in a structured, searchable format
- **VS Code Copilot Integration**: Generates detailed instructions for using the documentation with Copilot
- **Respectful Crawling**: Implements delays and limits to avoid overwhelming the server
- **Progress Logging**: Detailed logging of the crawling process

## 📋 Prerequisites

- Node.js (version 14 or higher)
- npm or yarn
- Internet connection

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd snippet
```

2. Install dependencies:
```bash
npm install
```

## 🎯 Usage

### Basic Usage

Run the complete crawling and instruction generation process:

```bash
npm start
```

This will:
1. Crawl Angular documentation from angular.dev
2. Save all pages to the `docs/` directory
3. Generate `instructions.md` with VS Code Copilot guidance

### Advanced Configuration

You can also run components separately:

```bash
# Run only the crawler
npm run crawl

# Or run with custom Node.js options
node src/index.js
```

## 📁 Project Structure

```
angular-docs-crawler/
├── src/
│   ├── index.js                 # Main entry point
│   ├── crawler.js               # Web crawling logic
│   └── instructions-generator.js # Instructions generation
├── docs/                        # Downloaded documentation (created after running)
├── logs/                        # Crawler logs (created after running)
├── output/                      # Additional output files
├── package.json                 # Project configuration
├── README.md                    # This file
└── instructions.md              # Generated Copilot instructions (created after running)
```

## 🔧 Configuration Options

The crawler can be configured by modifying the options in `src/index.js`:

```javascript
const crawler = new AngularDocsCrawler({
    maxPages: 100,     // Maximum number of pages to crawl
    delay: 1500,       // Delay between requests (ms)
    outputDir: './docs' // Directory to save documentation
});
```

## 📖 Output

### Documentation Files
- **Location**: `docs/` directory
- **Format**: HTML files with clean, extracted content
- **Naming**: URL-based naming scheme (e.g., `guide_components.html`)
- **Metadata**: Each file includes source URL and extraction timestamp

### Instructions File
- **Location**: `instructions.md`
- **Content**: Comprehensive guide for using Angular docs with VS Code Copilot
- **Includes**: Best practices, prompt examples, workflow tips, and integration strategies

### Summary File
- **Location**: `docs/crawl-summary.json`
- **Content**: Crawling statistics and list of all downloaded pages

## 🤖 Using with VS Code Copilot

After running the crawler, follow the generated `instructions.md` file for detailed guidance on:

- Setting up your workspace for optimal Copilot integration
- Using contextual prompts for better Angular code suggestions
- Leveraging the documentation for improved development workflow
- Best practices and common patterns

## 🔍 Features in Detail

### Intelligent Link Discovery
- Automatically discovers and follows internal Angular.dev links
- Filters out external links and non-documentation content
- Handles relative and absolute URLs correctly

### Content Extraction
- Removes navigation, scripts, and styling for clean content
- Preserves important structural elements (headings, code blocks, lists)
- Maintains links and references within the content

### Error Handling
- Graceful handling of network errors and timeouts
- Comprehensive logging of errors and progress
- Automatic retry logic for failed requests

### Rate Limiting
- Configurable delays between requests
- Respectful crawling to avoid server overload
- Maximum page limits to prevent infinite crawling

## 🚦 Troubleshooting

### Common Issues

1. **Network Connection Errors**
   - Check your internet connection
   - Verify that angular.dev is accessible
   - Consider increasing timeout values

2. **Permission Errors**
   - Ensure write permissions in the project directory
   - Check that the `docs/` and `logs/` directories can be created

3. **Memory Issues**
   - Reduce the `maxPages` limit in configuration
   - Increase Node.js memory limit: `node --max-old-space-size=4096 src/index.js`

### Debug Mode

For detailed debugging, check the log file:
```bash
cat logs/crawler.log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the ISC License - see the package.json file for details.

## ⚖️ Legal Notice

This tool is designed for educational and development purposes. Please respect Angular's terms of service and robots.txt when using this crawler. The tool implements respectful crawling practices, but users are responsible for ensuring compliance with applicable terms and policies.

## 🔄 Updates

The Angular documentation is regularly updated. Consider re-running the crawler periodically to keep your local documentation current:

```bash
# Clean previous crawl and start fresh
rm -rf docs/ logs/
npm start
```
