import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CROP_URL = os.getenv("CROP_URL", "https://your-crop-app.vercel.app")
    CHURN_URL = os.getenv("CHURN_URL", "https://your-churn-app.streamlit.app")
    API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000")
    LLM_API_KEY = os.getenv("LLM_API_KEY", "")