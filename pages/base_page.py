from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded")
        self._wait_for_streamlit_ready()

    def _wait_for_streamlit_ready(self):
        """Wait for Streamlit to wake up and finish rendering elements."""
        try:
            # Streamlit shows a 'running' status or loader spinner on cold starts
            self.page.wait_for_selector(".stApp", state="visible", timeout=30000)
            # Ensure loading spinners disappear
            self.page.wait_for_selector(".stSpinner", state="detached", timeout=30000)
        except Exception:
            # Fallback if app doesn't use standard spinners
            pass

    def get_title(self) -> str:
        return self.page.title()