# Open WebUI Frontend

This directory contains the frontend application for Open WebUI, built with SvelteKit.

## Directory Structure

```
frontend/
├── src/                    # Source code
│   ├── lib/               # Shared libraries and components
│   ├── routes/            # Application routes
│   ├── app.css           # Global styles
│   ├── app.d.ts          # TypeScript declarations
│   ├── app.html          # Base HTML template
│   └── tailwind.css      # Tailwind CSS imports
├── static/                # Static assets
│   ├── assets/           # General assets
│   ├── audio/            # Audio files
│   ├── pyodide/          # Pyodide runtime files
│   ├── themes/           # Theme files
│   └── static/           # Additional static files
└── package.json          # Frontend dependencies
```

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start development server:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

## Key Features

- Built with SvelteKit
- TypeScript support
- Tailwind CSS for styling
- Pyodide integration for Python runtime
- i18n support
- CodeMirror for code editing
- Tiptap for rich text editing
- Socket.IO for real-time communication

## Development

- Run tests: `npm run test:frontend`
- Lint code: `npm run lint`
- Format code: `npm run format`
- Check types: `npm run check` 