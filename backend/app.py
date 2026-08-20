"""
Flask API Backend for RAG Chatbot
=================================

Architecture:

React Frontend
      ↓
Flask API
      ↓
ChromaDB Retriever
      ↓
Relevant document chunks
      ↓
RAG Prompt
      ↓
Hugging Face Inference API
      ↓
Qwen/Qwen2.5-7B-Instruct
      ↓
Answer

Run:
    python app.py
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

from huggingface_hub import InferenceClient
from qdrant_client import QdrantClient
from qdrant_client.models import Distance


# ============================================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================================

load_dotenv()


# ============================================================================
# CONFIGURATION
# ============================================================================

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "all_documents")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

LLM_MODEL = "Qwen/Qwen2.5-7B-Instruct"

HF_TOKEN = os.getenv("HF_TOKEN")


# ============================================================================
# CHECK REQUIRED FILES / VARIABLES
# ============================================================================

if not QDRANT_URL:

    print("❌ Error: chroma_db/ not found!")

    print(
        "Make sure you have created the vector database first."
    )

    exit(1)


if not HF_TOKEN:

    print("❌ Error: HF_TOKEN not found in .env")

    print(
        "Add this to your .env file:"
    )

    print(
        "HF_TOKEN=your_huggingface_token"
    )

    exit(1)


# ============================================================================
# INITIALIZE FLASK
# ============================================================================

app = Flask(__name__)

CORS(app)


# ============================================================================
# INITIALIZE HUGGING FACE CLIENT
# ============================================================================

print("\n" + "=" * 70)
print("🤖 RAG CHATBOT API - HUGGING FACE")
print("=" * 70)

print("\nLoading RAG system...\n")


print("Initializing Hugging Face client...", end="", flush=True)

try:

    hf_client = InferenceClient(
         provider="together",
        api_key=HF_TOKEN
    )

    print(" ✓")

except Exception as e:

    print(f" ❌")

    print(f"Error: {e}")

    exit(1)


# ============================================================================
# INITIALIZE EMBEDDINGS
# ============================================================================

print(
    "Initializing Hugging Face embedding API...",
    end="",
    flush=True
)

try:

    hf_embedding_client = InferenceClient(
        provider="hf-inference",
        api_key=HF_TOKEN
    )

    print(" ✓")

except Exception as e:

    print(" ❌")

    print(
        f"Error initializing embedding API: {e}"
    )

    exit(1)

# ============================================================================
# LOAD CHROMADB
# ============================================================================

print(
    "Loading ChromaDB...",
    end="",
    flush=True
)

try:

    qdrant_client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
    )

    # Check that the collection exists
    collection_info = qdrant_client.get_collection(
        collection_name=COLLECTION_NAME
    )

    print(" ✓")
    print(
        f"   ✓ Qdrant collection: {COLLECTION_NAME}"
    )
    print(
        f"   ✓ Vectors: {collection_info.points_count}"
    )

except Exception as e:

    print(" ❌")

    print(f"Error connecting to Qdrant: {e}")

    exit(1)


# ============================================================================
# CHECK CHROMADB
# ============================================================================

try:

    collection_info = qdrant_client.get_collection(
        collection_name=COLLECTION_NAME
    )

    total_chunks = collection_info.points_count

    print(
        f"   ✓ Vectors in Qdrant: {total_chunks}"
    )

except Exception as e:

    print(
        f"   ⚠️ Could not read Qdrant collection count: {e}"
    )


# ============================================================================
# RAG PROMPT
# ============================================================================

RAG_PROMPT = """
You are a helpful RAG assistant.

Your job is to answer the user's question using ONLY the
information contained in the provided context.

IMPORTANT RULES:

1. Use the provided context as your primary source.
2. Do not invent information.
3. Do not use outside knowledge when the context does not
   contain the answer.
4. If the answer cannot be found in the context, say:

"I could not find this information in the provided documents."

5. Give a clear and concise answer.
6. If the context contains multiple relevant sections,
   combine them into a useful answer.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""


# ============================================================================
# GENERATE ANSWER USING HUGGING FACE
# ============================================================================

def generate_answer(prompt_text):

    response = hf_client.chat.completions.create(

        model=LLM_MODEL,

        messages=[
            {
                "role": "user",
                "content": prompt_text
            }
        ],

        max_tokens=512,

        temperature=0.7
    )

    return response.choices[0].message.content
def retrieve_documents(question, k=5):

    query_embedding = create_query_embedding(question)

    results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=k,
        with_payload=True
    )

    documents = []

    for point in results.points:

        payload = point.payload or {}

        content = payload.get(
            "document",
            ""
        )

        metadata = payload.get(
            "metadata",
            {}
        )

        documents.append({
            "content": content,
            "metadata": metadata
        })

    return documents
def create_query_embedding(text):

    result = hf_embedding_client.feature_extraction(
        text,
        model=EMBEDDING_MODEL
    )

    embedding = result.tolist()

    # Handle possible 2D output
    if len(embedding) == 1:
        embedding = embedding[0]

    if len(embedding) != 384:
        raise ValueError(
            f"Expected 384-dimensional embedding, "
            f"got {len(embedding)}"
        )

    return embedding
# ============================================================================
# RAG FUNCTION
# ============================================================================

def ask_rag(question):

    # --------------------------------------------------------
    # 1. RETRIEVE DOCUMENTS
    # --------------------------------------------------------

    documents = retrieve_documents(question)

    if not documents:
        return (
            "I could not find relevant information "
            "in the provided documents."
        )

    context_parts = []

    for document in documents:

        metadata = document.get(
            "metadata",
            {}
        )

        source = metadata.get(
            "source",
            "Unknown source"
        )

        content = document.get(
            "content",
            ""
        )

        context_parts.append(
            f"Source: {source}\n"
            f"Content:\n{content}"
        )

        context = "\n\n---\n\n".join(
            context_parts
        )


    # --------------------------------------------------------
    # 4. CREATE NORMAL STRING PROMPT
    # --------------------------------------------------------

    prompt_text = RAG_PROMPT.format(

        context=context,

        question=question
    )


    # --------------------------------------------------------
    # 5. SEND TO QWEN
    # --------------------------------------------------------

    answer = generate_answer(
        prompt_text
    )


    return answer


# ============================================================================
# HOME
# ============================================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({

        "status": "success",

        "message": "RAG API is running",

        "endpoint": "/api/chat"

    })


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({

        "status": "ok",

        "message": "RAG API is running",

        "using": "Hugging Face Inference API"

    })


# ============================================================================
# CHAT ENDPOINT
# ============================================================================

@app.route("/api/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json(
            silent=True
        )

        if not data:

            return jsonify({

                "success": False,

                "error": "Invalid JSON request"

            }), 400


        message = data.get(
            "message",
            ""
        ).strip()


        if not message:

            return jsonify({

                "success": False,

                "error": "No message provided"

            }), 400


        print(
            f"\nUser question: {message}"
        )


        # ----------------------------------------------------
        # RAG
        # ----------------------------------------------------

        answer = ask_rag(
            message
        )


        print(
            "✓ Answer generated"
        )


        return jsonify({

            "success": True,

            "response": answer,

            "message": message

        })


    except Exception as e:

        print(
            f"\n❌ Error: {e}"
        )


        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================================
# STATUS
# ============================================================================

@app.route("/api/status", methods=["GET"])
def status():
    try:

        collection_info = qdrant_client.get_collection(
            collection_name=COLLECTION_NAME
        )

        count = collection_info.points_count

        return jsonify({

            "status": "ready",

            "vectordb": {

                "type": "Qdrant",

                "collection": COLLECTION_NAME,

                "chunks": count

            },

            "embeddings": EMBEDDING_MODEL,

            "llm": LLM_MODEL,

            "api": "Hugging Face"

        })


    except Exception as e:

        return jsonify({

            "status": "error",

            "error": str(e)

        }), 500

# ============================================================================
# 404 HANDLER
# ============================================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({

        "error": "Endpoint not found"

    }), 404


# ============================================================================
# 500 HANDLER
# ============================================================================

@app.errorhandler(500)
def server_error(error):

    return jsonify({

        "error": "Internal server error"

    }), 500


# ============================================================================
# START SERVER
# ============================================================================

if __name__ == "__main__":

    print("\n" + "=" * 70)

    print(
        "🚀 Starting RAG API"
    )

    print("=" * 70)

    print(
        "\n✓ API: http://localhost:5000"
    )

    print(
        "✓ Chat: http://localhost:5000/api/chat"
    )

    print(
        "✓ Health: http://localhost:5000/api/health"
    )

    print(
        "✓ Status: http://localhost:5000/api/status"
    )

    print(
        f"✓ ChromaDB: {COLLECTION_NAME}"
    )

    print(
        f"✓ Collection: {COLLECTION_NAME}"
    )

    print(
        f"✓ Embeddings: {EMBEDDING_MODEL}"
    )

    print(
        f"✓ LLM: {LLM_MODEL}"
    )

    print(
        "\nPress Ctrl+C to stop the server\n"
    )

    print("=" * 70)


   
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
