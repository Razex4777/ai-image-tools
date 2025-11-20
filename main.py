"""
AI Image Tools MCP Server - Nano Banana Edition
Provides image generation capabilities using Google's Gemini models:
- Gemini 2.5 Flash Image (nano_banana) - Fast & efficient
- Gemini 3 Pro Image (nano_banana_pro) - Professional quality with 4K, Google Search, Thinking mode
AND background removal using Freepik API
"""

import sys
import os

# Redirect stdout to stderr during imports to prevent pollution
# This ensures that any library initialization logs don't break the MCP JSON-RPC stream
original_stdout = sys.stdout
sys.stdout = sys.stderr

try:
    from mcp.server.fastmcp import FastMCP
    from src.nano_banana import nano_banana
    from src.nano_banana_pro import nano_banana_pro
    from src.icon_generator import icon_generator
    from src.batch_icon_generator import batch_icon_generator
    from src.svg_converter import svg_converter
except Exception as e:
    # If imports fail, we still want to see the error in stderr
    print(f"Error importing modules: {e}", file=sys.stderr)
    raise
finally:
    # Always restore stdout
    sys.stdout = original_stdout

# Initialize FastMCP server
mcp = FastMCP("Nano Banana")

# Register tools with MCP
mcp.tool()(nano_banana)
mcp.tool()(nano_banana_pro)
mcp.tool()(icon_generator)
mcp.tool()(batch_icon_generator)
mcp.tool()(svg_converter)


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
