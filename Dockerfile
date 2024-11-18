# Stage 1: Build Vue app and install Express dependencies
FROM node:lts-alpine AS node-build
WORKDIR /app

# Copy project files and folders to the current working directory
COPY . .

# Install and build Vue app
RUN cd vue && npm install && npm run build

# Copy built Vue app to a separate directory
RUN cp -r vue/dist dist

# Install Express dependencies
RUN cd express && npm install && npm ci --only=production

# Stage 2: Build the final image with Python and Node.js
FROM python:3.10-alpine
WORKDIR /app

# Install necessary packages
RUN apk update && \
    apk add --no-cache musl-dev gcc libpq-dev mariadb-connector-c-dev postgresql-dev python3-dev nodejs npm

# Create a directory for SQLite data
RUN mkdir -p /data

# Install backend dependencies
COPY python/src/requirements.txt ./python/src/
RUN pip install -r python/src/requirements.txt

# Copy backend source files
COPY python/ ./python/

# Copy built Vue app and Express server files from the node-build stage
COPY --from=node-build /app/dist ./dist
COPY --from=node-build /app/express ./express

# Set the volume for SQLite data
VOLUME ["/data"]

# Expose ports
EXPOSE 3000
EXPOSE 8765

# Start both the Python backend and the Express server
CMD ["sh", "-c", "python python/src/main.py & node express/server.js"]