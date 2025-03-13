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
# Copy frontend build from frontend stage
COPY --from=frontend /app/frontend/build /app/frontend/build

# Install Flask to serve frontend
RUN pip install flask
RUN pip install flask-cors

# Create a simple server to serve both backend and frontend
COPY server.py .

EXPOSE 8080

CMD ["python", "server.py"]