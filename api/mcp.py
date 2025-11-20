"""
Vercel Serverless Function - Public MCP HTTP Bridge
Allows anyone to use the AI Image Tools remotely via HTTP
"""

from http.server import BaseHTTPRequestHandler
import json
import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import tools
from src.nano_banana import nano_banana
from src.nano_banana_pro import nano_banana_pro
from src.icon_generator import icon_generator
from src.batch_icon_generator import batch_icon_generator
from src.svg_converter import svg_converter


# Tool registry
TOOLS = {
    'nano_banana': {
        'function': nano_banana,
        'description': 'Fast image generation with Gemini 2.5 Flash'
    },
    'nano_banana_pro': {
        'function': nano_banana_pro,
        'description': 'Professional 4K image generation with Gemini 3 Pro'
    },
    'icon_generator': {
        'function': icon_generator,
        'description': 'Generate SVG icons with 50+ modern styles'
    },
    'batch_icon_generator': {
        'function': batch_icon_generator,
        'description': 'Generate multiple icons concurrently'
    },
    'svg_converter': {
        'function': svg_converter,
        'description': 'Convert images to SVG/SVGZ format'
    }
}


class handler(BaseHTTPRequestHandler):
    """
    Public HTTP API for AI Image Tools
    Anyone can POST requests to use the tools remotely
    """
    
    def do_GET(self):
        """Return available tools and status"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Check if environment variables are configured
        google_api_key = os.getenv('GOOGLE_API_KEY')
        freepik_api_key = os.getenv('FREEPIK_API_KEY')
        
        response = {
            'status': 'online',
            'service': 'AI Image Tools - Public API',
            'version': '1.0.0',
            'endpoint': '/api/mcp',
            'method': 'POST',
            'env': {
                'gemini': bool(google_api_key),
                'freepik': bool(freepik_api_key)
            },
            'tools': {name: {'description': info['description']} for name, info in TOOLS.items()},
            'usage': {
                'url': 'https://ai-image-tools-rosy.vercel.app/api/mcp',
                'example': {
                    'tool': 'nano_banana_pro',
                    'params': {
                        'prompt': 'A beautiful sunset over mountains',
                        'resolution': '2K',
                        'aspect_ratio': '16:9'
                    }
                }
            }
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def do_POST(self):
        """Handle tool execution requests"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            # Extract tool name and parameters
            tool_name = data.get('tool')
            params = data.get('params', {})
            
            if not tool_name:
                self.send_error_response(400, 'Missing "tool" field in request')
                return
            
            if tool_name not in TOOLS:
                self.send_error_response(404, f'Unknown tool: {tool_name}. Available: {list(TOOLS.keys())}')
                return
            
            # Execute tool asynchronously
            tool_function = TOOLS[tool_name]['function']
            
            # Run async function in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(tool_function(**params))
            loop.close()
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': True,
                'tool': tool_name,
                'result': result
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error_response(500, f'Error executing tool: {str(e)}')
    
    def send_error_response(self, code, message):
        """Send error response"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'success': False,
            'error': message
        }
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
