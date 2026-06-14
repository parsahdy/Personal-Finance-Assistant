from advisor.llm.ollama_client import OllamaClient
from advisor.services.forecasting import ForecastingService
from advisor.prompts.forecasting_prompt import forcasting_propmt
from advisor.services.intentclassifier import MLIntentClassifier
from advisor.ml.train import MLPredictor


class LLMPredictor:

    @staticmethod
    def forecast(user, question):

        intent = MLIntentClassifier.mlclassify(question=question)

        if intent.get("action") == "income":
            incomes = ForecastingService.get_income_time_series(
                user=user
            )
            furure_x = (len(incomes) - 1) + intent.get("month_ahead")
            data = MLPredictor.get_income_forecast(
                incomes=incomes,
                future_x=furure_x
            )
        elif intent.get("action") == "expense":
            expenses = ForecastingService.get_expense_time_series(
                user=user
            )
            furure_x = (len(expenses) - 1) + intent.get("month_ahead")
            data = MLPredictor.get_expense_forecat(
                expenses=expenses,
                future_x=furure_x
            )
        else:
            saving_rates = ForecastingService.get_saving_time_series(
                incomes=incomes,
                expenses=expenses
            )
            furure_x = (len(saving_rates) - 1) + intent.get("month_ahead")
            data = MLPredictor.get_saving_rate_forecast(
                saving_rates=saving_rates,
                future_x=furure_x
            )

        prompt_text = forcasting_propmt.format(
            question=question,
            data=data
            )

        return OllamaClient.generate(prompt=prompt_text)