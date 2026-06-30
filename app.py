
import requests
import src.config as config
from src.engine import retrieve_context

def main():
	print("--- Local RAG Pipeline ---")
	print("Type 'exit' to stop")

	# implementing constant chat loop. so model doesnt stop after one question.
	chat_history = []


	while True:
		# get users query from terminal
		user_question = input("\nAsk me anything: ")
		if not user_question.strip():
			print("Say something")
			return

		if user_question.lower().strip() in ["exit"]:
			print("\nEnding session. Goodbye.")
			break

		print("\n[step 1] Searching index...")
		# calls engine.py which loads FAISS index & pulls out top 3 most relevant snippets
		retrieved_knowledge = retrieve_context(user_question, k=3)

		print("[step 2] Sending retrieved data to LLM..")

		# constructing final prompt consisting of retrieved data and query
		final_prompt = f"""
		You are an expert AI/ML assistant. Answer user questions using provided textbook context.

		Textbook context: {retrieved_knowledge}

		User query: {user_question}
		Answer:
		"""

		# standard payload to hit local Ollama instance
		payload = {
			"model": config.MODEL_NAME,
			"prompt": final_prompt,
			"stream": False
		}

		# final component to recieve answer
		try:
			response = requests.post(f"{config.OLLAMA_URL}/api/generate", json=payload)
			response_data = response.json()
			ai_answer = response_data.get("response", "").strip()

			print("\n--- AI Response ---")
			print(ai_answer)

		except Exception as e:
			print(f"\nFailed to connect to Ollama : {str(e)}")

if __name__ == "__main__":
	main()

