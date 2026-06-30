# file handles document loading and chunking logic 

import os
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
import src.config as config

def load_and_chunk_books():
	"""uses llamaindex to natively ingest PDFs and parse them"""
	
	if not os.path.exists(config.BOOKS_DIR):
		print(f"Error: directory '{config.BOOKS_DIR}' does not exist")
		return []

	print(f"scanning {config.BOOKS_DIR} for data...")

	# SimpleDirectoryReader scans folder and extracts text automatically
	reader = SimpleDirectoryReader(input_dir=config.BOOKS_DIR, required_exts=[".pdf"])
	documents = reader.load_data()

	print("sanitizing text data and removing weird symbols...")
	# loop through the books to strip out illegal surrogate characters
	for doc in documents:
		text = doc.get_content()
		if text:
			cleaned_text = "".join(c for c in doc.text if not (0xD800 <= ord(c) <= 0xDFFF))
			doc.set_content(cleaned_text)	

	splitter = SentenceSplitter(
		chunk_size = config.CHUNK_SIZE,
		chunk_overlap = config.CHUNK_OVERLAP
	)

	nodes = splitter.get_nodes_from_documents(documents)
	return nodes