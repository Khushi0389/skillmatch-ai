#!/bin/bash

# Install Spacy language model
python -m spacy download en_core_web_sm

# Start the FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000
