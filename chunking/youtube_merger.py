def merge_youtube_chunks(yt_docs, max_chars=800):
    merged_docs = []
    buffer_text = ""
    buffer_start = None

    for d in yt_docs:
        if buffer_start is None:
            buffer_start = d["metadata"]["start"]

        buffer_text+= " " + d["text"]

        if len(buffer_text) >= max_chars:
            merged_docs.append({
                "text": buffer_text.strip(),
                "source": "youtube",
                "metadata": {
                    "start": buffer_start
                }
            })
            buffer_text = ""
            buffer_start = None

    if buffer_text.strip():
        merged_docs.append({
            "text": buffer_text.strip(),
            "source": "youtube",
            "metadata": {
                "start": buffer_start
            }
        })

    return merged_docs
