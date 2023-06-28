import os
import streamlit as st
from arch_assist_service import Architect_service, does_database_exist

os.environ["OPENAI_API_KEY"] = st.secrets['apikey']

aa_service = Architect_service()
data_directory = 'data'

# set up needed folders
aa_service.setup_folders()

st.title("Architect AI Assistant")
st.subheader("Please let me know how I can help you.")

with st.sidebar:
    st.title('About')
    st.markdown('''
        The goal of the Architect AI Assistant is to provide a way
        for users to use natural language by typing their questions.
        
        -The Assistant will then use OpenAi's GPT-3.5 large language model to
         interpret the questions and provide the best answer.
        
        -This is a Proof Of Concept (POC) and is not production ready. 

     ''')
    st.title('Technology')
    st.markdown('''
        Developed by Jorge Duenas using:
        - [OpenAI GPT-3.5 API](https://openai.com/product)
        - [Streamlit.io](https://streamlit.io/)
        - [LangChain](https://python.langchain.com/en/latest/index.html)
        - [Python](https://www.python.org/)
        - [Anaconda](https://www.anaconda.com/)   
        - [Pycharm IDE](https://www.jetbrains.com/pycharm/) 
        - [Chroma Vector DB](https://docs.trychroma.com/)    

    ''')

if not does_database_exist():
    uploaded_file = st.file_uploader("Please upload file", type='pdf')
    if uploaded_file:
        with open(os.path.join(data_directory, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner('Please wait, while I read and learn the document ..'):
            aa_service.load_files_to_db()

if does_database_exist():
    user_input = st.text_area('Type in your question below and then click the Submit button.')
    if st.button("Submit", help='Please click Submit again if you want me to generate the answer again.'):
        if user_input:
            with st.spinner("Please wait, looking for the best answer."):
                returned_answer = aa_service.retrieve_data(user_input)
                print(f"docs = {returned_answer} ")
                st.write(returned_answer)
        else:
            st.warning('Please enter your question, before clicking the Submit button.')
