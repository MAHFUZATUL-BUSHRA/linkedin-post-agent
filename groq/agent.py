"""LinkedIn Post Agent built with LangChain (LCEL).

Pipeline:
  1. Planner chain  -> builds a short outline (hook, key points, CTA) for the topic
  2. Writer chain   -> writes the final post in the requested language
  3. Validator      -> checks the structure (2-4 paragraphs + hashtags); if it fails,
                       the agent retries with feedback until it passes (max retries)
"""
import os
import re
from dataclasses import dataclass, field

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(override=True)  # .env wins over any old Windows environment variable

MIN_PARAGRAPHS, MAX_PARAGRAPHS = 2, 4


def _clean_env_keys():
    """Remove accidental quotes/spaces around API keys in .env."""
    for name in ("GROQ_API_KEY", "GOOGLE_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
        val = os.getenv(name)
        if val:
            os.environ[name] = val.strip().strip("\"'")


def get_llm(provider: str | None = None, temperature: float = 0.7):
    _clean_env_keys()
    provider = (provider or os.getenv("LLM_PROVIDER", "groq")).lower()
    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
            temperature=temperature,
            max_tokens=1200,
            timeout=60,
            max_retries=1,
        )
    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            temperature=temperature,
            timeout=60,
            max_retries=1,
        )
    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            # No temperature here: Gemini 3+ models use their recommended default (1.0)
            model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
            timeout=60,       # fail fast instead of hanging
            max_retries=1,
        )
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=temperature,
                      timeout=60, max_retries=1)


PLANNER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a LinkedIn content strategist. Plan concise, insightful posts."),
    ("human",
     "Topic: {topic}\n\n"
     "Create a short outline (in English) for a LinkedIn post with:\n"
     "- Hook: one attention-grabbing opening line\n"
     "- Key points: 2-3 specific, valuable insights (no vague filler)\n"
     "- Call to action: a question or invitation that drives comments\n"
     "Return only the outline."),
])

WRITER_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are an expert LinkedIn ghostwriter. You write in a professional yet engaging, "
     "human voice. Never mention that you are an AI."),
    ("human",
     "Write a LinkedIn post about: {topic}\n"
     "Language: {language} (write the ENTIRE post in {language}, naturally, not word-for-word translation)\n\n"
     "Use this outline:\n{outline}\n\n"
     "Rules:\n"
     "- Exactly {min_p} to {max_p} short paragraphs, separated by a blank line\n"
     "- Paragraph 1 starts with the hook\n"
     "- The last paragraph ends with a question or call to action\n"
     "- Add at most 1-2 tasteful emojis\n"
     "- After the paragraphs, add one final line with 3-5 relevant hashtags\n"
     "- Output only the post text, no titles, labels or commentary\n"
     "{feedback}"),
])


@dataclass
class PostResult:
    post: str
    outline: str
    attempts: int
    issues: list[str] = field(default_factory=list)


def validate_post(text: str) -> list[str]:
    """Return a list of structural problems (empty list = valid)."""
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text.strip()) if b.strip()]
    has_tags = bool(blocks) and all(w.startswith("#") for w in blocks[-1].split())
    body = blocks[:-1] if has_tags else blocks
    issues = []
    if not (MIN_PARAGRAPHS <= len(body) <= MAX_PARAGRAPHS):
        issues.append(f"Post has {len(body)} paragraphs; it must have {MIN_PARAGRAPHS}-{MAX_PARAGRAPHS}.")
    if not has_tags:
        issues.append("Missing a final hashtag line (3-5 hashtags).")
    return issues


class LinkedInPostAgent:
    def __init__(self, provider: str | None = None, max_retries: int = 2):
        llm = get_llm(provider)
        parser = StrOutputParser()
        self.planner = PLANNER_PROMPT | llm | parser
        self.writer = WRITER_PROMPT | llm | parser
        self.max_retries = max_retries

    def generate(self, topic: str, language: str = "English") -> PostResult:
        topic, language = topic.strip(), language.strip() or "English"
        if not topic:
            raise ValueError("Topic must not be empty.")

        outline = self.planner.invoke({"topic": topic})
        feedback, post, issues = "", "", []

        for attempt in range(1, self.max_retries + 2):
            post = self.writer.invoke({
                "topic": topic, "language": language, "outline": outline,
                "min_p": MIN_PARAGRAPHS, "max_p": MAX_PARAGRAPHS, "feedback": feedback,
            }).strip()
            issues = validate_post(post)
            if not issues:
                return PostResult(post, outline, attempt)
            feedback = "\nFix these problems from your previous draft: " + " ".join(issues)

        return PostResult(post, outline, self.max_retries + 1, issues)


if __name__ == "__main__":
    t = input("Topic: ")
    lang = input("Language (e.g. English, Bengali, Spanish): ")
    result = LinkedInPostAgent().generate(t, lang)
    print("\n--- LinkedIn Post ---\n")
    print(result.post)
