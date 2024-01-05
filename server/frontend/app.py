import os
import time
import random
import logging

import streamlit as st

from socket_client import ChatClient
from api_handler import send_file_to_api

server_address = os.environ.get("CHAT_HOST") or "localhost"
server_port = int(os.environ.get("CHAT_PORT") or 12345)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


def write_message(message, role):
    st.session_state.messages.append({"role": role, "content": message})
    message_placeholder = st.empty()
    full_response = ""
    for chunk in message.split():
        full_response += chunk + " "
        time.sleep(0.09)
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)


def main():
    chat_client = ChatClient(server_address, server_port)
    st.set_page_config(
        page_title="GenAI Partners",
        page_icon=":robot_face:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    with st.sidebar:
        st.header("Options")
        uploaded_file = st.file_uploader("Load custom file")

        def upload_file(uploaded_file):
            server_response = send_file_to_api(uploaded_file)
            with st.sidebar:
                with st.spinner("Loading..."):
                    if server_response:
                        time.sleep(0.1)
                st.success("Done!")
                uploaded_file = None

        st.button(
            "Upload File",
            on_click=upload_file,
            args=(uploaded_file,),
            disabled=True if uploaded_file is None else False,
        )

        st.markdown("---")
        st.write(
            """

            App created by [German Grandas](https://github.com/german-grandas) using [Streamlit](https://streamlit.io/)🎈

            """
        )
    st.markdown(
        "<h3 style='text-align: center; font-size:56px;'<p>&#129302;</p></h3>",
        unsafe_allow_html=True,
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask Something!"):
        if chat_client.connected:
            message = f"query: {prompt}"
            chat_client.send_message(message)

        with st.chat_message("user"):
            write_message(prompt, "user")

    if len(st.session_state.messages) < 1:
        with st.chat_message("assistant"):
            assistant_response = random.choice(
                [
                    "Hello there! How can I assist you today?",
                    "Hi, human! Is there anything I can help you with?",
                    "Do you need help?",
                ]
            )
            write_message(assistant_response, "assistant")

    with st.chat_message("assistant"):
        while True:
            if chat_client.received_message:
                write_message(chat_client.received_message, "assistant")
                chat_client.received_message = None


if __name__ == "__main__":
    main()
