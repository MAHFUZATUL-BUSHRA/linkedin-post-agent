"""Quick check: one tiny model call with timing. Run: python test_connection.py"""
import os
import time

from agent import get_llm

key = os.getenv("GROQ_API_KEY", "")
print("Provider:", os.getenv("LLM_PROVIDER"), "| Groq key prefix:", repr(key[:4]), "length:", len(key))

start = time.time()
try:
    reply = get_llm().invoke("Say hello in one short sentence.")
    print("OK:", reply.content)
except Exception as e:
    print("ERROR:", e)
    cause = e.__cause__
    while cause is not None:   # show the real underlying reason
        print("  caused by:", type(cause).__name__, "-", cause)
        cause = cause.__cause__
print(f"Took {time.time() - start:.1f} seconds")
