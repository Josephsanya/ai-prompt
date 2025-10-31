import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Set the GEMINI_API_KEY environment variable first.")

genai.configure(api_key=API_KEY)

# System prompt to guide AI response
SYSTEM_PROMPT = (
    "You are a helpful and polite AI assistant. "
    "Always answer clearly, concisely, and safely. Avoid any harmful or disallowed content."
)

# Banned keywords
BANNED_KEYWORDS = {"destroy", "attack", "rape", "fuck", "nigga", "shit", "kill", "hack", "bomb"}

# functions 
def is_input_safe(user_input: str) -> bool:
    """Check if the input contains banned keywords."""
    text = user_input.lower()
    return not any(word in text for word in BANNED_KEYWORDS)

def moderate_output(ai_response: str) -> str:
    """Replace banned words in AI output with [REDACTED]."""
    def replacer(match):
        return "[REDACTED]"
    pattern = re.compile(r"\b(" + "|".join(BANNED_KEYWORDS) + r")\b", re.IGNORECASE)
    return pattern.sub(replacer, ai_response)

# AI generation function

def generate_response(user_prompt: str):
    """Generate AI response with moderation checks."""
    if not is_input_safe(user_prompt):
        return "Your input violated the moderation policy."

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(f"{SYSTEM_PROMPT}\nUser: {user_prompt}")
        ai_text = response.text.strip()

        moderated_output = moderate_output(ai_text)

        if "[REDACTED]" in moderated_output:
            return "Your output violated the moderation policy."
        return moderated_output

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("Welcome! Type your prompt and press Enter.")
    user_input = input("Your prompt: ").strip()
    print("\nAI Response:\n", generate_response(user_input))
