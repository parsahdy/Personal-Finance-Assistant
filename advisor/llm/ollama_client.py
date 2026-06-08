from langchain_community.llms import Ollama


llm = Ollama(
    model="llama3.1",
    base_url="http://localhost:11434"
)


class OllamaClient:

    @staticmethod
    def generate(prompt):
        return llm.invoke(prompt)