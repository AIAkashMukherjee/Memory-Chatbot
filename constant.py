from dotenv import load_dotenv
import os
load_dotenv()

open_ai_api=os.getenv('OPENAI_API_KEY')
pinecone_api=os.getenv('PINECONE_API_KEY')
groq_api_key=os.getenv('GROQ_API_KEY')

PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# Model Configuration
DEFAULT_OPENAI_MODEL = "gpt-4"


# Memory Configuration
MEMORY_WINDOW_SIZE = 8

