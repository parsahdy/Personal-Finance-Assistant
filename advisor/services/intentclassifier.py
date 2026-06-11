import json

from advisor.llm.ollama_client import OllamaClient


example = json.dumps({
    "action": "largest_income",
    "category": "Food",
    "year": 2025,
    "month": 8
}, ensure_ascii=False, indent=4)


class IntentClassifier:

    @staticmethod
    def classify(question):

        prompt = f"""
        You are an intent classifier for a financial assistant.

        Available actions:

        - largest_income
        - largest_expense
        - monthly_income
        - monthly_expense
        - saving_rate
        - largest_category
        - budget_status
        - remaining_budget

        Rules:
        - Return the action name, year, month and category from question.
        - Return ONLY valid JSON.

        Example: {example}

        Question: {question}
        """ 

        result = OllamaClient.generate(prompt=prompt)

        data = json.loads(result)

        return {
            "action": data.get("action"),
            "category": data.get("category"),
            "year": data.get("year"),
            "month": data.get("month")
        }