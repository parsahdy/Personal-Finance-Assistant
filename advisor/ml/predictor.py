from advisor.llm.ollama_client import OllamaClient
from advisor.ml.train import MLPredictor
from advisor.prompts.forecasting_prompt import forcasting_propmt


class LLMPredictor:

    @staticmethod
    def forecast(data):
        
        data = MLPredictor.get_forecast_data()

        prompt_text = forcasting_propmt.format(data=data)

        OllamaClient.generate(prompt=prompt_text)