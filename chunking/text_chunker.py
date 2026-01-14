from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
# this code converts your dicts -> LangChain Documents,
# preserves metadata and standardizes format for splitting
def to_langchain_docs(raw_docs):
    lc_docs = []

    for d in raw_docs:
        lc_docs.append(
            Document(
                page_content=d["text"],
                metadata={
                    "source":d["source"],
                    **d["metadata"]
                }
            )
        )
    return lc_docs
        
def chunk_documents(documents, chunk_size=500, overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap = overlap
    )
    return splitter.split_documents(documents)