"""
Vercel Serverless Function - MCP Protocol + REST API Bridge
Supports both MCP protocol (for mcp-remote) and simple REST API
"""

from http.server import BaseHTTPRequestHandler
import json
import asyncio
import sys
import os
from typing import Dict, Any, List

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import tools
from src.nano_banana import nano_banana
from src.nano_banana_pro import nano_banana_pro
from src.icon_generator import icon_generator
from src.batch_icon_generator import batch_icon_generator
from src.svg_converter import svg_converter


# Tool registry with MCP-compatible schemas
TOOLS = {
    'nano_banana': {
        'function': nano_banana,
        'description': 'Fast image generation with Gemini 2.5 Flash',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'prompt': {'type': 'string', 'description': 'Image description'},
                'aspect_ratio': {'type': 'string', 'enum': ['1:1', '16:9', '9:16', '4:3', '3:4']},
                'remove_background': {'type': 'boolean'},
            },
            'required': ['prompt']
        }
    },
    'nano_banana_pro': {
        'function': nano_banana_pro,
        'description': 'Professional 4K image generation with Gemini 3 Pro',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'prompt': {'type': 'string'},
                'resolution': {'type': 'string', 'enum': ['1K', '2K', '4K']},
                'aspect_ratio': {'type': 'string'},
            },
            'required': ['prompt']
        }
    },
    'icon_generator': {
        'function': icon_generator,
        'description': 'Generate SVG icons with 50+ modern styles',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'prompt': {'type': 'string'},
                'style': {'type': 'string'},
            },
            'required': ['prompt']
        }
    },
    'batch_icon_generator': {
        'function': batch_icon_generator,
        'description': 'Generate multiple icons concurrently',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'prompts': {'type': 'array'},
            }
        }
    },
    'svg_converter': {
        'function': svg_converter,
        'description': 'Convert images to SVG/SVGZ format',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'input_path': {'type': 'string'},
            }
        }
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
        """Handle both MCP protocol and REST API requests"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            # Check if this is MCP JSON-RPC request
            if 'jsonrpc' in data:
                self.handle_mcp_request(data)
            else:
                # Legacy REST API
                self.handle_rest_request(data)
                
        except Exception as e:
            self.send_error_response(500, f'Error: {str(e)}')
    
    def handle_mcp_request(self, data: Dict[str, Any]):
        """Handle MCP JSON-RPC protocol requests"""
        method = data.get('method')
        request_id = data.get('id')
        params = data.get('params', {})
        
        try:
            if method == 'initialize':
                # MCP initialize handshake
                response = {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'result': {
                        'protocolVersion': '2024-11-05',
                        'capabilities': {
                            'tools': {}
                        },
                        'serverInfo': {
                            'name': 'ai-image-tools',
                            'version': '1.0.0'
                        }
                    }
                }
            
            elif method == 'tools/list':
                # Return available tools in MCP format
                tools_list = []
                for name, info in TOOLS.items():
                    tools_list.append({
                        'name': name,
                        'description': info['description'],
                        'inputSchema': info.get('inputSchema', {})
                    })
                
                response = {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'result': {
                        'tools': tools_list
                    }
                }
            
            elif method == 'tools/call':
                # Execute tool
                tool_name = params.get('name')
                tool_args = params.get('arguments', {})
                
                if tool_name not in TOOLS:
                    raise ValueError(f'Unknown tool: {tool_name}')
                
                # Execute tool
                tool_function = TOOLS[tool_name]['function']
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(tool_function(**tool_args))
                loop.close()
                
                response = {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'result': {
                        'content': [
                            {
                                'type': 'text',
                                'text': result
                            }
                        ]
                    }
                }
            
            else:
                raise ValueError(f'Unknown method: {method}')
            
            # Send MCP response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            # MCP error response
            error_response = {
                'jsonrpc': '2.0',
                'id': request_id,
                'error': {
                    'code': -32603,
                    'message': str(e)
                }
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())
    
    def handle_rest_request(self, data: Dict[str, Any]):
        """Handle simple REST API requests (legacy)"""
        tool_name = data.get('tool')
        params = data.get('params', {})
        
        if not tool_name:
            self.send_error_response(400, 'Missing "tool" field')
            return
        
        if tool_name not in TOOLS:
            self.send_error_response(404, f'Unknown tool: {tool_name}')
            return
        
        # Execute tool
        tool_function = TOOLS[tool_name]['function']
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(tool_function(**params))
        loop.close()
        
        # Send REST response
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
