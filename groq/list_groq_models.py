"""Lists Groq chat models your key can use and times a tiny call on a few.
Run: python list_groq_models.py
"""
import os
import time

from dotenv import load_dotenv
from groq import Groq

load_dotenv(override=True)
client = Groq(api_key=os.getenv("GROQ_API_KEY", "").strip(), timeout=20)

SKIP = ("whisper", "tts", "guard", "embed", "transcribe", "orpheus", "safeguard")
ids = sorted(m.id for m in client.models.list().data if not any(w in m.id.lower() for w in SKIP))

print("Chat models available to your key:")
for i in ids:
    print("  -", i)

print("\nTiming a tiny request on up to 6 of them...")
ok = []
for i in ids[:6]:
    start = time.time()
    try:
        r = client.chat.completions.create(
            model=i, max_tokens=30,
            messages=[{"role": "user", "content": "Say hello in one short sentence."}],
        )
        print(f"  {i}: OK in {time.time() - start:.1f}s -> {r.choices[0].message.content.strip()[:50]}")
        ok.append(i)
    except Exception as e:
        print(f"  {i}: FAILED -> {str(e)[:70]}")

if ok:
    print("\nPut this in your .env:  GROQ_MODEL=" + ok[0])
