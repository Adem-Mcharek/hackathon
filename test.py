import openai
import streamlit as st
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit UI
st.title("Let's get this over with")
st.subheader("Ask a question")

# Collect user input and setup file uploader
question = st.text_input("Put your question here", placeholder="Put your text here")
uploaded_file = st.file_uploader("Choose a file to upload", type=["txt", "csv", "pdf", "docx"])
send_button = st.button("Send")

if send_button and question:
    with st.spinner("Processing..."):
        # Upload file if one is provided
        if uploaded_file is not None:
            file_response = openai.File.create(file=uploaded_file, purpose="assistants")
            file_id = file_response['id']
        else:
            file_id = None

        # Establish initial message setup
        initial_message = [{
            "role": "user",
            "content": question
        }]
        
        # Initialize the thread with messages
        thread_response = openai.Thread.create(messages=initial_message)
        thread_id = thread_response['id']

        # Attach the file if uploaded
        if file_id:
            openai.ThreadMessage.create(
                thread_id=thread_id,
                role="user",
                content=f"Attached file: {uploaded_file.name}",
                file_ids=[file_id]
            )

        # Start a run using the assistant
        run_response = openai.ThreadRun.create(
            thread_id=thread_id,
            assistant_id="asst_lDlJUxCSuHNrmwQQhtuLAiGh"
        )
        run_id = run_response['id']

        # Poll for completion
        while True:
            run_status = openai.ThreadRun.retrieve(thread_id=thread_id, run_id=run_id)
            if run_status['status'] in ["completed", "failed", "cancelled"]:
                break
            time.sleep(5)

        # Retrieve messages when the run is completed
        if run_status['status'] == "completed":
            messages = openai.ThreadMessage.list(thread_id=thread_id)
            for msg in messages['data']:
                if msg['content'][0]['type'] == 'text':
                    st.markdown(msg['content'][0]['text']['value'])
        else:
            st.error("Run failed or was cancelled.")
