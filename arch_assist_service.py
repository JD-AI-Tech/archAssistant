from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from  langchain.llms import OpenAI

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from file_utility import create_directory, check_file_exists


def does_database_exist():
    db_file_name = "db/chroma-collections.parquet"
    exists = check_file_exists(db_file_name)
    print(f"!!!!!!!!!!does_database_exist() about to return db_exists = {exists}")
    return exists


class Architect_service:

    vectordb = []


    def load_files_to_db(self):
        db_exists = does_database_exist()
        if db_exists:
            return

        print("jddebug !!!!!!!!!!!!!!!!!!!! in load_files_to_db")
        loader = DirectoryLoader('./data/', glob = "./*.pdf", loader_cls=PyPDFLoader, show_progress=True)
        documents = loader.load()
        print(f"load_text_files loaded documents!!!!!!!!!!!!!!!!!!!!!!!!!")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        text_files = text_splitter.split_documents(documents)
        print(f"lenght of documents = {len(text_files)}")
        Architect_service.create_chromadb(text_files, 'db')


    def create_chromadb (text_files, db_path):
        print("jddebug ***** in create_chromadb")
        # do nothing if DB already exists
        db_exists = does_database_exist()
        if db_exists:
            return

        embedding = OpenAIEmbeddings()
        loc_vectordb = Chroma.from_documents(documents=text_files,
                                             embedding=embedding,
                                             persist_directory=db_path)

        print("jddebug ***** in create_chromadb after creating loc_vectordb")
        # persist to file system
        loc_vectordb.persist()
        print("jddebug ***** in create_chromadb presisted loc_vectordb")
        loc_vectordb = None

    def retrieve_data(self, query):
        print(f"retrieve_data() query = {query}")
        db_directory = "db"
        embedding = OpenAIEmbeddings()
        print(f"retrieve_data() after OpenAIEmbeddings() ")
        vectordb = Chroma(persist_directory=db_directory, embedding_function=embedding)

        print(f"retrieve_data() after creating vectordb ")
        retriever = vectordb.as_retriever(search_kwargs={"k": 3})
        print(f"retrieve_data() after as_retriever() ")

        # create the chain to answer questions
        qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(),
                                               chain_type="stuff",
                                               retriever=retriever)
        lms_response = qa_chain(query)
        answer = lms_response["result"]
        return answer

    def instantiate_db(self):
        if not self.vectordb:
            print(f" in instantiate_db vector db does not exist")
            db_directory = "db"
            embedding = OpenAIEmbeddings()
            print(f"retrieve_data() after OpenAIEmbeddings() ")
            vectordb = Chroma(persist_directory=db_directory, embedding_function=embedding)
        else:
            print(f" in instantiate_db vector db does not exist")

    def setup_folders(self):
        print("in setup folders")
        data_directory = "data"
        create_directory(data_directory, True)
        db_directory = "db"
        # delete_folder(db_directory)
        create_directory(db_directory, True)
        log_directory = "log"
        create_directory(log_directory, True)

