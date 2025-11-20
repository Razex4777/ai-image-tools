"""
Batch Icon Generator using Nano Banana Pro
Generate multiple icons concurrently using Gemini 3 Pro Image
"""

import os
import asyncio
from typing import Optional, List, Union, Dict
from .icon_generator import icon_generator


async def batch_icon_generator(
    prompts: Optional[List[str]] = None,
    icons: Optional[List[Dict]] = None,
    style: Optional[str] = None,
    sizes: Optional[list] = None,
    output_dir: str = "batch_icons",
) -> str:
    """
    🚀 BATCH ICON GENERATOR - Generate multiple icons at once!
    
    Create entire icon sets efficiently with batch processing.
    Supports simple batch (same style) or advanced batch (custom per icon).
    
    Args:
        prompts: Simple list of icon descriptions (all use same style).
                 Example: ["rocket", "star", "heart", "cloud"]
                 
        icons: Advanced list with custom settings per icon.
               Example: [
                   {"prompt": "rocket", "style": "minimal", "sizes": [32, 64]},
                   {"prompt": "star", "style": "kawaii"},
                   {"prompt": "heart", "style": "gradient", "sizes": [128]}
               ]
               
        style: Default style to apply to all icons (if using prompts list).
               Ignored if using icons list with individual styles.
               Available: All 38 styles from icon_generator
               
        sizes: Default sizes for all icons (if using prompts list).
               Example: [32, 64, 128, 256]
               
        output_dir: Directory to save all generated icons.
                   Created automatically if doesn't exist.
                   Default: "batch_icons"
    
    Returns:
        Summary report with success/failure count and file locations
    
    Features:
        - Generates icons concurrently using asyncio.gather for speed
        - Continues on individual failures (returns exceptions)
        - Auto-organizes output directory
        - Provides detailed summary report
        - Smart filename sanitization with index prefixing
    
    Examples:
        # Simple batch - same style for all
        batch_icon_generator(
            prompts=["rocket", "star", "heart", "cloud"],
            style="minimal",
            sizes=[32, 64, 128],
            output_dir="my_icons"
        )
        
        # Advanced batch - custom per icon
        batch_icon_generator(
            icons=[
                {"prompt": "rocket ship", "style": "minimal"},
                {"prompt": "cute cat", "style": "kawaii", "sizes": [64]},
                {"prompt": "tech logo", "style": "tech", "sizes": [128, 256]}
            ],
            output_dir="custom_icons"
        )
        
        # Icon pack with theme
        batch_icon_generator(
            prompts=["facebook", "twitter", "instagram", "linkedin"],
            style="brands",
            sizes=[48, 96],
            output_dir="social_media_pack"
        )
    """
    try:
        # Validate inputs
        if not prompts and not icons:
            return "🚨 Error: Must provide either 'prompts' or 'icons' parameter"
        
        if prompts and icons:
            return "🚨 Error: Provide either 'prompts' OR 'icons', not both"
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Build icon job list
        jobs = []
        
        if prompts:
            # Simple mode: same settings for all
            for prompt in prompts:
                jobs.append({
                    "prompt": prompt,
                    "style": style,
                    "sizes": sizes,
                })
        else:
            # Advanced mode: custom settings per icon
            for icon_spec in icons:
                jobs.append({
                    "prompt": icon_spec.get("prompt"),
                    "style": icon_spec.get("style", style),
                    "sizes": icon_spec.get("sizes", sizes),
                })
        
        # Initialize results tracking
        total = len(jobs)
        successful = []
        failed = []
        
        result_parts = [
            "🚀 BATCH ICON GENERATOR STARTED! 🚀",
            f"📦 Total icons to generate: {total}",
            f"📁 Output directory: {output_dir}",
            "",
            "⏳ Processing..."
        ]
        
        # Build tasks for concurrent execution
        tasks = []
        job_metadata = []
        
        for i, job in enumerate(jobs, 1):
            prompt = job["prompt"]
            job_style = job["style"]
            job_sizes = job["sizes"]
            
            # Sanitize filename from prompt with index prefix to prevent collisions
            safe_name = "".join(c for c in prompt.lower() if c.isalnum() or c in (' ', '-', '_'))
            safe_name = safe_name.replace(' ', '_')[:50]  # Limit length
            
            # Add zero-padded index prefix
            save_path = os.path.join(output_dir, f"{i:03d}_{safe_name}.svg")
            
            # Log what we're generating
            result_parts.append(f"\n[{i}/{total}] Queued: {prompt}")
            if job_style:
                result_parts.append(f"         Style: {job_style}")
            
            # Create coroutine and store metadata
            task = icon_generator(
                prompt=prompt,
                style=job_style,
                sizes=job_sizes,
                save_path=save_path
            )
            tasks.append(task)
            job_metadata.append({
                "prompt": prompt,
                "style": job_style,
                "path": save_path,
                "index": i
            })
        
        result_parts.append("\n🚀 Generating all icons concurrently...\n")
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, (result, metadata) in enumerate(zip(results, job_metadata)):
            idx = metadata["index"]
            prompt = metadata["prompt"]
            save_path = metadata["path"]
            job_style = metadata["style"]
            
            result_parts.append(f"[{idx}/{total}] Result for: {prompt}")
            
            if isinstance(result, Exception):
                # Task raised an exception
                failed.append({
                    "prompt": prompt,
                    "error": str(result)
                })
                result_parts.append(f"         ❌ Error: {str(result)[:100]}")
            elif "🚨" in str(result):
                # Task returned error message
                failed.append({
                    "prompt": prompt,
                    "error": result
                })
                result_parts.append(f"         ❌ Failed: {result[:100]}")
            else:
                # Success
                successful.append({
                    "prompt": prompt,
                    "style": job_style,
                    "path": save_path
                })
                result_parts.append(f"         ✅ Success")
        
        # Build summary report
        result_parts.extend([
            "",
            "=" * 60,
            "📊 BATCH GENERATION COMPLETE!",
            "=" * 60,
            f"✅ Successful: {len(successful)}/{total}",
            f"❌ Failed: {len(failed)}/{total}",
            f"📁 Output directory: {output_dir}",
            ""
        ])
        
        # List successful icons
        if successful:
            result_parts.append("✅ Successfully Generated Icons:")
            for item in successful:
                style_info = f" ({item['style']})" if item['style'] else ""
                result_parts.append(f"   • {item['prompt']}{style_info}")
                result_parts.append(f"     → {item['path']}")
        
        # List failed icons
        if failed:
            result_parts.append("")
            result_parts.append("❌ Failed Icons:")
            for item in failed:
                result_parts.append(f"   • {item['prompt']}")
                error_preview = str(item['error'])[:100]
                result_parts.append(f"     Error: {error_preview}")
        
        # Final stats
        result_parts.extend([
            "",
            "🎉 Batch processing complete!",
            f"📦 Total files created: {len(successful)}"
        ])
        
        return "\n".join(result_parts)
        
    except Exception as e:
        return f"🚨 Error in batch_icon_generator: {str(e)}"
