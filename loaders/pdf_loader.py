from pypdf import PdfReader

def load_pdf(pdf_path):
    documents = []

    # PdfReader(pdf_path) -> opens PDF
    reader = PdfReader(pdf_path)
                             
                        #   enumerate(reader.pages) -> page by page iteration
    for page_number, page in enumerate(reader.pages):
                  # extract_text() -> raw text
        text = page.extract_text()

                #   text.strip() -> avoid empty pages
        if text and text.strip():
            documents.append({
                "text": text,
                "source": "pdf",
                "metadata": {
                    "page":page_number + 1
                }
            })
    return documents