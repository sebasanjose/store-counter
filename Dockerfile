# Docker Compose setup for Store-Counter application

# Frontend Dockerfile
FROM node:16 AS frontend

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Backend Dockerfile
FROM python:3.9 AS backend

WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install OpenCV and PyTorch dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY backend/ .

# Final stage
FROM python:3.9-slim

WORKDIR /app

# Install runtime dependencies for OpenCV and PyTorch
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy backend from backend stage
COPY --from=backend /app/backend /app/backend
# Copy Python packages from backend stage
COPY --from=backend /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
# Copy frontend build from frontend stage
COPY --from=frontend /app/frontend/build /app/frontend/build

# No need to reinstall Flask as it's already copied from the backend stage
COPY server.py .

EXPOSE 8080

CMD ["python", "server.py"]