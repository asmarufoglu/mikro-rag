import os
from dotenv import load_dotenv
import google.generativeai as genai

# ---------- LLM Setup ----------
load_dotenv()
genai.configure(api_key=os.getenv("YOUR_GOOGLE_API_KEY"))

def generate_answer(context_text: str, user_input: str) -> str:
    """
    Generates a root-cause summary using Gemini 2.5 Flash based on retrieved network logs.
    """
    if not context_text.strip():
        return "⚠️ No sufficient context found."

    prompt = f"""
    You are a network reliability AI assistant.
    Analyze the following network logs and summarize the most probable root cause.
    Respond in one concise technical sentence.

    User query:
    {user_input}

    Logs:
    {context_text}
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ LLM request failed: {e}"
