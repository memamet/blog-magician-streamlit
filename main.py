import streamlit as st
from utils import load_openai_api_key
from llm_services import (
    generate_questions,
    stream_response,
    generate_title,
    generate_drawing_idea,
)

st.set_page_config(page_title="🧙‍♂️🔗 Blog Magician", page_icon="🧙‍♂️🔗")
st.title("🧙‍♂️🔗 Don't be lazy, write a blog post yourself (but use AI as a copilot)!")

openai_api_key = load_openai_api_key()

if openai_api_key is None:
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# Add model selection in the sidebar
model_name = st.sidebar.selectbox(
    "Select OpenAI Model", ["gpt-4o-mini", "gpt-4o"], index=0
)

selected_question = None

with st.form("generate_questions"):
    topic_text = st.text_input("Enter keyword (topic):", "")
    submitted = st.form_submit_button("Generate Questions")

    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API key!", icon="⚠")

    if submitted and openai_api_key.startswith("sk-"):
        questions = generate_questions(topic_text, openai_api_key, model_name)
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
    first_draft = st.text_area(
        "Write your first draft here! Relax.. This is only your first version ...",
        placeholder="Write your draft based on the selected question...",
        height=300,
        key="first_draft",
    )

    if "revised_by_ai" not in st.session_state:
        st.session_state["revised_by_ai"] = first_draft

    if st.button("Put in the oven"):
        if first_draft:
            st.write("### Revising your draft...")

            ai_revision = stream_response(first_draft, openai_api_key, model_name)
            st.session_state["revised_by_ai"] = ai_revision

            st.session_state["revised_by_human"] = st.session_state["revised_by_ai"]

    if "revised_by_human" in st.session_state:
        revised_by_human = st.text_area(
            "Revised Draft (You can modify this)",
            value=st.session_state["revised_by_human"],
            height=300,
            key="revised_by_human_input",
        )
        st.session_state["revised_by_human"] = revised_by_human

    if "revised_by_human" in st.session_state:
        if st.button("Generate Title and Drawing Suggestion"):
            revised_by_human = st.session_state["revised_by_human"]
            if revised_by_human:
                st.write("### Generating Title and Drawing Idea...")

                blog_title = generate_title(
                    revised_by_human, openai_api_key, model_name
                )
                st.write("#### Suggested Title for the Blog Post:")
                st.write(blog_title)

                drawing_idea = generate_drawing_idea(
                    revised_by_human, openai_api_key, model_name
                )
                st.write("#### Suggested Drawing Idea:")
                st.write(drawing_idea)
