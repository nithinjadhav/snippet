#!/usr/bin/env python3
"""
Angular Documentation Crawler - Main Script

This script crawls the Angular.dev documentation website and downloads
all documentation pages for local use with VS Code Copilot.
"""

import sys
import argparse
import json
from angular_docs_crawler.crawler import AngularDocsCrawler
from angular_docs_crawler.config import OUTPUT_DIR


def main():
    """Main entry point for the crawler."""
    parser = argparse.ArgumentParser(
        description="Crawl Angular.dev documentation for VS Code Copilot integration"
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--output-dir', '-o',
        default=OUTPUT_DIR,
        help=f'Output directory for downloaded docs (default: {OUTPUT_DIR})'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize and run crawler
        crawler = AngularDocsCrawler()
        
        if args.verbose:
            crawler.logger.setLevel('DEBUG')
        
        print("🚀 Starting Angular documentation crawl...")
        print(f"📁 Output directory: {args.output_dir}")
        print("⏱️  This may take several minutes depending on the size of documentation...")
        
        # Run the crawl
        summary = crawler.crawl()
        
        # Print summary
        print("\n✅ Crawl completed successfully!")
        print(f"📊 Summary:")
        print(f"   • Total pages processed: {summary['total_pages']}")
        print(f"   • Successful downloads: {summary['successful_downloads']}")
        print(f"   • Failed downloads: {summary['failed_downloads']}")
        print(f"   • Output directory: {args.output_dir}")
        
        if summary['failed_downloads'] > 0:
            print(f"\n⚠️  Some pages failed to download. Check crawl_summary.json for details.")
        
        # Generate instructions.md
        generate_instructions()
        print(f"📋 Generated instructions.md for VS Code Copilot usage")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⏹️  Crawl interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error during crawl: {e}")
        return 1


def generate_instructions():
    """Generate instructions.md file for VS Code Copilot usage."""
    instructions_content = """# Using Angular Documentation with VS Code Copilot

This guide explains how to effectively use the downloaded Angular documentation with VS Code Copilot to enhance your Angular development experience.

## 📁 Downloaded Documentation Structure

The Angular documentation has been downloaded and organized in the following structure:

```
angular_docs/
├── documentation/          # Main documentation pages
│   ├── docs/              # Core documentation
│   │   ├── overview/      # Angular overview and getting started
│   │   ├── tutorials/     # Step-by-step tutorials
│   │   ├── guide/         # Development guides
│   │   ├── api/           # API reference documentation
│   │   ├── cli/           # Angular CLI documentation
│   │   └── reference/     # Additional reference materials
│   └── assets/            # Images, styles, and other assets
├── crawl_summary.json     # Summary of downloaded content
└── instructions.md        # This file
```

## 🤖 VS Code Copilot Integration Tips

### 1. Opening Documentation Context

To provide Copilot with Angular documentation context:

1. **Open relevant documentation files** in VS Code alongside your code
2. **Reference specific sections** in your comments to guide Copilot
3. **Keep documentation tabs open** while coding for better context

### 2. Effective Prompting Techniques

#### Using Documentation References in Comments

```typescript
// Based on Angular docs: Component Lifecycle Hooks (docs/guide/lifecycle-hooks)
// Implement OnInit and OnDestroy interfaces for proper component cleanup
export class MyComponent implements OnInit, OnDestroy {
  // Copilot will suggest proper lifecycle method implementations
}
```

#### Asking for Code Examples

```typescript
// Generate a reactive form based on Angular reactive forms documentation
// Include validation and error handling as shown in the guides
```

#### API-Specific Requests

```typescript
// Use Angular HttpClient API as documented in docs/guide/http
// Include error handling and type safety
```

### 3. Copilot Chat Integration

Use these patterns in Copilot Chat for better results:

#### General Questions
- "Based on the Angular documentation, how do I implement lazy loading?"
- "Show me the best practices for Angular component communication from the docs"

#### Code Generation
- "Generate a service following Angular dependency injection patterns from the documentation"
- "Create a custom directive based on Angular directive development guide"

#### Code Review and Optimization
- "Review this component against Angular style guide recommendations"
- "Optimize this code following Angular performance best practices"

### 4. Documentation-Guided Development Workflow

#### Step 1: Explore Documentation First
```bash
# Search for relevant documentation sections
find angular_docs/documentation -name "*.html" | grep -i "component"
```

#### Step 2: Open Related Files
- Open the relevant documentation page in VS Code
- Open your code file in a split pane
- Use the documentation as reference while coding

#### Step 3: Use Contextual Comments
```typescript
/**
 * Component following Angular component architecture guidelines
 * Reference: docs/guide/component-overview.html
 * 
 * Features implemented:
 * - Property binding (docs/guide/property-binding)
 * - Event binding (docs/guide/event-binding) 
 * - Two-way binding (docs/guide/two-way-binding)
 */
```

## 🎯 Specific Use Cases and Examples

### 1. Component Development

```typescript
// Create a component following Angular component lifecycle best practices
// Reference: docs/guide/lifecycle-hooks documentation
// Include proper OnInit, OnDestroy, and change detection strategies

@Component({
  selector: 'app-example',
  templateUrl: './example.component.html',
  styleUrls: ['./example.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush // Copilot suggests based on docs
})
export class ExampleComponent implements OnInit, OnDestroy {
  // Copilot will suggest proper implementation
}
```

### 2. Service Development

```typescript
// Implement Angular service following dependency injection patterns
// Reference: docs/guide/dependency-injection documentation
// Include proper error handling and HTTP client usage

@Injectable({
  providedIn: 'root' // Copilot suggests based on DI documentation
})
export class DataService {
  // Copilot will suggest proper service implementation
}
```

### 3. Routing Configuration

```typescript
// Configure Angular routing based on router documentation
// Reference: docs/guide/router documentation
// Include route guards, lazy loading, and nested routes

const routes: Routes = [
  // Copilot suggests routes based on documentation patterns
];
```

### 4. Form Handling

```typescript
// Implement reactive forms following Angular forms guide
// Reference: docs/guide/reactive-forms documentation
// Include validation, custom validators, and form arrays

export class ContactFormComponent {
  // Copilot suggests form implementation based on docs
}
```

## 🔧 Advanced Copilot Configuration

### 1. Workspace Settings

Add to your `.vscode/settings.json`:

```json
{
  "github.copilot.enable": {
    "*": true,
    "typescript": true,
    "html": true,
    "scss": true
  },
  "github.copilot.advanced": {
    "length": 500,
    "temperature": 0.1
  }
}
```

### 2. File Associations

Configure VS Code to recognize Angular documentation:

```json
{
  "files.associations": {
    "*.component.html": "html",
    "*.component.scss": "scss",
    "*.guard.ts": "typescript",
    "*.service.ts": "typescript",
    "*.pipe.ts": "typescript"
  }
}
```

## 📚 Documentation Quick Reference

### Essential Sections for Daily Development

1. **Component Guide** (`docs/guide/component-*`)
   - Component lifecycle
   - Property and event binding
   - Component interaction

2. **Services and DI** (`docs/guide/dependency-injection`)
   - Service creation
   - Injection patterns
   - Hierarchical injectors

3. **Routing** (`docs/guide/router`)
   - Route configuration
   - Navigation
   - Route guards

4. **Forms** (`docs/guide/forms`)
   - Template-driven forms
   - Reactive forms
   - Validation

5. **HTTP Client** (`docs/guide/http`)
   - Making requests
   - Error handling
   - Interceptors

6. **Testing** (`docs/guide/testing`)
   - Unit testing
   - Component testing
   - Service testing

### CLI Reference (`docs/cli/`)

Quick commands for development:

```bash
# Generate components, services, etc.
ng generate component my-component
ng generate service my-service
ng generate module my-module

# Build and serve
ng serve
ng build
ng test
```

## 🚀 Pro Tips for Maximum Productivity

### 1. Create Documentation Snippets

Create VS Code snippets based on documentation patterns:

```json
{
  "Angular Component": {
    "prefix": "ng-component",
    "body": [
      "// Component following Angular style guide",
      "// Reference: Angular component documentation",
      "@Component({",
      "  selector: '${1:app-component}',",
      "  templateUrl: './${1:component}.component.html',",
      "  styleUrls: ['./${1:component}.component.css']",
      "})",
      "export class ${2:Component}Component implements OnInit {",
      "  constructor() { }",
      "",
      "  ngOnInit(): void {",
      "    $0",
      "  }",
      "}"
    ]
  }
}
```

### 2. Use Documentation Comments

```typescript
/**
 * Service for managing user data
 * 
 * Implements patterns from Angular documentation:
 * - Dependency injection (docs/guide/dependency-injection)
 * - HTTP client usage (docs/guide/http)
 * - Error handling best practices
 * 
 * @see angular_docs/documentation/docs/guide/http.html
 */
@Injectable({ providedIn: 'root' })
export class UserService {
  // Copilot will provide better suggestions with this context
}
```

### 3. Leverage Documentation Examples

When working on specific features, copy example code from documentation into comments:

```typescript
// Example from Angular docs: docs/guide/reactive-forms.html
// this.profileForm = this.fb.group({
//   firstName: ['', Validators.required],
//   lastName: [''],
//   address: this.fb.group({
//     street: [''],
//     city: [''],
//     state: [''],
//     zip: ['']
//   }),
// });

// Now implement similar pattern for my use case:
```

## 🔍 Troubleshooting Common Issues

### 1. Copilot Not Using Documentation Context

**Problem**: Copilot suggestions don't reflect Angular best practices

**Solution**:
- Ensure documentation files are open in VS Code workspace
- Add explicit references to documentation in comments
- Use more specific, documentation-based prompts

### 2. Outdated Suggestions

**Problem**: Copilot suggests deprecated Angular patterns

**Solution**:
- Reference specific version documentation in comments
- Include "latest Angular" or "Angular 17+" in prompts
- Keep documentation files updated

### 3. Generic Suggestions

**Problem**: Copilot provides generic JavaScript instead of Angular-specific code

**Solution**:
- Include Angular-specific terms in prompts
- Reference Angular documentation explicitly
- Use Angular CLI and component decorators in context

## 📖 Additional Resources

- **Angular Official Documentation**: The source of truth for all Angular features
- **Angular CLI Documentation**: Complete guide to Angular CLI commands
- **Angular Style Guide**: Best practices for Angular development
- **API Reference**: Detailed API documentation for all Angular packages

---

*Generated by Angular Documentation Crawler*
*Last updated: Generated from angular.dev documentation*

Happy coding with Angular and VS Code Copilot! 🚀
"""
    
    with open('instructions.md', 'w', encoding='utf-8') as f:
        f.write(instructions_content)


if __name__ == '__main__':
    sys.exit(main())