# /orchestration/main_orchestrator.py

from core_services.content_generator_service import ContentGeneratorService
from core_services.image_post_generator_service import ImagePostGeneratorService
from platform_services.instagram_service import InstagramService
from platform_services.instagram_connection_service import InstagramConnectionService # <-- NEW
from orchestration.automation_scheduler import AutomationScheduler

class MainOrchestrator:
    def __init__(self):
        print("Initializing the Planets Vibe Orchestrator...")

        # --- Initialize Services ---
        self.content_generator = ContentGeneratorService()
        self.image_post_generator = ImagePostGeneratorService()
        self.instagram_service = InstagramService(
            content_generator=self.content_generator,
            image_post_generator=self.image_post_generator
        )
        self.scheduler = AutomationScheduler(orchestrator=self)
        
        # --- NEW: Instantiate the connection service ---
        self.instagram_connection = InstagramConnectionService()
        
        print("✅ Planets Vibe Orchestrator and all services initialized.")

    def generate_all_astrology_posts(self) -> list:
        print("ORCHESTRATOR: Initiating a full run for all zodiac signs...")
        return self.instagram_service.create_daily_astrology_post_for_all_signs()

    # --- NEW: Methods to handle connection ---
    def login_to_instagram(self, username, password):
        return self.instagram_connection.login(username, password)

    def logout_from_instagram(self):
        return self.instagram_connection.logout()

    def get_instagram_status(self):
        return self.instagram_connection.get_status()

    # --- Automation Methods (unchanged) ---
    def start_automation(self, run_time: str):
        self.scheduler.start(run_time)

    def stop_automation(self):
        self.scheduler.stop()
