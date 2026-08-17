from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".md",
    ".markdown",
    ".py"
}


def load_all_documents():
    """
    Load all supported documents from the documents/ directory.
    """

    base_path = Path("documents")

    if not base_path.exists():
        raise FileNotFoundError(
            "documents/ folder not found"
        )

    all_docs = []

    print("\n" + "=" * 80)
    print("LOADING ALL DOCUMENTS")
    print("=" * 80)

    files_found = 0
    files_loaded = 0
    files_skipped = 0

    for file_path in base_path.rglob("*"):

        if not file_path.is_file():
            continue

        extension = file_path.suffix.lower()

        if extension not in SUPPORTED_EXTENSIONS:
            continue

        files_found += 1

        try:

            if extension == ".pdf":

                loader = PyPDFLoader(str(file_path))
                docs = loader.load()

            else:

                loader = TextLoader(
                    str(file_path),
                    encoding="utf-8"
                )

                docs = loader.load()

            all_docs.extend(docs)

            files_loaded += 1

            print(f"✓ Loaded: {file_path}")

        except Exception as e:

            files_skipped += 1

            print(
                f"⚠️ Skipped: {file_path}"
            )
            print(f"   Reason: {e}")

    print("\n" + "-" * 80)
    print(f"Supported files found : {files_found}")
    print(f"Successfully loaded   : {files_loaded}")
    print(f"Skipped/errors        : {files_skipped}")
    print(f"Documents/pages       : {len(all_docs)}")
    print("-" * 80)

    return all_docs


def split_documents(documents):
    """
    Split all loaded documents into chunks.
    """

    print("\n" + "=" * 80)
    print("SPLITTING DOCUMENTS INTO CHUNKS")
    print("=" * 80)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    print(f"✓ Created {len(chunks)} chunks")

    return chunks


def get_document_statistics(documents):

    total_documents = len(documents)

    total_characters = sum(
        len(doc.page_content)
        for doc in documents
    )

    file_types = {}

    for doc in documents:

        source = doc.metadata.get("source", "")

        extension = Path(source).suffix.lower()

        if extension:
            file_types[extension] = (
                file_types.get(extension, 0) + 1
            )

    average_size = (
        total_characters / total_documents
        if total_documents
        else 0
    )

    return {
        "total_documents": total_documents,
        "total_characters": total_characters,
        "average_doc_size": average_size,
        "files": file_types
    }


if __name__ == "__main__":

    documents = load_all_documents()

    chunks = split_documents(documents)

    print("\n✓ Loading complete")
    print(f"✓ Documents/pages: {len(documents)}")
    print(f"✓ Chunks: {len(chunks)}")