#!/bin/bash

# -----------------------------------------------
# Discord Bot Runner
# Usage:
#   ./run.sh         -> runs locally in terminal
#   ./run.sh docker  -> runs in Docker
#   ./run.sh stop    -> stops Docker container
#   ./run.sh logs    -> tail Docker logs
# -----------------------------------------------

MODE=${1:-local}

case "$MODE" in
  local)
    echo ">> Starting bot locally..."
    python main.py
    ;;

  docker)
    echo ">> Building and starting bot in Docker..."
    docker compose up --build -d
    echo ">> Bot is running. Use './run.sh logs' to follow output."
    ;;

  stop)
    echo ">> Stopping Docker container..."
    docker compose down
    ;;

  logs)
    echo ">> Tailing logs (Ctrl+C to exit)..."
    docker compose logs -f
    ;;

  *)
    echo "Unknown command: $MODE"
    echo "Usage: ./run.sh [local|docker|stop|logs]"
    exit 1
    ;;
esac
