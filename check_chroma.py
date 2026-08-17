import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection("all_documents")

data = collection.get(
    include=["metadatas"]
)

sources = set()

for metadata in data["metadatas"]:
    if metadata:
        source = metadata.get("source")
        if source:
            sources.add(source)

print("\n" + "=" * 80)
print("SOURCES INSIDE python_docs")
print("=" * 80)

for source in sorted(sources):
    print(source)

print("\n" + "=" * 80)
print("Total unique source files:", len(sources))
print("Total chunks:", collection.count())
print("=" * 80)