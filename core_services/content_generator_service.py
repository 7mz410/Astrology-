# /core_services/content_generator_service.py

import os
import json
from openai import OpenAI
from config import OPENAI_API_KEY

class ContentGeneratorService:
    def __init__(self):
        if not OPENAI_API_KEY:
            self.client = None
            print("❌ Critical Error: OPENAI_API_KEY not found in config.py.")
            return
        try:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            print("✅ OpenAI client for Astrology configured successfully.")
        except Exception as e:
            self.client = None
            print(f"❌ Critical Error configuring OpenAI client: {e}")

    def generate_astrology_data(self, zodiac_sign: str) -> dict | None:
        print(f"   - 🔮 Generating daily astrological data for {zodiac_sign}...")
        prompt = f"""
        You are a creative, insightful, and positive astrologer for a brand called "Planets Vibe".
        Generate a fictional but believable daily horoscope for the zodiac sign: {zodiac_sign.capitalize()}.
        The output MUST be a single, valid JSON object with NO other text or explanations.
        The JSON object must have these exact keys:
        - "description": A 1-2 sentence inspiring horoscope for the day.
        - "mood": A single word describing the primary mood (e.g., "Confident", "Reflective").
        - "lucky_number": A random number between 1 and 100.
        - "color": A lucky color for the day (e.g., "Sea Green", "Gold").
        """
        try:
            json_string = self._generate_content_with_openai(prompt)
            if not json_string: return None
            data = json.loads(json_string)
            data['sign'] = zodiac_sign
            return data
        except Exception as e:
            print(f"   - ❌ Failed to generate astrology data for {zodiac_sign}: {e}")
            return None

    def create_astrology_caption(self, astro_data: dict) -> str:
        print("   - ✍️ Crafting an engaging astrology caption...")
        prompt = f"""
        You are the social media manager for "Planets Vibe". Your tone is mystical and positive.
        You have this data for {astro_data.get('sign', 'a zodiac sign')}:
        - Vibe: {astro_data.get('description')}
        - Mood: {astro_data.get('mood')}
        - Lucky Color: {astro_data.get('color')}

        Transform this into a short, beautiful Instagram caption and provide hashtags.
        The entire output MUST be a single, valid JSON object.

        JSON STRUCTURE:
        {{
          "caption": "[Your beautifully crafted caption here]",
          "hashtags": ["#astrology", "#horoscope", ...]
        }}
        """
        try:
            json_string = self._generate_content_with_openai(prompt)
            if not json_string: raise Exception("API returned empty response")
            data = json.loads(json_string)
            final_caption = data.get('caption', astro_data.get('description'))
            hashtags_str = " ".join(data.get('hashtags', []))
            return f"{final_caption}\n\n{hashtags_str}"
        except Exception as e:
            print(f"   - ❌ Error generating caption: {e}. Falling back to default.")
            return f"{astro_data.get('description')}\n\n#astrology #horoscope #{astro_data.get('sign')}"

    def _generate_content_with_openai(self, prompt):
        if not self.client: return None
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a creative astrology social media expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ Error during OpenAI API call: {e}"); return None
