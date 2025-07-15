import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()


def prepare_rag_pipeline():
    # Load embedding model
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Load vector store
    vectordb = Chroma(
        persist_directory="./chroma_storage",
        embedding_function=embedding
    )

    # Retriever
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    # LLM via Groq
    groq_api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama3-8b-8192"
    )

    # Setup Retrieval QA
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain

rag_pipeline = prepare_rag_pipeline()

def answer_query(query):
    return rag_pipeline.run(query)
