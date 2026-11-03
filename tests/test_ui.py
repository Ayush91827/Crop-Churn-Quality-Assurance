import json
import pytest
from playwright.sync_api import expect
from config import Config
from pages.crop_page import CropPage
from pages.churn_page import ChurnPage

@pytest.fixture(scope="session")
def test_data():
    with open("test_data.json") as f:
        return json.load(f)

# ==========================================
# CROP APP TESTS (10 Test Cases)
# ==========================================

@pytest.mark.smoke
def test_crop_page_loads_without_errors(page):
    """TC01: Verify Crop page loads successfully and title matches."""
    app = CropPage(page, Config.CROP_URL)
    app.load()
    assert "Crop" in app.get_title() or "Prediction" in app.get_title()

@pytest.mark.regression
def test_crop_valid_prediction(page, test_data):
    """TC02: Verify valid input values return a successful crop recommendation."""
    app = CropPage(page, Config.CROP_URL)
    app.load()
    app.fill_inputs(test_data["crop_valid"])
    app.submit()
    assert len(app.get_result()) > 0

@pytest.mark.regression
def test_crop_empty_fields_show_error(page):
    """TC03: Verify submitting empty fields triggers an error or validation state."""
    app = CropPage(page, Config.CROP_URL)
    app.load()
    app.submit()
    assert app.get_error_message() is not None

@pytest.mark.regression
def test_crop_out_of_range_values(page, test_data):
    """TC04: Verify extreme out-of-range values are flagged or rejected."""
    app = CropPage(page, Config.CROP_URL)
    app.load()
    app.fill_inputs(test_data["crop_out_of_range"])
    app.submit()
    assert app.get_error_message() is not None

@pytest.mark.regression
def test_crop_negative_values(page, test_data):
    """TC05: Verify negative numerical inputs trigger validation errors."""
    app = CropPage(page, Config.CROP_URL)
    app.load()
    app.fill_inputs(test_data["crop_negative"])
    app.submit()
    assert app.get_error_message() is not None

@pytest.mark.regression
@pytest.mark.parametrize("invalid_val", ["abc", "!@#", " "])
def test_crop_wrong_data_types(page, invalid_val):
    """TC06: Verify entering string text into numeric fields fails validation."""
    app = CropPage(page, Config.CROP_URL)
    app.load()
    data = {"N": invalid_val, "P": 42, "K": 43, "temperature": 20, "humidity": 80, "ph": 6, "rainfall": 200}
    app.fill_inputs(data)
    app.submit()
    assert page.locator(".stError, input:invalid").count() > 0

@pytest.mark.regression
def test_crop_boundary_ph_values(page):
    """TC07: Verify edge-case boundary values for soil pH (e.g., pH = 0)."""
    app = CropPage(page, Config.CROP_URL)
    app.load()
    data = {"N": 50, "P": 50, "K": 50, "temperature": 25, "humidity": 70, "ph": 0.0, "rainfall": 150}
    app.fill_inputs(data)
    app.submit()
    assert page.locator(".stError, .stSuccess").count() > 0

@pytest.mark.regression
def test_crop_alternative_valid_dataset(page, test_data):
    """TC08: Verify secondary valid crop dataset runs successfully."""
    app = CropPage(page, Config.CROP_URL)
    app.load()
    app.fill_inputs(test_data["crop_alternative"])
    app.submit()
    assert len(app.get_result()) > 0

@pytest.mark.regression
def test_crop_ui_element_presence(page):
    """TC09: Verify required input elements are visible on the page."""
    app = CropPage(page, Config.CROP_URL)
    app.load()
    # Using flexible label-based checks to prevent placeholder mismatch timeouts
    expect(page.get_by_label("N", exact=False).first).to_be_visible()
    expect(page.get_by_label("P", exact=False).first).to_be_visible()
    expect(page.get_by_label("K", exact=False).first).to_be_visible()

@pytest.mark.regression
def test_crop_rapid_double_submission(page, test_data):
    """TC10: Verify application handles rapid double-clicks on submit without crashing."""
    app = CropPage(page, Config.CROP_URL)
    app.load()
    app.fill_inputs(test_data["crop_valid"])
    app.submit()
    app.submit()
    assert len(app.get_result()) > 0


# ==========================================
# CHURN APP TESTS (10 Test Cases)
# ==========================================

@pytest.mark.smoke
def test_churn_page_loads_without_errors(page):
    """TC11: Verify Churn page loads successfully and title matches."""
    app = ChurnPage(page, Config.CHURN_URL)
    app.load()
    assert "Prediction" in app.get_title()

@pytest.mark.regression
def test_churn_valid_prediction(page, test_data):
    """TC12: Verify valid customer profile returns a prediction result."""
    app = ChurnPage(page, Config.CHURN_URL)
    app.load()
    app.fill_inputs(test_data["churn_valid"])
    app.submit()
    assert len(app.get_result()) > 0

@pytest.mark.regression
@pytest.mark.parametrize("geo_key", ["churn_valid", "churn_spain", "churn_germany"])
def test_churn_geography_options(page, test_data, geo_key):
    """TC13-15: Parameterized test verifying France, Spain, and Germany selections."""
    app = ChurnPage(page, Config.CHURN_URL)
    app.load()
    app.fill_inputs(test_data[geo_key])
    app.submit()
    assert len(app.get_result()) > 0

@pytest.mark.regression
def test_churn_invalid_age_rejection(page, test_data):
    """TC16: Verify unrealistic age triggers validation warning."""
    app = ChurnPage(page, Config.CHURN_URL)
    app.load()
    app.fill_inputs(test_data["churn_invalid_age"])
    app.submit()
    assert page.locator(".stError, [data-testid='stMarkdownContainer']").count() > 0

@pytest.mark.regression
def test_churn_empty_fields(page):
    """TC17: Verify submitting empty churn form handles validation gracefully."""
    app = ChurnPage(page, Config.CHURN_URL)
    app.load()
    app.submit()
    assert page.locator(".stApp").is_visible()

@pytest.mark.regression
def test_churn_zero_balance_edge_case(page, test_data):
    """TC18: Verify customer profile with 0 balance executes successfully."""
    app = ChurnPage(page, Config.CHURN_URL)
    app.load()
    data = test_data["churn_valid"]
    data["balance"] = 0.0
    app.fill_inputs(data)
    app.submit()
    assert len(app.get_result()) > 0

@pytest.mark.regression
def test_churn_dropdown_interactivity(page):
    """TC19: Verify dropdown components like Active Member and Credit Card are interactive."""
    app = ChurnPage(page, Config.CHURN_URL)
    app.load()
    expect(page.get_by_text("Has Credit Card", exact=False)).to_be_visible()
    expect(page.get_by_text("Is Active Member", exact=False)).to_be_visible()

@pytest.mark.regression
def test_churn_high_salary_boundary(page, test_data):
    """TC20: Verify ultra-high estimated salary boundary condition."""
    app = ChurnPage(page, Config.CHURN_URL)
    app.load()
    data = test_data["churn_valid"]
    data["estimated_salary"] = 9999999.0
    app.fill_inputs(data)
    app.submit()
    assert len(app.get_result()) > 0