from langchain_ollama import OllamaLLM


llm = OllamaLLM(
    model="llama3.1",
    base_url="http://ollama:11434""
)


class OllamaClient:

    @staticmethod
    def generate(prompt):
        return llm.invoke(prompt)