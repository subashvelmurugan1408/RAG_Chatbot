You can replace your existing README.md with this:

# 🤖 RAG Chatbot


A full-stack **Retrieval-Augmented Generation (RAG) Chatbot** that allows users to ask questions about a collection of documents and receive AI-generated answers based on the retrieved document context.


The project uses a **Next.js frontend**, **Flask backend**, **Qdrant Cloud vector database**, **Sentence Transformers embeddings**, and **Qwen 2.5 7B Instruct** through the Hugging Face Inference API.


---


## 🚀 Features


- 📄 Document-based question answering
- 🔎 Semantic vector search
- 🧠 Retrieval-Augmented Generation (RAG)
- ⚡ Next.js frontend
- 🐍 Flask REST API backend
- ☁️ Qdrant Cloud vector database
- 🤗 Hugging Face Inference API
- 🧩 Qwen/Qwen2.5-7B-Instruct LLM
- 🔤 Sentence Transformers embeddings
- 🐳 Docker support
- 🐳 Docker Compose support
- 🌐 Ready for cloud deployment
- 📊 API health and status endpoints


---


# 🏗️ System Architecture


```text
                         USER
                           │
                           ▼
                 ┌───────────────────┐
                 │   Next.js Frontend│
                 │      v0 UI        │
                 └─────────┬─────────┘
                           │
                           │ POST /api/chat
                           ▼
                 ┌───────────────────┐
                 │   Flask Backend   │
                 │     REST API      │
                 └─────────┬─────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │ Sentence Transformers   │
              │ all-MiniLM-L6-v2        │
              └────────────┬────────────┘
                           │
                    Query Embedding
                           │
                           ▼
                 ┌───────────────────┐
                 │   Qdrant Cloud    │
                 │  Vector Database  │
                 │                   │
                 │  25,860 vectors   │
                 └─────────┬─────────┘
                           │
                     Top 5 Chunks
                           │
                           ▼
                 ┌───────────────────┐
                 │ RAG Context       │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Hugging Face      │
                 │ Qwen 2.5 7B       │
                 │ Instruct           │
                 └─────────┬─────────┘
                           │
                           ▼
                      AI Answer
🛠️ Technologies Used
Frontend
Next.js
React
TypeScript
Tailwind CSS
Lucide React
v0-generated UI
Backend
Python
Flask
Flask-CORS
Gunicorn
Python-dotenv
AI / RAG
Hugging Face
Qwen/Qwen2.5-7B-Instruct
Sentence Transformers
sentence-transformers/all-MiniLM-L6-v2
Vector Database
Qdrant Cloud
Development Database
ChromaDB
Containerization
Docker
Docker Compose
WSL 2
Docker Desktop
Deployment
GitHub
Render
Qdrant Cloud
Hugging Face
📂 Project Structure
rag_project/
│
├── backend/
│   ├── .env
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── app.py
│   ├── chat_rag.py
│   ├── migrate_chroma_to_qdrant.py
│   ├── requirements.txt
│   │
│   └── chroma_db/
│       └── Local ChromaDB backup
│
├── frontend/
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── package.json
│   ├── package-lock.json
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── public/
│
├── documents/
│   └── Source documents
│
├── chroma_db/
│
├── chroma_db_python/
│
├── create_embeddings.py
├── create_embeddings_final.py
├── create_sample_doc.py
├── download_ai_papers.py
├── download_python_resource.py
├── load_document.py
├── retriever.py
├── store_vectors.py
├── test_retrieval.py
├── check_chroma.py
│
├── docker-compose.yml
├── requirements.txt
├── package.json
├── package-lock.json
├── README.md
└── .gitignore
🔄 RAG Workflow

The chatbot follows the following workflow:

User Question
      │
      ▼
Generate Query Embedding
      │
      ▼
Search Qdrant Cloud
      │
      ▼
Retrieve Top 5 Relevant Chunks
      │
      ▼
Build RAG Context
      │
      ▼
Send Context + Question to Qwen
      │
      ▼
Generate Answer
      │
      ▼
Return Answer to Frontend
🗃️ ChromaDB → Qdrant Migration

During development, ChromaDB was initially used as the local vector database.

The original setup contained approximately:

25,860 document chunks

The embedding dimension was verified as:

384

The embedding model was:

sentence-transformers/all-MiniLM-L6-v2

The original ChromaDB collection was:

all_documents

The existing vectors were migrated to Qdrant Cloud without regenerating the embeddings.

After migration:

Qdrant Collection: all_documents
Vectors: 25,860
Dimension: 384
Distance: Cosine

The migration script is:

backend/migrate_chroma_to_qdrant.py
☁️ Qdrant Cloud

Qdrant is used as the production vector database.

The application connects using:

QDRANT_URL
QDRANT_API_KEY
QDRANT_COLLECTION

The collection used by the project is:

all_documents

The application retrieves the top 5 most relevant document chunks for each question.

🧠 Embedding Model

The project uses:

sentence-transformers/all-MiniLM-L6-v2

The embedding dimension is:

384

The same embedding model must be used when creating query embeddings because the Qdrant collection was created with 384-dimensional vectors.

🤖 Language Model

The project uses:

Qwen/Qwen2.5-7B-Instruct

The model is accessed through the Hugging Face Inference API.

The Hugging Face token is stored as an environment variable.

🔐 Environment Variables

Create:

backend/.env

Example:

HF_TOKEN=your_huggingface_token


QDRANT_URL=https://your-qdrant-cluster-url


QDRANT_API_KEY=your_qdrant_api_key


QDRANT_COLLECTION=all_documents
⚠️ Security

Never commit .env to GitHub.

The .gitignore should contain:

.env
backend/.env

Never expose your:

HF_TOKEN
QDRANT_API_KEY

in source code.

🖥️ Local Development
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

Move into the project:

cd rag_project
🐍 Backend Setup

Move into the backend:

cd backend

Create a virtual environment:

Windows
python -m venv venv

Activate:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the Flask backend:

python app.py

Backend:

http://localhost:5000
🌐 Frontend Setup

Open another terminal.

Move into:

cd frontend

Install dependencies:

npm install

Run the development server:

npm run dev

Frontend:

http://localhost:3000
🔗 Frontend → Backend

The frontend communicates with:

POST /api/chat

The frontend API URL is configured using:

NEXT_PUBLIC_API_URL=http://localhost:5000

The frontend sends:

{
  "message": "Your question"
}

The backend returns the generated RAG response.

🔌 API Endpoints
Health Check
GET /api/health

Example:

http://localhost:5000/api/health

Response:

{
  "status": "ok",
  "message": "RAG API is running",
  "using": "Hugging Face Inference API"
}
RAG Chat
POST /api/chat

Request:

{
  "message": "What is RAG?"
}

Response:

{
  "success": true,
  "response": "Generated answer..."
}
System Status
GET /api/status

Example response:

{
  "status": "ready",
  "vectordb": {
    "type": "Qdrant",
    "collection": "all_documents",
    "chunks": 25860
  },
  "embeddings": "sentence-transformers/all-MiniLM-L6-v2",
  "llm": "Qwen/Qwen2.5-7B-Instruct",
  "api": "Hugging Face"
}
🐳 Docker Setup

The project supports Docker for running the frontend and backend.

Backend Dockerfile

The backend Docker image contains:

Python
Flask
Gunicorn
Qdrant Client
Hugging Face dependencies
Sentence Transformers
PyTorch
Transformers

The production backend does not copy the local ChromaDB into the image.

Qdrant Cloud is used instead.

🐳 Docker Compose

The entire application can be started using:

docker compose up --build

The services are:

Frontend → localhost:3000


Backend → localhost:5000

Stop the containers:

docker compose down
🧪 Docker Testing

Check running containers:

docker ps

Check backend:

http://localhost:5000/api/status

Expected:

status: ready
vectordb: Qdrant
chunks: 25860

Check frontend:

http://localhost:3000

Ask a question and verify that the RAG response is returned.

📦 Docker Architecture
Docker Compose
│
├── Frontend Container
│     └── Next.js
│
└── Backend Container
      ├── Flask
      ├── Qdrant Client
      ├── Sentence Transformers
      ├── Hugging Face
      └── Qwen
             │
             ▼
        Qdrant Cloud
🐳 WSL 2 + Docker Desktop

The project was tested using:

Windows
WSL 2
Ubuntu
Docker Desktop

Docker was verified using:

docker --version

and:

docker run hello-world

Docker Compose was then used to run the RAG application.

📤 GitHub

Before pushing the project, make sure sensitive and generated files are ignored.

Recommended .gitignore entries:

# Environment variables
.env
backend/.env


# Python
__pycache__/
*.pyc
venv/


# Node
node_modules/
frontend/node_modules/


# Next.js
.next/
frontend/.next/


# Local vector database
backend/chroma_db/
chroma_db/
chroma_db_python/


# Logs
*.log


# OS
.DS_Store
Thumbs.db

Check ignored files:

git check-ignore -v backend/.env backend/chroma_db

Check status:

git status

Add files:

git add .

Commit:

git commit -m "Dockerize RAG chatbot with Qdrant"

Push:

git push origin main
☁️ Deployment

The recommended deployment architecture is:

                    Internet
                       │
                       ▼
              ┌────────────────┐
              │ Next.js Frontend│
              │     Render      │
              └───────┬────────┘
                      │
                      ▼
              ┌────────────────┐
              │  Flask Backend │
              │     Render      │
              └───────┬────────┘
                      │
              ┌───────┴────────┐
              ▼                ▼
        Qdrant Cloud      Hugging Face
        Vector Database       Qwen

The frontend and backend can remain in the same GitHub repository while being deployed as separate Render services.

🚀 Render Backend

Create a Render Web Service using the same GitHub repository.

Backend root directory:

backend

Dockerfile:

backend/Dockerfile

The backend requires these environment variables:

HF_TOKEN
QDRANT_URL
QDRANT_API_KEY
QDRANT_COLLECTION

Set:

QDRANT_COLLECTION=all_documents

The backend should connect directly to Qdrant Cloud.

🚀 Render Frontend

Create another Render service using the same GitHub repository.

Frontend root directory:

frontend

Dockerfile:

frontend/Dockerfile

Set the frontend environment variable:

NEXT_PUBLIC_API_URL=https://YOUR-BACKEND-URL

The frontend will then communicate with:

https://YOUR-BACKEND-URL/api/chat
💾 Why Qdrant Instead of Render Persistent Disk?

The original local ChromaDB was approximately:

234 MB

Render's default filesystem is not persistent across deployments/restarts.

A Render Persistent Disk requires a paid service.

Therefore, the project was migrated to Qdrant Cloud so that the vector database remains externally accessible from the deployed Flask backend.

🔄 Migration Process

The migration was performed as follows:

Local ChromaDB
       │
       │
       ▼
Collection: all_documents
       │
       │ 25,860 vectors
       │ 384 dimensions
       ▼
Migration Script
       │
       ▼
Qdrant Cloud
       │
       ▼
Migration Verified

The migration was verified with:

ChromaDB vectors: 25,860


Qdrant vectors: 25,860

The local ChromaDB should be kept as a backup until production deployment has been completely verified.

🧰 Troubleshooting
Docker Compose configuration not found

Error:

no configuration file provided

Make sure you are in the project root:

rag_project/

and that:

docker-compose.yml

exists.

Run:

docker compose up --build
Docker requirements hash error

Error:

THESE PACKAGES DO NOT MATCH THE HASHES

This can occur when using a requirements file containing package hashes that don't match the downloaded Linux package.

Use a clean backend requirements.txt without hash-pinned package entries.

Frontend JSON error

Error:

Unexpected token '<', "<!DOCTYPE "... is not valid JSON

This usually means the frontend received an HTML response instead of the Flask JSON API response.

Check:

NEXT_PUBLIC_API_URL=http://localhost:5000

and make sure the frontend calls:

/api/chat

Restart Next.js after changing environment variables.

Qdrant connection error

Check:

QDRANT_URL=...
QDRANT_API_KEY=...
QDRANT_COLLECTION=all_documents

Make sure the API key is valid and the Qdrant cluster is available.

Qdrant vector count

Check:

/api/status

Expected:

Qdrant
25,860 chunks
🔒 Security

Never commit:

.env
backend/.env
QDRANT_API_KEY
HF_TOKEN

API keys should always be stored using environment variables.

For production deployments, add secrets through the deployment platform's environment variable settings.

📈 Current Project Status
Frontend                  ✅
Next.js                   ✅
v0 UI                     ✅


Flask Backend             ✅
REST API                  ✅


Local ChromaDB            ✅ Development/Backup
Qdrant Cloud              ✅ Production Vector DB


Vectors                   ✅ 25,860
Embedding Dimension       ✅ 384


Embedding Model           ✅ all-MiniLM-L6-v2
LLM                       ✅ Qwen 2.5 7B Instruct
Hugging Face API          ✅


Docker                    ✅
Docker Compose            ✅
WSL 2                     ✅
Docker Desktop            ✅


Local Docker Testing      ✅
Qdrant Migration          ✅
🎯 Future Improvements

Possible future improvements include:

📄 Upload documents directly from the frontend
🔄 Automatic document ingestion
🗂️ Document management
👤 User authentication
💬 Conversation history
📌 Source citations in answers
📊 RAG analytics
⚡ Streaming AI responses
🧠 Improved retrieval strategies
🔎 Hybrid search
📱 Mobile responsive improvements
☁️ Production deployment
📈 Monitoring and logging
👨‍💻 Author

Subash V

Bachelor of Computer Science and Engineering

RVS Technical Campus, Coimbatore

⭐ Project Summary

This project demonstrates a complete Retrieval-Augmented Generation architecture by combining semantic search with a large language model.

The system retrieves relevant information from a vector database and provides that context to Qwen before generating an answer.

The final architecture uses:

Next.js
   +
Flask
   +
Qdrant Cloud
   +
Sentence Transformers
   +
Hugging Face
   +
Qwen 2.5
   +
Docker

This provides a scalable foundation for building a document-based AI chatbot.



### One important thing before you replace your README


Your repository currently has a **root `requirements.txt`** as well as `backend/requirements.txt`. For the Docker deployment, the important one is:


```text
backend/requirements.txt

Also, keep backend/chroma_db/ locally as your backup, but don't commit it to GitHub now that Qdrant contains your 25,860 vectors.

give me this as per i copied and paste in github

Yes. 👍 Below is a clean GitHub-ready README.md. Copy everything inside the code block and paste it directly into your repository's README.md.

# 🤖 RAG Chatbot


A full-stack **Retrieval-Augmented Generation (RAG) Chatbot** that allows users to ask questions about documents and receive AI-generated answers based on relevant document content.


The project uses **Next.js** for the frontend, **Flask** for the backend, **Qdrant Cloud** for vector search, **Sentence Transformers** for embeddings, and **Qwen 2.5 7B Instruct** through the Hugging Face API.


---


## 🚀 Features


- 📄 Document-based question answering
- 🔎 Semantic vector search
- 🧠 Retrieval-Augmented Generation (RAG)
- ⚡ Next.js frontend
- 🐍 Flask REST API backend
- ☁️ Qdrant Cloud vector database
- 🤗 Hugging Face Inference API
- 🧩 Qwen/Qwen2.5-7B-Instruct
- 🔤 Sentence Transformers embeddings
- 🐳 Docker support
- 🐳 Docker Compose support
- 🌐 Cloud deployment ready
- 📊 API health and status endpoints


---


## 🏗️ System Architecture


```text
                         USER
                           │
                           ▼
                 ┌───────────────────┐
                 │   Next.js Frontend│
                 │      v0 UI        │
                 └─────────┬─────────┘
                           │
                           │ POST /api/chat
                           ▼
                 ┌───────────────────┐
                 │   Flask Backend   │
                 │     REST API      │
                 └─────────┬─────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │ Sentence Transformers   │
              │ all-MiniLM-L6-v2        │
              └────────────┬────────────┘
                           │
                    Query Embedding
                           │
                           ▼
                 ┌───────────────────┐
                 │   Qdrant Cloud    │
                 │  Vector Database  │
                 │                   │
                 │  25,860 vectors   │
                 └─────────┬─────────┘
                           │
                     Top 5 Chunks
                           │
                           ▼
                 ┌───────────────────┐
                 │    RAG Context    │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │   Hugging Face    │
                 │   Qwen 2.5 7B    │
                 │     Instruct      │
                 └─────────┬─────────┘
                           │
                           ▼
                      AI Answer
🛠️ Technologies Used
Frontend
Next.js
React
TypeScript
Tailwind CSS
Lucide React
v0-generated UI
Backend
Python
Flask
Flask-CORS
Gunicorn
Python-dotenv
AI / RAG
Hugging Face
Qwen/Qwen2.5-7B-Instruct
Sentence Transformers
sentence-transformers/all-MiniLM-L6-v2
Vector Database
Qdrant Cloud
Development Database
ChromaDB
Containerization
Docker
Docker Compose
WSL 2
Docker Desktop
Deployment
GitHub
Render
Qdrant Cloud
Hugging Face
📂 Project Structure
rag_project/
│
├── backend/
│   ├── .dockerignore
│   ├── .env
│   ├── Dockerfile
│   ├── app.py
│   ├── chat_rag.py
│   ├── migrate_chroma_to_qdrant.py
│   ├── requirements.txt
│   │
│   └── chroma_db/
│       └── Local ChromaDB backup
│
├── frontend/
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── package.json
│   ├── package-lock.json
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── public/
│
├── documents/
│   └── Source documents
│
├── create_embeddings.py
├── create_embeddings_final.py
├── create_sample_doc.py
├── download_ai_papers.py
├── download_python_resource.py
├── load_document.py
├── retriever.py
├── store_vectors.py
├── test_retrieval.py
├── check_chroma.py
│
├── docker-compose.yml
├── README.md
└── .gitignore

Note: .env, chroma_db, node_modules, .next, and other sensitive/generated files should not be committed to GitHub.

🔄 RAG Workflow

The chatbot follows this workflow:

User Question
      │
      ▼
Generate Query Embedding
      │
      ▼
Search Qdrant Cloud
      │
      ▼
Retrieve Top 5 Relevant Chunks
      │
      ▼
Build RAG Context
      │
      ▼
Send Context + Question to Qwen
      │
      ▼
Generate Answer
      │
      ▼
Return Answer to Frontend
🗃️ ChromaDB → Qdrant Migration

During development, ChromaDB was initially used as the local vector database.

The existing ChromaDB contained:

25,860 document chunks
384-dimensional embeddings
Collection: all_documents

The embedding model used was:

sentence-transformers/all-MiniLM-L6-v2

The existing vectors were migrated to Qdrant Cloud without regenerating the embeddings.

After migration:

Qdrant Collection: all_documents
Vectors: 25,860
Embedding Dimension: 384
Distance: Cosine

The migration script is:

backend/migrate_chroma_to_qdrant.py

The original ChromaDB is kept locally as a backup.

☁️ Qdrant Cloud

Qdrant Cloud is used as the production vector database.

The application connects using:

QDRANT_URL
QDRANT_API_KEY
QDRANT_COLLECTION

The collection used by the project is:

all_documents

For every user question, the application creates a query embedding and retrieves the top 5 relevant document chunks from Qdrant.

🧠 Embedding Model

The project uses:

sentence-transformers/all-MiniLM-L6-v2

Embedding dimension:

384

The same embedding model is used for both document embeddings and query embeddings.

🤖 Language Model

The project uses:

Qwen/Qwen2.5-7B-Instruct

The model is accessed through the Hugging Face Inference API.

🔐 Environment Variables

Create the following file for local development:

backend/.env

Example:

HF_TOKEN=your_huggingface_token


QDRANT_URL=https://your-qdrant-cluster-url


QDRANT_API_KEY=your_qdrant_api_key


QDRANT_COLLECTION=all_documents

For the frontend:

frontend/.env.local

Example:

NEXT_PUBLIC_API_URL=http://localhost:5000
⚠️ Security

Never commit .env or .env.local to GitHub.

Never expose:

HF_TOKEN
QDRANT_API_KEY

in your source code.

For production, add these values through the deployment platform's environment-variable settings.

🖥️ Local Development
1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

Move into the project:

cd rag_project
🐍 Backend Setup

Move into the backend directory:

cd backend

Create a Python virtual environment:

Windows
python -m venv venv

Activate it:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the backend:

python app.py

Backend:

http://localhost:5000
🌐 Frontend Setup

Open another terminal.

Move into the frontend:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

Frontend:

http://localhost:3000
🔗 Frontend → Backend

The frontend communicates with the Flask API.

The API URL is configured using:

NEXT_PUBLIC_API_URL=http://localhost:5000

The chatbot sends requests to:

POST /api/chat

Example request:

{
  "message": "What is RAG?"
}
🔌 API Endpoints
Health Check
GET /api/health

Example:

http://localhost:5000/api/health

Response:

{
  "status": "ok",
  "message": "RAG API is running",
  "using": "Hugging Face Inference API"
}
RAG Chat
POST /api/chat

Request:

{
  "message": "What is RAG?"
}

Response:

{
  "success": true,
  "response": "Generated answer..."
}
System Status
GET /api/status

Example:

http://localhost:5000/api/status

Expected response:

{
  "status": "ready",
  "vectordb": {
    "type": "Qdrant",
    "collection": "all_documents",
    "chunks": 25860
  },
  "embeddings": "sentence-transformers/all-MiniLM-L6-v2",
  "llm": "Qwen/Qwen2.5-7B-Instruct",
  "api": "Hugging Face"
}
🐳 Docker Setup

The project supports Docker for running the frontend and backend.

Backend Docker

The backend Docker image contains:

Python
Flask
Gunicorn
Qdrant Client
Hugging Face dependencies
Sentence Transformers
PyTorch
Transformers

The production Docker image does not copy the local ChromaDB.

Qdrant Cloud is used as the vector database.

🐳 Docker Compose

The complete application can be started with:

docker compose up --build

Services:

Frontend → http://localhost:3000


Backend → http://localhost:5000

Stop the containers:

docker compose down
🧪 Docker Testing

Check running containers:

docker ps

Check backend status:

http://localhost:5000/api/status

Expected:

Status: ready
Vector DB: Qdrant
Collection: all_documents
Chunks: 25860

Check the frontend:

http://localhost:3000

Ask a question related to your documents and verify the generated answer.

🐳 Docker Architecture
                 Docker Compose
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
       Frontend Container   Backend Container
             │                   │
          Next.js              Flask
                                 │
                                 ▼
                            Qdrant Cloud
                                 │
                                 ▼
                            Hugging Face
                                 │
                                 ▼
                               Qwen
🖥️ WSL 2 + Docker Desktop

The project was developed and tested using:

Windows
WSL 2
Ubuntu
Docker Desktop

Docker installation was verified using:

docker --version

and:

docker run hello-world

Docker Compose was then used to run the complete RAG application.

📤 GitHub

Before pushing the project, make sure sensitive and generated files are ignored.

Recommended .gitignore:

# Environment variables
.env
backend/.env
frontend/.env.local


# Python
__pycache__/
*.pyc
venv/


# Node
node_modules/
frontend/node_modules/


# Next.js
.next/
frontend/.next/


# Local ChromaDB
backend/chroma_db/
chroma_db/
chroma_db_python/


# Logs
*.log


# OS
.DS_Store
Thumbs.db

Check ignored files:

git check-ignore -v backend/.env backend/chroma_db

Check Git status:

git status

Add files:

git add .

Commit:

git commit -m "Dockerize RAG chatbot with Qdrant"

Push:

git push origin main
☁️ Deployment Architecture

The recommended production architecture is:

                         Internet
                            │
                            ▼
                   ┌─────────────────┐
                   │ Next.js Frontend│
                   │     Render      │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │  Flask Backend  │
                   │     Render      │
                   └────────┬────────┘
                            │
                    ┌───────┴────────┐
                    ▼                ▼
              Qdrant Cloud      Hugging Face
              Vector Database        Qwen

The frontend and backend can remain in the same GitHub repository while being deployed as separate Render services.

🚀 Render Backend Deployment

Create a Render Web Service using the GitHub repository.

Backend root directory:

backend

Dockerfile:

backend/Dockerfile

Add the following environment variables in Render:

HF_TOKEN
QDRANT_URL
QDRANT_API_KEY
QDRANT_COLLECTION

Set:

QDRANT_COLLECTION=all_documents

The backend connects directly to Qdrant Cloud.

🚀 Render Frontend Deployment

Create another Render service using the same GitHub repository.

Frontend root directory:

frontend

Dockerfile:

frontend/Dockerfile

Set:

NEXT_PUBLIC_API_URL=https://YOUR-BACKEND-URL

The frontend will communicate with:

https://YOUR-BACKEND-URL/api/chat
💾 Why Qdrant Instead of Render Persistent Disk?

The original local ChromaDB was approximately:

234 MB

Render's default filesystem is ephemeral.

A Render Persistent Disk requires a paid service.

Therefore, the project was migrated to Qdrant Cloud so the vector database can be accessed remotely by the deployed Flask backend.

🔄 Complete Migration Process

The vector database migration was performed as follows:

Local ChromaDB
       │
       ▼
Collection: all_documents
       │
       ▼
25,860 vectors
       │
       ▼
384-dimensional embeddings
       │
       ▼
Migration Script
       │
       ▼
Qdrant Cloud
       │
       ▼
Migration Verified

Migration result:

ChromaDB vectors: 25,860
Qdrant vectors:   25,860

The local ChromaDB is kept as a backup.

🧰 Troubleshooting
Docker Compose Configuration Not Found

Error:

no configuration file provided

Make sure you are in the project root:

rag_project/

and that this file exists:

docker-compose.yml

Run:

docker compose up --build
Docker Requirements Hash Error

Error:

THESE PACKAGES DO NOT MATCH THE HASHES

This occurs when the requirements file contains package hashes that don't match the downloaded package.

Use a clean backend/requirements.txt without hash-pinned package entries.

Frontend JSON Error

Error:

Unexpected token '<', "<!DOCTYPE "... is not valid JSON

This usually means that the frontend received an HTML response instead of the Flask JSON API response.

Check:

NEXT_PUBLIC_API_URL=http://localhost:5000

Make sure the frontend calls:

/api/chat

Restart Next.js after changing environment variables.

Qdrant Connection Error

Check:

QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION=all_documents

Make sure the Qdrant cluster is active and the API key is valid.

Qdrant Vector Count

Check:

http://localhost:5000/api/status

Expected:

Vector DB: Qdrant
Collection: all_documents
Chunks: 25860
🔒 Security

Never commit:

.env
backend/.env
frontend/.env.local
QDRANT_API_KEY
HF_TOKEN

API keys should always be stored using environment variables.

For production deployment, add secrets through Render's environment-variable settings.

📈 Current Project Status
Component	Status
Next.js Frontend	✅
v0 UI	✅
Flask Backend	✅
REST API	✅
Local ChromaDB	✅ Backup
Qdrant Cloud	✅
Vector Migration	✅
Vectors	✅ 25,860
Embedding Dimension	✅ 384
all-MiniLM-L6-v2	✅
Qwen 2.5 7B Instruct	✅
Hugging Face API	✅
Docker	✅
Docker Compose	✅
WSL 2	✅
Docker Desktop	✅
Local Docker Testing	✅
Qdrant Migration	✅
🎯 Future Improvements
📄 Upload documents from the frontend
🔄 Automatic document ingestion
🗂️ Document management
👤 User authentication
💬 Conversation history
📌 Source citations
📊 RAG analytics
⚡ Streaming AI responses
🔎 Hybrid search
📱 Improved mobile responsiveness
☁️ Production deployment
📈 Monitoring and logging
👨‍💻 Author

Subash V

Bachelor of Computer Science and Engineering

RVS Technical Campus, Coimbatore

⭐ Project Summary

This project demonstrates a complete Retrieval-Augmented Generation (RAG) system by combining semantic vector search with a large language model.

The system retrieves relevant information from a vector database and provides that context to Qwen before generating an AI response.

Final Technology Stack
Next.js
   +
React
   +
Flask
   +
Qdrant Cloud
   +
Sentence Transformers
   +
Hugging Face
   +
Qwen 2.5
   +
Docker
   +
Docker Compose

The project provides a scalable foundation for building document-based AI applications.



**Copy everything from `# 🤖 RAG Chatbot` through the end of the code block into your GitHub `README.md`.**
