#!/usr/bin/env node

const { main } = require('./src/index');
const AngularDocsCrawler = require('./src/crawler');
const path = require('path');

// Parse command line arguments
const args = process.argv.slice(2);
const options = {};

for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
        case '--max-pages':
            options.maxPages = parseInt(args[++i]);
            break;
        case '--delay':
            options.delay = parseInt(args[++i]);
            break;
        case '--output-dir':
            options.outputDir = args[++i];
            break;
        case '--help':
        case '-h':
            console.log(`
Angular Documentation Crawler

Usage: node cli.js [options]

Options:
  --max-pages <number>    Maximum number of pages to crawl (default: 10)
  --delay <number>        Delay between requests in ms (default: 1500)
  --output-dir <path>     Output directory for documentation (default: ./docs)
  --help, -h              Show this help message

Examples:
  node cli.js                              # Run with default settings
  node cli.js --max-pages 50 --delay 2000 # Crawl more pages with longer delay
  node cli.js --output-dir ./my-docs       # Save to custom directory
            `);
            process.exit(0);
        case '--version':
        case '-v':
            const pkg = require('./package.json');
            console.log(`Angular Documentation Crawler v${pkg.version}`);
            process.exit(0);
        default:
            console.error(`Unknown option: ${args[i]}`);
            console.log('Use --help for usage information');
            process.exit(1);
    }
}

// Set defaults
if (!options.maxPages) options.maxPages = 10;
if (!options.delay) options.delay = 1500;
if (!options.outputDir) options.outputDir = path.join(__dirname, 'docs');

console.log('Starting Angular Documentation Crawler with options:');
console.log(`  Max pages: ${options.maxPages}`);
console.log(`  Delay: ${options.delay}ms`);
console.log(`  Output directory: ${options.outputDir}`);
console.log('');

// Override the default crawler configuration
const originalMain = main;
async function configuredMain() {
    const AngularDocsCrawler = require('./src/crawler');
    const InstructionsGenerator = require('./src/instructions-generator');
    const { createDemoDocumentation } = require('./src/index');
    
    console.log('Angular Documentation Crawler');
    console.log('=============================');
    
    try {
        let summary;
        
        console.log('Attempting to crawl angular.dev...');
        const crawler = new AngularDocsCrawler({
            maxPages: options.maxPages,
            delay: options.delay,
            outputDir: options.outputDir
        });
        
        summary = await crawler.start();
        
        if (summary.totalPages === 0 || !summary.successfulCrawl) {
            console.log('\n⚠️  Unable to access angular.dev - creating demo content...');
            summary = await createDemoDocumentation();
        }
        
        console.log('\nGenerating instructions.md...');
        const instructionsGen = new InstructionsGenerator({
            docsDir: options.outputDir,
            outputPath: path.join(path.dirname(options.outputDir), 'instructions.md')
        });
        
        await instructionsGen.generate(summary);
        
        console.log('\n✅ Process completed successfully!');
        console.log(`📄 Downloaded/Created ${summary.totalPages} pages`);
        console.log(`📁 Documentation saved to: ${options.outputDir}`);
        console.log(`📋 Instructions generated: ./instructions.md`);
        
        if (summary.note) {
            console.log(`\n💡 Note: ${summary.note}`);
            console.log('   To crawl real angular.dev content, ensure network access and run again.');
        }
        
    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}

configuredMain();