from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from stream_handler import StreamHandler
import streamlit as st


def generate_questions(topic, api_key):
    llm = ChatOpenAI(model_name="gpt-4", openai_api_key=api_key)
    template = (
        "As an experienced blog technical writer, generate a list of 3 questions "
        "that could be used as a blog post title for the following topic: {topic}."
    )
    prompt = PromptTemplate(input_variables=["topic"], template=template)
    prompt_query = prompt.format(topic=topic)

    # Create a HumanMessage instead of a dictionary
    message = HumanMessage(content=prompt_query)

    response = llm([message])
    return response.content.split("\n")


def stream_response(draft_text, api_key):
    chat_box = st.empty()  # A container to stream the tokens in real-time
    stream_handler = StreamHandler(
        chat_box, display_method="write"
    )  # Stream tokens as they are generated

    llm = ChatOpenAI(
        model_name="gpt-4",
        openai_api_key=api_key,
        streaming=True,
        callbacks=[stream_handler],
    )

    template = (
        "Here is a blog draft:\n\n"
        "{draft_text}\n\n"
        "Please revise it and suggest the following:\n"
        "- Add examples (inline in the text in brackets)\n"
        "- Point out where the text is unclear (inline in the text in brackets)\n"
        "- Provide additional punchlines (inline in the text in parentheses)"
    )
    prompt_query = template.format(draft_text=draft_text)

    # Create a HumanMessage instead of a dictionary
    message = HumanMessage(content=prompt_query)

    response = llm([message])  # The response is handled by the callback
