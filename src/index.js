const AngularDocsCrawler = require('./crawler');
const InstructionsGenerator = require('./instructions-generator');
const path = require('path');
const fs = require('fs-extra');

// Demo content for testing when network is unavailable
const demoContent = {
    'https://angular.dev': {
        title: 'Angular - The modern web developer\'s platform',
        content: `
        <main>
            <h1>Angular</h1>
            <p>Angular is a development platform built on TypeScript. It includes:</p>
            <ul>
                <li>A component-based framework for building scalable web applications</li>
                <li>A collection of well-integrated libraries</li>
                <li>A suite of developer tools</li>
            </ul>
            <h2>Getting Started</h2>
            <p>Start your first Angular app with the Angular CLI.</p>
            <a href="/guide">Explore the Guide</a>
            <a href="/tutorials">Try the Tutorials</a>
        </main>
        `
    },
    'https://angular.dev/guide': {
        title: 'Angular Guide - Introduction',
        content: `
        <main>
            <h1>Introduction to Angular</h1>
            <p>Angular is a platform and framework for building single-page client applications using HTML and TypeScript.</p>
            <h2>Core Concepts</h2>
            <ul>
                <li>Components</li>
                <li>Templates</li>
                <li>Directives</li>
                <li>Services</li>
                <li>Dependency Injection</li>
            </ul>
            <a href="/guide/components">Learn about Components</a>
        </main>
        `
    },
    'https://angular.dev/guide/components': {
        title: 'Angular Components',
        content: `
        <main>
            <h1>Components</h1>
            <p>Components are the main building block for Angular applications.</p>
            <h2>Creating a Component</h2>
            <pre><code>
import { Component } from '@angular/core';

@Component({
  selector: 'app-hello-world',
  template: \`<p>Hello World!</p>\`
})
export class HelloWorldComponent {
  // Component logic here
}
            </code></pre>
        </main>
        `
    }
};

async function createDemoDocumentation() {
    const docsDir = path.join(__dirname, '..', 'docs');
    await fs.ensureDir(docsDir);
    
    console.log('Creating demo documentation...');
    
    for (const [url, data] of Object.entries(demoContent)) {
        const filename = url.replace('https://angular.dev', '').replace(/\//g, '_') || 'index';
        const filepath = path.join(docsDir, `${filename}.html`);
        
        const htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${data.title}</title>
    <meta name="source-url" content="${url}">
    <meta name="extracted-at" content="${new Date().toISOString()}">
</head>
<body>
    <h1>${data.title}</h1>
    <p><strong>Source:</strong> <a href="${url}">${url}</a></p>
    <hr>
    ${data.content}
</body>
</html>`;

        await fs.writeFile(filepath, htmlContent, 'utf8');
        console.log(`Created demo file: ${filename}.html`);
    }
    
    // Create demo summary
    const summary = {
        totalPages: Object.keys(demoContent).length,
        completedAt: new Date().toISOString(),
        pages: Object.keys(demoContent),
        note: 'This is demo content created when angular.dev was not accessible'
    };
    
    await fs.writeFile(
        path.join(docsDir, 'crawl-summary.json'),
        JSON.stringify(summary, null, 2)
    );
    
    return summary;
}

async function main() {
    console.log('Angular Documentation Crawler');
    console.log('=============================');
    
    try {
        let summary;
        
        // Try real crawling first
        console.log('Attempting to crawl angular.dev...');
        const crawler = new AngularDocsCrawler({
            maxPages: 10, // Small number for testing
            delay: 1500,
            outputDir: path.join(__dirname, '..', 'docs')
        });
        
        summary = await crawler.start();
        
        // If no pages were successfully downloaded, create demo content
        if (summary.totalPages === 0 || !summary.successfulCrawl) {
            console.log('\n⚠️  Unable to access angular.dev - creating demo content...');
            summary = await createDemoDocumentation();
        }
        
        // Generate instructions.md
        console.log('\nGenerating instructions.md...');
        const instructionsGen = new InstructionsGenerator({
            docsDir: path.join(__dirname, '..', 'docs'),
            outputPath: path.join(__dirname, '..', 'instructions.md')
        });
        
        await instructionsGen.generate(summary);
        
        console.log('\n✅ Process completed successfully!');
        console.log(`📄 Downloaded/Created ${summary.totalPages} pages`);
        console.log(`📁 Documentation saved to: ./docs/`);
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

if (require.main === module) {
    main();
}

module.exports = { main, createDemoDocumentation };