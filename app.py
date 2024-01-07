"""Inspired by:

Source: https://medium.com/streamlit/how-to-build-an-llm-powered-chatbot-with-streamlit-a1bf0b2701e8
Source: https://medium.com/@m.nusret.ozates/unleashing-the-future-of-ai-powered-qa-chatbots-streamlit-langchain-retrieval-qa-chatgpt-53c0dd8876ed
"""
import os
import warnings

import streamlit as st
from dotenv import load_dotenv
from streamlit_extras.add_vertical_space import add_vertical_space

from assistant import initialize_bot

warnings.simplefilter('ignore', UserWarning)


load_dotenv()


st.set_page_config(page_title='VA Chatbot - An LLM-powered Streamlit app')

BOT = None


def initialize_chat(st):
    """Initialize chat session."""
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {'role': 'assistant', 'content': 'How can I help you?'}
        ]
    for index, msg in enumerate(st.session_state.messages):
        st.chat_message(msg['role']).write(msg['content'])


def initialize_assistant():
    try:
        # Initialize assistance bot and stop if there is an error.
        global BOT
        if st.session_state.dataset_path.startswith('hub://'):
            dataset_path = st.session_state.dataset_path
        else:
            dataset_path = os.path.join('deeplake', st.session_state.dataset_path)
        BOT = initialize_bot(dataset_path=dataset_path)
    except Exception as ex:
        st.error(ex)
        BOT = None


st.title('💬 Virtual Assistance Chatbot')

with st.sidebar:
    st.title('💬 Virtual Assistance Chatbot')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](<https://streamlit.io/>)
    - [LangChain](<https://github.com/langchain-ai/langchain>)
    - [Deep Lake](<https://github.com/activeloopai/deeplake>)
    - [OpenAI API](<https://openai.com/blog/openai-api>)
    ''')

    dataset_path = st.selectbox(
        label='Which database do you want to use?',
        options=os.listdir('deeplake/') +
        [
            'hub://haritsahm/spotify_reviews_cleaned_filtered_balanced_50K_docs_1000_chunk',
            'hub://haritsahm/spotify_filter_version_ratings_count_balanced_50K_docs_1000_chunk',
        ],
        on_change=initialize_assistant,
        key='dataset_path'
    )

    add_vertical_space(5)
    st.write('Made with ❤️ by [Data Professor](<https://youtube.com/dataprofessor>)')

initialize_assistant()

# Stop process if bot is not valid
if BOT is None:
    st.stop()

initialize_chat(st)

if question := st.chat_input():
    # Get and save the question
    st.session_state.messages.append({'role': 'user', 'content': question})
    st.chat_message('user').write(question)

    # Get an answer using question and the conversation history
    answer: str = BOT.process(
        {
            'question': question,
        }
    )

    # Save the answer
    st.session_state.messages.append({'role': 'assistant', 'content': answer})
    st.chat_message('assistant').write(answer)
