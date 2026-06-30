this portion is dedicated to understanding llamaindex by reading its documentation and noting thoughts
note: only things relevant to project will be mentioned. ill only be using llamaindex for structured data extraction. im running llama3.2 with 3b parameters due to limited RAM (8gb). 

why am i using this instead of langchain?
1. because its better suited to my project. since langchain is a general purpose framework it introduces tons of unnecessary load in the form of massive abstraction layers. meanwhile llamaindex is specifically designed for data ingestion and retrieval. for the project it provides the exact tools needed without general purpose bloat.

2. moreover langchain forces use of LCEL (langchain expressive language) which is a whole other rabbit hole in itself. llamaindex maps directly to standard rag concepts meaning i can learn the theory of how rag systems function and translate it into real working code with the same logic. its straight to the point and direct.

3.langchain has a massive dependency tree that pulls tons of external packages drastically increasing memory footprint. llamaindex on the other hand uses a much lower memory footprint by using RAM alongside the ollama daemon. difference is very noticeable on lower end hardware with limited memory (such as my setup)

-provides the ability to use RAG pipelines for AI agents

-context augmentation, the exact thing im trying to do. makes your custom data available to the LLM to allow for more specialised answers.

-llamaindex can extract this data from apis, sql databases, text files and documents and even pdfs (which is what im using)

-for my scale i only need data connectors (for parsing my data) and data indexes (to structure the data into vectors)

-listed use case is what my project falls into (question answering with your own data)

-followed the instructions to install llamaindex but used uv instead of pip

-created 2 files first "llama-index-tutorial.py" to test calling the model using code itself. defined a multiply function and asked the LLM to multiply 2 numbers together which it succesfully did

-after this created another file titled "rag-test.py" which included the actual RAG code itself. followed most of the code from llamaindex starter tutorial on the website but added my own embedder (nomic-embed-text) instead of the huggingface embedder in the tutorial

-after writing all the necessary code in the RAG file created a text file titled "textdata.txt" and added a secret password inside it. initially included it in the main directory.

-however upon running the LLM it started searching every file in the main directory so had to move the file into a dedicated folder titled "test-data" to improve execution speeds.

-upon first tests it was observed that answers were never consistent. the majority of answers were hallucinations while the rest were the model saying it couldnt locate the password.

-to fix this first set the model temperature to 0.0. this increased answer precision at the cost of most answers being code for data extraction rather than the actual answer.

-slightly increased temperature to 0.3 which fixed the code issue but resulted in higher hallucination rates.

-eventually changed secret password to validation token because model guard rails kept intervening. this change sucessfully prevented the guardrails from blocking the answer.

-since model success rate (how many times it output the correct answer) was still only 30% (3 out of 10 tries), changed the system prompt to be in XML. this was a breakthrough and skyrocketed the success rate to 100%. reset the temperature to 0.0

-with model precision improving, began work on preserving the casing of the validation token. the model would constantly output the token in lowercase regardless of the actual casing in the file.

-first attempt at fixing this was adding the following line into system prompt which was still in the XML format:
"you MUST preserve the EXACT casing of the extracted text." however model ignored this instruction and still output in lowercase 100% of the time

-the fix that worked was to include this sentence at the end of the user query. since the instruction was at the very end, the model had it loaded in memory while it generated an output and hence followed the instruction. a case of recency bias 

concepts learned (summary):
1. system tag isolation. XML tags force tiny models to strictly follow the given instructions by forcing them into utility modes.

2. recency/proximity bias. formatiing constraints and specific instructions work best when appended directly to the query string, not in the system prompt.


-tested the RAG model with multiple prompts and after some basic prompt engineering got 100% success rates on all. prompts included retrieving validation token, retrieving username of the file creator (mentioned in the file), and retrieving the file username but in JSON format. 

Now beginning work on the actual LLM code. Modularity will be used to ensure easier feature expansion and debugging in the future.

errors encountered:
- UnicodeEncodeError utf-8 codec cannot encode character. caused by mathematical symbols. fixed by writing a sanitizing script that removed these symbols.
- cannot assign to attribute 'text' for class 'document'. fixed by replacing 'doc.text' in documents which was being blocked as its a read-only attribute with llamaindex's official setter method '.set_content()'.
- ResponseError 404 page not found status code 404. was caused by a broken OLLAMA_URL in config.py. fixed by correcting the url.
- UnboundLocalError cannot access local variable index where its not associated with a value. caused by a missing index assignment line in retrieve_context in engine.py. was initially solved by adding an 'index = None' at the start of 'retrieve_context()' in engine.py but that resulted in a seperate error so had to rewrite parts of engine.py.
- AttributeError 'NoneType' object has no attribute 'as_retriever'. casued by adding 'index = None' in 'retrieve_context()'. the broken line causing this error was 'load_index_from_storage(storage_context)' which was changed to 'index = load_index_from_storage(storage_context)' which fixed both errors. 


code for the basic RAG is now fully complete.
features added:

- chat loop to allow followup questions. done with encasing 'main()' in app.py in a while loop.
- RAM cache to store the database in temporary memory to allow for much faster responses on follow up prompts.
- context continuity by allowing the model to remember the topic in previous prompts or questions and providing relevant context.


planned features:
- source citations with the exact title and page number of the document used at the end of every generated response
- a GUI either terminal based or web based. (either Streamlit or Textual)
- hybrid search which combines vector search with keyword matching for even more accurate responses
- adding a reranker whose sole purpose is to rerank the top extracted chunks to ensure even more contextual accuracy
