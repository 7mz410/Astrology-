# /orchestration/main_orchestrator.py
import time
import random
from core_services.content_generator_service import ContentGeneratorService
from core_services.image_post_generator_service import ImagePostGeneratorService
from platform_services.instagram_service import InstagramService
from platform_services.instagram_connection_service import InstagramConnectionService
from orchestration.automation_scheduler import AutomationScheduler

class MainOrchestrator:
    def __init__(self):
        print("Initializing the Planets Vibe Orchestrator...")

        # --- Initialize Services ---
        self.instagram_connection = InstagramConnectionService()
        self.content_generator = ContentGeneratorService()
        self.image_post_generator = ImagePostGeneratorService()
        
        # --- MODIFIED: Pass the authenticated client to the Instagram service ---
        self.instagram_service = InstagramService(
            content_generator=self.content_generator,
            image_post_generator=self.image_post_generator,
            instagram_client=self.instagram_connection.client # Pass the client here
        )
        self.scheduler = AutomationScheduler(orchestrator=self)
        
        print("✅ Planets Vibe Orchestrator and all services initialized.")

    def generate_and_publish_all_astrology_posts(self) -> list:
        print("ORCHESTRATOR: Initiating a full run for all zodiac signs...")
        
        # Step 1: Generate all post files and captions
        post_packages = self.instagram_service.create_daily_astrology_post_for_all_signs()
        
        if not post_packages:
            print("ORCHESTRATOR: Generation phase failed. No posts to publish.")
            return []

        print("\n🚀 ORCHESTRATOR: Starting publishing phase... 🚀")
        published_posts_info = []
        for post in post_packages:
            print(f"\n--- Publishing post for {post['sign'].upper()} ---")
            success = self.instagram_service.publish_post(
                image_path=post['path'],
                caption=post['caption']
            )
            if success:
                published_posts_info.append(post)
                # IMPORTANT: Wait for a random time between posts to seem more human
                sleep_time = random.randint(30, 90) 
                print(f"   - 😴 Sleeping for {sleep_time} seconds before the next post...")
                time.sleep(sleep_time)

        print(f"\n🏁 ORCHESTRATOR: Publishing run complete! {len(published_posts_info)} posts were published. 🏁")
        return published_posts_info

    def login_to_instagram(self, username, password):
        return self.instagram_connection.login(username, password)

    def logout_from_instagram(self):
        return self.instagram_connection.logout()

    def get_instagram_status(self):
        return self.instagram_connection.get_status()

    def start_automation(self, run_time: str):
        self.scheduler.start(run_time)

    def stop_automation(self):
        self.scheduler.stop()
