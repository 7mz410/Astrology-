# /manual_login.py
import os
from instagrapi import Client

SESSION_FILE = "instagram_session.json"

print("--- Instagram Manual Login Script ---")
print("This script will help you log in interactively to solve any challenges.")

cl = Client()

# Get credentials from user input
username = input("Enter your Instagram username: ")
password = input("Enter your Instagram password: ")

try:
    print(f"\nAttempting to log in as {username}...")
    cl.login(username, password)
    
    # If login is successful, dump the session settings to the file
    cl.dump_settings(SESSION_FILE)
    print(f"\n✅ SUCCESS! Login successful for {username}.")
    print(f"Session file '{SESSION_FILE}' has been created.")
    print("You can now close this script and restart your main Streamlit application.")

except Exception as e:
    print(f"\n❌ FAILED! An error occurred: {e}")
    print("Please check your credentials and try again.")
    # Clean up failed session file if it exists
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
