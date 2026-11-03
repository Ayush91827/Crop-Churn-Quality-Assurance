import re
from pages.base_page import BasePage

class CropPage(BasePage):
    def __init__(self, page, url):
        super().__init__(page)
        self.url = url

    def load(self):
        self.navigate(self.url)

    def fill_inputs(self, data: dict):
        """Fills out the Crop app form fields safely using labels or input types."""
        field_mapping = {
            "N": "N",
            "P": "P",
            "K": "K",
            "temperature": "Temperature",
            "humidity": "Humidity",
            "ph": "ph",
            "rainfall": "Rainfall"
        }

        for key, label in field_mapping.items():
            if key in data:
                try:
                    # Try targeting by Streamlit widget label first
                    locator = self.page.get_by_label(label, exact=False).first
                    locator.click(timeout=3000)
                    locator.press("Control+A")
                    locator.fill(str(data[key]))
                except Exception:
                    # Fallback: target number inputs sequentially if labels differ
                    try:
                        inputs = self.page.locator("input[type='text'], input[type='spinbutton']")
                        index_map = {"N": 0, "P": 1, "K": 2, "temperature": 3, "humidity": 4, "ph": 5, "rainfall": 6}
                        inputs.nth(index_map[key]).fill(str(data[key]))
                    except Exception as e:
                        print(f"Could not fill field {key}: {e}")

    def submit(self):
        # Matches the 'Get Crop Recommendation' or similar submit button safely
        submit_button = self.page.get_by_role("button", name=re.compile("Crop|Recommendation|Predict|Submit", re.IGNORECASE))
        submit_button.first.click()

    def get_result(self) -> str:
        result_element = self.page.locator(".stSuccess, [data-testid='stMarkdownContainer']")
        result_element.first.wait_for(state="visible", timeout=20000)
        return result_element.inner_text()

    def get_error_message(self) -> str:
        error_element = self.page.locator(".stError, .stAlert")
        error_element.first.wait_for(state="visible", timeout=5000)
        return error_element.inner_text()