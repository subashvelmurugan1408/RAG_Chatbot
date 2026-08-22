#!/bin/sh

echo "======================================"
echo "Starting RAG Chatbot"
echo "======================================"

echo "Starting Flask backend..."

cd /app/backend

gunicorn \
  --bind 127.0.0.1:5000 \
  app:app &

echo "Flask backend started on port 5000"

echo "Starting Next.js frontend..."

cd /app/frontend

npm start -- --hostname 0.0.0.0 --port 3000
