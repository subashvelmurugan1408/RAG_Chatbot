FROM node:20-bookworm-slim

WORKDIR /app

# Install Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# =========================
# FRONTEND
# =========================

WORKDIR /app/frontend

COPY frontend/package*.json ./

RUN npm ci

COPY frontend/ ./

RUN npm run build

# =========================
# BACKEND
# =========================

WORKDIR /app/backend

COPY backend/requirements.txt ./

RUN pip3 install \
    --no-cache-dir \
    --break-system-packages \
    -r requirements.txt

COPY backend/ ./

# =========================
# STARTUP
# =========================

WORKDIR /app

COPY start.sh /start.sh

RUN chmod +x /start.sh

EXPOSE 3000

CMD ["/start.sh"]