# 💼 LinkedIn Post Agent

An AI agent built with **LangChain** that turns a **topic** and a **language** into a professional, engaging LinkedIn post (2–4 paragraphs plus hashtags).

🎥 **Demo video:** [https://github.com/MAHFUZATUL-BUSHRA/linkedin-post-agent/tree/main/Demo%20Video}

---

## ✨ Features

- Generates LinkedIn-style posts for any topic
- Multilingual output: English, Bengali, Spanish, French, German, Hindi, Arabic, or any language you type
- Three-step agent workflow (plan → write → validate), not a single prompt
- Automatic structure check with retries: 2–4 paragraphs, closing call to action, 3–5 hashtags
- Simple web UI built with Streamlit, plus a command-line mode
- Switchable LLM provider: Gemini (free tier), OpenAI, or Anthropic

## 🧠 How It Works

```
Topic + Language
      │
      ▼
┌──────────────┐
│ Planner chain │  → outline: hook, key points, call to action
└──────┬───────┘
       ▼
┌──────────────┐
│ Writer chain  │  → full post in the chosen language
└──────┬───────┘
       ▼
┌──────────────┐
│  Validator    │  → 2–4 paragraphs? hashtags present?
└──────┬───────┘
   no  │  yes
  retry│   ▼
 with  │  Final post
feedback
```

The chains are built with the LangChain Expression Language (`prompt | llm | output_parser`).

## 🛠️ Tech Stack

- Python 3.10+
- LangChain (`langchain-core`, `langchain-google-genai`, `langchain-openai`, `langchain-anthropic`)
- Streamlit
- python-dotenv

## 📁 Project Structure

```
linkedin-post-agent/
├── agent.py             # LangChain agent: planner, writer, validator
├── app.py               # Streamlit web UI
├── test_connection.py   # Quick check that your API key and model work
├── list_models.py       # Lists Gemini models your key can use
├── requirements.txt
├── .env.example         # Template for your API keys
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/linkedin-post-agent.git
cd linkedin-post-agent
```

### 2. Create a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
Copy the example file and edit it:
```bash
# Windows
copy .env.example .env
# Mac / Linux
cp .env.example .env
```

For the **free** option, get a Gemini key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey) and set:
```
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your-key-here
GEMINI_MODEL=gemini-3-flash-preview
```

OpenAI and Anthropic are also supported (see `.env.example`).

### 5. Run it
```bash
streamlit run app.py     # web UI at http://localhost:8501
python agent.py          # command-line mode
```

## 📝 Example

**Input**
- Topic: `Remote Work Productivity`
- Language: `Spanish`

**Output:** a 3-paragraph Spanish LinkedIn post with an attention-grabbing hook, practical insights, a closing question for engagement, and relevant hashtags.

## 🔧 Troubleshooting

| Problem | Fix |
|---|---|
| `429 no credits remaining` (OpenAI) | Add billing credit, or switch to Gemini (free) |
| `404 model not found` | Run `python list_models.py` and set `GEMINI_MODEL` to a listed model |
| `503` or `504` / very slow | The model is overloaded; try another model from `list_models.py` |
| `No module named ...` | Activate the venv and run `pip install -r requirements.txt` |
| Provider option missing in the app | Make sure you are running the latest `app.py`, then refresh the page |

Run `python test_connection.py` to quickly check that your key and model work.

## 🔒 Security

Never commit your `.env` file. It is listed in `.gitignore`.

## 🔮 Future Improvements

- Tone selector (formal, casual, storytelling)
- Post length and emoji controls
- Generate multiple variants to choose from
- Direct publishing to LinkedIn via its API


## 👤 Author

**[Mahfuzatul Bushra]** 
