from langchain_huggingface import HuggingFaceEmbeddings
from load_document import load_documents, split_documents

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Test embedding
if __name__ == "__main__":
    documents = load_documents()
    chunks = split_documents(documents)
    
    # Create embedding for first chunk
    text = chunks[0].page_content
    embedding = embeddings.embed_query(text)
    
    print(f"Text: {text[:100]}...")
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")