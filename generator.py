import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Set the GEMINI_API_KEY environment variable first.")

# Configure Gemini
genai.configure(api_key=API_KEY)

def generate_response(prompt):
    try:
        
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("Welcome! Type your prompt and press Enter.")
    prompt = input("Your prompt: ").strip()
    answer = generate_response(prompt)
    print("\nAI Response:\n", answer)
