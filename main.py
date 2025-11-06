"""
AI Image Tools MCP Server - Nano Banana Edition
Provides image generation capabilities using Google's Gemini 2.5 Flash Image API
AND background removal using Freepik API
"""

from mcp.server.fastmcp import FastMCP
from src.nano_banana import nano_banana

# Initialize FastMCP server
mcp = FastMCP("Nano Banana")


# Register the nano_banana tool with MCP
mcp.tool()(nano_banana)


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
