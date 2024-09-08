import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langchain.callbacks.base import BaseCallbackHandler
import dotenv

st.set_page_config(
    page_title="🧙‍♂️🔗 Blog Magician",
    page_icon="🧙‍♂️🔗",
)
st.title("🧙‍♂️🔗 Don't be lazy, write a blog post yourself (but use AI)!")

openai_api_key = dotenv.get_key(key_to_get="OPENAI_API_KEY", dotenv_path=".env")

if openai_api_key is None:
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")


# Define a StreamHandler to handle streamed tokens
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text="", display_method="markdown"):
        self.container = container
        self.text = initial_text
        self.display_method = display_method

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        display_function = getattr(self.container, self.display_method, None)
        if display_function is not None:
            display_function(self.text)
        else:
            raise ValueError(f"Invalid display_method: {self.display_method}")


def generate_questions(topic):
    llm = ChatOpenAI(model_name="gpt-4", openai_api_key=openai_api_key)
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


def get_feedback(draft_text):
    llm = ChatOpenAI(model_name="gpt-4", openai_api_key=openai_api_key)
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

    response = llm([message])
    return response.content


def stream_response(draft_text):
    chat_box = st.empty()  # A container to stream the tokens in real-time
    stream_handler = StreamHandler(
        chat_box, display_method="write"
    )  # Stream tokens as they are generated

    llm = ChatOpenAI(
        model_name="gpt-4",
        openai_api_key=openai_api_key,
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


# Event handling and form submission
selected_question = None

with st.form("generate_questions"):
    topic_text = st.text_input("Enter keyword (topic):", "")
    submitted = st.form_submit_button("Generate Questions")

    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API key!", icon="⚠")

    if submitted and openai_api_key.startswith("sk-"):
        questions = generate_questions(topic_text)
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
    st.write("")  # Adds a vertical space
    draft_text = st.text_area(
        "Write your first draft here! Relax.. This is only your first version ...",
        placeholder="Write your draft based on the selected question...",
        height=300,
    )

    if st.button("Put in the oven"):
        if draft_text:
            st.write("### Revising your draft...")
            stream_response(draft_text)

    st.write("")  # Adds another vertical space
    if st.button("Make it a blog Post"):
        st.write("### Now let's prepare your final blog post!")
        blog_title = st.text_input(
            "Blog Post Title", value="Add your blog post title here"
        )
        drawing_idea = st.text_area(
            "Drawing Idea",
            value="Write down an idea for a sketch that could complement your blog post."
            "You can sketch it using Excalidraw in minutes!",
        )

        st.write("#### Title for the Blog Post:")
        st.write(blog_title)

        st.write("#### Drawing Idea:")
        st.write(drawing_idea)
