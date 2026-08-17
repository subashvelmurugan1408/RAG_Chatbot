from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def get_retriever():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma(
        persist_directory="./chroma_db",
        collection_name="all_documents",
        embedding_function=embeddings
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    return retriever


# Test retriever
if __name__ == "__main__":

    retriever = get_retriever()

    query = "What is a regular expression in Python?"

    docs = retriever.invoke(query)

    print("\n" + "=" * 80)
    print("RETRIEVAL TEST")
    print("=" * 80)

    print(f"\nQuery: {query}")
    print(f"Retrieved documents: {len(docs)}")

    for i, doc in enumerate(docs, 1):

        print("\n" + "-" * 80)
        print(f"RESULT {i}")

        print("SOURCE:")
        print(doc.metadata.get("source"))

        print("\nCONTENT:")
        print(doc.page_content[:1000])