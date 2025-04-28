from chunking import chunk_text
from embedding import embed_texts

text = """
My printer shows 'fiscal error' when I try to print any document. I've tried restarting it but it doesn’t help.
This started after a recent Windows update.
"""

chunks = chunk_text(text)
vectors = embed_texts(chunks)

print("Chunks:")
for i, ch in enumerate(chunks):
    print(f"{i+1}.", ch[:100])

print("\nVectors:")
print(vectors[0][:5], "...")  # Print first 5 dims for preview
