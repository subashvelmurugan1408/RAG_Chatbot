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
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# ============================================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================================

load_dotenv()


# ============================================================================
# CONFIGURATION
# ============================================================================

CHROMA_PATH = "./chroma_db"

COLLECTION_NAME = "all_documents"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

LLM_MODEL = "Qwen/Qwen2.5-7B-Instruct"

HF_TOKEN = os.getenv("HF_TOKEN")


# ============================================================================
# CHECK REQUIRED FILES / VARIABLES
# ============================================================================

if not Path(CHROMA_PATH).exists():

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
        provider="auto",
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
    "Initializing Hugging Face embeddings...",
    end="",
    flush=True
)

try:

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    print(" ✓")

except Exception as e:

    print(" ❌")

    print(f"Error loading embeddings: {e}")

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

    vector_store = Chroma(
        persist_directory=CHROMA_PATH,

        collection_name=COLLECTION_NAME,

        embedding_function=embeddings
    )

    print(" ✓")

except Exception as e:

    print(" ❌")

    print(f"Error loading ChromaDB: {e}")

    exit(1)


# ============================================================================
# CHECK CHROMADB
# ============================================================================

try:

    collection = vector_store._collection

    total_chunks = collection.count()

    print(
        f"   ✓ Chunks in database: {total_chunks}"
    )

except Exception as e:

    print(
        f"   ⚠️ Could not read collection count: {e}"
    )


# ============================================================================
# CREATE RETRIEVER
# ============================================================================

print(
    "Setting up retriever...",
    end="",
    flush=True
)

try:

    retriever = vector_store.as_retriever(

        search_type="similarity",

        search_kwargs={
            "k": 5
        }
    )

    print(" ✓")

except Exception as e:

    print(" ❌")

    print(f"Error creating retriever: {e}")

    exit(1)


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


# ============================================================================
# RAG FUNCTION
# ============================================================================

def ask_rag(question):

    # --------------------------------------------------------
    # 1. RETRIEVE DOCUMENTS
    # --------------------------------------------------------

    documents = retriever.invoke(question)


    # --------------------------------------------------------
    # 2. CHECK RETRIEVAL
    # --------------------------------------------------------

    if not documents:

        return (
            "I could not find relevant information "
            "in the provided documents."
        )


    # --------------------------------------------------------
    # 3. BUILD CONTEXT
    # --------------------------------------------------------

    context_parts = []

    for document in documents:

        source = document.metadata.get(
            "source",
            "Unknown source"
        )

        content = document.page_content

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

        collection = vector_store._collection

        count = collection.count()


        return jsonify({

            "status": "ready",

            "vectordb": {

                "type": "ChromaDB",

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
        f"✓ ChromaDB: {CHROMA_PATH}"
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