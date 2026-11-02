"""Lists Gemini models your key can use and times a tiny call on the fast ones.
Run: python list_models.py
"""
import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

names = []
for m in client.models.list():
    actions = getattr(m, "supported_actions", None) or []
    if "generateContent" in actions:
        names.append(m.name.replace("models/", ""))

print("Models available to your key:")
for n in names:
    print("  -", n)

candidates = [n for n in names if "flash" in n and "image" not in n and "tts" not in n][:5]
print("\nTiming a tiny request on each (20s limit)...")
for n in candidates:
    start = time.time()
    try:
        r = client.models.generate_content(
            model=n,
            contents="Say hello in one short sentence.",
            config={"http_options": {"timeout": 20000}},
        )
        print(f"  {n}: OK in {time.time() - start:.1f}s -> {r.text.strip()[:60]}")
    except Exception as e:
        print(f"  {n}: FAILED after {time.time() - start:.1f}s -> {str(e)[:80]}")
