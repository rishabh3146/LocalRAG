import streamlit as st

from loaders.pdf_loader import load_pdf
from loaders.youtube_loader import load_youtube
from chunking.youtube_merger import merge_youtube_chunks
from chunking.text_chunker import to_langchain_docs, chunk_documents
from embeddings.vector_store import build_vector_store, retrieve_chunks
from prompts.rag_prompts import build_rag_prompt
from llm.qa_llm import get_llm


st.set_page_config(page_title="Local RAG App", layout="wide")

st.title("📄🔍 Local RAG Question Answering App")

st.write(
    "Ask questions over PDFs and YouTube videos using a **fully local RAG system**."
)

# ---- Inputs ----
pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])
youtube_id = st.text_input("YouTube Video ID (optional)")
query = st.text_input("Ask a question")

if st.button("Run RAG"):

    if not pdf_file and not youtube_id:
        st.error("Please upload a PDF or provide a YouTube ID.")
        st.stop()

    with st.spinner("Processing documents..."):

        all_docs = []

        # ---- PDF ----
        if pdf_file:
            with open("temp.pdf", "wb") as f:
                f.write(pdf_file.read())

            pdf_docs = load_pdf("temp.pdf")
            all_docs.extend(pdf_docs)

        # ---- YouTube ----
        if youtube_id.strip():
            yt_raw = load_youtube(youtube_id.strip())
            yt_docs = merge_youtube_chunks(yt_raw)
            all_docs.extend(yt_docs)

        # ---- Chunking ----
        lc_docs = to_langchain_docs(all_docs)
        chunks = chunk_documents(lc_docs)

        # ---- Vector Store ----
        vector_store = build_vector_store(chunks)

    if not query:
        st.warning("Enter a question.")
        st.stop()

    with st.spinner("Retrieving and generating answer..."):

        retrieved_docs = retrieve_chunks(vector_store, query, k=4)

        # ---- Show retrieved chunks ----
        st.subheader("🔎 Retrieved Context")
        for i, doc in enumerate(retrieved_docs):
            st.markdown(f"**Chunk {i+1}**")
            st.write(doc.page_content)
            st.caption(doc.metadata)

        # ---- RAG Prompt ----
        context = "\n\n".join(doc.page_content for doc in retrieved_docs)
        prompt = build_rag_prompt(context, query)

        llm = get_llm()
        answer = llm.invoke(prompt)

    st.subheader("✅ Final Answer")
    st.write(answer)
