# /orchestration/main_orchestrator.py

from core_services.content_generator_service import ContentGeneratorService
from core_services.image_post_generator_service import ImagePostGeneratorService
from platform_services.instagram_service import InstagramService
from platform_services.instagram_connection_service import InstagramConnectionService
from orchestration.automation_scheduler import AutomationScheduler

class MainOrchestrator:
    def __init__(self):
        print("Initializing the Planets Vibe Orchestrator...")
        self.instagram_connection = InstagramConnectionService()
        self.content_generator = ContentGeneratorService()
        self.image_post_generator = ImagePostGeneratorService()
        self.instagram_service = InstagramService(
            content_generator=self.content_generator,
            image_post_generator=self.image_post_generator,
            instagram_client=self.instagram_connection.client
        )
        self.scheduler = AutomationScheduler(orchestrator=self)
        print("✅ Planets Vibe Orchestrator and all services initialized.")

    # --- MODIFIED: The main function to generate and publish a single carousel post ---
    def generate_and_publish_all_astrology_posts(self):
        print("ORCHESTRATOR: Initiating run to create one carousel post for all signs...")
        
        # Step 1: Generate all 12 post images and collect their data
        post_packages = self.instagram_service.create_daily_astrology_post_for_all_signs()
        
        if not post_packages or len(post_packages) < 12:
            print("ORCHESTRATOR: Generation phase failed. Not enough posts to create a carousel.")
            return []

        # Step 2: Extract all image paths into a list
        image_paths = [post['path'] for post in post_packages]

        # Step 3: Create a single, master caption for the carousel post
        master_caption = self._create_master_caption(post_packages)

        print("\n🚀 ORCHESTRATOR: Publishing all signs as a single carousel post... 🚀")
        
        # Step 4: Call the new carousel publishing function
        success = self.instagram_service.publish_carousel_post(
            image_paths=image_paths,
            caption=master_caption
        )
        
        if success:
            print("\n🏁 ORCHESTRATOR: Carousel post published successfully! 🏁")
            return post_packages # Return the data to confirm success
        else:
            print("\n❌ ORCHESTRATOR: Failed to publish the carousel post. ❌")
            return []
    
    # --- NEW: Helper function to build the combined caption ---
    def _create_master_caption(self, post_packages: list) -> str:
        """Builds a single descriptive caption from all individual post data."""
        
        caption_parts = []
        caption_parts.append("✨ Your daily horoscope is here! ✨\nSwipe to find your sign 🔮\n")

        for post in post_packages:
            sign_name = post['sign'].capitalize()
            description = post['description']
            caption_parts.append(f"• {sign_name}: {description}")
        
        # Add a common set of hashtags at the end
        hashtags = "\n\n#horoscope #astrology #zodiac #dailyhoroscope #starsigns #planetsvibe"
        caption_parts.append(hashtags)
        
        return "\n".join(caption_parts)


    # --- Login/Logout and Automation functions remain the same ---
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
