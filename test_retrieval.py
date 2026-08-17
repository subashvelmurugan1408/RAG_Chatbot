import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Hugging Face embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load existing ChromaDB
vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
    collection_name="all_documents"
)

# Test question
query = "What is Python programming?"

print("\n" + "=" * 80)
print("TESTING CHROMADB RETRIEVAL")
print("=" * 80)

results = vector_store.similarity_search(
    query,
    k=5
)

print(f"\nQuery: {query}")
print(f"Retrieved chunks: {len(results)}")

for i, doc in enumerate(results, 1):

    print("\n" + "-" * 80)
    print(f"RESULT {i}")

    print("\nSOURCE:")
    print(doc.metadata.get("source"))

    print("\nCONTENT:")
    print(doc.page_content[:1000])