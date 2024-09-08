import streamlit as st
from utils import load_openai_api_key
from llm_services import (
    generate_questions,
    stream_response,
    generate_title,
    generate_drawing_idea,
)

st.set_page_config(page_title="🧙‍♂️🔗 Blog Magician", page_icon="🧙‍♂️🔗")
st.title("🧙‍♂️🔗 Don't be lazy, write a blog post yourself (but use AI)!")

openai_api_key = load_openai_api_key()

if openai_api_key is None:
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

selected_question = None

with st.form("generate_questions"):
    topic_text = st.text_input("Enter keyword (topic):", "")
    submitted = st.form_submit_button("Generate Questions")

    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API key!", icon="⚠")

    if submitted and openai_api_key.startswith("sk-"):
        questions = generate_questions(topic_text, openai_api_key)
        st.session_state["questions"] = questions

if "questions" in st.session_state:
    st.write("### Select one of the questions generated for your blog:")
    for i, question in enumerate(st.session_state["questions"]):
        if st.button(question, key=f"question_{i}"):
            selected_question = question
            st.session_state["selected_question"] = selected_question

if "selected_question" in st.session_state:
    st.success(f"Active Question: {st.session_state['selected_question']}")

if "selected_question" in st.session_state:
    st.write("")
    draft_text = st.text_area(
        "Write your first draft here! Relax.. This is only your first version ...",
        placeholder="Write your draft based on the selected question...",
        height=300,
    )

    if st.button("Put in the oven"):
        if draft_text:
            st.write("### Revising your draft...")
            stream_response(draft_text, openai_api_key)

    st.write("")
    if st.button("Generate Title and Drawing Suggestion"):
        if draft_text:
            st.write("### Generating Title and Drawing Idea...")

            blog_title = generate_title(draft_text, openai_api_key)
            st.write("#### Suggested Title for the Blog Post:")
            st.write(blog_title)

            drawing_idea = generate_drawing_idea(draft_text, openai_api_key)
            st.write("#### Suggested Drawing Idea:")
            st.write(drawing_idea)
