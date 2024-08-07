#!/bin/bash

# Set up the environment
echo "Setting up the environment..."
source /home/ncacord/qRaphael/.env

# Ensure necessary directories exist
LOG_DIR="/home/ncacord/qRaphael/logs/standard"
mkdir -p $LOG_DIR

# Function to log system metrics
log_system_metrics() {
  echo "Logging system metrics..."
  echo "CPU Usage:" >> $LOG_DIR/system_metrics.log
  top -bn1 | grep "Cpu(s)" >> $LOG_DIR/system_metrics.log
  echo "Memory Usage:" >> $LOG_DIR/system_metrics.log
  free -m >> $LOG_DIR/system_metrics.log
  if command -v nvidia-smi &> /dev/null; then
    echo "GPU Usage:" >> $LOG_DIR/system_metrics.log
    nvidia-smi >> $LOG_DIR/system_metrics.log
  fi
}

# Function to send notification (placeholder for email/slack integration)
send_notification() {
  echo "Sending notification: $1"
  # Implement your notification logic here (email, slack, etc.)
}

# Trap function to ensure graceful shutdown
graceful_shutdown() {
  echo "Stopping the model loader..."
  kill $MODEL_LOADER_PID
  send_notification "Model loader stopped."
  echo "Script execution completed."
  exit
}

trap graceful_shutdown SIGINT SIGTERM

# Log start time
START_TIME=$(date +%s)

# Load the model (assuming model_loader.py runs in the background and keeps the model in memory)
echo "Loading the model..."
python /home/ncacord/qRaphael/scripts/model_loader.py &

# Capture the PID of the background model loader script
MODEL_LOADER_PID=$!

# Wait for a few seconds to ensure the model is loaded (configurable via .env)
MODEL_LOAD_WAIT_TIME=${MODEL_LOAD_WAIT_TIME:-5}
sleep $MODEL_LOAD_WAIT_TIME

# Log system metrics before running the text generation script
log_system_metrics

# Check if arguments are provided; if not, default to loop mode with user ID "Gelid"
if [ "$#" -eq 0 ]; then
  PROMPT=""
  USER_ID="Gelid"
  LOOP_MODE=true
else
  PROMPT=${1:-"Default prompt"}
  USER_ID=${2:-"default_user_id"}
  LOOP_MODE=false
  if [[ " $@ " =~ " --loop " ]]; then
    LOOP_MODE=true
  fi
fi

# Run the text generation script
if [ "$LOOP_MODE" = true ]; then
    echo "Running the text generation script in loop mode..."
    python /home/ncacord/qRaphael/scripts/generate_text.py --user_id "$USER_ID" --log_level INFO --loop
else
    echo "Running the text generation script..."
    python /home/ncacord/qRaphael/scripts/generate_text.py --prompt "$PROMPT" --user_id "$USER_ID" --max_length 50 --log_level INFO
    graceful_shutdown
fi

# Log end time
END_TIME=$(date +%s)
EXECUTION_TIME=$((END_TIME - START_TIME))
echo "Execution time: $EXECUTION_TIME seconds" >> $LOG_DIR/execution_time.log

# Clean up: stop the model loader process if not in loop mode
if [ "$LOOP_MODE" = false ]; then
    graceful_shutdown
fi
