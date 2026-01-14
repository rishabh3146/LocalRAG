from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma

def build_vector_store(chunks):
    """
    Takes LangChain Document chunks
    Returns a Chroma vector store
    """
    embeddings = HuggingFaceBgeEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    return vector_store

def retrieve_chunks(vector_store, query, k=4):
    """
    Takes a query string
    Return top-k similar Document chunks
    """
    return vector_store.similarity_search(query, k=k)