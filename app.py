# streamlit_app.py
import os
import io
import time
import requests
import subprocess
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


API_BASE = f"http://backend:{os.getenv('BACKEND_PORT')}"


def wait_for_backend(retries=10, delay=2):
    for _ in range(retries):
        try:
            r = requests.get(f"{API_BASE}/health")
            if r.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(delay)
    return False

if not wait_for_backend():
    st.error("Backend service is not available. Please try again later.")
    st.stop()


if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("📁 Document Ingestion")
    uploaded_files = st.file_uploader(
        "Choose one or more files",
        accept_multiple_files=True,
        key="uploader"
    )
    if st.button("Upload & Update DB"):
        if not uploaded_files:
            st.warning("Please select at least one file first.")
            st.stop()

        files_for_api = [
            ("files", (f.name, f.getvalue(), f.type))
            for f in uploaded_files
        ]
        with st.spinner("Uploading files..."):
            r = requests.post(
                f"{API_BASE}/upload_files/",
                files=files_for_api
            )
            if r.status_code != 200:
                st.error("Upload failed: " + r.json().get("message", str(r)))
                st.stop()
            st.success(r.json()["message"])

        with st.spinner("Ingesting documents into vector DB..."):
            r = requests.post(f"{API_BASE}/update_database/")
            if r.status_code != 200:
                st.error("Update failed: " + r.json().get("message", str(r)))
            else:
                st.success(r.json()["message"])


st.title("📚 Chat with Documents")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                with requests.post(
                    f"{API_BASE}/ask_stream",
                    json={"question": prompt},
                    stream=True,
                    headers={"Accept": "text/event-stream"}
                ) as r:
                    r.raise_for_status()
                    for chunk in r.iter_lines(delimiter=b"\n"):
                        if chunk:
                            decoded = chunk.decode("utf-8").strip()
                            if decoded.startswith("data: "):
                                token = decoded.removeprefix("data: ")
                                full_response += token
                                message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
            except Exception as e:
                st.error("Streaming error: " + str(e))

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )

if __name__ == "__main__":
    frontend_port = os.getenv("FRONTEND_PORT", "9011")
    subprocess.run(["streamlit", "run", "app.py", "--server.port=" + frontend_port, "--server.enableCORS=false"])