# Project Structure

## Overview
AI Image Tools - Professional MCP server for AI-powered image generation and processing.
Dual Gemini models: Fast (2.5 Flash) and Professional (3 Pro Image with 4K, Google Search, Thinking mode).

## Directory Structure
```
ai-image-tools/
├── 📁 api/                               # Vercel deployment endpoints
│   └── 📄 mcp.py                         # HTTP MCP bridge for remote access
├── 📁 docs/                              # Documentation directory
│   ├── 📄 changelog.md                   # Historical record of changes
│   └── 📄 project_structure.md           # This file - current architecture
├── 📁 examples/                          # Generated images output folder
│   └── 📄 .gitkeep                       # Keep folder in git
├── 📁 src/                               # Source code directory
│   ├── 📄 __init__.py                    # Package initialization and exports
│   ├── 📄 nano_banana.py                 # Gemini 2.5 Flash Image (fast & efficient)
│   ├── 📄 nano_banana_pro.py             # Gemini 3 Pro Image (professional, 4K, grounding)
│   ├── 📄 icon_generator.py              # SVG icon generation tool
│   ├── 📄 batch_icon_generator.py        # Batch icon processing
│   └── 📄 svg_converter.py               # Image to SVG/SVGZ converter
├── 📄 .gitignore                         # Git exclusions
├── 📄 main.py                            # Local MCP server entry point
├── 📄 vercel.json                        # Vercel deployment configuration
├── 📄 pyproject.toml                     # Project metadata and dependencies
├── 📄 requirements.txt                   # Python dependencies (local)
├── 📄 requirements-vercel.txt            # Python dependencies (Vercel)
├── 📄 uv.lock                            # Dependency lock file
└── 📄 README.md                          # Project documentation

## Key Files

### Core Application
- `main.py`: Local MCP server entry point - stdio-based communication
- `api/mcp.py`: HTTP MCP bridge for Vercel deployment - remote access

### Image Generation Tools
- `src/nano_banana.py`: Fast image generation (Gemini 2.5 Flash, 1024px)
- `src/nano_banana_pro.py`: Professional quality (Gemini 3 Pro, up to 4K, 14 ref images, Google Search)
- `src/icon_generator.py`: Icon generation with 40+ style presets
- `src/batch_icon_generator.py`: Batch processing for multiple icons
- `src/svg_converter.py`: Convert images to SVG/SVGZ format

### Configuration
- `vercel.json`: Vercel deployment settings and environment variables
- `pyproject.toml`, `requirements.txt`, `uv.lock`: Dependency management
- `.gitignore`: Git exclusions (cache, venv, generated images)

## Deployment Options

### Local (MCP stdio)
```bash
python main.py
```

### Remote (HTTP via Vercel)
```bash
vercel deploy
```
