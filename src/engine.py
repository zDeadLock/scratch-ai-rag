# contains the actual code for the LLM

import os
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
import src.config as config
from src.query import load_and_chunk_books

# RAM cache optimization to keep the database loaded in memory and significantly improve model speeds
# so follow-up questions can respond quicker
_RAM_INDEX_CACHE = None

def init_global_settings():
	"""ties llamaindex pipeline into local ollama embedding engine"""
	Settings.embed_model = OllamaEmbedding(
		model_name=config.EMBEDDING_MODEL,
		base_url=config.OLLAMA_URL
	)

def get_or_create_index():
	"""checks disk for a saved llamaindex database or compiles one"""
	global _RAM_INDEX_CACHE

	# return instantly if already exists in RAM
	if _RAM_INDEX_CACHE is not None:
		return _RAM_INDEX_CACHE

	init_global_settings()

	# to check if database has already been compiled & saved
	if os.path.exists(config.VECTOR_DIR) and os.listdir(config.VECTOR_DIR):
		print("Loading persistent vector store from disk...")
		storage_context = StorageContext.from_defaults(persist_dir= config.VECTOR_DIR)
		index = load_index_from_storage(storage_context)

	else:
		print("No local index found. Initializing compilation pipeline...")
		# retrieve processed PDF chunks from query.py
		nodes = load_and_chunk_books()

		if not nodes:
			raise ValueError(f"No text chunks extracted. Ensure documents are inside {config.BOOKS_DIR}")

		print(f"Embedding {len(nodes)} chunks using {config.EMBEDDING_MODEL}. Might take a while...")

		# compile the index
		index = VectorStoreIndex(nodes)

		# save to disk permanently
		index.storage_context.persist(persist_dir=config.VECTOR_DIR)
		print(f"Success! Vector database created in directory: {config.VECTOR_DIR}")

	_RAM_INDEX_CACHE = index	
	return index

def retrieve_context(query: str, k: int = 3) -> str:
	"""finds the top 'k' the most relevant data for given question"""
	index = get_or_create_index()

	if index is None:
		raise ValueError("Critical Error: Vector failed to initialize properly")

	# cast index into retriever object
	retriever = index.as_retriever(similarity_top_k = k)
	retrieved_nodes = retriever.retrieve(query)

	# extract text from nodes and join them together
	return "\n\n".join([node.text for node in retrieved_nodes])