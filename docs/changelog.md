# Changelog

## 2025-11-20 21:52
- **DEPLOYMENT READY**: Created Vercel HTTP bridge in `api/mcp.py`
- **CLEANED**: Removed all test files, extra MD docs, and example images
- **UPDATED**: Enhanced `.gitignore` with comprehensive __pycache__ patterns
- **UPDATED**: Refreshed `project_structure.md` to reflect clean production structure
- **ADDED**: `vercel.json` for Vercel deployment configuration
- **ADDED**: `requirements-vercel.txt` for serverless function dependencies
- Repository ready for GitHub and Vercel deployment

## 2025-11-20 21:42
- **REFACTORED**: `nano_banana_pro.py` now uses temporary files for background removal
- **OPTIMIZATION**: Only saves final transparent image to user's path (no double-write)
- **CLEANUP**: Automatic cleanup of temporary files after processing
- **MATCHING**: Flow now matches `nano_banana.py` pattern perfectly

## 2025-11-20 21:08
- **MAJOR FEATURE**: Added `nano_banana_pro.py` - Professional image generation with Gemini 3 Pro Image Preview
- **New Capabilities**:
  - 4K resolution support (1K, 2K, 4K image sizes)
  - Up to 14 reference images (6 objects + 5 humans for character consistency)
  - Google Search grounding for real-time data (weather, stocks, events)
  - Thinking mode with reasoning process visualization
  - Advanced text rendering for infographics, menus, diagrams
  - 10 aspect ratios (added 2:3, 3:2, 4:5, 5:4, 21:9)
- Updated `src/__init__.py` to export `nano_banana_pro`
- Updated `main.py` to register nano_banana_pro with MCP server
- Updated `docs/project_structure.md` with new file and enhanced formatting
- Created `docs/MODEL_COMPARISON.md` - Comprehensive comparison guide
- Created `docs/NANO_BANANA_PRO.md` - Quick reference and examples
- Model comparison: nano_banana (fast) vs nano_banana_pro (professional quality)
- File size: 295 lines (under 500-line limit ✅)

## 2025-11-18 20:34
- Initialized docs/ directory with changelog.md and project_structure.md
- Validated existing project structure
