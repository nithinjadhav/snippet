const fs = require('fs-extra');
const path = require('path');

class InstructionsGenerator {
    constructor(options = {}) {
        this.docsDir = options.docsDir;
        this.outputPath = options.outputPath;
    }

    generateInstructions(summary) {
        const instructions = `# Using Angular Documentation with VS Code Copilot

This document provides comprehensive guidance on how to effectively use the downloaded Angular documentation with VS Code Copilot to enhance your Angular development workflow.

## 📁 Documentation Structure

The Angular documentation has been crawled from \`https://angular.dev\` and organized locally in the \`docs/\` directory. The documentation includes:

- **${summary.totalPages} pages** of Angular documentation
- Guide sections, tutorials, API references, and CLI documentation
- Downloaded on: ${new Date(summary.completedAt).toLocaleDateString()}

## 🤖 Using VS Code Copilot with Angular Documentation

### 1. Setting Up Your Workspace

To maximize Copilot's effectiveness with the Angular documentation:

\`\`\`bash
# Open your Angular project in VS Code
code your-angular-project/

# Keep the documentation folder accessible
# Option 1: Copy docs folder to your project root
cp -r ./docs ./your-angular-project/angular-docs

# Option 2: Create a symbolic link
ln -s /path/to/docs ./your-angular-project/angular-docs
\`\`\`

### 2. Contextual Prompts for Copilot

Use these proven prompt patterns to get better results from Copilot:

#### 🏗️ Component Generation
\`\`\`typescript
// Prompt: "Create an Angular component following the style guide with proper lifecycle hooks"
// Copilot will suggest a component structure based on Angular best practices

// Example result:
import { Component, OnInit, OnDestroy } from '@angular/core';

@Component({
  selector: 'app-my-component',
  templateUrl: './my-component.component.html',
  styleUrls: ['./my-component.component.css']
})
export class MyComponent implements OnInit, OnDestroy {
  // Component implementation
}
\`\`\`

#### 🔄 Service Implementation
\`\`\`typescript
// Prompt: "Create an Angular service with HTTP client for API calls and error handling"
// Reference the downloaded API documentation for accurate method signatures

import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
\`\`\`

#### 🛡️ Reactive Forms
\`\`\`typescript
// Prompt: "Implement reactive forms with validation following Angular guidelines"
// Copilot can reference the forms documentation for proper patterns

import { FormBuilder, FormGroup, Validators } from '@angular/forms';
\`\`\`

### 3. Advanced Copilot Techniques

#### Using Documentation Context
When working on specific Angular features, open the relevant documentation files to provide context:

1. **Open relevant docs**: \`Ctrl+P\` → type \`angular-docs/forms\` for forms-related files
2. **Reference in comments**: Add comments referencing documentation sections
3. **Use specific terminology**: Use Angular-specific terms from the documentation

#### Example Workflow:
\`\`\`typescript
/**
 * Based on Angular Reactive Forms documentation:
 * - Use FormBuilder for complex forms
 * - Implement custom validators
 * - Handle form state and validation errors
 */
// Copilot will now provide more accurate suggestions aligned with Angular patterns
\`\`\`

### 4. Common Copilot Prompts for Angular Development

#### 🎯 Specific Feature Implementation
\`\`\`
// Comment prompts that work well with Angular docs context:

// "Create a custom pipe that formats currency according to locale"
// "Implement lazy loading for this feature module"
// "Add route guards with authentication check"
// "Create a reusable form component with custom validation"
// "Implement OnPush change detection strategy"
\`\`\`

#### 🧪 Testing Patterns
\`\`\`typescript
// "Generate unit tests for this component using TestBed"
// "Create integration tests for this service with HTTP mocking"
// "Add e2e tests for this user workflow"

describe('MyComponent', () => {
  // Copilot will suggest proper Angular testing patterns
});
\`\`\`

### 5. Best Practices for Copilot + Angular

#### ✅ Do:
- **Keep documentation files open** when working on related features
- **Use descriptive variable and function names** that match Angular conventions
- **Write clear comments** describing the intended Angular pattern
- **Reference specific Angular APIs** in your prompts
- **Include import statements** to provide context about which Angular modules you're using

#### ❌ Don't:
- Rely solely on Copilot without understanding Angular fundamentals
- Accept suggestions that violate Angular style guide
- Use deprecated APIs that Copilot might suggest from outdated training data
- Skip type checking and linting

### 6. Workflow Integration

#### Daily Development Routine:
1. **Morning Setup**: Open relevant documentation sections for today's features
2. **Feature Development**: Use specific Angular terminology in comments
3. **Code Review**: Cross-reference Copilot suggestions with documentation
4. **Testing**: Let Copilot generate test scaffolding based on Angular testing patterns

#### Project-Specific Setup:
\`\`\`json
// .vscode/settings.json
{
  "files.associations": {
    "*.component.html": "html",
    "*.component.ts": "typescript"
  },
  "copilot.enable": {
    "*": true,
    "yaml": false,
    "plaintext": false
  }
}
\`\`\`

### 7. Advanced Integration Tips

#### Custom Snippets with Copilot:
Create Angular-specific snippets that work well with Copilot suggestions:

\`\`\`json
// .vscode/angular.code-snippets
{
  "Angular Component with Copilot": {
    "prefix": "ng-component-copilot",
    "body": [
      "// Create Angular component with specific functionality",
      "// Following Angular style guide and best practices",
      "// Include proper lifecycle hooks and dependency injection",
      "",
      "@Component({",
      "  selector: 'app-component-name',",
      "  templateUrl: './component-name.component.html',",
      "  styleUrls: ['./component-name.component.css']",
      "})",
      "export class ComponentNameComponent implements OnInit {",
      "  // Component implementation",
      "}"
    ]
  }
}
\`\`\`

### 8. Troubleshooting Common Issues

#### When Copilot Suggests Outdated Patterns:
- Reference the latest documentation files in your workspace
- Add comments specifying Angular version requirements
- Use explicit import statements for new APIs

#### Improving Suggestion Quality:
- Keep related test files open alongside implementation
- Use consistent naming conventions throughout your project
- Maintain updated Angular dependencies

### 9. Documentation Reference Quick Guide

The crawled documentation is organized by topic:

- **Getting Started**: \`docs/guide_*\` files
- **Components**: \`docs/components_*\` files  
- **Services**: \`docs/services_*\` files
- **Routing**: \`docs/router_*\` files
- **Forms**: \`docs/forms_*\` files
- **HTTP**: \`docs/http_*\` files
- **Testing**: \`docs/testing_*\` files
- **CLI**: \`docs/cli_*\` files

### 10. Continuous Learning

#### Stay Updated:
- Regularly re-crawl documentation for updates
- Compare Copilot suggestions with official Angular examples
- Participate in Angular community discussions
- Follow Angular team updates and best practices

---

## 🎯 Quick Start Checklist

- [ ] Copy or link Angular docs to your project workspace
- [ ] Configure VS Code settings for optimal Copilot experience  
- [ ] Create custom snippets for common Angular patterns
- [ ] Practice using contextual comments for better suggestions
- [ ] Set up project-specific documentation organization
- [ ] Integrate documentation review into your code review process

---

**Last Updated**: ${new Date().toLocaleDateString()}  
**Documentation Version**: Angular.dev crawled content  
**Total Pages**: ${summary.totalPages}

> 💡 **Pro Tip**: The more context you provide through comments, open files, and specific Angular terminology, the better Copilot will understand your intent and provide accurate suggestions.
`;

        return instructions;
    }

    async generate(summary) {
        const instructions = this.generateInstructions(summary);
        await fs.writeFile(this.outputPath, instructions, 'utf8');
        console.log(`Instructions generated: ${this.outputPath}`);
    }
}

module.exports = InstructionsGenerator;