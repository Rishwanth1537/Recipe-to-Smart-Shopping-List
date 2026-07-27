import re

# Gemini 2.5 Flash's context window comfortably fits far more than this in
# a single request. This is a practical cutoff so that ordinary recipe
# transcripts (a few thousand words) are sent to Gemini in ONE request —
# chunking only kicks in for unusually long transcripts, per requirement #7.
SAFE_SINGLE_REQUEST_CHARS = 20000


def split_transcript(transcript, max_chars=SAFE_SINGLE_REQUEST_CHARS):
    """
    Split transcript into chunks no larger than max_chars.

    If the whole transcript already fits inside max_chars, this returns a
    single chunk containing the entire transcript — no unnecessary
    splitting, and no unnecessary loss of cross-sentence context.
    """

    transcript = transcript.replace("\n", " ")
    transcript = re.sub(r"\s+", " ", transcript).strip()

    if len(transcript) <= max_chars:
        return [transcript]

    sentences = re.split(r'(?<=[.!?])\s+', transcript)

    chunks = []

    current = ""

    for sentence in sentences:

        if len(current) + len(sentence) <= max_chars:

            current += sentence + " "

        else:

            chunks.append(current.strip())

            current = sentence + " "

    if current:

        chunks.append(current.strip())

    return chunks
