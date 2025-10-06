# CX helpers - placeholder for customer experience utilities
import os
from dotenv import load_dotenv

def load_environment_variables():
    # Load environment variables from .env file
    load_dotenv()
    return {
        'api_key': os.getenv('API_KEY'),
        'database_url': os.getenv('DATABASE_URL'),
        'model_name': os.getenv('MODEL_NAME', 'default-model')
    }

def format_response(response):
    # Format response for better UX
    return f"Assistant: {response}"

def log_conversation(user_input, assistant_output):
    # Placeholder for conversation logging
    with open('conversation_log.txt', 'a') as f:
        f.write(f"User: {user_input}\nAssistant: {assistant_output}\n\n")

def validate_input(input_text):
    # Basic input validation
    if not input_text or len(input_text.strip()) == 0:
        raise ValueError("Input cannot be empty")
    return input_text.strip()
