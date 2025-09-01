# /platform_services/instagram_connection_service.py

import os
from instagrapi import Client

class InstagramConnectionService:
    """
    Handles the connection, login, and session management for Instagram.
    """
    SESSION_FILE = "instagram_session.json"

    def __init__(self):
        self.client = Client()
        self.is_logged_in = False
        self.username = None
        
        # Attempt to load a saved session on startup
        if os.path.exists(self.SESSION_FILE):
            try:
                self.client.load_settings(self.SESSION_FILE)
                self.client.login_by_sessionid(self.client.sessionid)
                self.username = self.client.username
                self.is_logged_in = True
                print(f"✅ Successfully logged in from saved session as {self.username}.")
            except Exception as e:
                print(f"⚠️ Could not log in with saved session: {e}. Manual login required.")
                self.is_logged_in = False
        else:
            print("ℹ️ No saved Instagram session found. Manual login required.")
    
    def login(self, username, password):
        """
        Logs in to Instagram using username and password, then saves the session.
        """
        try:
            print(f"Attempting to log in as {username}...")
            self.client.login(username, password)
            
            # Save the session settings to a file for future use
            self.client.dump_settings(self.SESSION_FILE)
            
            self.username = username
            self.is_logged_in = True
            print(f"✅ Login successful for {username}. Session saved.")
            return {"success": True, "username": username}
        except Exception as e:
            print(f"❌ Login failed for {username}: {e}")
            self.is_logged_in = False
            # Ensure we clean up if the login fails
            if os.path.exists(self.SESSION_FILE):
                os.remove(self.SESSION_FILE)
            return {"success": False, "message": str(e)}
    
    def logout(self):
        """
        Logs out and deletes the session file.
        """
        try:
            print(f"Logging out {self.username}...")
            self.client.logout()
            if os.path.exists(self.SESSION_FILE):
                os.remove(self.SESSION_FILE)
            
            self.is_logged_in = False
            self.username = None
            print("✅ Logout successful. Session file deleted.")
            return {"success": True}
        except Exception as e:
            print(f"❌ Error during logout: {e}")
            return {"success": False, "message": str(e)}

    def get_status(self):
        """Returns the current connection status."""
        return {
            "is_logged_in": self.is_logged_in,
            "username": self.username
        }
