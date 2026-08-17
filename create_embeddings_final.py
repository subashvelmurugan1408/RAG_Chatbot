"""
Create Embeddings for ALL Documents
====================================

Loads every supported document from:

    documents/

Supported:
    .pdf
    .txt
    .md
    .markdown
    .py

Pipeline:

    Documents
        ↓
    Load
        ↓
    Split into chunks
        ↓
    Hugging Face embeddings
        ↓
    ChromaDB

ChromaDB:
    ./chroma_db

Collection:
    all_documents
"""

import sys
from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_chroma import Chroma


# ============================================================================
# CONFIGURATION
# ============================================================================

DOCUMENTS_PATH = Path("documents")

CHROMA_PATH = "./chroma_db"

COLLECTION_NAME = "all_documents"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".md",
    ".markdown",
    ".py"
}

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


# ============================================================================
# HEADER
# ============================================================================

print("\n" + "=" * 80)
print("ALL DOCUMENTS → HUGGING FACE EMBEDDINGS → CHROMADB")
print("=" * 80)

print(f"\n📁 Documents path : {DOCUMENTS_PATH}")
print(f"📦 ChromaDB path  : {CHROMA_PATH}")
print(f"🗂️ Collection      : {COLLECTION_NAME}")
print(f"🤖 Embedding model : {EMBEDDING_MODEL}")


# ============================================================================
# CHECK DOCUMENTS FOLDER
# ============================================================================

if not DOCUMENTS_PATH.exists():

    print(
        f"\n❌ ERROR: '{DOCUMENTS_PATH}' folder was not found."
    )

    print(
        "\nMake sure you are running this command from:"
    )

    print(
        "C:\\Users\\subas\\OneDrive\\Desktop\\rag_project"
    )

    sys.exit(1)


# ============================================================================
# STEP 1 — FIND DOCUMENTS
# ============================================================================

print("\n" + "=" * 80)
print("STEP 1: FINDING DOCUMENTS")
print("=" * 80)

files = []

for file_path in DOCUMENTS_PATH.rglob("*"):

    if not file_path.is_file():
        continue

    extension = file_path.suffix.lower()

    if extension in SUPPORTED_EXTENSIONS:
        files.append(file_path)


print(f"\n✓ Supported files found: {len(files)}")


# ============================================================================
# SHOW FILE TYPE COUNTS
# ============================================================================

file_type_counts = {}

for file_path in files:

    extension = file_path.suffix.lower()

    file_type_counts[extension] = (
        file_type_counts.get(extension, 0) + 1
    )


print("\nFile types:")

for extension, count in sorted(file_type_counts.items()):

    print(f"  {extension:10} : {count}")


# ============================================================================
# STEP 2 — LOAD DOCUMENTS
# ============================================================================

print("\n" + "=" * 80)
print("STEP 2: LOADING DOCUMENTS")
print("=" * 80)

all_documents = []

loaded_files = []

failed_files = []


for index, file_path in enumerate(files, 1):

    print(
        f"\n[{index}/{len(files)}] Loading: {file_path}"
    )

    try:

        extension = file_path.suffix.lower()


        # ------------------------------------------------------------
        # PDF
        # ------------------------------------------------------------

        if extension == ".pdf":

            loader = PyPDFLoader(
                str(file_path)
            )

            documents = loader.load()


        # ------------------------------------------------------------
        # TXT / MD / PY
        # ------------------------------------------------------------

        else:

            loader = TextLoader(
                str(file_path),
                encoding="utf-8",
                autodetect_encoding=True
            )

            documents = loader.load()


        # ------------------------------------------------------------
        # Add documents
        # ------------------------------------------------------------

        all_documents.extend(documents)

        loaded_files.append(file_path)

        print(
            f"    ✓ Loaded {len(documents)} document/page(s)"
        )


    except Exception as e:

        failed_files.append(
            (file_path, str(e))
        )

        print(
            f"    ⚠️ SKIPPED: {e}"
        )


# ============================================================================
# LOADING SUMMARY
# ============================================================================

print("\n" + "-" * 80)

print(
    f"Files found       : {len(files)}"
)

print(
    f"Files loaded      : {len(loaded_files)}"
)

print(
    f"Files skipped     : {len(failed_files)}"
)

print(
    f"Documents/pages   : {len(all_documents)}"
)

print("-" * 80)


if not all_documents:

    print(
        "\n❌ ERROR: No documents were successfully loaded."
    )

    sys.exit(1)


# ============================================================================
# STEP 3 — SPLIT DOCUMENTS
# ============================================================================

print("\n" + "=" * 80)
print("STEP 3: SPLITTING DOCUMENTS INTO CHUNKS")
print("=" * 80)

print(
    f"\nChunk size    : {CHUNK_SIZE}"
)

print(
    f"Chunk overlap : {CHUNK_OVERLAP}"
)


text_splitter = RecursiveCharacterTextSplitter(

    chunk_size=CHUNK_SIZE,

    chunk_overlap=CHUNK_OVERLAP
)


chunks = text_splitter.split_documents(
    all_documents
)


print(
    f"\n✓ Created {len(chunks)} chunks"
)


if not chunks:

    print(
        "\n❌ ERROR: No chunks were created."
    )

    sys.exit(1)


# ============================================================================
# STEP 4 — INITIALIZE HUGGING FACE EMBEDDINGS
# ============================================================================

print("\n" + "=" * 80)
print("STEP 4: INITIALIZING HUGGING FACE EMBEDDINGS")
print("=" * 80)

print(
    f"\nModel: {EMBEDDING_MODEL}"
)

print(
    "\n⏳ Loading embedding model..."
)

try:

    embeddings = HuggingFaceEmbeddings(

        model_name=EMBEDDING_MODEL
    )

    print(
        "✓ Hugging Face embedding model loaded"
    )


except Exception as e:

    print(
        f"\n❌ ERROR loading embedding model: {e}"
    )

    sys.exit(1)


# ============================================================================
# STEP 5 — CREATE CHROMADB
# ============================================================================

print("\n" + "=" * 80)
print("STEP 5: CREATING CHROMADB")
print("=" * 80)

print(
    f"\nDatabase : {CHROMA_PATH}"
)

print(
    f"Collection : {COLLECTION_NAME}"
)

print(
    f"Chunks to embed : {len(chunks)}"
)

print(
    "\n⏳ Creating embeddings..."
)

print(
    "This may take some time depending on the number of documents."
)


try:

    vector_store = Chroma.from_documents(

        documents=chunks,

        embedding=embeddings,

        persist_directory=CHROMA_PATH,

        collection_name=COLLECTION_NAME
    )


    print(
        "\n✓ ChromaDB created successfully!"
    )

    print(
        f"✓ Database location: {CHROMA_PATH}"
    )

    print(
        f"✓ Collection: {COLLECTION_NAME}"
    )

    print(
        f"✓ Chunks indexed: {len(chunks)}"
    )


except Exception as e:

    print(
        f"\n❌ ERROR creating ChromaDB: {e}"
    )

    sys.exit(1)


# ============================================================================
# STEP 6 — VERIFY DATABASE
# ============================================================================

print("\n" + "=" * 80)
print("STEP 6: VERIFYING CHROMADB")
print("=" * 80)


try:

    collection = vector_store._collection

    total_chunks = collection.count()

    print(
        f"\n✓ ChromaDB contains {total_chunks} chunks"
    )


    # ------------------------------------------------------------
    # Get metadata
    # ------------------------------------------------------------

    data = collection.get(
        include=["metadatas"]
    )


    sources = set()


    for metadata in data["metadatas"]:

        if metadata:

            source = metadata.get(
                "source"
            )

            if source:
                sources.add(source)


    print(
        f"✓ Unique source files: {len(sources)}"
    )


except Exception as e:

    print(
        f"\n⚠️ Could not verify database: {e}"
    )


# ============================================================================
# STEP 7 — TEST RETRIEVAL
# ============================================================================

print("\n" + "=" * 80)
print("STEP 7: TESTING RETRIEVAL")
print("=" * 80)


test_questions = [

    "What is Python?",

    "What is machine learning?",

    "What is Retrieval Augmented Generation?",

    "What is a transformer?",

    "What are regular expressions in Python?"
]


for question in test_questions:

    print(
        f"\n🔎 Query: {question}"
    )

    try:

        results = vector_store.similarity_search(
            question,
            k=3
        )


        for i, document in enumerate(
            results,
            1
        ):

            source = document.metadata.get(
                "source",
                "Unknown"
            )


            preview = (
                document.page_content
                .replace("\n", " ")
                [:150]
            )


            print(
                f"   {i}. {source}"
            )

            print(
                f"      {preview}..."
            )


    except Exception as e:

        print(
            f"   ⚠️ Retrieval error: {e}"
        )


# ============================================================================
# STEP 8 — FAILED FILES
# ============================================================================

if failed_files:

    print("\n" + "=" * 80)
    print("SKIPPED / FAILED FILES")
    print("=" * 80)

    for file_path, error in failed_files:

        print(
            f"\n⚠️ {file_path}"
        )

        print(
            f"   Reason: {error}"
        )


# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("✅ ALL DOCUMENTS EMBEDDING COMPLETE")
print("=" * 80)

print(
    f"\n📁 Files found       : {len(files)}"
)

print(
    f"📄 Files loaded      : {len(loaded_files)}"
)

print(
    f"⚠️ Files skipped     : {len(failed_files)}"
)

print(
    f"📦 Chunks created    : {len(chunks)}"
)

print(
    f"🗃️ ChromaDB          : {CHROMA_PATH}"
)

print(
    f"📚 Collection        : {COLLECTION_NAME}"
)

print(
    f"🤖 Embedding model   : {EMBEDDING_MODEL}"
)


print("\n" + "=" * 80)

print(
    "Your complete document collection is now ready for RAG!"
)

print("=" * 80 + "\n")