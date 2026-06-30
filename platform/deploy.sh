#!/bin/bash
set -e

APP_NAME="Project TRIAD"
APP_DIR="$HOME/project-triad"
PLATFORM_DIR="$APP_DIR/platform"
BRANCH="develop"
HEALTH_URL="http://127.0.0.1:5090"

echo "===================================================="
echo "          $APP_NAME Deployment"
echo "===================================================="
echo "Branch      : $BRANCH"
echo "Directory   : $APP_DIR"
echo "Health URL  : $HEALTH_URL"
echo "Started     : $(date)"
echo "===================================================="

cd "$APP_DIR"

echo "1/6 Checking current branch..."
git checkout "$BRANCH"

echo "2/6 Saving current commit for rollback..."
git rev-parse HEAD > "$PLATFORM_DIR/.last_successful_commit"

echo "3/6 Pulling latest changes..."
git pull origin "$BRANCH"

echo "4/6 Building and restarting Docker container..."
cd "$PLATFORM_DIR"
docker compose up -d --build

echo "5/6 Waiting for service health check..."
for i in {1..30}; do
    if curl -fsS "$HEALTH_URL" >/dev/null; then
        echo "Health check passed on attempt $i."
        echo "6/6 Deployment successful."
        echo "===================================================="
        echo "Completed: $(date)"
        echo "===================================================="
        exit 0
    fi
    echo "Waiting... attempt $i/30"
    sleep 3
done

echo "Deployment failed: health check did not pass."
echo "Recent container logs:"
docker compose logs --tail=100
exit 1