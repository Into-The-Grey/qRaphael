#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

# Start the model loader script in the background
python scripts/model_loader.py &

# Wait for a few seconds to ensure the model loader is up and running
sleep 10

# Start the text generation script
python scripts/generate_text.py "$@"
