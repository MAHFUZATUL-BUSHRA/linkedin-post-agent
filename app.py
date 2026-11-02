import streamlit as st
from agent import LinkedInPostAgent

st.set_page_config(page_title="LinkedIn Post Agent", page_icon="💼")
st.title("💼 LinkedIn Post Generator Agent")
st.caption("Powered by LangChain · plans an outline, writes the post, validates the structure.")

LANGS = ["English", "Bengali", "Spanish", "French", "German", "Hindi", "Arabic", "Other…"]

topic = st.text_input("Post topic", placeholder="e.g. AI in Healthcare")
choice = st.selectbox("Language", LANGS)
language = st.text_input("Type the language") if choice == "Other…" else choice
provider = st.radio("LLM provider", ["gemini", "openai", "anthropic"], horizontal=True)

if st.button("Generate post", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        try:
            with st.spinner("Planning and writing your post..."):
                result = LinkedInPostAgent(provider=provider).generate(topic, language)
            st.subheader("Your LinkedIn post")
            st.write(result.post)
            st.code(result.post, language=None)  # one-click copy button
            with st.expander("Agent details"):
                st.markdown(f"**Attempts:** {result.attempts}")
                st.markdown("**Outline used:**")
                st.text(result.outline)
                if result.issues:
                    st.warning("Remaining issues: " + " ".join(result.issues))
        except Exception as e:
            st.error(f"Something went wrong: {e}")
