# file will contain a the RAG code from the LlamaIndex tutorial

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.embeddings.ollama import OllamaEmbedding
import os
import asyncio

from llama_index.llms.ollama.base import Ollama
from pydantic_core.core_schema import none_schema

# settings control global defaults
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    base_url="http://localhost:11434",
    embed_batch_size=32,
)

# settings for the actual LLM
Settings.llm = Ollama(
    model="llama3.2",
    temperature=0.0,
    request_timeout=360.0,
    context_window=1000,
)

# the actual RAG code
documents = SimpleDirectoryReader("./test-data").load_data()
index = VectorStoreIndex.from_documents(
    documents,
)

query_engine = index.as_query_engine()


async def search_documents(query: str) -> str:
    """useful for checking data retrieval functionality"""
    response = await query_engine.aquery(query)
    return str(response)


# calling the model
agent = AgentWorkflow.from_tools_or_functions(
    [search_documents],
    llm=Settings.llm,
    # now resorting to XML tags because standard english isnt working
    system_prompt="""<system>\n
    You are a strict text-extraction utility. ONLY WRITE CODE WHEN INSTRUCTED AND DO NOT USE MARKDOWN CODE BLOCKS.\n
    </system>\n\n""",
)

extracted_token = None

async def main():
    response = await agent.run("who made the text file. preserve the casing of the username and output in JSON format")
    print(response)

# modifying code to include case sensitivty for the extracted text.
# this is done by creating a python script which searches the file the text was extracted from
# for an exact match of string and then copying that into the response instead.
# discovered a better solution instead.

# new solution utilizes how LLMs work on a fundamental level by moving the casing instruction
# to the very end of the user query. in this way the instruction is still in recent memory while 
# the LLM is generating a response. 

asyncio.run(main())
