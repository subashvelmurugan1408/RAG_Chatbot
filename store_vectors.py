from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from load_document import load_documents, split_documents

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create vector database
def create_vector_store():
    documents = load_documents()
    chunks = split_documents(documents)
    
    # Create Chroma vector store
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"  # Save locally
    )
    
    print(f"Vector store created with {len(chunks)} chunks")
    return vector_store

# Test search
if __name__ == "__main__":
    vector_store = create_vector_store()
    
    # Test retrieval
    query = "What is machine learning?"
    results = vector_store.similarity_search(query, k=2)
    
    print(f"\nQuery: {query}")
    print(f"\nTop {len(results)} results:")
    for i, doc in enumerate(results, 1):
        print(f"\n{i}. {doc.page_content[:200]}...")