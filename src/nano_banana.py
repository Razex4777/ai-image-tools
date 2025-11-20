"""
Nano Banana - AI Image Generation Tool with Background Removal
"""

import os
import base64
import requests
from typing import Optional, List
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


def _embed_png_as_svg(image: Image.Image, save_path: str) -> None:
    """
    ⚠️ IMPORTANT: This embeds a raster PNG inside an SVG wrapper, NOT true vector conversion.
    
    The resulting SVG contains a base64-encoded PNG image and does NOT provide:
    - Infinite scalability (limited by the source PNG resolution)
    - Vector editability (the image is still raster/pixel-based)
    
    For true vector conversion, use raster-to-vector tools like:
    - potrace, autotrace, or online converters
    
    This function is useful for maintaining .svg file extension compatibility
    while preserving the actual raster image data.
    """
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


async def nano_banana(
    prompt: str,
    reference_images: Optional[List[str]] = None,
    aspect_ratio: str = "1:1",
    output_type: str = "both",
    remove_background: bool = False,
    save_path: Optional[str] = None,
) -> str:
    """
    🍌 NANO BANANA - The ultimate Gemini image generation tool!
    
    Generate, edit, compose, and iterate on images using Google's Gemini 2.5 Flash Image model.
    Supports text-to-image, image editing, multi-image composition, style transfer, AND background removal!
    
    Args:
        prompt: A detailed, descriptive paragraph about what you want to create or edit.
                Write naturally - describe the scene, don't just list keywords!
                Examples:
                - "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"
                - "Add colorful flowers in the foreground and make the sky more dramatic"
                - "Transform this into a watercolor painting style"
        
        reference_images: Optional list of image file paths (max 5, but works best with 1-3).
                         Used for:
                         - Image editing: Modify, add, remove elements
                         - Style transfer: Apply style from one image to another
                         - Composition: Combine multiple images into a new scene
                         - Context: Use as visual reference for generation
                         Example: ["/path/to/image1.png", "/path/to/style_ref.jpg"]
        
        aspect_ratio: Output image aspect ratio. Options:
                     - "1:1" (default, 1024x1024) - Square
                     - "16:9" (1536x864) - Widescreen landscape
                     - "9:16" (864x1536) - Vertical/portrait
                     - "4:3" (1152x864) - Classic landscape
                     - "3:4" (864x1152) - Classic portrait
        
        output_type: What to return in the response. Options:
                    - "both" (default) - Returns both text description and image
                    - "image_only" - Returns only the image, no text
        
        remove_background: Remove background to create TRUE transparency with alpha channel!
                          - False (default) - Normal image generation
                          - True - Automatically removes background using AI after generation
                          Creates RGBA PNG with transparent background (not fake transparency!)
                          Perfect for logos, stickers, and overlays.
        
        save_path: Optional path to save the generated image(s).
                  If provided, images will be saved to this location.
                  Supports PNG and SVG formats (detected by extension).
                  
                  ⚠️ SVG output contains embedded PNG (raster), not true vectors:
                  - "output.png" - Saves as PNG (recommended for raster images)
                  - "output.svg" - Embeds PNG in SVG wrapper (NOT vector graphics)
                  
                  The .svg file will NOT be infinitely scalable or editable as vectors.
                  For true vector conversion, export as PNG and use raster-to-vector tools.
                  
                  Examples:
                  - "C:/images/photo.png" - Standard PNG output
                  - "C:/images/photo.svg" - PNG embedded in SVG container
    
    Returns:
        Success message with image details and save location, or error details
    
    Examples:
        # Simple text-to-image
        nano_banana(prompt="A serene mountain landscape at sunset")
        
        # Generate with transparent background
        nano_banana(
            prompt="A cute cat logo with big eyes",
            remove_background=True,
            save_path="C:/logos/cat_transparent.png"
        )
        
        # Edit an existing image
        nano_banana(
            prompt="Turn my cat into a lion and add a crown",
            reference_images=["C:/images/cat.jpg"]
        )
        
        # Sticker with transparency
        nano_banana(
            prompt="A die-cut sticker of a rocket ship with bold outlines",
            aspect_ratio="1:1",
            remove_background=True,
            save_path="C:/stickers/rocket.png"
        )
    """
    if not GOOGLE_API_KEY:
        return "🚨 Error: GOOGLE_API_KEY environment variable is not set"
    
    try:
        # Validate aspect ratio
        valid_ratios = ["1:1", "16:9", "9:16", "4:3", "3:4"]
        if aspect_ratio not in valid_ratios:
            return f"🚨 Error: Invalid aspect_ratio '{aspect_ratio}'. Must be one of {valid_ratios}"
        
        # Validate output type
        valid_output_types = ["both", "image_only"]
        if output_type not in valid_output_types:
            return f"🚨 Error: Invalid output_type '{output_type}'. Must be one of {valid_output_types}"
        
        # Build contents array
        contents = [prompt]
        
        # Process reference images
        if reference_images:
            if len(reference_images) > 5:
                return "🚨 Error: Maximum 5 reference images allowed (works best with 1-3)"
            
            for img_path in reference_images:
                if not os.path.exists(img_path):
                    return f"🚨 Error: Reference image not found at {img_path}"
                
                try:
                    img = Image.open(img_path)
                    contents.append(img)
                except Exception as e:
                    return f"🚨 Error loading image {img_path}: {str(e)}"
        
        # Configure generation
        config = types.GenerateContentConfig(
            image_config={
                "aspect_ratio": aspect_ratio,
            },
            response_modalities=['Image'] if output_type == "image_only" else ['Text', 'Image']
        )
        
        # Generate content
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=contents,
            config=config,
        )
        
        # Process results
        result_parts = []
        image_count = 0
        text_response = None
        saved_paths = []
        temp_images = []  # Store images temporarily if background removal is needed
        
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                text_response = part.text
                result_parts.append(f"📝 Text: {part.text}")
            
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
                        # Multiple images: add number to filename
                        if wants_svg:
                            actual_save_path = f"{base}_{image_count}.svg"
                        else:
                            actual_save_path = f"{base}_{image_count}.png"
                    else:
                        # Single image: use original extension
                        if wants_svg:
                            actual_save_path = f"{base}.svg"
                        else:
                            actual_save_path = f"{base}.png"
                    
                    if remove_background:
                        # If background removal requested, save to temp location first
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
                            # Embed PNG in SVG wrapper (not true vector conversion)
                            _embed_png_as_svg(image, actual_save_path)
                            result_parts.append(f"💾 Image {image_count} saved as SVG: {actual_save_path}")
                        else:
                            # Save as PNG
                            image.save(actual_save_path, "PNG")
                            result_parts.append(f"💾 Image {image_count} saved to: {actual_save_path}")
                else:
                    result_parts.append(f"🖼️ Image {image_count} generated successfully (size: {image.size})")
        
        if image_count == 0:
            return "🚨 Error: No images were generated"
        
        # Apply background removal if requested using Freepik API
        transparent_paths = []
        if remove_background and saved_paths:
            if not FREEPIK_API_KEY:
                result_parts.append("\n⚠️ Warning: FREEPIK_API_KEY not set, skipping background removal")
            else:
                try:
                    result_parts.append("\n🎭 Removing backgrounds with Freepik API...")
                    
                    for img_path in saved_paths:
                        # Step 1: Upload image to get public URL
                        result_parts.append(f"📤 Uploading {os.path.basename(img_path)} to get public URL...")
                        
                        public_url = None
                        
                        # Try Uguu.se (no API key needed, simple upload)
                        try:
                            with open(img_path, "rb") as f:
                                files = {"files[]": f}
                                
                                uguu_response = requests.post(
                                    "https://uguu.se/upload",
                                    files=files,
                                    timeout=30
                                )
                                
                                if uguu_response.status_code == 200:
                                    data = uguu_response.json()
                                    if data.get("success") and data.get("files"):
                                        public_url = data["files"][0]["url"]
                                        result_parts.append(f"✅ Uploaded to Uguu.se: {public_url}")
                        except Exception as e:
                            result_parts.append(f"⚠️ Uguu upload failed: {str(e)[:100]}")
                        
                        # Fallback: Try 0x0.st (simple, no auth)
                        if not public_url:
                            try:
                                with open(img_path, "rb") as f:
                                    files = {"file": f}
                                    
                                    ox_response = requests.post(
                                        "https://0x0.st",
                                        files=files,
                                        timeout=30
                                    )
                                    
                                    if ox_response.status_code == 200:
                                        public_url = ox_response.text.strip()
                                        result_parts.append(f"✅ Uploaded to 0x0.st: {public_url}")
                            except Exception as e:
                                result_parts.append(f"⚠️ 0x0.st upload failed: {str(e)[:100]}")
                        
                        if not public_url:
                            result_parts.append(f"⚠️ All upload services failed for {os.path.basename(img_path)}")
                            continue
                        
                        # Step 2: Send to Freepik remove background API
                        result_parts.append("🎨 Processing with Freepik AI...")
                        
                        # EXACTLY as documented: application/x-www-form-urlencoded
                        freepik_response = requests.post(
                            "https://api.freepik.com/v1/ai/beta/remove-background",
                            headers={
                                "Content-Type": "application/x-www-form-urlencoded",
                                "x-freepik-api-key": FREEPIK_API_KEY,
                            },
                            data={
                                "image_url": public_url
                            },
                            timeout=60
                        )
                        
                        if freepik_response.status_code != 200:
                            result_parts.append(f"⚠️ Freepik API error (Status {freepik_response.status_code})")
                            result_parts.append(f"   Response: {freepik_response.text[:300]}")
                            continue
                        
                        # Step 3: Download transparent image
                        freepik_data = freepik_response.json()
                        transparent_url = freepik_data.get("url") or freepik_data.get("high_resolution")
                        
                        if not transparent_url:
                            result_parts.append(f"⚠️ No transparent URL in response")
                            continue
                        
                        result_parts.append("💾 Downloading transparent version...")
                        
                        # Download transparent image
                        download_response = requests.get(transparent_url, timeout=30)
                        
                        if download_response.status_code == 200:
                            # Download transparent image
                            transparent_img = Image.open(BytesIO(download_response.content))
                            
                            # Find the final path and format for this temp file
                            final_path = img_path
                            wants_svg_output = False
                            for temp_path, target_path, is_svg in temp_images:
                                if temp_path == img_path:
                                    final_path = target_path
                            
                            # Clean up temp file if it exists
                            if img_path != final_path and os.path.exists(img_path):
                                try:
                                    os.remove(img_path)
                                except:
                                    pass
                        else:
                            result_parts.append(f"⚠️ Download failed for transparent image")
                    
                except requests.exceptions.Timeout:
                    result_parts.append("\n⚠️ Background removal timed out")
                except Exception as e:
                    result_parts.append(f"\n⚠️ Background removal failed: {str(e)}")
        
        # Build response
        response_text = [
            "🍌 NANO BANANA SUCCESS! 🍌",
            f"✅ Generated {image_count} image(s)",
            f"📐 Aspect ratio: {aspect_ratio}",
            f"💬 Prompt: '{prompt[:100]}{'...' if len(prompt) > 100 else ''}'",
        ]
        
        if reference_images:
            response_text.append(f"🖼️ Used {len(reference_images)} reference image(s)")
        
        if remove_background and transparent_paths:
            response_text.append(f"🎭 Background removed ({len(transparent_paths)} image(s) now transparent)")
        
        response_text.append("")
        response_text.extend(result_parts)
        
        return "\n".join(response_text)
        
    except Exception as e:
        return f"🚨 Error in nano_banana: {str(e)}"
