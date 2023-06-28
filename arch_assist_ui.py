import os
import streamlit as st
from arch_assist_service import Architect_service, does_database_exist

os.environ["OPENAI_API_KEY"] = st.secrets['apikey']

aa_service = Architect_service()
data_directory = 'data'
# db_file_name = './db/chroma-collections.parquet'
# set up needed folders
aa_service.setup_folders()

st.title("Architect AI Assistant")
st.subheader("Artificial AI assistant for Architect")

if not does_database_exist():
    uploaded_file = st.file_uploader("Please upload file", type='pdf')
    if uploaded_file:
        with open(os.path.join(data_directory, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner('Please wait, while I read and learn the document ..'):
            aa_service.load_files_to_db()

if does_database_exist():
    user_input = st.text_area('What can I help you with?')
    if st.button("Submit", help='Click Submit after entering your question.'):
        if user_input:
            with st.spinner("Please wait, looking for the best answer."):
                returned_answer = aa_service.retrieve_data(user_input)
                print(f"docs = {returned_answer} ")
                st.write(returned_answer)
        else:
            st.warning('Please enter your question, before clicking the Submit button.')
