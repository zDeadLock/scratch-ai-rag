# contains settings and parameters

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "llama3.2"
EMBEDDING_MODEL = "nomic-embed-text" #fast and lightweight 

BOOKS_DIR = "./local_assets/ML Books" #database directory location
VECTOR_DIR = "./local_assets/VectorDB" #compiled vector database location

# splitting parameters according to model size and system resources
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

