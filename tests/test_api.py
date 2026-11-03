import pytest
import requests
from config import Config

@pytest.mark.api
def test_crop_prediction_happy_path():
    url = f"{Config.API_BASE_URL}/predict"
    payload = {
        "N": 90, "P": 42, "K": 43,
        "temperature": 20.8, "humidity": 82.0,
        "ph": 6.5, "rainfall": 202.9
    }
    response = requests.post(url, json=payload)
    
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 0.5
    data = response.json()
    assert "prediction" in data

@pytest.mark.api
def test_crop_prediction_missing_fields():
    url = f"{Config.API_BASE_URL}/predict"
    payload = {"N": 90}
    response = requests.post(url, json=payload)
    
    assert response.status_code == 400
    assert "error" in response.json()

@pytest.mark.api
def test_crop_prediction_wrong_types():
    url = f"{Config.API_BASE_URL}/predict"
    payload = {
        "N": "ninety",
        "P": 42, "K": 43, "temperature": 20.8, 
        "humidity": 82.0, "ph": 6.5, "rainfall": 202.9
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 400

@pytest.mark.api
def test_crop_prediction_empty_body():
    url = f"{Config.API_BASE_URL}/predict"
    response = requests.post(url, json={})
    assert response.status_code == 400