"""
Icon Generator - Creates SVG icons using Nano Banana
"""

import os
import tempfile
from typing import Optional
from .nano_banana import nano_banana


async def icon_generator(
    prompt: str,
    style: Optional[str] = None,
    sizes: Optional[list] = None,
    save_path: Optional[str] = None,
) -> str:
    """
    🎨 ICON GENERATOR - Create SVG icons with transparent backgrounds!
    
    This tool uses Nano Banana to generate 1:1 square images with transparent backgrounds,
    then converts them to SVG format for perfect scalability.
    
    Args:
        prompt: Just a simple word or short phrase - AI will design the perfect icon!
                The AI automatically creates a professional icon description from your input.
                Examples:
                - "rocket" → AI designs a beautiful rocket icon
                - "smile" → AI creates an expressive smile icon
                - "chart" → AI generates a data visualization icon
                - "coffee" → AI crafts a coffee-related icon
                Just say what you want - the AI handles the rest!
        
        style: Optional style preset. Automatically enhances the prompt.
               Available styles (40 total):
               
               SPECIAL:
               - "custom" - Let AI decide the best style for your icon (no preset)
               - "isometric" - 3D isometric perspective tech illustration style
               
               ORIGINAL STYLES:
               - "minimal" - Clean, simple, modern minimalism
               - "flat" - Flat design, bold colors, no gradients
               - "outlined" - Line art, outlined style
               - "3d" - Three-dimensional, depth and shadows
               - "geometric" - Geometric shapes, angular design
               - "gradient" - Smooth gradients and modern look
               - "hand-drawn" - Sketchy, artistic feel
               - "neon" - Glowing neon lights
               - "retro" - Vintage aesthetic
               - "pixel" - 8-bit pixel art
               - "watercolor" - Watercolor painting
               - "corporate" - Professional business
               - "playful" - Fun and whimsical
               - "tech" - Futuristic digital
               - "nature" - Organic eco-friendly
               - "lineal" - Clean outlined line art
               - "lineal-color" - Outlined with color accents
               - "filled" - Solid filled shapes
               - "rounded" - Soft rounded corners
               - "straight" - Sharp angular lines
               - "circular-flat" - Round flat shapes
               - "kawaii" - Cute Japanese anime style
               - "detailed" - Intricate complex design
               - "doodle" - Casual sketchy scribbles
               - "cartoon" - Fun animated look
               - "isometric" - Isometric 3D perspective
               - "duotone" - Two-color design
               - "monochrome" - Single color
               - "glassmorphism" - Frosted glass effect
               - "flat-circular" - Circular flat elements
               - "bicolor" - Two-tone contrast
               - "glyph" - Simple filled symbol
               - "hand-drawn-detailed" - Intricate sketchy
               - "ultrathin" - Extra thin lines
               - "offset" - Layered shadow effect
               - "faded" - Soft pastel tones
               - "retro-neon" - 80s neon glow
               - "3d-color" - Full color 3D
               - "pixel-art" - Retro pixelated
               - "brands" - Company logo style
               
               Default: None (uses your prompt as-is)
        
        sizes: Optional list of sizes to generate.
               Example: [32, 64, 128, 256, 512, 1024]
               If provided, generates multiple SVG files at different sizes.
               Default: None (generates single 1024x1024 icon)
        
        save_path: Path to save the SVG icon(s).
                  If not provided, saves as "icon_output.svg" in current directory.
                  For multiple sizes, adds size suffix: "icon_32.svg", "icon_64.svg", etc.
                  Example: "C:/icons/rocket_icon.svg"
    
    Returns:
        Success message with SVG file location, or error details
    
    Features:
        - Always generates 1:1 (square) aspect ratio
        - Always removes background (transparent PNG first)
        - Converts to SVG for infinite scalability
        - Perfect for web icons, logos, UI elements
    
    Examples:
        # Simple icon generation
        icon_generator(prompt="A settings gear icon, simple and clean")
        
        # Custom save location
        icon_generator(
            prompt="A user profile avatar icon, minimalist",
            save_path="C:/project/icons/user.svg"
        )
    """
    # Style presets with hidden prompts (includes Freepik/Flaticon official styles)
    STYLE_PROMPTS = {
        # Special Styles
        "custom": None,  # AI decides - no style injection
        "isometric": "isometric 3D illustration, tech aesthetic, dark background with neon green accents, metallic surfaces, futuristic hardware design, floating on platform, dramatic lighting, cyberpunk tech style, high detail isometric perspective",
        
        # Original Styles
        "minimal": "ultra minimalist design, clean lines, simple shapes, modern, lots of negative space, essential elements only",
        "flat": "flat design style, bold solid colors, no gradients, simple shapes, modern flat icon design, 2D appearance",
        "outlined": "outline style, line art, stroke-based design, no fill, clean outlines, vector line icon",
        "3d": "three-dimensional design, depth and perspective, subtle shadows, isometric or 3D appearance, dimensional icon",
        "geometric": "geometric shapes, angular design, abstract geometry, sharp edges, mathematical precision, polygonal style",
        "gradient": "smooth gradients, modern gradient design, color transitions, vibrant gradient effects, contemporary style",
        "hand-drawn": "hand-drawn style, sketchy appearance, artistic, organic lines, illustrated feel, imperfect lines",
        "neon": "neon glow effect, vibrant glowing colors, luminous design, electric appearance, bright neon lights",
        "retro": "retro vintage style, classic design, nostalgic aesthetic, old-school vibes, vintage colors and shapes",
        "pixel": "pixel art style, 8-bit design, pixelated appearance, retro gaming aesthetic, blocky pixels",
        "watercolor": "soft watercolor style, artistic painting effect, gentle colors, watercolor brush strokes, artistic blend",
        "corporate": "professional corporate design, clean business style, trustworthy appearance, formal and polished",
        "playful": "playful and fun design, whimsical style, cheerful colors, casual and friendly appearance",
        "tech": "futuristic technological design, digital aesthetic, high-tech appearance, modern tech style, cybernetic",
        "nature": "organic natural design, eco-friendly style, nature-inspired shapes, earthy and natural appearance",
        "lineal": "lineal style icon, clean outlined design, line art, stroke-based, simple vector lines, professional outline icon",
        "lineal-color": "lineal color style, outlined design with selective color fills, line art with color accents, modern colored outlines",
        "filled": "filled solid style, completely filled shapes, bold solid colors, no outlines, filled vector icon",
        "rounded": "rounded style icon, soft rounded corners, smooth curves, friendly rounded shapes, gentle edges",
        "straight": "straight style, sharp clean lines, angular edges, geometric straight shapes, precise corners",
        "circular-flat": "circular flat design, round shapes, flat circular elements, modern circular icon style",
        "kawaii": "kawaii cute style, adorable design, big eyes, chibi proportions, cute Japanese anime aesthetic, sweet and charming",
        "detailed": "detailed intricate design, complex elements, rich detail, elaborate patterns, sophisticated icon",
        "doodle": "doodle hand-drawn style, sketchy casual lines, playful scribble aesthetic, informal doodle art",
        "cartoon": "cartoon style icon, fun animated look, bold playful design, cartoon character aesthetic",
        "isometric": "isometric 3D style, isometric perspective, pseudo-3D design, dimensional isometric icon",
        "duotone": "duotone two-color design, limited color palette, dual tone aesthetic, modern duotone style",
        "monochrome": "monochrome single color, one color design, black and white or single hue, minimalist monochromatic",
        "glassmorphism": "glassmorphism frosted glass effect, translucent design, blurred background, modern glass aesthetic",
        "flat-circular": "flat circular design, round flat shapes, circular elements with flat colors, modern circular flat",
        "bicolor": "bicolor two-tone design, dual color scheme, contrasting color combination, modern bicolor style",
        "glyph": "glyph solid icon, simple filled symbol, single color glyph, basic pictogram",
        "hand-drawn-detailed": "detailed hand-drawn style, intricate sketchy design, artistic hand-crafted look, elaborate drawn details",
        "ultrathin": "ultra thin line style, extremely thin strokes, delicate minimal lines, lightweight outlined design",
        "offset": "offset style with shadow, layered offset effect, depth with offset shadows, dimensional offset design",
        "faded": "faded soft colors, muted pastel tones, gentle faded aesthetic, soft vintage fade",
        "retro-neon": "retro neon style, 80s neon lights, vibrant retro glow, nostalgic neon aesthetic, synthwave inspired",
        "3d-color": "3D colored design, full color 3D rendering, realistic 3D icon, dimensional color depth",
        "pixel-art": "pixel art 8-bit, retro pixel design, blocky pixelated style, classic pixel aesthetic",
        "brands": "brand style icon, company logo aesthetic, professional brand identity, recognizable brand design",
    }
    
    try:
        # Enhance prompt with style if provided
        enhanced_prompt = prompt
        if style and style.lower() in STYLE_PROMPTS:
            style_enhancement = STYLE_PROMPTS[style.lower()]
            
            if style.lower() == "custom":
                # Custom style: Generate elaborate, detailed prompt for AI
                enhanced_prompt = f"Design a sleek and modern {prompt} icon with vibrant colors, highly detailed elements, professional quality, perfect composition, stunning visual appeal, cutting-edge design aesthetics, crisp and clean execution, visually striking appearance, carefully crafted details, contemporary style, premium quality look, sophisticated design language, eye-catching presence, polished and refined execution, masterful use of color and form, exceptional clarity and readability, innovative visual approach, professional-grade craftsmanship, beautiful and memorable design"
            elif style_enhancement:
                # Regular style: Apply preset enhancement
                enhanced_prompt = f"{prompt}. Icon design: {style_enhancement}, bold outlines, perfect for an icon, professional quality"
        else:
            # No style: Basic enhancement
            enhanced_prompt = f"Icon design: {prompt}. Simple, clean, bold outlines, perfect for an icon"
        
        # Step 1: Generate transparent PNG using nano_banana
        temp_png = tempfile.mktemp(suffix=".png")
        
        result = await nano_banana(
            prompt=enhanced_prompt,
            aspect_ratio="1:1",
            output_type="image_only",
            remove_background=True,
            save_path=temp_png
        )
        
        # Check if generation was successful
        if "🚨" in result or not os.path.exists(temp_png):
            return f"🚨 Error: Failed to generate icon\n{result}"
        
        # Import PIL for PNG to SVG conversion
        from PIL import Image
        import base64
        
        # Get base image
        base_img = Image.open(temp_png)
        base_width, base_height = base_img.size
        
        # Determine sizes to generate
        if sizes is None:
            sizes = [base_width]  # Just the original size
        
        # Prepare save paths
        if not save_path:
            save_path = "icon_output.svg"
        
        # Remove extension to add size suffix
        base_name = save_path.replace(".svg", "").replace(".SVG", "")
        
        generated_files = []
        
        # Generate icons at each requested size
        for size in sizes:
            # Resize if needed
            if size != base_width:
                resized_img = base_img.resize((size, size), Image.Resampling.LANCZOS)
                temp_resized = tempfile.mktemp(suffix=".png")
                resized_img.save(temp_resized, "PNG")
                img_to_convert = temp_resized
                img_size = size
            else:
                img_to_convert = temp_png
                img_size = base_width
            
            # Read the PNG
            with open(img_to_convert, "rb") as f:
                png_data = base64.b64encode(f.read()).decode()
            
            # Create SVG with embedded PNG
            svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{img_size}" height="{img_size}" viewBox="0 0 {img_size} {img_size}" 
     xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <image width="{img_size}" height="{img_size}" 
           xlink:href="data:image/png;base64,{png_data}"/>
</svg>'''
            
            # Determine output filename
            if len(sizes) > 1:
                output_file = f"{base_name}_{img_size}.svg"
            else:
                output_file = f"{base_name}.svg"
            
            # Save SVG
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(svg_content)
            
            generated_files.append((output_file, img_size))
            
            # Clean up temp resized file
            if size != base_width:
                try:
                    os.remove(img_to_convert)
                except:
                    pass
        
        # Clean up temp PNG
        try:
            os.remove(temp_png)
        except:
            pass
        
        # Build response
        response_text = [
            "🎨 ICON GENERATOR SUCCESS! 🎨",
            "✅ Generated icon(s) with transparent background",
        ]
        
        if style:
            response_text.append(f"🎨 Style: {style}")
        
        response_text.append(f"📐 Base size: {base_width}×{base_height} (1:1 square)")
        
        # Show enhanced prompt for custom style
        if style and style.lower() == "custom":
            response_text.append(f"")
            response_text.append(f"📝 Custom AI Prompt Used:")
            response_text.append(f'   "{enhanced_prompt}"')
            response_text.append(f"")
        response_text.append(f"🖼️ Format: SVG (scalable vector)")
        response_text.append("")
        
        if len(generated_files) > 1:
            response_text.append(f"💾 Generated {len(generated_files)} sizes:")
            for file_path, size in generated_files:
                response_text.append(f"   - {size}×{size}: {file_path}")
        else:
            response_text.append(f"💾 Saved to: {generated_files[0][0]}")
        
        response_text.extend([
            "",
            "🚀 Features:",
            "   - Transparent background (RGBA)",
            "   - Scalable to any size without quality loss",
            "   - Perfect for web, apps, and print",
        ])
        
        return "\n".join(response_text)
        
    except Exception as e:
        return f"🚨 Error in icon_generator: {str(e)}"
