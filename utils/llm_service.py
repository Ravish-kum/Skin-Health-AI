import os
import google.generativeai as genai
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

gemini_model = None

class DummyModel:
    def generate_content(self, contents, **kwargs):
        class DummyResponse:
            def __init__(self):
                self.text = "Hello! I am your AI Dermatologist. I'm currently in a limited mode because the Gemini API key is missing or invalid. Please check your .env file."
        return DummyResponse()

def get_llm():
    global gemini_model
    if gemini_model is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            print("Warning: GEMINI_API_KEY not found or not set in .env.")
            return DummyModel()
        
        try:
            genai.configure(api_key=api_key)
            # Using gemini-pro-latest based on the list of available models in your environment
            gemini_model = genai.GenerativeModel('gemini-pro-latest')
            print("Gemini model initialized successfully.")
        except Exception as e:
            print(f"Error initializing Gemini: {e}")
            return DummyModel()
            
    return gemini_model
