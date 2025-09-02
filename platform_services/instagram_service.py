# /platform_services/instagram_service.py

import os
import requests
import random
from config import PEXELS_API_KEY
from pexels_api import API

class InstagramService:
    def __init__(self, content_generator, image_post_generator, instagram_client):
        self.content_generator = content_generator
        self.image_post_generator = image_post_generator
        self.client = instagram_client
        
        if not PEXELS_API_KEY:
            self.pexels_api = None
            print("⚠️ Warning: Pexels API key not configured.")
        else:
            self.pexels_api = API(PEXELS_API_KEY)
            print("✅ Instagram Service initialized with Pexels API.")

    # --- NEW: Function to publish a multi-image carousel post ---
    def publish_carousel_post(self, image_paths: list[str], caption: str) -> bool:
        """
        Uploads multiple photos as a single carousel/album post.
        """
        if not self.client or not self.client.user_id:
            print("❌ Error: Instagram client is not logged in. Cannot publish.")
            return False
        
        if not image_paths or len(image_paths) < 2:
            print("❌ Error: A carousel post requires at least 2 images.")
            return False
            
        try:
            print(f"   - ⬆️  Attempting to upload a carousel post with {len(image_paths)} images...")
            self.client.album_upload(
                paths=image_paths,
                caption=caption
            )
            print("   - ✅ Carousel post published successfully to Instagram!")
            return True
        except Exception as e:
            print(f"   - ❌ CRITICAL: Failed to publish carousel post to Instagram: {e}")
            return False

    def create_daily_astrology_post_for_all_signs(self) -> list:
        print("\n🔮 Starting Daily Astrology Post Generation for ALL SIGNS 🔮")
        zodiac_signs = [
            "aries", "taurus", "gemini", "cancer", "leo", "virgo", 
            "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
        ]
        
        all_posts = []
        for sign in zodiac_signs:
            print(f"\n--- Generating post for {sign.upper()} ---")
            raw_data = self.content_generator.generate_astrology_data(sign)
            if not raw_data: continue
            
            caption = self.content_generator.create_astrology_caption(raw_data)
            
            image_query = f"mystical {raw_data.get('color', 'space')} abstract"
            base_image_path = self._get_royalty_free_image(image_query)
            if not base_image_path: continue
            
            final_post_path = self.image_post_generator.create_post_image(
                base_image_path=base_image_path,
                text=raw_data.get('description'),
                title=sign.capitalize()
            )
            
            if final_post_path:
                print(f"✅ Successfully created post package for {sign}!")
                # We store the full caption data now
                all_posts.append({
                    "sign": sign,
                    "path": final_post_path,
                    "caption_text": caption, # Original individual caption
                    "description": raw_data.get('description', '')
                })
        
        print(f"\n✨ --- Generation Complete! Created {len(all_posts)} post packages. --- ✨")
        return all_posts

    def _get_royalty_free_image(self, query: str) -> str | None:
        # This function remains unchanged
        if not self.pexels_api:
            print("   - ❗ Pexels API not configured. Skipping image search.")
            return None
        try:
            print(f"   - 🔎 Searching Pexels for: '{query}'...")
            self.pexels_api.search(query, page=1, results_per_page=15)
            photos = self.pexels_api.get_entries()
            if not photos:
                print(f"   - ❗ No photos found on Pexels for '{query}'.")
                return None
            photo_url = random.choice(photos).original
            response = requests.get(photo_url)
            response.raise_for_status()
            os.makedirs("generated_images", exist_ok=True)
            temp_path = os.path.join("generated_images", "temp_pexels_image.jpg")
            with open(temp_path, "wb") as f:
                f.write(response.content)
            print(f"   - ✅ Image downloaded successfully from Pexels.")
            return temp_path
        except Exception as e:
            print(f"   - ❌ Error fetching image from Pexels: {e}")
            return None
