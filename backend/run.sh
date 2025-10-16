#!/bin/bash

# Load environment variables
export $(cat .env | xargs)

# Run the FastAPI application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
EOF

chmod +x run.sh