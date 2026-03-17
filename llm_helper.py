from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the real LLM only when a GROQ API key is present. Otherwise
# provide a lightweight fallback so the app can run without external creds.
_GROQ_KEY = os.getenv("GROQ_API_KEY")


class _MockResponse:
    def __init__(self, content: str):
        self.content = content


class _MockLLM:
    def invoke(self, prompt: str):
        return _MockResponse(
            "GROQ_API_KEY is not set. Provide a valid GROQ_API_KEY in .env to generate real responses."
        )


if _GROQ_KEY:
    llm = ChatGroq(groq_api_key=_GROQ_KEY, model_name="llama-3.3-70b-versatile")
else:
    llm = _MockLLM()


if __name__ == "__main__":
    response = llm.invoke("Two most important ingradient in samosa are ")
    print(response.content)





