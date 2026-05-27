FROM registry.digitalocean.com/enfeca/manim-base:latest

WORKDIR /app

# Copy source code
COPY . .

# Use base image virtualenv
ENV PATH="/opt/venv/bin:$PATH"

# Install backend dependencies
RUN pip install --no-cache-dir -r platform/backend/requirements.txt

# Build frontend
WORKDIR /app/platform/frontend

RUN npm ci

RUN npm run build

# Back to app root
WORKDIR /app

# Startup script
COPY start.sh /start.sh

RUN chmod +x /start.sh

# Expose nginx + backend ports
EXPOSE 80
EXPOSE 8000

# Start application
CMD ["/start.sh"]
