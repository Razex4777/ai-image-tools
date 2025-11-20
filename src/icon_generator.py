"""
Icon Generator using Nano Banana Pro
Generates SVG icons with transparent backgrounds using Gemini 3 Pro Image
"""

import os
import tempfile
import base64
from typing import Optional, List
from PIL import Image
from .nano_banana_pro import nano_banana_pro


async def icon_generator(
    prompt: str,
    style: Optional[str] = None,
    sizes: Optional[List[int]] = None,
    save_path: Optional[str] = None,
) -> str:
    """
    �✨ ICON GENERATOR - Create SVG icons with transparent backgrounds!

    This tool uses Nano Banana Pro (Gemini 3 Pro Image) to generate 1:1 square images 
    with transparent backgrounds, then converts them to SVG format for perfect scalability.
    
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
        "isometric": "isometric 3D illustration, tech aesthetic, dark background with neon green accents, metallic surfaces, futuristic hardware design, floating on platform, dramatic lighting, cyberpunk tech style, high detail isometric perspective, premium rendering",
        
        # Trending & Next-Level Modern
        "neumorphism": "neumorphism style, soft UI, embossed plastic texture, soft shadows, clean minimal design, off-white or soft pastel colors, smooth surface, tactile feel",
        "claymorphism": "claymorphism style, 3D clay texture, soft rounded shapes, matte finish, playful and friendly, fluffy look, high quality 3D render, cute and modern",
        "glassmorphism": "glassmorphism frosted glass effect, translucent layers, background blur, vivid colors behind glass, modern UI aesthetic, premium crystal look, glossy finish",
        "holographic": "holographic iridescent style, shifting colors, foil texture, metallic gradients, futuristic shiny look, prismatic light reflection, trendy and vibrant",
        "apple-style": "macOS app icon style, squircle shape, realistic shading, subtle drop shadow, premium detail, high-fidelity rendering, glossy finish, Apple design aesthetic",
        "cyberpunk": "cyberpunk aesthetic, neon lights, dark futuristic tech, glitch effects, high contrast, magenta and cyan lighting, detailed mechanical parts, next-gen digital style",
        "origami": "origami paper fold style, layered paper craft, realistic shadows, paper texture, angular geometric folds, vibrant paper colors, handcrafted look",
        "sticker": "die-cut sticker style, thick white border, slight drop shadow, vibrant vector illustration, clean isolated look, pop art aesthetic, vinyl sticker feel",
        "material": "Google Material Design, flat colors, subtle depth, material paper layers, crisp edges, bold geometric shapes, distinct lighting, modern Android aesthetic",
        "glass-premium": "ultra-premium glass icon, crystal clear transparency, light refraction, caustic lighting effects, polished gemstone look, luxury aesthetic, 8k render",

        # Original Styles (Upgraded)
        "minimal": "ultra minimalist design, clean lines, simple shapes, modern, lots of negative space, essential elements only, vector perfection",
        "flat": "modern flat design, bold solid colors, no gradients, simple geometric shapes, clean vector aesthetic, 2D appearance, professional UI",
        "outlined": "clean outline style, consistent stroke width, monoline art, no fill, vector precision, minimal line icon, sharp details",
        "3d": "high-fidelity 3D design, realistic lighting and materials, depth and perspective, subtle ambient occlusion, premium 3D render",
        "geometric": "abstract geometric shapes, mathematical precision, golden ratio composition, sharp angular design, polygonal style, modern vector art",
        "gradient": "modern fluid gradients, vibrant color transitions, mesh gradient style, contemporary digital art, rich color depth, smooth blending",
        "hand-drawn": "artistic hand-drawn style, organic sketch lines, pencil texture, imperfect human touch, creative illustration, authentic doodle",
        "neon": "glowing neon sign style, electric light tubes, vibrant luminescent colors, dark background contrast, retro-futuristic glow",
        "retro": "retro 70s/80s vintage style, noise texture, muted color palette, nostalgic aesthetic, old-school typography vibes, classic design",
        "pixel": "pixel art style, 8-bit retro game aesthetic, crisp blocky pixels, limited color palette, arcade nostalgia, precise grid alignment",
        "watercolor": "artistic watercolor painting, soft wash effects, wet-on-wet texture, gentle color blending, hand-painted look, organic edges",
        "corporate": "premium corporate identity, trustworthy blue/grey tones, clean professional lines, business-ready aesthetic, polished vector design",
        "playful": "fun and whimsical style, bright cheerful colors, rounded bouncy shapes, friendly mascot vibes, energetic design, kid-friendly",
        "tech": "futuristic tech circuit style, digital nodes, connecting lines, cyan and blue palette, high-tech data visualization, sci-fi interface",
        "nature": "eco-friendly organic style, leafy textures, earth tones, natural curves, sustainable design aesthetic, botanical illustration",
        "lineal": "modern lineal icon, sleek thin strokes, elegant outline design, professional vector art, scalable clarity",
        "lineal-color": "lineal color style, clean outlines with vibrant color accents, modern illustrative icon, balanced fill and stroke",
        "filled": "solid filled vector style, bold silhouette, high contrast, recognizable shape, minimalist glyph, clean and readable",
        "rounded": "soft rounded style, friendly curves, squircle shapes, bubble-like aesthetic, modern app interface look",
        "straight": "brutalist straight style, sharp hard edges, industrial design, precision engineering look, architectural aesthetic",
        "circular-flat": "modern circular flat design, round container, centered composition, clean vector colors, unified icon set style",
        "kawaii": "kawaii Japanese cute style, adorable chibi proportions, pastel colors, blushing cheeks, sweet and charming character",
        "detailed": "hyper-detailed illustration, intricate patterns, rich texture, complex composition, masterpiece icon design",
        "doodle": "casual doodle style, whiteboard marker look, playful scribble, simplified hand-drawn concept, creative brainstorming vibe",
        "cartoon": "vibrant cartoon style, cel-shaded coloring, bold expressive lines, animated character look, fun and dynamic",
        "duotone": "trendy duotone style, two contrasting colors, modern double-exposure effect, artistic color grading, spotify style",
        "monochrome": "sleek monochrome design, single color sophistication, black and white or brand color, minimalist luxury",
        "flat-circular": "flat design in circular frame, modern UI element, consistent round shape, clean vector graphics",
        "bicolor": "modern bicolor style, primary and secondary color harmony, clean split-tone design, professional interface icon",
        "glyph": "universal glyph symbol, high-contrast silhouette, wayfinding signage style, clear communicative icon",
        "hand-drawn-detailed": "intricate ink drawing, fine liner pen style, cross-hatching shading, artistic sketchbook aesthetic, detailed illustration",
        "ultrathin": "ultra-thin elegance, hairline strokes, delicate minimalist design, luxury brand aesthetic, sophisticated lightness",
        "offset": "modern offset print style, misregistered color layers, retro printing effect, artistic color separation, trendy graphic design",
        "faded": "soft faded aesthetic, muted vintage tones, washed-out look, nostalgic memory style, gentle lo-fi vibes",
        "retro-neon": "synthwave retro-neon, 80s sunset grid, chrome text styling, laser beams, vibrant magenta and violet, retro-future",
        "3d-color": "vibrant 3D color render, plastic toy texture, smooth lighting, playful 3D character style, high saturation",
        "pixel-art": "modern pixel art, indie game asset style, detailed sprite work, vibrant pixel colors, sharp edge definition",
        "brands": "modern brand logo style, abstract minimalist symbol, memorable identity, professional trademark design, vector logo",
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
        # Use NamedTemporaryFile to avoid race conditions
        temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        temp_png = temp_file.name
        temp_file.close()  # Close before nano_banana writes to it (important on Windows)
        
        try:
            result = await nano_banana_pro(
                prompt=enhanced_prompt,
                aspect_ratio="1:1",
                output_type="image_only",
                remove_background=True,
                save_path=temp_png
            )
            
            # Check if generation was successful
            if "🚨" in result or not os.path.exists(temp_png):
                return f"🚨 Error: Failed to generate icon\n{result}"
            
            # Get base image
            base_img = Image.open(temp_png)
            base_width, base_height = base_img.size
            
            # Determine sizes to generate
            if not sizes:
                sizes = [base_width]  # Default to original size
            
            if not save_path:
                save_path = "icon_output.svg"
            
            # Remove extension to add size suffix
            base_name = save_path.replace(".svg", "").replace(".SVG", "")
            
            generated_files = []
            
            # Generate icons at each requested size
            for size in sizes:
                # Resize if needed
                temp_resized = None
                if size != base_width:
                    resized_img = base_img.resize((size, size), Image.Resampling.LANCZOS)
                    # Use NamedTemporaryFile to avoid race conditions
                    temp_resized_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                    temp_resized = temp_resized_file.name
                    temp_resized_file.close()
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
                if temp_resized:
                    try:
                        os.remove(temp_resized)
                    except (OSError, FileNotFoundError):
                        pass  # Ignore cleanup errors
        
        finally:
            # Clean up temp PNG
            try:
                os.remove(temp_png)
            except (OSError, FileNotFoundError):
                pass  # Ignore cleanup errors
        
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
