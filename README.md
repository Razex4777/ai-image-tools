# 🎨 AI Image Tools - Public API & MCP Server

Professional image generation API powered by Google Gemini. **Use it remotely or run locally!**

## 🌐 Public API (Use Remotely)

**Anyone can use this API!** No installation required.

### API Endpoint
```bash
POST https://ai-image-tools-rosy.vercel.app/api/mcp
```

### Example Usage

```bash
curl -X POST https://ai-image-tools-rosy.vercel.app/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "nano_banana_pro",
    "params": {
      "prompt": "A futuristic rocket ship",
      "resolution": "2K",
      "aspect_ratio": "1:1"
    }
  }'
```

```python
import requests

response = requests.post(
    'https://ai-image-tools-rosy.vercel.app/api/mcp',
    json={
        'tool': 'icon_generator',
        'params': {
            'prompt': 'rocket',
            'style': 'glassmorphism'
        }
    }
)
result = response.json()
print(result['result'])
```

### 🛠️ Available Tools

- **nano_banana** - Fast image generation (Gemini 2.5 Flash)
- **nano_banana_pro** - Professional 4K (Gemini 3 Pro, up to 14 refs)
- **icon_generator** - SVG icons with 50+ modern styles
- **batch_icon_generator** - Generate multiple icons concurrently
- **svg_converter** - Convert images to SVG/SVGZ

## 🖥️ Local MCP Server

Run locally for faster performance and private API keys.

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/Razex4777/ai-image-tools.git
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
