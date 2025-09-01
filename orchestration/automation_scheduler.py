# /orchestration/automation_scheduler.py

import schedule
import time
import threading

class AutomationScheduler:
    """
    A focused scheduler to run the astrology post generation task daily.
    """
    def __init__(self, orchestrator):
        # It needs a reference to the orchestrator to call the main function
        self.orchestrator = orchestrator
        self.is_running = False
        self.scheduler_thread = None
        print("✅ Automation Scheduler initialized.")

    def _run_daily_job(self):
        """The function that will be executed by the schedule."""
        print("⏰ AUTOMATION: It's time! Running the daily astrology post generation...")
        self.orchestrator.generate_all_astrology_posts()
        print("✅ AUTOMATION: Daily job finished. Waiting for the next scheduled run.")

    def start(self, run_time: str = "10:30"):
        """Starts the scheduler in a background thread."""
        if self.is_running:
            print("Scheduler is already running.")
            return
        
        print(f"▶️ Starting automation. Job will run daily at {run_time}.")
        self.is_running = True
        
        # Configure the schedule
        schedule.every().day.at(run_time).do(self._run_daily_job)
        
        # Start the background thread
        self.scheduler_thread = threading.Thread(target=self._run_pending_jobs, daemon=True)
        self.scheduler_thread.start()

    def stop(self):
        """Stops the background scheduler thread."""
        if not self.is_running:
            print("Scheduler is not running.")
            return
            
        print("⏹️ Stopping automation scheduler...")
        self.is_running = False
        schedule.clear()
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=2)
        print("Scheduler stopped.")

    def _run_pending_jobs(self):
        """The loop that continuously checks for and runs scheduled jobs."""
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)
