const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs-extra');
const path = require('path');
const { URL } = require('url');

class AngularDocsCrawler {
    constructor(options = {}) {
        this.baseUrl = 'https://angular.dev';
        this.visited = new Set();
        this.queue = [];
        this.maxPages = options.maxPages || 500; // Limit to prevent infinite crawling
        this.delay = options.delay || 1000; // Delay between requests in ms
        this.outputDir = options.outputDir || path.join(__dirname, '..', 'docs');
        this.logFile = path.join(__dirname, '..', 'logs', 'crawler.log');
        
        // Initialize output directory
        fs.ensureDirSync(this.outputDir);
        fs.ensureDirSync(path.dirname(this.logFile));
    }

    log(message) {
        const timestamp = new Date().toISOString();
        const logMessage = `[${timestamp}] ${message}\n`;
        console.log(message);
        fs.appendFileSync(this.logFile, logMessage);
    }

    async delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    normalizeUrl(url) {
        try {
            const urlObj = new URL(url, this.baseUrl);
            // Remove fragment and normalize
            urlObj.hash = '';
            return urlObj.href;
        } catch (error) {
            return null;
        }
    }

    isValidAngularDevUrl(url) {
        try {
            const urlObj = new URL(url);
            return urlObj.hostname === 'angular.dev' || urlObj.hostname === 'www.angular.dev';
        } catch (error) {
            return false;
        }
    }

    getPageFilename(url) {
        try {
            const urlObj = new URL(url);
            let pathname = urlObj.pathname;
            
            // Remove leading slash and replace slashes with underscores
            pathname = pathname.replace(/^\//, '').replace(/\//g, '_');
            
            // If empty or just slashes, use 'index'
            if (!pathname || pathname === '') {
                pathname = 'index';
            }
            
            // Ensure it ends with .html
            if (!pathname.endsWith('.html')) {
                pathname += '.html';
            }
            
            return pathname;
        } catch (error) {
            return 'unknown.html';
        }
    }

    async fetchPage(url) {
        try {
            this.log(`Fetching: ${url}`);
            const response = await axios.get(url, {
                timeout: 10000,
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            });
            return response.data;
        } catch (error) {
            this.log(`Error fetching ${url}: ${error.message}`);
            return null;
        }
    }

    extractLinks($) {
        const links = [];
        $('a[href]').each((i, element) => {
            const href = $(element).attr('href');
            if (href) {
                const fullUrl = this.normalizeUrl(href);
                if (fullUrl && this.isValidAngularDevUrl(fullUrl)) {
                    links.push(fullUrl);
                }
            }
        });
        return links;
    }

    extractContent($, url) {
        // Remove script tags, style tags, and navigation elements
        $('script, style, nav, header, footer, .sidebar, .navigation').remove();
        
        // Extract main content
        let title = $('title').text() || $('h1').first().text() || 'Untitled';
        let content = '';
        
        // Try to find main content area
        const mainContent = $('main, .main-content, .content, .docs-content, article').first();
        if (mainContent.length > 0) {
            content = mainContent.html();
        } else {
            // Fallback to body content
            content = $('body').html();
        }
        
        return {
            url,
            title: title.trim(),
            content: content || '',
            extractedAt: new Date().toISOString()
        };
    }

    async savePage(pageData) {
        const filename = this.getPageFilename(pageData.url);
        const filepath = path.join(this.outputDir, filename);
        
        const htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${pageData.title}</title>
    <meta name="source-url" content="${pageData.url}">
    <meta name="extracted-at" content="${pageData.extractedAt}">
</head>
<body>
    <h1>${pageData.title}</h1>
    <p><strong>Source:</strong> <a href="${pageData.url}">${pageData.url}</a></p>
    <hr>
    ${pageData.content}
</body>
</html>`;

        await fs.writeFile(filepath, htmlContent, 'utf8');
        this.log(`Saved: ${filename}`);
    }

    async crawlPage(url) {
        if (this.visited.has(url) || this.visited.size >= this.maxPages) {
            return false;
        }

        this.visited.add(url);
        
        const html = await this.fetchPage(url);
        if (!html) {
            return false;
        }

        const $ = cheerio.load(html);
        
        // Extract and save page content
        const pageData = this.extractContent($, url);
        await this.savePage(pageData);
        
        // Extract links for further crawling
        const links = this.extractLinks($);
        for (const link of links) {
            if (!this.visited.has(link)) {
                this.queue.push(link);
            }
        }
        
        // Add delay to be respectful to the server
        await this.delay(this.delay);
        return true;
    }

    async start() {
        this.log('Starting Angular documentation crawl...');
        
        // Start with main pages
        const startUrls = [
            `${this.baseUrl}`,
            `${this.baseUrl}/guide`,
            `${this.baseUrl}/tutorials`,
            `${this.baseUrl}/reference`,
            `${this.baseUrl}/api`,
            `${this.baseUrl}/cli`,
            `${this.baseUrl}/overview`
        ];
        
        this.queue.push(...startUrls);
        
        let successfulPages = 0;
        while (this.queue.length > 0 && this.visited.size < this.maxPages) {
            const url = this.queue.shift();
            const success = await this.crawlPage(url);
            if (success) {
                successfulPages++;
            }
        }
        
        this.log(`Crawling completed. Downloaded ${successfulPages} pages successfully out of ${this.visited.size} attempted.`);
        
        // Generate summary
        const summary = {
            totalPages: successfulPages,
            attemptedPages: this.visited.size,
            completedAt: new Date().toISOString(),
            pages: Array.from(this.visited),
            successfulCrawl: successfulPages > 0
        };
        
        await fs.writeFile(
            path.join(this.outputDir, 'crawl-summary.json'),
            JSON.stringify(summary, null, 2)
        );
        
        this.log('Crawl summary saved to crawl-summary.json');
        return summary;
    }
}

module.exports = AngularDocsCrawler;