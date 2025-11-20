"""
Vercel Serverless Function - Simple Status Page
The actual MCP server runs locally via stdio
"""

from http.server import BaseHTTPRequestHandler
import json


class handler(BaseHTTPRequestHandler):
    """
    Simple status endpoint for Vercel deployment
    Shows that the deployment is live
    """
    
    def do_GET(self):
        """Return status information"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'status': 'online',
            'service': 'ai-image-tools-mcp',
            'version': '1.0.0',
            'message': 'MCP server is running locally via stdio protocol',
            'tools': [
                'nano_banana',
                'nano_banana_pro',
                'icon_generator',
                'batch_icon_generator',
                'svg_converter'
            ],
            'deployment': 'vercel',
            'note': 'This is a status page. Use the local MCP server via stdio for tool access.'
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def do_POST(self):
        """Return helpful message for POST requests"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'error': 'MCP server operates via stdio protocol, not HTTP',
            'message': 'Please use the local MCP server configuration in your mcp_config.json',
            'local_server': {
                'command': 'python',
                'args': ['main.py'],
                'working_directory': 'your-project-path'
            }
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
