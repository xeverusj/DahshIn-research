#!/bin/bash
# DigitalOcean App Platform startup script for Dashin Research
set -e

APP_DIR="app to test with Jan"

cd "$APP_DIR"

# Initialise / migrate the database on every deploy
echo "[startup] Initialising database..."
python core/db.py

# Start Streamlit on the port DigitalOcean provides
echo "[startup] Starting Streamlit on port ${PORT:-8080}..."
exec streamlit run app.py \
  --server.port "${PORT:-8080}" \
  --server.address 0.0.0.0 \
  --server.headless true \
  --browser.gatherUsageStats false
