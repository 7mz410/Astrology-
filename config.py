# /config.py

import os
from dotenv import load_dotenv

#إعدادات السيرفر
load_dotenv()

# --- API Keys are now read securely from the environment ---

# OpenAI API Key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Pexels API Key
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

# Stability AI API Key (from your .env file)
STABILITY_AI_API_KEY = os.environ.get("STABILITY_AI_API_KEY")

# Instagram Credentials (if you plan to use them directly)
INSTAGRAM_ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID")

# --- Error checking (optional but good practice) ---
if not OPENAI_API_KEY or not PEXELS_API_KEY:
    raise ValueError("API keys for OpenAI or Pexels are not set in the environment.")
