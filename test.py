import openai
import streamlit as st
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit UI
st.title("Let's get this over with")
st.subheader("Ask a question")

# Collect user query and setup file uploader
question = st.text_input("Put your question here", placeholder="Put your text here")
uploaded_file = st.file_uploader("Choose a file to upload", type=["txt", "csv", "pdf", "docx"])
send_button = st.button("Send")

if send_button and question:
    with st.spinner("Processing..."):
        # Upload file if one was uploaded
        file_id = None
        if uploaded_file:
            file = openai.File.create(file=uploaded_file, purpose="assistants")
            file_id = file['id']

        # Create a message and attach file
        message_content = [{"type": "text", "text": {"value": question}}]
        if file_id:
            message_content.append({"type": "file", "file_id": file_id})

        # Create the thread and initial message
        thread = openai.Thread.create(messages=[{"role": "user", "content": message_content}])

        # Start a run using a specific assistant
        run = openai.ThreadRun.create(
            thread_id=thread.id,
            assistant_id="asst_lDlJUxCSuHNrmwQQhtuLAiGh"
        )

        # Poll for completion
        while True:
            run_status = openai.ThreadRun.retrieve(thread_id=thread.id, run_id=run.id)
            if run_status['status'] in ["completed", "failed", "cancelled"]:
                break
            time.sleep(5)

        # Retrieve messages when the run is completed
        if run_status['status'] == "completed":
            messages = openai.ThreadMessage.list(thread_id=thread.id)
            for msg in messages['data']:
                st.markdown(msg['content'][0]['text']['value'])
        else:
            st.error("Run failed or was cancelled.")
