def build_rag_prompt(context, question):
    prompt = f"""
You are an assistant answering questions ONLY using the provided context.

Rules:
- Use ONLY the information in the context.
- Do NOT use prior knowledge.
- If the answer is not present in the context, say: "The answer is not found in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""
    return prompt
