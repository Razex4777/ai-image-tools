"""
Nano Banana Pro - Professional AI Image Generation with Gemini 3 Pro Image
Advanced features: 4K resolution, 14 reference images, Google Search grounding, Thinking mode
"""

import os
import base64
import requests
from typing import Optional, List, Dict, Any
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO


# Configure APIs
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
FREEPIK_API_KEY = os.getenv("FREEPIK_API_KEY")

# Initialize Google GenAI client
client = None
if GOOGLE_API_KEY:
    client = genai.Client(api_key=GOOGLE_API_KEY)


def _save_as_svg(image: Image.Image, save_path: str) -> None:
    """Helper function to convert PIL Image to SVG with embedded PNG"""
    width, height = image.size
    
    # Convert image to base64
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    png_data = base64.b64encode(buffer.getvalue()).decode()
    
    # Create SVG with embedded PNG
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" 
     xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <image width="{width}" height="{height}" 
           xlink:href="data:image/png;base64,{png_data}"/>
</svg>'''
    
    # Save SVG file
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(svg_content)


async def nano_banana_pro(
    prompt: str,
    reference_images: Optional[List[str]] = None,
    aspect_ratio: str = "1:1",
    resolution: str = "2K",
    output_type: str = "both",
    use_google_search: bool = False,
    show_thinking: bool = False,
    remove_background: bool = False,
    save_path: Optional[str] = None,
) -> str:
    """
    🍌✨ NANO BANANA PRO - Professional image generation with Gemini 3 Pro Image!
    
    State-of-the-art image generation optimized for professional asset production.
    Features advanced reasoning, high-resolution output (up to 4K), Google Search grounding,
    thinking mode, and support for up to 14 reference images.
    
    Args:
        prompt: A detailed, descriptive paragraph about what you want to create or edit.
                The Pro model excels at complex instructions and advanced text rendering.
                Examples:
                - "Create a professional infographic showing quarterly sales data with charts and graphs"
                - "Design a restaurant menu with elegant typography and food photography styling"
                - "Generate a 4K marketing poster for a tech conference with futuristic elements"
        
        reference_images: Optional list of image file paths (max 14 for Pro model!).
                         Supports:
                         - Up to 6 images of objects (high-fidelity inclusion)
                         - Up to 5 images of humans (character consistency)
                         - Combined use for complex compositions
                         Example: ["/path/to/person1.png", "/path/to/object.jpg", ...]
        
        aspect_ratio: Output image aspect ratio. Pro model supports MORE ratios:
                     - "1:1" (default) - Square
                     - "16:9" - Widescreen landscape
                     - "9:16" - Vertical/portrait
                     - "4:3" - Classic landscape
                     - "3:4" - Classic portrait
                     - "2:3" - Portrait
                     - "3:2" - Landscape
                     - "4:5" - Portrait
                     - "5:4" - Landscape
                     - "21:9" - Ultra-wide
        
        resolution: Image resolution (Pro model exclusive feature!):
                   - "1K" - Standard quality (faster)
                   - "2K" (default) - High quality (recommended)
                   - "4K" - Ultra high quality (professional assets)
                   Note: Requires SDK v1.49.0+ with ImageConfig.image_size support
        
        output_type: What to return in the response:
                    - "both" (default) - Returns both text description and image
                    - "image_only" - Returns only the image, no text
        
        use_google_search: Enable Google Search grounding for real-time data (NEW!):
                          - False (default) - Standard generation
                          - True - Use Google Search for facts, current events, weather, stocks
                          Perfect for: Weather maps, stock charts, recent events, factual accuracy
                          Note: Cannot be used with "image_only" mode
        
        show_thinking: Display the model's reasoning process (NEW!):
                      - False (default) - Only show final image
                      - True - Show intermediate "thought images" and reasoning text
                      The Pro model thinks before generating for better composition
        
        remove_background: Remove background using Freepik API (NEW!):
                          - False (default) - Keep generated background
                          - True - Remove background for true transparency with alpha channel
                          Strategy: Automatically adds "isolated object on plain white background" 
                          to prompt, making Freepik API background removal extremely accurate
                          Creates RGBA PNG perfect for logos, stickers, and overlays
                          Requires FREEPIK_API_KEY environment variable
        
        save_path: Optional path to save the generated image(s).
                  If provided, images will be saved to this location.
                  Supports PNG and SVG formats (detected by extension).
                  Examples:
                  - "output.png" - Saves as PNG (default)
                  - "output_4k.png" - For 4K images
                  - "output.svg" - Automatically converts to SVG
    
    Returns:
        Success message with image details, resolution, thinking process (if enabled),
        and save location, or error details
    
    Examples:
        # Simple text-to-image with Pro model
        nano_banana_pro(
            prompt="A professional tech conference poster with bold typography",
            resolution="4K"
        )
        
        # Character-consistent group photo with 5 people
        nano_banana_pro(
            prompt="Office team photo with everyone making funny faces",
            reference_images=["person1.png", "person2.png", "person3.png", 
                             "person4.png", "person5.png"],
            aspect_ratio="5:4",
            resolution="2K"
        )
        
        # Grounded generation with real-time data
        nano_banana_pro(
            prompt="Create an infographic showing today's weather forecast for Tokyo",
            use_google_search=True,
            resolution="2K"
        )
        
        # Complex composition with objects and thinking mode
        nano_banana_pro(
            prompt="Design a product showcase combining all these items in a studio setting",
            reference_images=["product1.png", "product2.png", "product3.png"],
            show_thinking=True,
            resolution="4K",
            save_path="showcase_4k.png"
        )
        
        # Advanced text rendering for menu design
        nano_banana_pro(
            prompt="Create an elegant restaurant menu with sections for appetizers, "
                   "mains, and desserts. Include prices and descriptions in cursive font.",
            aspect_ratio="3:4",
            resolution="2K"
        )
        
        # Transparent logo/sticker generation
        nano_banana_pro(
            prompt="A cute cartoon rocket ship with flames",
            remove_background=True,
            save_path="rocket_transparent.png"
        )
    """
    if not GOOGLE_API_KEY:
        return "🚨 Error: GOOGLE_API_KEY environment variable is not set"
    
    try:
        # Validate aspect ratio
        valid_ratios = ["1:1", "16:9", "9:16", "4:3", "3:4", "2:3", "3:2", "4:5", "5:4", "21:9"]
        if aspect_ratio not in valid_ratios:
            return f"🚨 Error: Invalid aspect_ratio '{aspect_ratio}'. Must be one of {valid_ratios}"
        
        # Validate resolution (supported since SDK v1.49.0)
        valid_resolutions = ["1K", "2K", "4K"]
        if resolution not in valid_resolutions:
            return f"🚨 Error: Invalid resolution '{resolution}'. Must be one of {valid_resolutions}"
        
        # Validate output type
        valid_output_types = ["both", "image_only"]
        if output_type not in valid_output_types:
            return f"🚨 Error: Invalid output_type '{output_type}'. Must be one of {valid_output_types}"
        
        # Validate Google Search constraint
        if use_google_search and output_type == "image_only":
            return "🚨 Error: Google Search grounding cannot be used with 'image_only' mode. Use 'both' instead."
        
        # Modify prompt for background removal
        # Strategy: Add white/gray background instruction so Freepik API can cleanly remove it
        enhanced_prompt = prompt
        if remove_background:
            enhanced_prompt = f"{prompt}. Isolated object on plain white or light gray background, no distracting elements, clean simple background for easy removal, centered composition."
        
        # Build contents array
        contents = [enhanced_prompt]
        
        # Process reference images
        if reference_images:
            if len(reference_images) > 14:
                return "🚨 Error: Maximum 14 reference images allowed for Pro model"
            
            for img_path in reference_images:
                if not os.path.exists(img_path):
                    return f"🚨 Error: Reference image not found at {img_path}"
                
                try:
                    img = Image.open(img_path)
                    contents.append(img)
                except Exception as e:
                    return f"🚨 Error loading image {img_path}: {str(e)}"
        
        # Configure generation (ImageConfig.image_size supported since SDK v1.49.0)
        config_params: Dict[str, Any] = {
            "image_config": types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=resolution,
            ),
            "response_modalities": ['IMAGE'] if output_type == "image_only" else ['TEXT', 'IMAGE']
        }
        
        # Add Google Search grounding if enabled
        if use_google_search:
            config_params["tools"] = [types.Tool(google_search=types.GoogleSearch())]
        
        config = types.GenerateContentConfig(**config_params)
        
        # Generate content
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=contents,
            config=config,
        )
        
        # Process results
        result_parts = []
        image_count = 0
        thought_count = 0
        text_response = None
        saved_paths = []
        temp_images = []  # Store (temp_path, final_path, wants_svg) tuples for background removal
        
        for part in response.parts:
            # Process thinking/reasoning (if show_thinking enabled)
            if show_thinking and hasattr(part, 'thought') and part.thought:
                thought_count += 1
                
                if part.text is not None:
                    result_parts.append(f"🧠 Thought {thought_count} (Text): {part.text}")
                
                if hasattr(part, 'inline_data') and part.inline_data is not None:
                    result_parts.append(f"🧠 Thought {thought_count} (Image): Intermediate composition test")
                    # Optionally save thought images if requested
            
            # Process final text
            elif part.text is not None:
                text_response = part.text
                result_parts.append(f"📝 Description: {part.text}")
            
            # Process final images
            elif part.inline_data is not None:
                image_count += 1
                image = Image.open(BytesIO(part.inline_data.data))
                
                # Determine final save path and format
                actual_save_path = None
                wants_svg = False
                if save_path:
                    base, ext = os.path.splitext(save_path)
                    wants_svg = ext.lower() == ".svg"
                    
                    if image_count > 1:
                        if wants_svg:
                            actual_save_path = f"{base}_{image_count}.svg"
                        else:
                            actual_save_path = f"{base}_{image_count}.png"
                    else:
                        if wants_svg:
                            actual_save_path = f"{base}.svg"
                        else:
                            actual_save_path = f"{base}.png"
                    
                    if remove_background:
                        # Save to temporary location first for background removal
                        import tempfile
                        temp_fd, temp_path = tempfile.mkstemp(suffix=".png")
                        os.close(temp_fd)
                        image.save(temp_path, "PNG")
                        temp_images.append((temp_path, actual_save_path, wants_svg))
                        saved_paths.append(temp_path)
                        result_parts.append(f"🖼️ Image {image_count} generated (pending background removal)")
                    else:
                        # No background removal, save directly
                        if wants_svg:
                            _save_as_svg(image, actual_save_path)
                            result_parts.append(f"💾 Image {image_count} saved as SVG: {actual_save_path}")
                        else:
                            image.save(actual_save_path, "PNG")
                            result_parts.append(f"💾 Image {image_count} saved as PNG: {actual_save_path}")
                else:
                    result_parts.append(f"🖼️ Image {image_count} generated")
        
        # Apply background removal if requested using Freepik API
        if remove_background and saved_paths:
            if not FREEPIK_API_KEY:
                result_parts.append("\n⚠️  Warning: FREEPIK_API_KEY not set, skipping background removal")
            else:
                result_parts.append("\n🎭 Removing backgrounds with Freepik API...")
                
                for idx, img_path in enumerate(saved_paths):
                    try:
                        # Upload to temporary hosting
                        result_parts.append(f"📤 Processing {os.path.basename(img_path)}...")
                        
                        public_url = None
                        try:
                            with open(img_path, "rb") as f:
                                uguu_response = requests.post(
                                    "https://uguu.se/upload",
                                    files={"files[]": f},
                                    timeout=30
                                )
                                if uguu_response.status_code == 200:
                                    data = uguu_response.json()
                                    if data.get("success") and data.get("files"):
                                        public_url = data["files"][0]["url"]
                        except:
                            pass
                        
                        if not public_url:
                            try:
                                with open(img_path, "rb") as f:
                                    ox_response = requests.post("https://0x0.st", files={"file": f}, timeout=30)
                                    if ox_response.status_code == 200:
                                        public_url = ox_response.text.strip()
                            except:
                                pass
                        
                        if not public_url:
                            result_parts.append(f"⚠️  Upload failed for {os.path.basename(img_path)}")
                            continue
                        
                        # Call Freepik API
                        freepik_response = requests.post(
                            "https://api.freepik.com/v1/ai/beta/remove-background",
                            headers={
                                "Content-Type": "application/x-www-form-urlencoded",
                                "x-freepik-api-key": FREEPIK_API_KEY,
                            },
                            data={"image_url": public_url},
                            timeout=60
                        )
                        
                        if freepik_response.status_code == 200:
                            data = freepik_response.json()
                            # Freepik returns a URL to download, not base64
                            transparent_url = data.get("url") or data.get("high_resolution")
                            
                            if transparent_url:
                                # Download the transparent image
                                result_parts.append("💾 Downloading transparent version...")
                                download_response = requests.get(transparent_url, timeout=30)
                                
                                if download_response.status_code == 200:
                                    transparent_img = Image.open(BytesIO(download_response.content))
                                    
                                    # Find the final path for this temp file
                                    final_path = None
                                    wants_svg_output = False
                                    for temp_path, target_path, is_svg in temp_images:
                                        if temp_path == img_path:
                                            final_path = target_path
                                            wants_svg_output = is_svg
                                            break
                                    
                                    if final_path:
                                        # Save to final path in requested format
                                        if wants_svg_output:
                                            _save_as_svg(transparent_img, final_path)
                                            result_parts.append(f"✨ Transparent SVG saved: {os.path.basename(final_path)}")
                                        else:
                                            transparent_img.save(final_path, "PNG")
                                            result_parts.append(f"✨ Background removed: {os.path.basename(final_path)}")
                                else:
                                    result_parts.append(f"⚠️  Download failed: {download_response.status_code}")
                            else:
                                result_parts.append(f"⚠️  No transparent URL in response")
                        else:
                            result_parts.append(f"⚠️  Freepik API error: {freepik_response.status_code}")
                    
                    except Exception as e:
                        result_parts.append(f"⚠️  Error processing {os.path.basename(img_path)}: {str(e)[:100]}")
                
                # Cleanup temporary files
                for temp_path, _, _ in temp_images:
                    try:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                    except:
                        pass  # Silently ignore cleanup errors
        
        # Build final response
        response_lines = [
            "✅ Nano Banana Pro generation complete!",
            f"🎨 Model: Gemini 3 Pro Image Preview",
            f"📏 Resolution: {resolution}",
            f"📏 Aspect Ratio: {aspect_ratio}",
        ]
        
        if use_google_search:
            response_lines.append("🔍 Google Search: Enabled (real-time grounding)")
        if show_thinking and thought_count > 0:
            response_lines.append(f"🧠 Thinking Steps: {thought_count} reasoning iterations")
        
        if reference_images:
            response_lines.append(f"🖼️ Reference Images: {len(reference_images)}")
        
        if remove_background:
            response_lines.append("🎭 Background Removal: Enabled (Freepik API)")
        
        response_lines.append(f"📊 Images Generated: {image_count}")
        response_lines.append("")
        response_lines.extend(result_parts)
        
        return "\n".join(response_lines)
        
    except Exception as e:
        return f"🚨 Error in nano_banana_pro: {str(e)}"
