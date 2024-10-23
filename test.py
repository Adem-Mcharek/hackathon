import openai
import streamlit as st
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create an OpenAI client with your API key
api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = api_key

# Create the title and subheader for the Streamlit page
st.title("Let's get this over with")
st.subheader("Ask a question")

thread_id = "thread_qAQx7zSPmINgZnR2ocdMELYf"

question = st.text_input("Put your question here", placeholder="Put your text here")
uploaded_file = st.file_uploader("Choose a file to upload", type=["txt", "csv", "pdf", "docx"])
send_button = st.button("Send")

# Check if send button is clicked
if send_button and question:
    with st.spinner("Starting work..."):
        
        file_id = None
        if uploaded_file is not None:
            # Pass the file to the API and get its unique file ID
            file_response = openai.File.create(file=uploaded_file)
            file_id = file_response['id']
        
        # Create a new thread with a message, attaching the uploaded file's ID
        additional_content = f" - File ID: {file_id}" if file_id else ""
        message_content = question + additional_content

        message = openai.ThreadMessage.create(
            thread_id=thread_id, sender_type="user", content=message_content
        )

        # Create a run with the new thread
        run = openai.ThreadRun.create(thread_id=thread_id, assistant_id=assistant.id)

        # Check periodically whether the run is done
        while run.status != "completed":
            time.sleep(5)
            run = openai.ThreadRun.retrieve(thread_id=thread_id, run_id=run.id)

        # Retrieve messages once the run is complete
        messages = openai.ThreadMessage.list(thread_id=thread_id)
        for msg in messages['data']:
            st.markdown(msg['content'])

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



