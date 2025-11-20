# 🎨 AI Image Tools - MCP Server

Professional AI image generation tools powered by Google Gemini.

## 🚀 Features

- **Nano Banana** - Fast image generation (Gemini 2.5 Flash)
- **Nano Banana Pro** - Professional quality (Gemini 3 Pro, 4K, 14 refs)
- **Icon Generator** - SVG icon generation with 40+ styles
- **Batch Generator** - Process multiple icons at once
- **SVG Converter** - Convert images to SVG/SVGZ
- **Background Removal** - Freepik API integration for transparency

## 📦 Installation

```bash
# Clone repository (replace YOUR_USERNAME with your GitHub username)
git clone https://github.com/YOUR_USERNAME/ai-image-tools.git
cd ai-image-tools

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_API_KEY="your_key"
export FREEPIK_API_KEY="your_key"
```

## 🔧 Local Usage

```bash
python main.py
```

## 🌐 Deploy to Vercel

```bash
vercel deploy
```

Set environment variables in Vercel dashboard:
- `GOOGLE_API_KEY`
- `FREEPIK_API_KEY`

## 📝 License

MIT
