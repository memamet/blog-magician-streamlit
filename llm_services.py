from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from stream_handler import StreamHandler
import streamlit as st


def generate_questions(topic, api_key, model_name):
    llm = ChatOpenAI(model_name=model_name, openai_api_key=api_key)
    template = (
        "As an experienced blog technical writer, generate a list of 3 questions "
        "that could be used as a blog post title for the following topic: {topic}."
        "dont output anything else"
    )
    prompt_query = template.format(topic=topic)

    message = HumanMessage(content=prompt_query)
    response = llm([message])
    return response.content.split("\n")


def stream_response(draft_text, api_key, model_name):
    chat_box = st.empty()
    stream_handler = StreamHandler(chat_box, display_method="write")

    llm = ChatOpenAI(
        model_name=model_name,
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
        "Don't output an intro sentence, only the revised draft"
    )
    prompt_query = template.format(draft_text=draft_text)
    message = HumanMessage(content=prompt_query)

    response = llm([message])

    return response.content


def generate_title(draft_text, api_key, model_name):
    llm = ChatOpenAI(model_name=model_name, openai_api_key=api_key)
    template = (
        "Generate a creative and engaging title for the following blog post:\n\n"
        "{draft_text}\n"
    )
    prompt_query = template.format(draft_text=draft_text)

    message = HumanMessage(content=prompt_query)
    response = llm([message])
    return response.content


def generate_drawing_idea(draft_text, api_key, model_name):
    llm = ChatOpenAI(model_name=model_name, openai_api_key=api_key)
    template = (
        "Suggest in two sentences a very simple illustration schema (using excalidraw) that could complement the following blog post. "
        "{draft_text}\n"
    )
    prompt_query = template.format(draft_text=draft_text)

    message = HumanMessage(content=prompt_query)
    response = llm([message])
    return response.content
