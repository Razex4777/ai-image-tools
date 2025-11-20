#!/usr/bin/env python3
"""
Remote MCP Bridge - Connects local MCP clients to remote Vercel API
Allows using the public API through MCP stdio protocol
"""

import sys
import json
import asyncio
import requests
from typing import Any, Dict

# Import FastMCP for protocol handling
from mcp import FastMCP

# Get API URL from command line argument
if len(sys.argv) < 2:
    print("Usage: remote_bridge.py <api_url>", file=sys.stderr)
    sys.exit(1)

API_URL = sys.argv[1]

# Create MCP server
mcp = FastMCP("AI Image Tools (Remote)")

# Tool definitions
@mcp.tool()
async def nano_banana(
    prompt: str,
    reference_images: list[str] | None = None,
    aspect_ratio: str = "1:1",
    output_type: str = "both",
    remove_background: bool = False,
    save_path: str | None = None,
) -> str:
    """
    🍌 NANO BANANA - Fast image generation with Gemini 2.5 Flash!
    
    Remote connection to https://ai-image-tools-rosy.vercel.app
    """
    params = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "output_type": output_type,
        "remove_background": remove_background,
    }
    if reference_images:
        params["reference_images"] = reference_images
    if save_path:
        params["save_path"] = save_path
    
    return await call_remote_tool("nano_banana", params)


@mcp.tool()
async def nano_banana_pro(
    prompt: str,
    reference_images: list[str] | None = None,
    aspect_ratio: str = "1:1",
    resolution: str = "2K",
    output_type: str = "both",
    use_google_search: bool = False,
    show_thinking: bool = False,
    remove_background: bool = False,
    save_path: str | None = None,
) -> str:
    """
    🍌✨ NANO BANANA PRO - Professional 4K with Gemini 3 Pro Image!
    
    Remote connection to https://ai-image-tools-rosy.vercel.app
    """
    params = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
        "output_type": output_type,
        "use_google_search": use_google_search,
        "show_thinking": show_thinking,
        "remove_background": remove_background,
    }
    if reference_images:
        params["reference_images"] = reference_images
    if save_path:
        params["save_path"] = save_path
    
    return await call_remote_tool("nano_banana_pro", params)


@mcp.tool()
async def icon_generator(
    prompt: str,
    style: str | None = None,
    sizes: list[int] | None = None,
    save_path: str | None = None,
) -> str:
    """
    🎨 ICON GENERATOR - SVG icons with 50+ modern styles!
    
    Remote connection to https://ai-image-tools-rosy.vercel.app
    """
    params = {"prompt": prompt}
    if style:
        params["style"] = style
    if sizes:
        params["sizes"] = sizes
    if save_path:
        params["save_path"] = save_path
    
    return await call_remote_tool("icon_generator", params)


@mcp.tool()
async def batch_icon_generator(
    prompts: list[str] | None = None,
    icons: list[dict] | None = None,
    style: str | None = None,
    sizes: list[int] | None = None,
    output_dir: str = "batch_icons",
) -> str:
    """
    📦 BATCH ICON GENERATOR - Generate multiple icons concurrently!
    
    Remote connection to https://ai-image-tools-rosy.vercel.app
    """
    params = {"output_dir": output_dir}
    if prompts:
        params["prompts"] = prompts
    if icons:
        params["icons"] = icons
    if style:
        params["style"] = style
    if sizes:
        params["sizes"] = sizes
    
    return await call_remote_tool("batch_icon_generator", params)


@mcp.tool()
async def svg_converter(
    input_path: str | None = None,
    input_paths: list[str] | None = None,
    output_dir: str | None = None,
    quality: int = 95,
    compress: bool = False,
) -> str:
    """
    🔄 SVG CONVERTER - Convert images to SVG/SVGZ!
    
    Remote connection to https://ai-image-tools-rosy.vercel.app
    """
    params = {"quality": quality, "compress": compress}
    if input_path:
        params["input_path"] = input_path
    if input_paths:
        params["input_paths"] = input_paths
    if output_dir:
        params["output_dir"] = output_dir
    
    return await call_remote_tool("svg_converter", params)


async def call_remote_tool(tool_name: str, params: Dict[str, Any]) -> str:
    """Call remote API endpoint"""
    try:
        response = requests.post(
            API_URL,
            json={"tool": tool_name, "params": params},
            headers={"Content-Type": "application/json"},
            timeout=120  # 2 minute timeout for image generation
        )
        
        data = response.json()
        
        if response.status_code == 200 and data.get("success"):
            return data.get("result", "Success (no result data)")
        else:
            error_msg = data.get("error", f"HTTP {response.status_code}")
            return f"🚨 Remote API Error: {error_msg}"
    
    except requests.exceptions.Timeout:
        return "🚨 Error: Request timed out (>2 minutes). Try a simpler prompt or smaller batch."
    except requests.exceptions.RequestException as e:
        return f"🚨 Connection Error: {str(e)}"
    except Exception as e:
        return f"🚨 Unexpected Error: {str(e)}"


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
