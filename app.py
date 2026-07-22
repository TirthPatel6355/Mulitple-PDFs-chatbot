# import streamlit as st 
# from dotenv import load_dotenv
# from PyPDF2 import PdfReader
# from langchain_text_splitters import CharacterTextSplitter
# # from langchain_openai import OpenAIEmbeddings
# from langchain.embeddings import HuggingFaceInstructEmbeddings
# # from langchain_huggingface import HuggingFaceEmbeddings
# # from langchain.memory import ConversationBufferMemory
# # from langchain.memory import ConversationBufferMemory
# # from langchain.chains import ConversationalRetrievalChain
# # from langchain.chat_models import ChatOpenAI
# from langchain_openai import ChatOpenAI
# from htmlTemplates import css, bot_template, user_template
# from langchain_community.vectorstores import FAISS



# def get_pdf_text(pdf_docs):
#     text = ""
#     for pdf in pdf_docs:
#         pdf_reader = PdfReader(pdf)
#         for page in pdf_reader.pages:
#             text += page.extract_text()
#     return text

# def get_text_chunks(raw_text):
#     text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200,length_function=len)
#     return text_splitter.split_text(raw_text)

# def get_vectorstore(text_chunks):
#     # embeddings = OpenAIEmbeddings()
#     embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl", model_kwargs={"device": "cpu"})
#     # embeddings = HuggingFaceEmbeddings(
#     # model_name="sentence-transformers/all-MiniLM-L6-v2"
#     # )
#     vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
#     return vectorstore
import os
import streamlit as st 
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from sympy import use
from htmlTemplates import css, bot_template, user_template
from langchain_community.vectorstores import FAISS
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
    return text_splitter.split_text(raw_text)

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    # llm = ChatOpenAI()
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.5, groq_api_key=os.getenv("GROQ_API_KEY"))
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory= memory
    )
    return conversation

def handle_userinput(user_question):
    if st.session_state.conversation is None:
        st.warning("⚠️ Please upload and process your PDFs first before asking a question.")
        return
    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response["chat_history"]

    for i , message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    

def main(): 
    load_dotenv()
    st.set_page_config(page_title="Chat with Multiple PDFs", page_icon=":books:", layout="wide")

    st.write(css, unsafe_allow_html=True)
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    

    st.header("Chat with Multiple PDFs :books:")
    user_question = st.chat_input("Ask a question about your documents...")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    if user_question:
       handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Upload your PDFs")
        pdf_docs = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
        if st.button("Process PDFs"):
            for pdf in pdf_docs:
                with st.spinner("Processing..."):
                    # Get PDF text
                    raw_text = get_pdf_text(pdf_docs)

                    #get the text chunks
                    text_chunks = get_text_chunks(raw_text)

                    # create vector store
                    vectorstore = get_vectorstore(text_chunks)
                    # print("Vector store created successfully!")

                    #  create conversation chain
                    st.session_state.conversation = get_conversation_chain(vectorstore)
    

if __name__ == '__main__':
    main()