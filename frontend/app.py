import os

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
TIMEOUT = 120  # the agent may search the web, replies can take a while

ROLE_LABELS = {"user": "You", "assistant": "Verifier"}


def create_conversation() -> str:
    response = requests.post(f"{BACKEND_URL}/conversations", timeout=10)
    response.raise_for_status()
    return response.json()["id"]


def send_message(conversation_id: str, content: str) -> dict:
    response = requests.post(
        f"{BACKEND_URL}/conversations/{conversation_id}/messages",
        json={"content": content},
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def show_message(message: dict) -> None:
    st.markdown(f"**{ROLE_LABELS[message['role']]}:** {message['content']}")
    verification = message.get("verification")
    if verification:
        st.markdown(
            f"Verdict: **{verification['verdict']}** "
            f"(confidence {verification['confidence']:.0%})  \n"
            f"{verification['explanation']}"
        )
        if verification["sources"]:
            st.markdown(
                "Sources:\n"
                + "\n".join(
                    f"- [{s.get('title') or s['url']}]({s['url']})"
                    for s in verification["sources"]
                )
            )
    st.divider()


st.set_page_config(page_title="Fake News Verifier")
st.title("Fake News Verifier")

if "conversation_id" not in st.session_state:
    try:
        st.session_state.conversation_id = create_conversation()
    except requests.RequestException as exc:
        st.error(f"Can't reach the backend at {BACKEND_URL}: {exc}")
        st.stop()
    st.session_state.messages = []

col_id, col_button = st.columns([3, 1])
col_id.text(f"Conversation {st.session_state.conversation_id}")
if col_button.button("New conversation"):
    del st.session_state.conversation_id
    st.rerun()

for message in st.session_state.messages:
    show_message(message)

if prompt := st.chat_input("Claim or news to verify"):
    user_message = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_message)
    show_message(user_message)

    with st.spinner("Verifying..."):
        try:
            reply = send_message(st.session_state.conversation_id, prompt)
        except requests.RequestException as exc:
            st.error(f"Request failed: {exc}")
            st.stop()

    st.session_state.messages.append(reply)
    show_message(reply)
