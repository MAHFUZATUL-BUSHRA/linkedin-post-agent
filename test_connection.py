"""Quick check: one tiny model call with timing. Run: python test_connection.py"""
import time
from agent import get_llm

start = time.time()
try:
    reply = get_llm().invoke("Say hello in one short sentence.")
    print("OK:", reply.content)
except Exception as e:
    print("ERROR:", e)
print(f"Took {time.time() - start:.1f} seconds")
