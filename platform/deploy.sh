#!/bin/bash

set -e

APP_DIR="$HOME/project-triad"
PLATFORM_DIR="$APP_DIR/platform"
HEALTH_URL="http://127.0.0.1:5090"

echo "Deploying Project TRIAD..."

cd "$APP_DIR"

echo "Checking branch..."
git checkout develop

echo "Pulling latest changes..."
git pull origin develop

echo "Building and starting Docker container..."
cd "$PLATFORM_DIR"
docker compose up -d --build

echo "Waiting for Project TRIAD to become available..."

for i in {1..20}; do
    if curl -fsS "$HEALTH_URL" >/dev/null; then
        echo "Project TRIAD deployed successfully."
        exit 0
    fi

    echo "Waiting... attempt $i/20"
    sleep 3
done

echo "Deployment completed, but health check failed."
echo "Showing recent container logs:"
docker compose logs --tail=80

exit 1