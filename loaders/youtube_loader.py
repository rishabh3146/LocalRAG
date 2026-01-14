from youtube_transcript_api import YouTubeTranscriptApi

def load_youtube(video_id):
    documents = []
    transcript = YouTubeTranscriptApi().fetch(video_id)

    for chunk in transcript:
        documents.append({
            "text": chunk.text,
            "source": "youtube",
            "metadata": {"start": chunk.start}
        })
    return documents
        
