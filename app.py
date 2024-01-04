import os

import streamlit as st
from dotenv import load_dotenv
from streamlit_extras.add_vertical_space import add_vertical_space

from assistant import initialize_bot

load_dotenv()


st.set_page_config(page_title='HugChat - An LLM-powered Streamlit app')


def initialize_chat(st):
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {'role': 'assistant', 'content': 'How can I help you?'}
        ]
    for index, msg in enumerate(st.session_state.messages):
        st.chat_message(msg['role']).write(msg['content'])


st.title('💬 Virtual Assistance Chatbot')

with st.sidebar:
    st.title('💬 Virtual Assistance Chatbot')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](<https://streamlit.io/>)
    - [HugChat](<https://github.com/Soulter/hugging-chat-api>)
    - [OpenAssistant/oasst-sft-6-llama-30b-xor](<https://huggingface.co/OpenAssistant/oasst-sft-6-llama-30b-xor>) LLM model

    💡 Note: No API key required!
    ''')

    dataset_path = st.selectbox(
        label='Which database do you want to use?',
        options=os.listdir('deeplake/')
    )
    if 'dataset_path' not in st.session_state:
        st.session_state.dataset_path = os.path.join('deeplake', dataset_path)

    add_vertical_space(5)
    st.write('Made with ❤️ by [Data Professor](<https://youtube.com/dataprofessor>)')

try:
    bot = initialize_bot(dataset_path=st.session_state.dataset_path)
except Exception as ex:
    st.error(ex)
    st.stop()

initialize_chat(st)

if question := st.chat_input():
    # Get and save the question
    st.session_state.messages.append({'role': 'user', 'content': question})
    st.chat_message('user').write(question)

    # Get an answer using question and the conversation history
    answer: str = bot.process(
        {
            'question': question,
        }
    )

    # Save the answer
    st.session_state.messages.append({'role': 'assistant', 'content': answer})
    st.chat_message('assistant').write(answer)
