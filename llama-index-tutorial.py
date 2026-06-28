import asyncio
import sys

from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.ollama import Ollama


def multiply(a: float, b: float) -> float:
    """useful for multiplying 2 numbers"""
    return a * b


agent = FunctionAgent(
    # tools=[multiply],
    llm=Ollama(
        model="llama3.2",
        request_timeout=360.0,
        context_window=1000,
    ),
    # system_prompt="you are an assistant that can multiply 2 numbers.",
    system_prompt="this is a test to see how good your memory is.",
)

# async def main():
# response = await agent.run("What is 100*100?")
# print(str(response))

# asyncio.run(main())

# for this code to work Ollama must be running with local LLM in the background
# all this code did so far is process a basic prompt
# code has been appended to add chat history too
# RAG will be coded from scratch in the file rag-test.py

from llama_index.core.workflow import Context

ctx = Context(agent)


async def main():
    response = await agent.run("my name is amazon", ctx=ctx)
    print(response)
    response = await agent.run("What is my name?", ctx=ctx)
    print(response)


asyncio.run(main())
