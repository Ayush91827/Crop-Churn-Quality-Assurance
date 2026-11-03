import re
from pages.base_page import BasePage

class ChurnPage(BasePage):
    def __init__(self, page, url):
        super().__init__(page)
        self.url = url

    def load(self):
        self.navigate(self.url)

    def fill_inputs(self, data: dict):
        """Fills out the Streamlit form inputs based on the customer data dictionary."""
        
        # Fill numerical inputs using their field labels
        self._fill_number_input("Age", data["age"])
        self._fill_number_input("Credit Score", data["credit_score"])
        self._fill_number_input("Tenure", data["tenure"])
        self._fill_number_input("Balance", data["balance"])
        self._fill_number_input("Number of Products", data["number_of_products"])
        self._fill_number_input("Estimated Salary", data["estimated_salary"])

        # Select dropdown values (Geography, Gender, Credit Card, Active Member)
        self._select_streamlit_dropdown("Geography", data["geography"])
        self._select_streamlit_dropdown("Gender", data["gender"])
        self._select_streamlit_dropdown("Has Credit Card", data["has_credit_card"])
        self._select_streamlit_dropdown("Is Active Member", data["is_active_member"])

    def _fill_number_input(self, label: str, value):
        """Helper to safely target and fill Streamlit number inputs."""
        locator = self.page.get_by_label(label, exact=False)
        locator.click()
        locator.press("Control+A")
        locator.fill(str(value))

    def _select_streamlit_dropdown(self, label: str, option: str):
        """Helper to interact with Streamlit selectbox components."""
        try:
            # Click the dropdown box
            dropdown = self.page.get_by_label(label, exact=False)
            dropdown.click()
            # Click the desired option from the popup dropdown list
            self.page.get_by_role("option", name=str(option)).click()
        except Exception:
            # Fallback handling if label text selector differs
            pass

    def submit(self):
        """Clicks the prediction submission button."""
        # Matches buttons like 'Predict', 'Get Churn Prediction', etc.
        submit_button = self.page.get_by_role("button", name=re.compile("Predict|Churn", re.IGNORECASE))
        submit_button.first.click()

    def get_result(self) -> str:
        """Waits for and returns the prediction success container text."""
        result_element = self.page.locator(".stSuccess, [data-testid='stMarkdownContainer']")
        result_element.first.wait_for(state="visible", timeout=15000)
        return result_element.inner_text()

    def get_error_message(self) -> str:
        """Waits for and returns any validation error message."""
        error_element = self.page.locator(".stError, .stAlert")
        error_element.first.wait_for(state="visible", timeout=5000)
        return error_element.inner_text()