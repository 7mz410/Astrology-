# /platform_services/instagram_service.py

import os
import requests
import random
from config import PEXELS_API_KEY
from pexels_api import API

class InstagramService:
    """
    A service dedicated to creating and (eventually) publishing daily astrology
    posts for an account like 'planetsvibe'.
    """
    def __init__(self, content_generator, image_post_generator):
        """
        Initializes the service with dependencies.
        """
        self.content_generator = content_generator
        self.image_post_generator = image_post_generator
        
        if not PEXELS_API_KEY or "YOUR_PEXELS_API_KEY_HERE" in PEXELS_API_KEY:
            self.pexels_api = None
            print("⚠️ Warning: Pexels API key not configured in config.py.")
        else:
            self.pexels_api = API(PEXELS_API_KEY)
            print("✅ Instagram Service initialized with Pexels API.")

    def _get_royalty_free_image(self, query: str) -> str | None:
        """
        Searches and downloads a high-quality, royalty-free image from Pexels.
        """
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

    def create_daily_astrology_post_for_all_signs(self):
        """
        The main automation loop. It generates a post for every zodiac sign.
        """
        print("\n🔮 Starting Daily Astrology Post Generation for ALL SIGNS 🔮")
        zodiac_signs = [
            "aries", "taurus", "gemini", "cancer", "leo", "virgo", 
            "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
        ]
        
        all_posts = []
        for sign in zodiac_signs:
            print(f"\n--- Generating post for {sign.upper()} ---")
            
            raw_data = self.content_generator.generate_astrology_data(sign)
            if not raw_data:
                continue
            
            caption = self.content_generator.create_astrology_caption(raw_data)
            
            image_query = f"mystical {raw_data.get('color', 'space')} abstract"
            base_image_path = self._get_royalty_free_image(image_query)
            if not base_image_path:
                continue
            
            final_post_path = self.image_post_generator.create_post_image(
                base_image_path=base_image_path,
                text=raw_data.get('description'),
                title=sign.capitalize()
            )
            
            if final_post_path:
                print(f"✅ Successfully created post package for {sign}!")
                # --- THIS IS THE FIX ---
                # We now save the caption along with the image path.
                all_posts.append({
                    "sign": sign,
                    "path": final_post_path,
                    "caption": caption
                })
        
        print(f"\n✨ --- Process Complete! Generated {len(all_posts)} post packages. --- ✨")
        return all_posts
