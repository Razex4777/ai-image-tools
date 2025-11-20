"""
Vercel Serverless Function for MCP HTTP Bridge
Exposes MCP tools over HTTP for remote access
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.nano_banana import nano_banana
from src.nano_banana_pro import nano_banana_pro
from src.icon_generator import icon_generator
from src.batch_icon_generator import batch_icon_generator
from src.svg_converter import svg_converter


class handler(BaseHTTPRequestHandler):
    """
    Vercel serverless function handler
    Receives HTTP requests and routes to MCP tools
    """
    
    async def do_POST(self):
        """Handle POST requests to MCP tools"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            # Extract tool and parameters
            tool_name = data.get('tool')
            params = data.get('params', {})
            
            # Route to appropriate tool
            result = None
            if tool_name == 'nano_banana':
                result = await nano_banana(**params)
            elif tool_name == 'nano_banana_pro':
                result = await nano_banana_pro(**params)
            elif tool_name == 'icon_generator':
                result = await icon_generator(**params)
            elif tool_name == 'batch_icon_generator':
                result = await batch_icon_generator(**params)
            elif tool_name == 'svg_converter':
                result = await svg_converter(**params)
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': f'Unknown tool: {tool_name}'
                }).encode())
                return
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': True,
                'result': result
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': str(e)
            }).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Health check endpoint"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            'status': 'online',
            'service': 'ai-image-tools-mcp',
            'tools': [
                'nano_banana',
                'nano_banana_pro',
                'icon_generator',
                'batch_icon_generator',
                'svg_converter'
            ]
        }
        self.wfile.write(json.dumps(response).encode())
