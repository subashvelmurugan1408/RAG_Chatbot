import os
import chromadb
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()

# -----------------------------
# Configuration
# -----------------------------

CHROMA_PATH = "./chroma_db"
CHROMA_COLLECTION = "all_documents"

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv(
    "QDRANT_COLLECTION",
    "all_documents"
)

BATCH_SIZE = 100


# -----------------------------
# Check credentials
# -----------------------------

if not QDRANT_URL:
    raise ValueError("QDRANT_URL is missing from .env")

if not QDRANT_API_KEY:
    raise ValueError("QDRANT_API_KEY is missing from .env")


# -----------------------------
# Connect to ChromaDB
# -----------------------------

print("Connecting to ChromaDB...")

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

chroma_collection = chroma_client.get_collection(
    CHROMA_COLLECTION
)

total = chroma_collection.count()

print(f"✓ ChromaDB chunks: {total}")


# -----------------------------
# Connect to Qdrant
# -----------------------------

print("Connecting to Qdrant...")

qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

print("✓ Connected to Qdrant")


# -----------------------------
# Create Qdrant collection
# -----------------------------

existing_collections = [
    collection.name
    for collection in qdrant_client.get_collections().collections
]

if QDRANT_COLLECTION not in existing_collections:

    print(
        f"Creating collection: {QDRANT_COLLECTION}"
    )

    qdrant_client.create_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

    print("✓ Collection created")

else:

    print(
        f"✓ Collection already exists: "
        f"{QDRANT_COLLECTION}"
    )


# -----------------------------
# Migrate in batches
# -----------------------------

print("\nStarting migration...\n")

for offset in range(0, total, BATCH_SIZE):

    end = min(
        offset + BATCH_SIZE,
        total
    )

    print(
        f"Migrating {offset + 1}-{end} "
        f"of {total}..."
    )

    data = chroma_collection.get(
        include=[
            "embeddings",
            "documents",
            "metadatas"
        ],
        limit=BATCH_SIZE,
        offset=offset
    )

    points = []

    ids = data["ids"]
    embeddings = data["embeddings"]
    documents = data["documents"]
    metadatas = data["metadatas"]

    for i in range(len(ids)):

        payload = {
            "document": documents[i],
            "metadata": metadatas[i] or {}
        }

        point = PointStruct(
            id=ids[i],
            vector=embeddings[i],
            payload=payload
        )

        points.append(point)

    qdrant_client.upsert(
        collection_name=QDRANT_COLLECTION,
        points=points,
        wait=True
    )

print("\n====================================")
print("Migration completed successfully!")
print("====================================")


# -----------------------------
# Verify
# -----------------------------

info = qdrant_client.get_collection(
    QDRANT_COLLECTION
)

print(
    f"Qdrant vectors: "
    f"{info.points_count}"
)

print(
    f"Expected vectors: "
    f"{total}"
)

if info.points_count == total:
    print("✓ Migration verified successfully!")

else:
    print(
        "⚠️ Vector count does not match."
    )