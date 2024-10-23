import openai
import streamlit as st
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API key
api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = api_key

# Streamlit UI
st.title("Let's get this over with")
st.subheader("Ask a question")

question = st.text_input("Put your question here", placeholder="Put your text here")
uploaded_file = st.file_uploader("Choose a file to upload", type=["txt", "csv", "pdf", "docx"])
send_button = st.button("Send")

if send_button and question:
    with st.spinner("Starting work..."):

        file_id = None
        if uploaded_file is not None:
            # Assume there's a method to upload the file and get a file ID
            file_response = openai.File.create(file=uploaded_file)
            file_id = file_response['id']
        
        # Create a new message with or without a file ID
        content = question + (f"\nAttached file ID: {file_id}" if file_id else "")
        
        # Send the message to the assistant
        message_response = openai.beta.assistant.create.message(
            assistant_id="asst_lDlJUxCSuHNrmwQQhtuLAiGh",
            thread_id="thread_qAQx7zSPmINgZnR2ocdMELYf",
            message={
                "role": "user",
                "content": content
            }
        )

        # Poll for the completion of the assistant's response
        run = openai.beta.assistant.run.create(
            assistant_id="asst_lDlJUxCSuHNrmwQQhtuLAiGh",
            message_id=message_response['id']
        )

        while run['status'] != "completed":
            time.sleep(5)
            run = openai.beta.assistant.run.retrieve(run_id=run['id'])

        # Display the assistant's response
        response_message = openai.beta.assistant.messages.retrieve(
            message_id=run['final_message_id']
        )
        st.markdown(response_message['content'])
