# /config.py

import os
from dotenv import load_dotenv

# --- BULLETPROOF DEBUGGING SCRIPT ---
# This code will tell us exactly what the program is seeing.

# First, we get the absolute path of the directory where this config.py file lives.
# This should be your main project folder.
project_directory = os.path.dirname(os.path.abspath(__file__))

# The .env file should be in that same directory.
dotenv_path = os.path.join(project_directory, '.env')

print("\n\n--- DIAGNOSTICS ---")
print(f"Directory where I'm running from: {project_directory}")
print(f"Full path where I expect .env to be: {dotenv_path}")

# Check if the file actually exists at that path
file_exists = os.path.exists(dotenv_path)
print(f"Does the .env file exist at that path? -> {file_exists}")

if file_exists:
    # If the file exists, try to load it and check the result
    load_was_successful = load_dotenv(dotenv_path=dotenv_path)
    print(f"Did the dotenv library load it successfully? -> {load_was_successful}")
else:
    print("CRITICAL: I could not find the .env file. Please check its location and name.")
    
print("--- END DIAGNOSTICS ---\n\n")


# --- API Keys Reading ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")
STABILITY_AI_API_KEY = os.environ.get("STABILITY_AI_API_KEY")
INSTAGRAM_ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID")


# --- Final Error Check ---
if not OPENAI_API_KEY or not PEXELS_API_KEY:
    raise ValueError("API keys for OpenAI or Pexels are not set in the environment.")
