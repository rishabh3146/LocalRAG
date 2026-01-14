from loaders.pdf_loader import load_pdf
from loaders.youtube_loader import load_youtube
from chunking.youtube_merger import merge_youtube_chunks
from chunking.text_chunker import to_langchain_docs, chunk_documents
from embeddings.vector_store import build_vector_store, retrieve_chunks
from prompts.rag_prompts import build_rag_prompt
from llm.qa_llm import get_llm

def main():
    # 1. LOAD DATA
    pdf_docs = load_pdf("data/apjspeech.pdf")
    yt_raw = load_youtube("G3EB5E9-CY8")
    yt_docs = merge_youtube_chunks(yt_raw)

    all_docs = pdf_docs + yt_docs

    # 2. CHUNK
    lc_docs = to_langchain_docs(all_docs)
    chunks = chunk_documents(lc_docs)

    print(f"Total chunks going into vector store: {len(chunks)}")

    # 3. BUILD VECTOR STORE
    vector_store = build_vector_store(chunks)

    # 4. QUERY
    query = "What were the key messages of Abdul Kalam's speech?"
    retrieved_docs = retrieve_chunks(vector_store, query, k=4)

    print("\nRetrieved chunks:\n")
    for i, doc in enumerate(retrieved_docs):
        print(f"--- Result {i+1} ---")
        print(doc.page_content)
        print(doc.metadata)
        print()

    # 5. BUILD RAG PROMPT
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)
    prompt = build_rag_prompt(context, query)

    # 6. LLM ANSWER
    llm = get_llm()
    response = llm.invoke(prompt)

    print("\nFINAL ANSWER:\n")
    print(response)


if __name__ == "__main__":
    main()
