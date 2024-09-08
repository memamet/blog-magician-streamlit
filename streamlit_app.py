import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import dotenv

st.set_page_config(
    page_title="🧙‍♂️🔗 Blog Magician",
    page_icon="🧙‍♂️🔗",
)
st.title("🧙‍♂️🔗 Don't be lazy, write a blog post yourself (but use AI)!")

openai_api_key = dotenv.get_key(key_to_get="OPENAI_API_KEY", dotenv_path=".env")

if openai_api_key is None:
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")


def generate_response(topic):
    llm = ChatOpenAI(model_name="gpt-4", openai_api_key=openai_api_key)
    template = "As an experienced blog technical writer, generate a list of 3 questions that could be used as a blog post title for the following topic: {topic}"
    prompt = PromptTemplate(input_variables=["topic"], template=template)
    prompt_query = prompt.format(topic=topic)
    messages = [{"role": "user", "content": prompt_query}]
    response = llm.invoke(messages)
    return st.info(response.content)


with st.form("myform"):
    topic_text = st.text_input("Enter keyword:", "")
    submitted = st.form_submit_button("Submit")

    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API key!", icon="⚠")

    if submitted and openai_api_key.startswith("sk-"):
        generate_response(topic_text)
