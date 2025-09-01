# /core_services/image_post_generator_service.py

import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import textwrap

class ImagePostGeneratorService:
    def __init__(self):
        os.makedirs("generated_posts", exist_ok=True)
        print("✅ Image Post Generator Service initialized.")

    # --- NEW: Helper function to crop images to the perfect size ---
    def _crop_to_instagram_portrait(self, img: Image.Image) -> Image.Image:
        """Crops an image to a 1080x1350 aspect ratio from the center."""
        target_width, target_height = 1080, 1350
        target_aspect = target_width / target_height
        
        source_width, source_height = img.size
        source_aspect = source_width / source_height

        if source_aspect > target_aspect:
            # Image is wider than target (crop the sides)
            new_width = int(target_aspect * source_height)
            left = (source_width - new_width) / 2
            top = 0
            right = left + new_width
            bottom = source_height
        else:
            # Image is taller than target or same aspect (crop top/bottom)
            new_height = int(source_width / target_aspect)
            left = 0
            top = (source_height - new_height) / 2
            right = source_width
            bottom = top + new_height
            
        cropped_img = img.crop((left, top, right, bottom))
        # Finally, resize to the exact dimensions
        return cropped_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
    def create_post_image(self, base_image_path: str, text: str, title: str) -> str | None:
        try:
            with Image.open(base_image_path) as img:
                # --- THIS IS THE FIX for image size ---
                img = self._crop_to_instagram_portrait(img)
                img = img.convert("RGBA")
                
                overlay = Image.new("RGBA", img.size, (0, 0, 0, 128))
                img = Image.alpha_composite(img, overlay)
                draw = ImageDraw.Draw(img)
                
                try:
                    font_path = os.path.join("assets/fonts", "Arial.ttf")
                    # --- THIS IS THE FIX for font size ---
                    title_font = ImageFont.truetype(font_path, size=110) # Increased size
                    body_font = ImageFont.truetype(font_path, size=75)   # Increased size
                except IOError:
                    print("⚠️ Warning: Arial.ttf not found. Using default font.")
                    title_font = ImageFont.load_default()
                    body_font = ImageFont.load_default()

                margin = 80 # Increased margin for the larger post
                wrapped_text = textwrap.fill(text, width=22) # Adjusted width for larger font
                
                title_bbox = draw.textbbox((0, 0), title, font=title_font)
                body_bbox = draw.textbbox((0, 0), wrapped_text, font=body_font, spacing=20)
                title_width = title_bbox[2] - title_bbox[0]
                body_height = body_bbox[3] - body_bbox[1]
                
                total_height = (title_bbox[3] - title_bbox[1]) + 40 + body_height
                start_y = (img.height - total_height) / 2
                
                title_x = (img.width - title_width) / 2
                draw.text((title_x, start_y), title, font=title_font, fill="white")
                
                body_start_y = start_y + (title_bbox[3] - title_bbox[1]) + 60
                draw.text((margin, body_start_y), wrapped_text, font=body_font, fill="white", spacing=20)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = os.path.join("generated_posts", f"post_{title.replace(' ','_')}_{timestamp}.png")
                img.save(output_filename, "PNG")
                
                print(f"✅ Post image created and saved to: {output_filename}")
                return output_filename
        
        except Exception as e:
            print(f"❌ Error creating post image: {e}")
            return None
