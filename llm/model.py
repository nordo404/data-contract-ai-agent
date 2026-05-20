import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file automatically
load_dotenv()

# Read provider + model from environment (optional)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def _call_gemini(prompt: str) -> str:
    """
    Calls Gemini using the API key stored in .env.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found. Did you set it in your .env file?")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(GEMINI_MODEL)

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.1,
            "max_output_tokens": 4096,
        }
    )

    return response.text


def call_llm(prompt: str) -> str:
    """
    Single entry point for the entire system.
    """
    if LLM_PROVIDER == "gemini":
        return _call_gemini(prompt)

    raise ValueError(f"Unknown LLM_PROVIDER: {LLM_PROVIDER}")
