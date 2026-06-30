#!/bin/bash
set -e

APP_NAME="Project TRIAD"
APP_DIR="$HOME/project-triad"
PLATFORM_DIR="$APP_DIR/platform"
HEALTH_URL="http://127.0.0.1:5090"
ROLLBACK_FILE="$PLATFORM_DIR/.last_successful_commit"

echo "===================================================="
echo "          $APP_NAME Rollback"
echo "===================================================="

if [ ! -f "$ROLLBACK_FILE" ]; then
    echo "No rollback commit found."
    exit 1
fi

ROLLBACK_COMMIT=$(cat "$ROLLBACK_FILE")

echo "Rolling back to commit:"
echo "$ROLLBACK_COMMIT"

cd "$APP_DIR"

echo "1/4 Resetting repository..."
git reset --hard "$ROLLBACK_COMMIT"

echo "2/4 Rebuilding and restarting Docker container..."
cd "$PLATFORM_DIR"
docker compose up -d --build

echo "3/4 Running health check..."
for i in {1..30}; do
    if curl -fsS "$HEALTH_URL" >/dev/null; then
        echo "Rollback successful on attempt $i."
        echo "===================================================="
        echo "Completed: $(date)"
        echo "===================================================="
        exit 0
    fi
    echo "Waiting... attempt $i/30"
    sleep 3
done

echo "Rollback failed: health check did not pass."
docker compose logs --tail=100
exit 1