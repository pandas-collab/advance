#!/bin/bash

set -e

echo "=== API INTEGRATION TESTING ==="

# Navigate to backend directory
cd /workspace/backend

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "Setting up Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run the Python integration test
echo "Running API integration tests..."
python3 tests/test_api_integration.py

echo "API integration tests completed successfully!"
