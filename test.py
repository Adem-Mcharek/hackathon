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
        message_response = openai.Assistant.create_message(
            assistant_id="asst_lDlJUxCSuHNrmwQQhtuLAiGh",
            thread_id="thread_qAQx7zSPmINgZnR2ocdMELYf",
            message={
                "role": "user",
                "content": content
            }
        )

        # Poll for the completion of the assistant's response
        run = openai.Assistant.create_run(
            assistant_id="asst_lDlJUxCSuHNrmwQQhtuLAiGh",
            message_id=message_response['id']
        )

        while run['status'] != "completed":
            time.sleep(5)
            run = openai.Assistant.retrieve_run(run_id=run['id'])

        # Display the assistant's response
        response_message = openai.Assistant.retrieve_message(
            message_id=run['final_message_id']
        )
        st.markdown(response_message['content'])
# import openai
# import streamlit as st
# import os
# import time
# import openai
# from dotenv import load_dotenv




# # Create an OpenAI client with your API key
# openai_client = openai.Client(api_key=st.secrets["OPENAI_API_KEY"])


# # Retrieve the assistant you want to use
# assistant = openai_client.beta.assistants.retrieve(
#     "asst_lDlJUxCSuHNrmwQQhtuLAiGh"
# )

# # Create the title and subheader for the Streamlit page
# st.title("Let's get this over with")
# st.subheader("ask a question")



# thread = "thread_qAQx7zSPmINgZnR2ocdMELYf"
# placeholder ="placeholder"

# question = st.text_input(
#     "put your question here",
#     placeholder ="put your text here",
   
#     )
# send_button = st.button("Send")

# # Check if send button is clicked
# if send_button and question:
#     with st.status("Starting work...", expanded=True) as status_box:
       

#             # Create a new thread with a message that has the uploaded file's ID
#         openai_client.beta.threads.messages.create(
#         thread,
#         role = "user",
#         content = question
#         )

#         # Create a run with the new thread
#         run = openai_client.beta.threads.runs.create(
#             thread_id=thread,
#             assistant_id=assistant.id,
#             )

#         # Check periodically whether the run is done, and update the status
#         while run.status != "completed":
#             time.sleep(5)
#             status_box.update(label=f"{run.status}...", state="running")    
#             run = openai_client.beta.threads.runs.retrieve(
#                 thread_id=thread, run_id=run.id
#             )

#         # Once the run is complete, update the status box and show the content
#         status_box.update(label="Complete", state="complete", expanded=True)
#         messages = openai_client.beta.threads.messages.list(
#             thread_id=thread
#         )
#         st.markdown(messages.data[0].content[0].text.value)



