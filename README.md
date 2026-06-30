# scratch-ai-rag
RAG system built from scratch 

Local RAG Chatbot
A high-performance, modular, zero-bloat Retrieval-Augmented Generation (RAG) system built to query heavy textbooks and PDF documents locally on resource-constrained hardware.

Overview:
Pproject maps unstructured PDF textbooks into a local semantic vector space and provides a stateful, continuous conversational interface through a terminal REPL loop. It is intentionally designed to bypass general-purpose framework bloat, optimizing execution speed and RAM management. Great emphasis has been placed on efficiency and performance.

Tech Stack
Core Orchestrator: LlamaIndex (Data ingestion, node parsing, vector indexing)

Local Inference Engine: Ollama

Large Language Model: llama3.2 (3B parameters, optimized for local execution)

Embedding Matrix Model: nomic-embed-text (768-dimensional local vectors)

Package Manager: uv (Fast, lightweight alternative to pip)

Target Hardware Profile: Bare-metal Linux setup running on only 8GB RAM (since model actually only consumes 3.5GB of RAM it may also run on 6GB setups).

Core Features
Stateful REPL Chat Shell: Continuous command-line terminal to execute follow-up prompts without script re-initialization.

Global RAM Cache Optimization: Injects the compiled vector index database into system memory on model startup, ensuring sub-second response times for subsequent conversational turns.

Context Continuity: Tracks dialogue history dynamically, allowing the 3B model to interpret structural pronouns.

Quick Start
Ensure local Ollama daemon is running (ollama pull llama3.2 and ollama pull nomic-embed-text), drop your raw textbooks and pdf files into your local database folder, and in your terminal execute:

python app.py

note: By default the system prompt for the model has been set to specifically target AI/LLM related queries as my local database consisted of that. for other use cases change the 'system_prompt' in 'main() in 'app.py' to something related to what you use it for.

For detailed notes regarding the framework design philosophy (LlamaIndex vs LangChain), deep prompt engineering discoveries (XML boundaries and recency bias formatting), full project file layout, and the comprehensive error troubleshooting ledger, please refer to your active notes.md file.