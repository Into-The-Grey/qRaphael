#!/bin/bash

# Set up the environment
echo "Setting up the environment..."
source /home/ncacord/qRaphael/.env

# Ensure necessary directories exist
LOG_DIR="/home/ncacord/qRaphael/logs/standard"
mkdir -p $LOG_DIR

# Load the model (assuming model_loader.py runs in the background and keeps the model in memory)
echo "Loading the model..."
python /home/ncacord/qRaphael/scripts/model_loader.py &

# Capture the PID of the background model loader script
MODEL_LOADER_PID=$!

# Wait for a few seconds to ensure the model is loaded
sleep 5

# Run the text generation script
echo "Running the text generation script..."
python /home/ncacord/qRaphael/scripts/generate_text.py "$@"

# Clean up: stop the model loader process
echo "Stopping the model loader..."
kill $MODEL_LOADER_PID

echo "Script execution completed."
