# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

from app.services.gemini_service import GeminiService

# Load environment variables
load_dotenv()


def main():
    service = GeminiService()

    prompt = """
You are a professional communication assistant.

Write a professional WhatsApp message informing my manager that
I'll be approximately 20 minutes late because of traffic.

Keep it polite and concise.
"""

    response = service.generate(prompt)

    print("\n" + "=" * 60)
    print("GEMINI RESPONSE")
    print("=" * 60)
    print(response)
    print("=" * 60)


if __name__ == "__main__":
    main()